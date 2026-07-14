from dataclasses import replace
from pathlib import Path
from typing import Callable

from acp.builder.apply.fork.change_summary import (
    build_apply_fork_change_summary_parameter,
)
from cmoc_runtime import SessionState, reports_dir, run_git, timestamp
from config.cmoc_config import CmocConfig


CodexExec = Callable[..., object]
MANAGED_CHANGE_DIFF_OPTIONS = ("--find-renames", "--diff-filter=ACMRT")
UNCONVERGED_FINDINGS_NOTE = "まだ所見が残っている可能性があります。"


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
    # <work-root>/oracle/doc/app_spec/sub_command/apply_fork.md
    # Initialization errors can be reported before the linked worktree exists.
    if not apply_worktree.is_dir():
        return [
            {
                "category": "初期化失敗",
                "summary": "apply worktree が作成される前に失敗しました。",
                "changed_paths": [],
            }
        ]
    raw_diff = changed_diff_since_fork(apply_worktree, fork_commit)
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
            replace(
                build_apply_fork_change_summary_parameter(raw_diff),
                cwd=apply_worktree,
            ),
            root=root,
            cwd=apply_worktree,
            config=config,
            purpose="apply fork change summary",
        ).output_json
    except Exception:
        return fallback_change_summary(apply_worktree, fork_commit, "変更要約生成失敗")
    changes = list((summary or {}).get("changes", []))
    if not changes:
        return fallback_change_summary(apply_worktree, fork_commit, "変更要約なし")
    return changes


def changed_diff_since_fork(apply_worktree: Path, fork_commit: str) -> str:
    # <work-root>/oracle/doc/app_spec/misc_spec.md excludes deleted paths from
    # managed-branch event scope and classifies renames by their new path.
    commands = (
        [
            ["diff", *MANAGED_CHANGE_DIFF_OPTIONS, f"{fork_commit}..HEAD"],
            ["diff", *MANAGED_CHANGE_DIFF_OPTIONS],
            ["diff", "--cached", *MANAGED_CHANGE_DIFF_OPTIONS],
        ]
        if fork_commit
        else [
            ["diff", *MANAGED_CHANGE_DIFF_OPTIONS, "HEAD"],
        ]
    )
    diffs = [
        diff for command in commands if (diff := run_git(command, apply_worktree).stdout)
    ]
    diffs.extend(untracked_file_diffs(apply_worktree))
    return "\n".join(diffs)


def untracked_paths(apply_worktree: Path) -> list[str]:
    return run_git(
        ["ls-files", "--others", "--exclude-standard"], apply_worktree
    ).stdout.splitlines()


def untracked_file_diffs(apply_worktree: Path) -> list[str]:
    # `<work-root>/oracle/doc/app_spec/sub_command/apply_fork.md` requires all
    # apply-branch changes; `<work-root>/oracle/doc/app_spec/misc_spec.md` makes
    # untracked worktree files part of that.
    diffs: list[str] = []
    for path in untracked_paths(apply_worktree):
        result = run_git(
            ["diff", "--no-index", "--", "/dev/null", path],
            apply_worktree,
            check=False,
        )
        if result.stdout:
            diffs.append(result.stdout)
    return diffs


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
            [
                "diff",
                "--name-only",
                *MANAGED_CHANGE_DIFF_OPTIONS,
                f"{fork_commit}..HEAD",
            ],
            ["diff", "--name-only", *MANAGED_CHANGE_DIFF_OPTIONS],
            ["diff", "--cached", "--name-only", *MANAGED_CHANGE_DIFF_OPTIONS],
        ]
        if fork_commit
        else [
            ["diff", "--name-only", *MANAGED_CHANGE_DIFF_OPTIONS, "HEAD"],
            ["diff", "--name-only", *MANAGED_CHANGE_DIFF_OPTIONS],
            ["diff", "--cached", "--name-only", *MANAGED_CHANGE_DIFF_OPTIONS],
        ]
    )
    paths: list[str] = []
    for path in [
        path
        for command in commands
        for path in run_git(command, apply_worktree).stdout.splitlines()
    ] + untracked_paths(apply_worktree):
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
        "unconverged": "未収束: 回数上限に達したためループを終了しました。",
        "error": "エラー: 途中でエラーが起きてループを正常に終了出来ませんでした。",
    }.get(result_label, result_label)
    count_line_items = [
        f"- ループ {idx}: {count}" for idx, count in enumerate(finding_counts, 1)
    ] or ["- 所見列挙ループは実行されませんでした"]
    # <work-root>/oracle/doc/app_spec/sub_command/apply_fork.md requires this
    # warning in the finding-count transition section, not only in the result.
    if result_label == "unconverged":
        count_line_items.append(UNCONVERGED_FINDINGS_NOTE)
    count_lines = "\n".join(count_line_items)
    change_lines = "\n".join(
        (
            f"- {change.get('category')}: {change.get('summary')} "
            f"({', '.join(change.get('changed_paths', [])) or '変更 path なし'})"
        )
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
            "# cmoc apply fork 作業レポート",
            "## 作業結果",
            result_text,
            "## 所見数の推移",
            count_lines,
            "## 変更内容要約",
            change_lines,
            "",
        ]
    )
