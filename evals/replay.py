#!/usr/bin/env python3
"""Replay skill scenarios in fresh sessions and score the replies.

Each scenario in evals/scenarios.toml is answered by a session whose only
instructions are the listed files (a skill name expands to its SKILL.md). A judge
model then scores the reply against the scenario's criteria. Comparing two runs
shows which criteria flipped, so an edit to a skill can be checked for lost rules.

  python3 evals/replay.py check [--ref REF]
  python3 evals/replay.py run --label NAME --models M1,M2@effort --judge M3 [--ref REF]
  python3 evals/replay.py compare RUN_DIR_A RUN_DIR_B

The endpoint is any OpenAI-compatible chat completions API: REPLAY_BASE_URL (for
example http://host/v1) and optional REPLAY_API_KEY. A model spec may end in
"@<reasoning effort>"; specs without it run at temperature 0. --ref reads the files
from a git revision instead of the working tree. Results are cached per scenario,
model and repeat, keyed by the exact inputs, under --out/<label>/.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCENARIOS = HERE / "scenarios.toml"
MIN_REPLY_CHARS = 150

ANSWER_SYSTEM = "你在一个全新的会话里工作。宿主已为本会话加载下列文件全文，请按其中的规则处理用户的请求。\n\n{files}"

JUDGE_SYSTEM = """你是严格、一致的评审。你会看到一个场景、一个回答和若干条评分标准，逐条判断回答是否满足该条标准：
- 只看回答文字本身，回答没有明确表达的内容判为不满足；
- 回答用不同措辞表达了同一意思，判为满足；
- 回答虽提到标准要求的做法，但同时又做了与之相悖的事，判为不满足。
只输出 JSON：{"results": [{"id": 1, "pass": true, "reason": "不超过 30 字"}]}，id 与标准序号一一对应，不输出任何其他文字。"""


def load_scenarios() -> list[dict]:
    return tomllib.loads(SCENARIOS.read_text(encoding="utf-8")).get("scenario", [])


def scenario_files(s: dict) -> list[str]:
    return [f"skills/{name}/SKILL.md" for name in s.get("skills", [])] + list(s.get("files", []))


def read_file(root: Path, ref: str | None, path: str) -> str:
    if ref:
        r = subprocess.run(["git", "-C", str(root), "show", f"{ref}:{path}"], capture_output=True, text=True)
        if r.returncode != 0:
            raise FileNotFoundError(f"{ref}:{path}")
        return r.stdout
    p = root / path
    if not p.is_file():
        raise FileNotFoundError(str(p))
    return p.read_text(encoding="utf-8")


def check(scenarios: list[dict], root: Path, ref: str | None) -> list[str]:
    errors, seen = [], set()
    for s in scenarios:
        sid = s.get("id")
        if not sid or sid in seen:
            errors.append(f"missing or duplicate id: {sid!r}")
        seen.add(sid)
        if not str(s.get("prompt", "")).strip():
            errors.append(f"{sid}: empty prompt")
        if not s.get("criteria"):
            errors.append(f"{sid}: no criteria")
        if not scenario_files(s):
            errors.append(f"{sid}: no skills or files to load")
        for path in scenario_files(s):
            try:
                read_file(root, ref, path)
            except FileNotFoundError as e:
                errors.append(f"{sid}: missing {e}")
    return errors


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def slug(model: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", model.split("/")[-1])


def chat(model_spec: str, system: str, user: str) -> tuple[str, dict]:
    base = os.environ.get("REPLAY_BASE_URL")
    if not base:
        raise SystemExit("REPLAY_BASE_URL is not set")
    name, _, effort = model_spec.partition("@")
    min_chars = MIN_REPLY_CHARS if system.startswith(ANSWER_SYSTEM[:10]) else 1
    body: dict = {"model": name, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    if effort:
        body["reasoning_effort"] = effort
    else:
        body["temperature"] = 0
    headers = {"Content-Type": "application/json"}
    if key := os.environ.get("REPLAY_API_KEY"):
        headers["Authorization"] = f"Bearer {key}"
    request = urllib.request.Request(base.rstrip("/") + "/chat/completions", data=json.dumps(body).encode("utf-8"), headers=headers)
    last = ""
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=600) as resp:
                data = json.load(resp)
            choice = data["choices"][0]
            content = (choice["message"].get("content") or "").strip()
            usage = data.get("usage") or {}
            # Some providers cut a stream short and still report success; every scenario needs a
            # multi-step answer, so a reply this short is treated as truncated and retried.
            if content and choice.get("finish_reason") in (None, "stop") and len(content) >= min_chars:
                return content, usage
            last = f"reply looks truncated ({len(content)} chars, finish_reason={choice.get('finish_reason')})" if content else "empty reply"
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read()[:300].decode('utf-8', 'replace')}"
            if e.code < 500 and e.code != 429:
                break
        except (urllib.error.URLError, TimeoutError, KeyError, IndexError, json.JSONDecodeError) as e:
            last = f"{type(e).__name__}: {e}"
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"{model_spec}: {last}")


def parse_judgement(text: str, n: int) -> list[dict]:
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError("no JSON object in judge output")
    results = json.loads(match.group(0)).get("results")
    if not isinstance(results, list) or len(results) != n:
        raise ValueError(f"expected {n} results")
    out = []
    for i, r in enumerate(sorted(results, key=lambda r: r.get("id", 0)), 1):
        if r.get("id") != i or not isinstance(r.get("pass"), bool):
            raise ValueError(f"bad result entry {r!r}")
        out.append({"pass": r["pass"], "reason": str(r.get("reason", ""))})
    return out


def judge(judge_spec: str, s: dict, reply: str) -> tuple[list[dict], str]:
    criteria = "\n".join(f"{i}. {c}" for i, c in enumerate(s["criteria"], 1))
    user = f"## 场景\n{s['prompt'].strip()}\n\n## 回答\n{reply}\n\n## 评分标准\n{criteria}"
    problem = ""
    for _ in range(2):
        text, _ = chat(judge_spec, JUDGE_SYSTEM, user)
        try:
            return parse_judgement(text, len(s["criteria"])), text
        except (ValueError, json.JSONDecodeError) as e:
            problem = str(e)
    raise RuntimeError(f"judge output unusable: {problem}")


def run_one(s: dict, model: str, k: int, args: argparse.Namespace, out: Path) -> str:
    files = [(p, read_file(args.root, args.ref, p)) for p in scenario_files(s)]
    system = ANSWER_SYSTEM.format(files="\n\n".join(f'<file path="{p}">\n{t}\n</file>' for p, t in files))
    input_sha, criteria_sha = sha(system + "\n\n" + s["prompt"]), sha(json.dumps(s["criteria"], ensure_ascii=False))
    path = out / s["id"] / f"{slug(model)}.{k}.json"
    record = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    if record.get("input_sha") != input_sha:
        reply, usage = chat(model, system, s["prompt"].strip())
        record = {"scenario": s["id"], "model": model, "repeat": k, "input_sha": input_sha, "files": [p for p, _ in files], "reply": reply, "usage": usage}
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    elif record.get("criteria_sha") == criteria_sha and record.get("judge") == args.judge:
        return f"cached  {s['id']} {slug(model)}#{k}"
    record["results"], record["judge_raw"] = judge(args.judge, s, record["reply"])
    record.update(criteria_sha=criteria_sha, judge=args.judge)
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    passed = sum(r["pass"] for r in record["results"])
    return f"done    {s['id']} {slug(model)}#{k}: {passed}/{len(record['results'])}"


def load_records(run_dir: Path, scenarios: list[dict]) -> dict[tuple[str, str], list[dict]]:
    current = {s["id"]: sha(json.dumps(s["criteria"], ensure_ascii=False)) for s in scenarios}
    records: dict[tuple[str, str], list[dict]] = {}
    for f in sorted(run_dir.glob("*/*.json")):
        r = json.loads(f.read_text(encoding="utf-8"))
        if current.get(r.get("scenario")) == r.get("criteria_sha") and r.get("results"):
            records.setdefault((r["scenario"], r["model"]), []).append(r)
    return records


def summarize(run_dir: Path, scenarios: list[dict]) -> None:
    records = load_records(run_dir, scenarios)
    models = sorted({m for _, m in records})
    print(f"\n{run_dir.name}: criteria passed per scenario (summed over repeats)")
    print(f"{'scenario':28}" + "".join(f"{slug(m):>22}" for m in models))
    totals = {m: [0, 0] for m in models}
    for s in scenarios:
        row = f"{s['id']:28}"
        for m in models:
            recs = records.get((s["id"], m), [])
            ok = sum(r["pass"] for rec in recs for r in rec["results"])
            n = sum(len(rec["results"]) for rec in recs)
            totals[m][0] += ok
            totals[m][1] += n
            row += f"{(f'{ok}/{n}' if n else '-'):>22}"
        print(row)
    print(f"{'total':28}" + "".join(f"{f'{a}/{b}':>22}" for a, b in totals.values()))


def compare(dir_a: Path, dir_b: Path, scenarios: list[dict]) -> int:
    ra, rb = load_records(dir_a, scenarios), load_records(dir_b, scenarios)
    models = sorted({m for _, m in ra} & {m for _, m in rb})
    worse = better = 0
    for s in scenarios:
        for m in models:
            a, b = ra.get((s["id"], m), []), rb.get((s["id"], m), [])
            if not a or not b:
                continue
            for i, c in enumerate(s["criteria"]):
                pa = sum(rec["results"][i]["pass"] for rec in a) / len(a)
                pb = sum(rec["results"][i]["pass"] for rec in b) / len(b)
                if pb == pa:
                    continue
                mark = "WORSE " if pb < pa else "better"
                worse += pb < pa
                better += pb > pa
                why = "; ".join(rec["results"][i]["reason"] for rec in (b if pb < pa else a) if not rec["results"][i]["pass"])
                print(f"{mark} {s['id']} {slug(m)} #{i + 1} {pa:.0%} -> {pb:.0%}  {c}\n       judge on the failing side: {why}")
    print(f"\n{dir_a.name} -> {dir_b.name}: {worse} criteria worse, {better} better, models compared: {', '.join(slug(m) for m in models)}")
    return 1 if worse else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("check", "run"):
        p = sub.add_parser(name)
        p.add_argument("--root", type=Path, default=HERE.parent, help="repository root holding skills/ (default: this checkout)")
        p.add_argument("--ref", help="read files from this git revision instead of the working tree")
    run_p = sub.choices["run"]
    run_p.add_argument("--label", required=True)
    run_p.add_argument("--models", required=True, help="comma-separated model specs")
    run_p.add_argument("--judge", required=True)
    run_p.add_argument("--out", type=Path, default=Path(".local/replay"))
    run_p.add_argument("--only", help="comma-separated scenario ids")
    run_p.add_argument("--repeat", type=int, default=1)
    run_p.add_argument("--jobs", type=int, default=6)
    cmp_p = sub.add_parser("compare")
    cmp_p.add_argument("run_a", type=Path)
    cmp_p.add_argument("run_b", type=Path)
    args = parser.parse_args()

    scenarios = load_scenarios()
    if args.cmd == "compare":
        return compare(args.run_a, args.run_b, scenarios)
    if getattr(args, "only", None):
        wanted = set(args.only.split(","))
        scenarios = [s for s in scenarios if s["id"] in wanted]
        missing = wanted - {s["id"] for s in scenarios}
        if missing:
            print(f"unknown scenario ids: {', '.join(sorted(missing))}", file=sys.stderr)
            return 2
    errors = check(scenarios, args.root, args.ref)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 2
    if args.cmd == "check":
        print(f"OK: {len(scenarios)} scenarios, all files present at {args.ref or 'working tree'}")
        return 0

    out = args.out / args.label
    out.mkdir(parents=True, exist_ok=True)
    head = args.ref or "working tree"
    commit = subprocess.run(["git", "-C", str(args.root), "rev-parse", "--short", args.ref or "HEAD"], capture_output=True, text=True).stdout.strip()
    (out / "meta.json").write_text(json.dumps({"root": str(args.root.resolve()), "source": head, "commit": commit, "judge": args.judge}, indent=2), encoding="utf-8")
    models = [m.strip() for m in args.models.split(",") if m.strip()]
    jobs = [(s, m, k) for s in scenarios for m in models for k in range(args.repeat)]
    failed = 0
    with cf.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(run_one, s, m, k, args, out): (s["id"], m, k) for s, m, k in jobs}
        for future in cf.as_completed(futures):
            try:
                print(future.result(), flush=True)
            except Exception as e:  # report and keep the other jobs running
                failed += 1
                sid, m, k = futures[future]
                print(f"FAILED  {sid} {slug(m)}#{k}: {e}", flush=True)
    summarize(out, scenarios)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
