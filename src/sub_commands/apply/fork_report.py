from pathlib import Path
from typing import Callable

from acp.builder.apply.fork.change_summary import (
    build_apply_fork_change_summary_parameter,
)
from cmoc_runtime import SessionState, reports_dir, run_git, timestamp
from config.cmoc_config import CmocConfig


CodexExec = Callable[..., object]


def write_apply_fork_report(
    root: Path,
    apply_worktree: Path,
    session_branch: str,
    state: SessionState,
    finding_counts: list[int],
    result_label: str,
    config: CmocConfig,
    codex_exec: CodexExec,
) -> Path:
    """apply fork の実行結果 report を生成する。"""
    apply_branch = state.apply.apply_branch or ""
    fork_commit = state.apply.oracle_snapshot_commit or ""
    changes = build_change_summary(
        root, apply_worktree, fork_commit, config, codex_exec
    )
    report_dir = reports_dir(root, "apply/fork")
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"{timestamp()}.md"
    path.write_text(
        render_apply_fork_report(
            root,
            session_branch,
            state,
            apply_branch,
            fork_commit,
            apply_worktree,
            result_label,
            finding_counts,
            changes,
        )
    )
    return path


def write_apply_fork_error_report(
    root: Path,
    session_branch: str,
    state: SessionState,
    finding_counts: list[int],
    apply_worktree: Path,
    config: CmocConfig,
    codex_exec: CodexExec,
) -> Path:
    """apply fork 失敗時の report を生成する。"""
    apply_branch = state.apply.apply_branch or ""
    fork_commit = state.apply.oracle_snapshot_commit or ""
    changes = build_change_summary(
        root, apply_worktree, fork_commit, config, codex_exec
    )
    report_dir = reports_dir(root, "apply/fork")
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"{timestamp()}.md"
    path.write_text(
        render_apply_fork_report(
            root,
            session_branch,
            state,
            apply_branch,
            fork_commit,
            apply_worktree,
            "error",
            finding_counts,
            changes,
        )
    )
    return path


def build_change_summary(
    root: Path,
    apply_worktree: Path,
    fork_commit: str,
    config: CmocConfig,
    codex_exec: CodexExec,
) -> list[dict]:
    raw_diff = (
        run_git(["diff", f"{fork_commit}..HEAD"], apply_worktree).stdout
        if fork_commit
        else run_git(["diff", "HEAD"], apply_worktree).stdout
    )
    if not raw_diff.strip():
        return [
            {
                "category": "変更なし",
                "summary": "apply fork による実装差分はありません。",
                "changed_paths": [],
            }
        ]
    try:
        summary = codex_exec(
            build_apply_fork_change_summary_parameter(raw_diff),
            root=root,
            cwd=apply_worktree,
            config=config,
            purpose="apply fork change summary",
        ).output_json
    except Exception:
        return fallback_change_summary(apply_worktree, fork_commit, "変更要約生成失敗")
    return list((summary or {}).get("changes", [])) or [
        {
            "category": "変更要約なし",
            "summary": "変更差分はありますが、構造化された変更要約は空でした。",
            "changed_paths": [],
        }
    ]


def fallback_change_summary(
    apply_worktree: Path, fork_commit: str, category: str
) -> list[dict]:
    paths = changed_paths_since_fork(apply_worktree, fork_commit)
    if not paths:
        return [
            {
                "category": "変更なし",
                "summary": "apply fork による実装差分はありません。",
                "changed_paths": [],
            }
        ]
    return [
        {
            "category": category,
            "summary": "変更 path のみを機械的に記録しました。",
            "changed_paths": paths,
        }
    ]


def changed_paths_since_fork(apply_worktree: Path, fork_commit: str) -> list[str]:
    commands = (
        [
            ["diff", "--name-only", f"{fork_commit}..HEAD"],
            ["diff", "--name-only"],
            ["diff", "--cached", "--name-only"],
        ]
        if fork_commit
        else [
            ["diff", "--name-only", "HEAD"],
            ["diff", "--name-only"],
            ["diff", "--cached", "--name-only"],
        ]
    )
    paths: list[str] = []
    for command in commands:
        for path in run_git(command, apply_worktree).stdout.splitlines():
            if path not in paths:
                paths.append(path)
    return paths


def render_apply_fork_report(
    root: Path,
    session_branch: str,
    state: SessionState,
    apply_branch: str,
    apply_fork_commit: str,
    apply_worktree: Path,
    result_label: str,
    finding_counts: list[int],
    changes: list[dict],
) -> str:
    """apply fork report を Markdown + YAML frontmatter で描画する。"""
    result_text = {
        "converged": "収束: 検出された所見リストが空によりループを終了しました。",
        "unconverged": "未収束: 回数上限に達したためループを終了しました。まだ所見が残っている可能性があります。",
        "error": "エラー: 途中でエラーが起きてループを正常に終了出来ませんでした。",
    }.get(result_label, result_label)
    count_lines = "\n".join(
        f"- loop {idx}: {count}" for idx, count in enumerate(finding_counts, 1)
    ) or "- no finding enumeration loops were executed"
    change_lines = "\n".join(
        f"- {change.get('category')}: {change.get('summary')} ({', '.join(change.get('changed_paths', [])) or 'no paths'})"
        for change in changes
    )
    return "\n".join(
        [
            "---",
            f"cmoc_session_branch: {session_branch}",
            f"cmoc_session_fork_commit: {state.session.session_start_commit}",
            f"cmoc_apply_branch: {apply_branch}",
            f"cmoc_apply_fork_commit: {apply_fork_commit}",
            f"cmoc_apply_worktree: {apply_worktree}",
            f"result: {result_label}",
            "---",
            "# cmoc apply fork report",
            "## Result",
            result_text,
            "## Finding Count",
            count_lines,
            "## Change Summary",
            change_lines,
            "",
        ]
    )
