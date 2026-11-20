#!/usr/bin/env python3
"""Unit and integration guard tests for verify.py, replay.py, and the git-bus hook."""

from __future__ import annotations

import contextlib
import io
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "evals"))

import replay  # noqa: E402
import verify  # noqa: E402


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.setdefault("GIT_AUTHOR_NAME", "Test")
    env.setdefault("GIT_AUTHOR_EMAIL", "test@example.com")
    env.setdefault("GIT_COMMITTER_NAME", "Test")
    env.setdefault("GIT_COMMITTER_EMAIL", "test@example.com")
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )


def _init_min_aperture_repo(repo: Path) -> None:
    _git(repo, "init", "-b", "main")
    (repo / "VERSION").write_text("1.0.0\n", encoding="utf-8")
    skill_dir = repo / "skills" / "demo"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: demo\nversion: 1.0.0\ndescription: >\n  Demo skill.\n---\n\n# Demo\n",
        encoding="utf-8",
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "init")


class VerifyGuardTests(unittest.TestCase):
    def test_clean_repo_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _init_min_aperture_repo(repo)
            ver, skills, mds, errors = verify.verify_repo(repo)
            self.assertEqual(ver, "1.0.0")
            self.assertEqual(skills, 1)
            self.assertEqual(mds, 1)
            self.assertEqual(errors, [])

    def test_untracked_skill_link_escape_and_broken_link_caught(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _init_min_aperture_repo(repo)
            (repo / "README.md").write_text("# Root\n", encoding="utf-8")
            # Untracked new skill file escaping boundary + untracked doc with broken link.
            new_skill = repo / "skills" / "fresh"
            new_skill.mkdir(parents=True)
            (new_skill / "SKILL.md").write_text(
                "---\nname: fresh\nversion: 1.0.0\ndescription: Fresh.\n---\n\n[escape](../../README.md)\n",
                encoding="utf-8",
            )
            (repo / "notes.md").write_text("[missing](does-not-exist.md)\n", encoding="utf-8")
            _, _, _, errors = verify.verify_repo(repo)
            self.assertTrue(any("escapes standalone skill boundary" in e for e in errors), errors)
            self.assertTrue(any("broken relative link 'does-not-exist.md'" in e for e in errors), errors)

    def test_percent_encoded_path_and_anchor_and_double_backtick_code_span(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _init_min_aperture_repo(repo)
            target = repo / "中文文档.md"
            target.write_text("# 第一节 概述\n", encoding="utf-8")
            encoded_path = quote("中文文档.md")
            encoded_anchor = quote("第一节-概述")
            (repo / "README.md").write_text(
                f"[ok]({encoded_path}#{encoded_anchor})\n\n"
                "Inline double backticks: ``[not a link](missing.md)`` and `[also ignored](nope.md)`.\n\n"
                "Multiline single span: `line1\n[multiline-ignored](missing1.md)\nline3`.\n\n"
                "Multiline double span: ``line1\n`[multiline-ignored-2](missing2.md)`\nline3``.\n",
                encoding="utf-8",
            )
            _, _, _, errors = verify.verify_repo(repo)
            self.assertEqual(errors, [])

    def test_unclosed_backtick_does_not_swallow_next_paragraph(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _init_min_aperture_repo(repo)
            (repo / "README.md").write_text(
                "Paragraph with unclosed `backtick.\n\n"
                "Second paragraph has a real [broken](still-missing.md) link.\n",
                encoding="utf-8",
            )
            _, _, _, errors = verify.verify_repo(repo)
            self.assertTrue(any("still-missing.md" in e for e in errors), errors)

    def test_forbidden_asset_filenames_caught(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _init_min_aperture_repo(repo)
            assets = repo / "skills" / "demo" / "assets"
            assets.mkdir()
            (assets / "AGENTS.md").write_text("# bad\n", encoding="utf-8")
            (assets / "CLAUDE.md").write_text("# bad\n", encoding="utf-8")
            _, _, _, errors = verify.verify_repo(repo)
            self.assertTrue(any("AGENTS.md" in e for e in errors), errors)
            self.assertTrue(any("CLAUDE.md" in e for e in errors), errors)

    def test_version_mismatch_caught(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _init_min_aperture_repo(repo)
            (repo / "VERSION").write_text("2.0.0\n", encoding="utf-8")
            _, _, _, errors = verify.verify_repo(repo)
            self.assertTrue(any("does not match root VERSION '2.0.0'" in e for e in errors), errors)


class ReplayTests(unittest.TestCase):
    def test_slug_preserves_provider_prefix(self) -> None:
        self.assertNotEqual(replay.slug("providerA/gpt-5@high"), replay.slug("providerB/gpt-5@high"))
        self.assertEqual(replay.slug("providerA/gpt-5@high"), "providerA__gpt-5_high")

    def test_parse_judgement_with_surrounding_braces_and_prose(self) -> None:
        raw = (
            'Note {ignored}: {"meta": 1}\n'
            '{"results": [{"id": 2, "pass": false, "reason": "missed"}, '
            '{"id": 1, "pass": true, "reason": "ok"}]}\n'
            "Trailing {comment}"
        )
        parsed = replay.parse_judgement(raw, 2)
        self.assertEqual(parsed, [{"pass": True, "reason": "ok"}, {"pass": False, "reason": "missed"}])

    def test_parse_judgement_rejects_bad_ids_without_type_error(self) -> None:
        for bad in (
            '{"results": [{"id": "1", "pass": true}]}',
            '{"results": [{"id": true, "pass": true}]}',
            '{"results": ["not-a-dict"]}',
            '{"results": [{"id": 1, "pass": "yes"}]}',
        ):
            with self.assertRaises(ValueError):
                replay.parse_judgement(bad, 1)

    def _write_record(
        self,
        run_dir: Path,
        sid: str,
        model: str,
        criteria: list[str],
        passes: list[bool],
        *,
        judge: str | None = "judge-a",
        criteria_override: list[str] | None = None,
    ) -> None:
        c_sha = replay.sha(json.dumps(criteria_override or criteria, ensure_ascii=False))
        rec = {
            "scenario": sid,
            "model": model,
            "repeat": 0,
            "criteria_sha": c_sha,
            "results": [{"pass": p, "reason": "ok" if p else "fail"} for p in passes],
        }
        if judge is not None:
            rec["judge"] = judge
        p = run_dir / sid / f"{replay.slug(model)}.0.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(rec), encoding="utf-8")

    def test_compare_fail_closed_cases_and_pass_worse(self) -> None:
        scenarios = [
            {"id": "s1", "criteria": ["c1", "c2"]},
            {"id": "s2", "criteria": ["c3"]},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            a, b = root / "a", root / "b"
            a.mkdir()
            b.mkdir()

            # Missing directory -> fail closed (2)
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(replay.compare(a, root / "missing", scenarios), 2)

            # Empty / no overlapping models -> fail closed (2)
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(replay.compare(a, b, scenarios), 2)

            # Stale criteria_sha on s1 alongside valid s2 -> MUST fail closed (2) mentioning stale, not silently compare only s2
            self._write_record(a, "s1", "m1", scenarios[0]["criteria"], [True, True], criteria_override=["old"])
            self._write_record(b, "s1", "m1", scenarios[0]["criteria"], [True, True])
            self._write_record(a, "s2", "m1", scenarios[1]["criteria"], [True])
            self._write_record(b, "s2", "m1", scenarios[1]["criteria"], [True])
            stale_err = io.StringIO()
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(stale_err):
                self.assertEqual(replay.compare(a, b, scenarios), 2)
            self.assertIn("stale", stale_err.getvalue())

            # Judge mismatch -> fail closed (2)
            self._write_record(a, "s1", "m1", scenarios[0]["criteria"], [True, True], judge="judge-a")
            self._write_record(b, "s1", "m1", scenarios[0]["criteria"], [True, True], judge="judge-b")
            self._write_record(b, "s2", "m1", scenarios[1]["criteria"], [True], judge="judge-b")
            judge_err = io.StringIO()
            with contextlib.redirect_stderr(judge_err):
                self.assertEqual(replay.compare(a, b, scenarios), 2)
            self.assertIn("judge mismatch", judge_err.getvalue())

            # Matching judge + one-sided new scenario s2 (only in b) -> passes (0) and notes s2
            (a / "s2" / f"{replay.slug('m1')}.0.json").unlink()
            self._write_record(b, "s1", "m1", scenarios[0]["criteria"], [True, True], judge="judge-a")
            self._write_record(b, "s2", "m1", scenarios[1]["criteria"], [True], judge="judge-a")
            err_buf = io.StringIO()
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err_buf):
                self.assertEqual(replay.compare(a, b, scenarios), 0)
            self.assertIn("s2", err_buf.getvalue())

            # Regression -> exit 1
            self._write_record(b, "s1", "m1", scenarios[0]["criteria"], [True, False], judge="judge-a")
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(replay.compare(a, b, scenarios), 1)

    def test_compare_rejects_missing_baseline_swapped_judges_and_missing_judge(self) -> None:
        scenarios = [
            {"id": "s1", "criteria": ["c1"]},
            {"id": "s2", "criteria": ["c2"]},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            a, b = root / "a", root / "b"
            a.mkdir()
            b.mkdir()

            # Baseline has s1 & s2, candidate b lost s2 -> MUST fail closed (2)
            self._write_record(a, "s1", "m1", scenarios[0]["criteria"], [True], judge="j1")
            self._write_record(a, "s2", "m1", scenarios[1]["criteria"], [True], judge="j1")
            self._write_record(b, "s1", "m1", scenarios[0]["criteria"], [True], judge="j1")
            err = io.StringIO()
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
                self.assertEqual(replay.compare(a, b, scenarios), 2)
            self.assertIn("missing baseline", err.getvalue())

            # Swapped per-scenario judges (global set is {j1, j2} on both sides) -> MUST fail closed (2)
            self._write_record(a, "s1", "m1", scenarios[0]["criteria"], [True], judge="j1")
            self._write_record(a, "s2", "m1", scenarios[1]["criteria"], [True], judge="j2")
            self._write_record(b, "s1", "m1", scenarios[0]["criteria"], [True], judge="j2")
            self._write_record(b, "s2", "m1", scenarios[1]["criteria"], [True], judge="j1")
            err = io.StringIO()
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
                self.assertEqual(replay.compare(a, b, scenarios), 2)
            self.assertIn("judge mismatch", err.getvalue())

            # Missing judge field on a record -> MUST fail closed (2)
            self._write_record(a, "s1", "m1", scenarios[0]["criteria"], [True], judge=None)
            self._write_record(a, "s2", "m1", scenarios[1]["criteria"], [True], judge="j1")
            self._write_record(b, "s1", "m1", scenarios[0]["criteria"], [True], judge="j1")
            self._write_record(b, "s2", "m1", scenarios[1]["criteria"], [True], judge="j1")
            err = io.StringIO()
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
                self.assertEqual(replay.compare(a, b, scenarios), 2)
            self.assertIn("missing judge", err.getvalue())


class GitBusHookTests(unittest.TestCase):
    def _extract_hook_script(self) -> str:
        text = (ROOT / "skills" / "multi-agent-collab" / "references" / "git-bus.md").read_text(encoding="utf-8")
        m = re.search(r"```bash\n(.*?)\n```", text, re.S)
        self.assertIsNotNone(m, "git-bus.md must contain a bash hook block")
        assert m is not None
        return m.group(1)

    def test_post_commit_hook_edge_triggers_and_worktree_isolation(self) -> None:
        template = self._extract_hook_script()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            _git(repo, "init", "-b", "main")
            wake_log = Path(tmp) / "wakes.log"
            wake_bin = Path(tmp) / "wake.sh"
            wake_bin.write_text(f'#!/usr/bin/env bash\necho "$*" >> "{wake_log}"\n', encoding="utf-8")
            wake_bin.chmod(wake_bin.stat().st_mode | stat.S_IXUSR)

            hook_script = template.replace("<wake-project-router-command>", str(wake_bin)).replace("<project>", "demo")
            hook_path = repo / ".git" / "hooks" / "post-commit"
            hook_path.write_text(hook_script + "\n", encoding="utf-8")
            hook_path.chmod(hook_path.stat().st_mode | stat.S_IXUSR)

            def wake_count() -> int:
                return len(wake_log.read_text(encoding="utf-8").splitlines()) if wake_log.exists() else 0

            (repo / ".gitignore").write_text(".tmp/\n", encoding="utf-8")
            tasks = repo / "docs" / "TASKS.md"
            tasks.parent.mkdir()

            # 1. Initial commit adding Milestone #1 (pending) -> wakes (1)
            tasks.write_text("# Tasks\n\n## [Milestone #1] First\n- **Status**: pending\n", encoding="utf-8")
            _git(repo, "add", ".gitignore", "docs/TASKS.md")
            _git(repo, "commit", "-m", "add m1")
            self.assertEqual(wake_count(), 1)

            # 2. Unrelated code commit -> no wake (1)
            (repo / "app.txt").write_text("v1\n", encoding="utf-8")
            _git(repo, "add", "app.txt")
            _git(repo, "commit", "-m", "code change")
            self.assertEqual(wake_count(), 1)

            # 3. Router closes #1 (pending -> verified) -> no self-wake (1)
            tasks.write_text("# Tasks\n\n## [Milestone #1] First\n- **Status**: verified\n", encoding="utf-8")
            _git(repo, "commit", "--only", "docs/TASKS.md", "-m", "verify m1")
            self.assertEqual(wake_count(), 1)

            # 4. Create linked worktree before Brain adds #2
            wt = repo / ".tmp" / "worktrees" / "m2-s1"
            _git(repo, "worktree", "add", "-b", "m2-s1", str(wt))

            # 5. Brain appends #2 with plain "Status: pending" on main -> wakes (2)
            tasks.write_text(
                "# Tasks\n\n## [Milestone #1] First\n- **Status**: verified\n\n"
                "## [Milestone #2] Second\nStatus: pending\n",
                encoding="utf-8",
            )
            _git(repo, "commit", "--only", "docs/TASKS.md", "-m", "add m2")
            self.assertEqual(wake_count(), 2)

            # 6. Worker commits and resolves a merge of main inside linked worktree (fires post-commit)
            # -> MUST NOT wake (still 2) and must not error on `.git` being a file
            (wt / "slice.txt").write_text("work\n", encoding="utf-8")
            _git(wt, "add", "slice.txt")
            _git(wt, "commit", "-m", "worker slice")
            _git(wt, "merge", "--no-commit", "--no-ff", "main")
            merge_res = _git(wt, "commit", "-m", "merge main into worktree")
            self.assertNotIn("Not a directory", merge_res.stderr)
            self.assertEqual(wake_count(), 2)

            # 7. Rewriting block heading so diff treats Status: pending as context -> NEW_PENDING wakes (3)
            tasks.write_text(
                "# Tasks\n\n## [Milestone #1] First\n- **Status**: verified\n\n"
                "## [Milestone #3] Rewritten\nStatus: pending\n",
                encoding="utf-8",
            )
            _git(repo, "commit", "--only", "docs/TASKS.md", "-m", "rewrite heading")
            self.assertEqual(wake_count(), 3)

            err_file = repo / ".git" / "router-wakeup.err"
            if err_file.exists():
                self.assertEqual(err_file.read_text(encoding="utf-8").strip(), "")


if __name__ == "__main__":
    unittest.main()
