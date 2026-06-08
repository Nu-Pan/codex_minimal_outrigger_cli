"""tests.test_subcommands package common imports and helpers."""

import ast
import builtins
import inspect
import json
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest
import typer
from pytest import MonkeyPatch

import sub_commands.apply.fork as apply_module
import sub_commands.apply.join as apply_join_module
import sub_commands.indexing as indexing_module
import sub_commands.review.oracles as review_oracles_module
import sub_commands.session.abandon as session_abandon_module
import sub_commands.session.fork as session_fork_module
import sub_commands.session.join as session_join_module
import commons.repo as repo_module
import commons.timing as timing_module
from commons.codex import COST_PERFORMANCE_MODEL
from commons.codex import COST_PERFORMANCE_REASONING_EFFORT
from commons.codex import FRONTIER_HIGH_REASONING_EFFORT
from commons.codex import FRONTIER_MODEL
from commons.codex import FRONTIER_REASONING_EFFORT
from commons.codex import COMMIT_MESSAGE_MODEL
from commons.codex import COMMIT_MESSAGE_REASONING_EFFORT
from commons.command_runner import run_command
from commons.errors import CmocError
from commons.errors import format_error_report
from commons.repo import write_apply_process_id
from commons.repo import write_session_state
from commons.subcommand_log import log_event
from commons.subcommand_log import subcommand_log
from commons.timing import StepTimer, start_step
from commons.timestamps import is_timestamp
from sub_commands.apply.fork import cmoc_apply_impl
from sub_commands.apply.fork import _apply_prompt
from sub_commands.apply.fork import _apply_index_excluded_roots
from sub_commands.apply.fork import APPLY_FORK_EXIT_CODE_CONVERGED
from sub_commands.apply.fork import APPLY_FORK_EXIT_CODE_UNCONVERGED
from sub_commands.apply.fork import _DISCREPANCY_OUTPUT_SCHEMA
from sub_commands.apply.fork import _commit_all_changes
from sub_commands.apply.fork import _organize_prompt
from sub_commands.apply.fork import _validate_discrepancy_payload
from sub_commands.apply.abandon import cmoc_apply_abandon_impl
from sub_commands.apply.join import cmoc_apply_join_impl
from sub_commands.review.oracles import cmoc_review_oracles_impl
from sub_commands.indexing import cmoc_indexing_impl
from sub_commands.review.oracles import _evaluation_prompt
from sub_commands.review.oracles import _improvement_prompt
from sub_commands.init import cmoc_init_impl
from sub_commands.session.abandon import cmoc_session_abandon_impl
from sub_commands.session.fork import cmoc_session_fork_impl
from sub_commands.session.join import cmoc_session_join_impl
from sub_commands.session.join import _conflict_prompt
from sub_commands.session.join import _files_with_conflict_markers


def _assert_markdown_error_report(report: str) -> None:
    """共通エラーレポートは markdown 見出しで区切り、空行を含めない。"""
    assert "# ERROR" in report
    assert "## Summary" in report
    assert "## Next actions" in report
    assert "## Detail" in report
    assert "## Call stack" in report
    assert all(line != "" for line in report.splitlines())




def _discrepancy_json(suggested_fix: str) -> str:
    """テスト用の valid な不整合 JSON を返す。"""
    return json.dumps(
        {
            "git_head_commit_hash": None,
            "fixing_points": [
                {
                    "title": "t",
                    "evidences": [
                        {
                            "path": "/repo/oracles/spec.md",
                            "line_start": 1,
                            "line_end": 1,
                            "summary": "spec",
                        }
                    ],
                    "oracle_requirement": "r",
                    "observed_implementation": "o",
                    "reason": "x",
                    "suggested_fix": suggested_fix,
                }
            ]
        }
    )


def _change_summary_json() -> str:
    """テスト用の valid な変更要約 JSON を返す。"""
    return json.dumps(
        {
            "changes": [
                {
                    "category": "実装修正",
                    "summary": "テスト用の変更内容を整理しました。",
                    "changed_paths": ["app.py"],
                }
            ]
        }
    )


def _apply_report(prompt: str, result_label: str, counts: list[int]) -> str:
    """apply report prompt から branch 名を抜き出した valid report を返す。"""
    match = re.search(r"ブランチ `([^`]+)`", prompt)
    branch_name = match.group(1) if match else "cmoc/apply/session/run"
    count_lines = [
        f"{index} 回目: {count} 件"
        for index, count in enumerate(counts, start=1)
    ]
    if result_label == "未収束":
        count_lines.append("まだ要修正点が残っている可能性があります。")
    return "\n".join(
        [
            "## 作業結果",
            result_label,
            "## 要修正点件数の推移",
            *count_lines,
            f"## ブランチ {branch_name} 上の全変更内容",
            "- カテゴリ: 実装修正",
            "  - テスト用の変更内容を整理しました。",
        ]
    )


def _eval_oracle_issue(
    severity: str,
    title: str,
    oracle_path: Path,
    line_start: int | None,
    line_end: int | None,
    referenced_paths: list[Path] | None = None,
) -> dict[str, object]:
    """テスト用の valid な eval-oracles issue item を返す。"""
    references = referenced_paths or [oracle_path]
    return {
        "severity": severity,
        "title": title,
        "oracle_path": str(oracle_path.resolve()),
        "oracle_line_start": line_start,
        "oracle_line_end": line_end,
        "referenced_paths": [str(path.resolve()) for path in references],
        "affected_workflow": "cmoc review oracles",
        "requirement": f"{title} requirement",
        "problem": f"{title} problem",
        "reason": f"{title} reason",
        "suggested_oracle_change": f"{title} change",
        "specification_only_basis": "oracles 配下の仕様だけを参照しました。",
    }


def _init_repo(tmp_path: Path) -> Path:
    """テスト用 git repo を作り、初期 commit を置く。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")
    (repo / "README.md").write_text("test\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "initial")
    return repo


def _checkout_session_branch(repo: Path) -> None:
    """テスト用 cmoc session branch に移動し、state を作る。"""
    session_id = "2026-05-10_22-21_10_000000123"
    branch_name = f"cmoc/session/{session_id}"
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _git(repo, "checkout", "-b", branch_name)
    write_session_state(
        repo,
        session_id,
        {
            "session": {
                "state": "active",
                "session_home_branch": home_branch,
                "session_start_commit": base_commit,
                "last_joined_apply_oracle_snapshot_commit": None,
            },
            "apply": {
                "state": "ready",
                "apply_branch": None,
                "oracle_snapshot_commit": None,
            },
        },
    )
    exclude = repo / ".git" / "info" / "exclude"
    exclude.write_text(f"{exclude.read_text(encoding='utf-8')}\n.cmoc/\n")


def _prepare_review_oracles_session(repo: Path) -> None:
    """review oracles 実行用に clean な session branch へ移動する。"""
    gitignore = repo / ".gitignore"
    content = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    if "/.cmoc/" not in content.splitlines():
        prefix = content
        if prefix and not prefix.endswith("\n"):
            prefix += "\n"
        gitignore.write_text(f"{prefix}/.cmoc/\n", encoding="utf-8")

    if _git(repo, "status", "--porcelain").stdout.strip():
        _git(repo, "add", "-A")
        _git(repo, "commit", "-m", "prepare review oracles")

    branch_name = _git(repo, "branch", "--show-current").stdout.strip()
    if not branch_name.startswith("cmoc/session/"):
        _checkout_session_branch(repo)


def _repo_with_session_join_conflict(
    tmp_path: Path,
    auto_path: str = "auto.txt",
) -> Path:
    """session join で conflict と自動 merge path が発生する repo を作る。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    (repo / "conflict.txt").write_text("base\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", "conflict.txt")
    _git(repo, "commit", "-m", "prepare session")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / "conflict.txt").write_text("session\n", encoding="utf-8")
    auto_file = repo / auto_path
    auto_file.parent.mkdir(parents=True, exist_ok=True)
    auto_file.write_text("session auto\n", encoding="utf-8")
    _git(repo, "add", "conflict.txt", auto_path)
    _git(repo, "commit", "-m", "session change")
    _git(repo, "switch", home_branch)
    (repo / "conflict.txt").write_text("home\n", encoding="utf-8")
    _git(repo, "add", "conflict.txt")
    _git(repo, "commit", "-m", "home change")
    _git(repo, "switch", session_branch)
    return repo


def _repo_with_session_join_oracle_conflict(tmp_path: Path) -> Path:
    """session join で oracle file conflict が発生する repo を作る。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("base oracle\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", "oracles/spec.md")
    _git(repo, "commit", "-m", "prepare oracle session")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    (oracle_root / "spec.md").write_text("session oracle\n", encoding="utf-8")
    _git(repo, "add", "oracles/spec.md")
    _git(repo, "commit", "-m", "session oracle change")
    _git(repo, "switch", home_branch)
    (oracle_root / "spec.md").write_text("home oracle\n", encoding="utf-8")
    _git(repo, "add", "oracles/spec.md")
    _git(repo, "commit", "-m", "home oracle change")
    _git(repo, "switch", session_branch)
    return repo


def _repo_with_session_join_root_doc_conflict(
    tmp_path: Path,
    relative_path: str,
) -> Path:
    """session join で root doc file conflict が発生する repo を作る。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    target = repo / relative_path
    target.write_text("base\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", relative_path)
    _git(repo, "commit", "-m", "prepare root doc session")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    target.write_text("session\n", encoding="utf-8")
    _git(repo, "add", relative_path)
    _git(repo, "commit", "-m", "session change")
    _git(repo, "switch", home_branch)
    target.write_text("home\n", encoding="utf-8")
    _git(repo, "add", relative_path)
    _git(repo, "commit", "-m", "home change")
    _git(repo, "switch", session_branch)
    return repo


def _add_oracle_snapshot(repo: Path) -> str:
    """テスト用 oracle snapshot commit を作る。"""
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", "oracles/spec.md")
    _git(repo, "commit", "-m", "add oracle")
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


def _create_completed_apply_run(
    repo: Path,
    oracle_snapshot: str,
    *,
    report_text: str | None = None,
) -> tuple[str, Path, Path]:
    """completed apply run の branch/worktree/state を作る。"""
    session_id = "2026-05-10_22-21_10_000000123"
    apply_branch = f"cmoc/apply/{session_id}/2026-05-10_22-22_10_000000123"
    apply_worktree = (
        repo
        / ".cmoc"
        / "worktrees"
        / session_id
        / "2026-05-10_22-22_10_000000123"
    )
    report_path = repo / ".cmoc" / "reports" / "apply" / "fork" / "report.md"
    report_path.parent.mkdir(parents=True)
    if report_text is None:
        report_text = "\n".join(
            [
                "---",
                f'cmoc_apply_branch: "{apply_branch}"',
                'result: "収束"',
                "---",
                "",
                "## 作業結果",
                "収束",
                "",
            ]
        )
    report_path.write_text(report_text, encoding="utf-8")
    _git(repo, "branch", apply_branch, oracle_snapshot)
    _git(repo, "worktree", "add", str(apply_worktree), apply_branch)
    state = json.loads(
        (repo / ".cmoc" / "sessions" / f"{session_id}.json").read_text(
            encoding="utf-8"
        )
    )
    state["apply"] = {
        "state": "completed",
        "apply_branch": apply_branch,
        "apply_worktree": str(apply_worktree),
        "oracle_snapshot_commit": oracle_snapshot,
        "completed": True,
        "discrepancy_counts": [0],
        "report_path": str(report_path),
    }
    write_session_state(repo, session_id, state)
    return apply_branch, apply_worktree, report_path


def _session_state_paths(repo: Path) -> list[Path]:
    """テスト repo の session state file 一覧を返す。"""
    session_root = repo / ".cmoc" / "sessions"
    if not session_root.exists():
        return []
    return sorted(session_root.glob("*.json"))


def _run_completion_probe(
    arguments: list[str],
    comp_words: str,
    comp_cword: int,
    *,
    complete_value: str = "complete_bash",
) -> subprocess.CompletedProcess[str]:
    """main module を Click/Typer 補完プローブとして実行する。"""
    repo_root = Path(__file__).resolve().parents[2]
    return subprocess.run(
        [sys.executable, "-m", "main", *arguments],
        cwd=repo_root,
        env={
            "PYTHONPATH": str(repo_root / "src"),
            "_CMOC_COMPLETE": complete_value,
            "COMP_WORDS": comp_words,
            "COMP_CWORD": str(comp_cword),
        },
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """git をテスト repo で実行する。"""
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


__all__ = [name for name in globals() if not name.startswith("__")]
