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
MIN_REPLY_CHARS = 40

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
    return re.sub(r"[^A-Za-z0-9._-]+", "_", model.replace("/", "__"))


def chat(model_spec: str, system: str, user: str, *, min_chars: int = 1) -> tuple[str, dict]:
    base = os.environ.get("REPLAY_BASE_URL")
    if not base:
        raise SystemExit("REPLAY_BASE_URL is not set")
    name, _, effort = model_spec.partition("@")
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
    decoder = json.JSONDecoder()
    results = None
    idx = 0
    while True:
        pos = text.find("{", idx)
        if pos == -1:
            break
        try:
            obj, _ = decoder.raw_decode(text, pos)
        except json.JSONDecodeError:
            idx = pos + 1
            continue
        if isinstance(obj, dict) and isinstance(obj.get("results"), list):
            results = obj["results"]
            break
        idx = pos + 1
    if not isinstance(results, list) or len(results) != n:
        raise ValueError(f"expected {n} results in judge output")
    for r in results:
        if not isinstance(r, dict) or not isinstance(r.get("id"), int) or isinstance(r.get("id"), bool):
            raise ValueError(f"bad result entry {r!r}")
    out = []
    for i, r in enumerate(sorted(results, key=lambda r: r["id"]), 1):
        if r["id"] != i or not isinstance(r.get("pass"), bool):
            raise ValueError(f"bad result entry {r!r}")
        out.append({"pass": r["pass"], "reason": str(r.get("reason", ""))})
    return out


def judge(judge_spec: str, s: dict, reply: str) -> tuple[list[dict], str]:
    criteria = "\n".join(f"{i}. {c}" for i, c in enumerate(s["criteria"], 1))
    user = f"## 场景\n{s['prompt'].strip()}\n\n## 回答\n{reply}\n\n## 评分标准\n{criteria}"
    problem = ""
    for _ in range(2):
        text, _ = chat(judge_spec, JUDGE_SYSTEM, user, min_chars=1)
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
        reply, usage = chat(model, system, s["prompt"].strip(), min_chars=MIN_REPLY_CHARS)
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


def load_records(run_dir: Path, scenarios: list[dict]) -> tuple[dict[tuple[str, str], list[dict]], list[str]]:
    current = {s["id"]: sha(json.dumps(s["criteria"], ensure_ascii=False)) for s in scenarios}
    records: dict[tuple[str, str], list[dict]] = {}
    stale: list[str] = []
    for f in sorted(run_dir.glob("*/*.json")):
        r = json.loads(f.read_text(encoding="utf-8"))
        sid = r.get("scenario")
        if sid not in current:
            continue
        if current[sid] != r.get("criteria_sha") or not r.get("results"):
            stale.append(f"{sid} ({f.name})")
            continue
        records.setdefault((sid, r["model"]), []).append(r)
    return records, stale


def summarize(run_dir: Path, scenarios: list[dict]) -> None:
    records, stale = load_records(run_dir, scenarios)
    models = sorted({m for _, m in records})
    col_w = max([22] + [len(slug(m)) + 2 for m in models])
    print(f"\n{run_dir.name}: criteria passed per scenario (summed over repeats)")
    print(f"{'scenario':32}" + "".join(f"{slug(m):>{col_w}}" for m in models))
    totals = {m: [0, 0] for m in models}
    for s in scenarios:
        row = f"{s['id']:32}"
        for m in models:
            recs = records.get((s["id"], m), [])
            ok = sum(r["pass"] for rec in recs for r in rec["results"])
            n = sum(len(rec["results"]) for rec in recs)
            totals[m][0] += ok
            totals[m][1] += n
            row += f"{(f'{ok}/{n}' if n else '-'):>{col_w}}"
        print(row)
    print(f"{'total':32}" + "".join(f"{f'{a}/{b}':>{col_w}}" for a, b in totals.values()))
    if stale:
        print(f"WARNING: ignored {len(stale)} stale record(s) in {run_dir.name}: {', '.join(stale)}", file=sys.stderr)


def compare(dir_a: Path, dir_b: Path, scenarios: list[dict]) -> int:
    for d in (dir_a, dir_b):
        if not d.is_dir():
            print(f"ERROR: run directory does not exist: {d}", file=sys.stderr)
            return 2
    ra, stale_a = load_records(dir_a, scenarios)
    rb, stale_b = load_records(dir_b, scenarios)
    if stale_a or stale_b:
        if stale_a:
            print(f"ERROR: {dir_a.name} has stale criteria records (re-judge before comparing): {', '.join(stale_a)}", file=sys.stderr)
        if stale_b:
            print(f"ERROR: {dir_b.name} has stale criteria records (re-judge before comparing): {', '.join(stale_b)}", file=sys.stderr)
        return 2
    models = sorted({m for _, m in ra} & {m for _, m in rb})
    if not models:
        print(f"ERROR: no overlapping models between {dir_a.name} and {dir_b.name}", file=sys.stderr)
        return 2
    missing_in_b: list[str] = []
    new_in_b: list[str] = []
    judge_errors: list[str] = []
    for s in scenarios:
        for m in models:
            a, b = ra.get((s["id"], m), []), rb.get((s["id"], m), [])
            if not a and not b:
                continue
            if a and not b:
                missing_in_b.append(f"{s['id']} ({slug(m)})")
                continue
            if not a and b:
                new_in_b.append(f"{s['id']} ({slug(m)})")
                continue
            ja = {rec.get("judge") for rec in a}
            jb = {rec.get("judge") for rec in b}
            if any(not isinstance(j, str) or not j.strip() for j in ja | jb):
                judge_errors.append(f"{s['id']} ({slug(m)}): missing judge")
            elif len(ja) != 1 or len(jb) != 1 or ja != jb:
                judge_errors.append(f"{s['id']} ({slug(m)}): {sorted(ja)} vs {sorted(jb)}")
    if missing_in_b:
        print(
            f"ERROR: {dir_b.name} is missing baseline scenario/model pair(s) from {dir_a.name}: {', '.join(missing_in_b)}",
            file=sys.stderr,
        )
        return 2
    if judge_errors:
        print(f"ERROR: judge mismatch or missing judge: {', '.join(judge_errors)}", file=sys.stderr)
        return 2
    worse = better = compared = 0
    for s in scenarios:
        for m in models:
            a, b = ra.get((s["id"], m), []), rb.get((s["id"], m), [])
            if not a or not b:
                continue
            for i, c in enumerate(s["criteria"]):
                compared += 1
                pa = sum(rec["results"][i]["pass"] for rec in a) / len(a)
                pb = sum(rec["results"][i]["pass"] for rec in b) / len(b)
                if pb == pa:
                    continue
                mark = "WORSE " if pb < pa else "better"
                worse += pb < pa
                better += pb > pa
                why = "; ".join(rec["results"][i]["reason"] for rec in (b if pb < pa else a) if not rec["results"][i]["pass"])
                print(f"{mark} {s['id']} {slug(m)} #{i + 1} {pa:.0%} -> {pb:.0%}  {c}\n       judge on the failing side: {why}")
    if new_in_b:
        print(f"NOTE: skipped {len(new_in_b)} newly added scenario/model pair(s) only in {dir_b.name}: {', '.join(new_in_b)}", file=sys.stderr)
    if compared == 0:
        print(f"ERROR: 0 overlapping criteria compared between {dir_a.name} and {dir_b.name}", file=sys.stderr)
        return 2
    print(f"\n{dir_a.name} -> {dir_b.name}: {compared} criteria compared, {worse} worse, {better} better, models compared: {', '.join(slug(m) for m in models)}")
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
    meta: dict = {"root": str(args.root.resolve()), "source": head, "commit": commit, "judge": args.judge}
    if not args.ref:
        meta["dirty"] = bool(subprocess.run(["git", "-C", str(args.root), "status", "--porcelain"], capture_output=True, text=True).stdout.strip())
    (out / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
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
