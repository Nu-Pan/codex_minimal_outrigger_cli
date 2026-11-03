"""join 中の内容統合と cmoc 管理物の解消を分担する。"""

import hashlib
from collections.abc import Callable
from pathlib import Path
from typing import Any

from oracle.request_builder.basic import AgentCallParameter

from .runtime_codex import run_codex_exec
from .runtime_errors import CmocError
from .runtime_git import (
    run_git,
    status_path_statuses,
)
from .runtime_paths import refactor_state_path, repo_root
from .runtime_primary_report import update_primary_report_fields
from .runtime_refactor import merge_refactor_states
from .runtime_results import CodexExecCallable


def unmerged_paths(root: Path) -> list[str]:
    """marker の有無に依存せず Git index の未統合 path を列挙する。"""
    return [
        path
        for path in run_git(
            ["diff", "--name-only", "-z", "--diff-filter=U"], root
        ).stdout.split("\0")
        if path
    ]


def resolve_merge_conflicts(
    root: Path,
    build_parameter: Callable[[], AgentCallParameter],
    *,
    codex_exec: CodexExecCallable | None = None,
    purpose: str,
    initial_conflicts: list[str] | None = None,
    before_commit: Callable[[], None] | None = None,
    record_result: Callable[[dict[str, Any]], None] | None = None,
    sync_managed_entries: bool = True,
) -> dict[str, Any]:
    """内容を agent に委ね、refactor state と全変更を merge commit に収める。"""
    # report 用の初期一覧を受け取った場合は、同じ index を再照会しない。
    conflicts = unmerged_paths(root) if initial_conflicts is None else initial_conflicts
    if not conflicts:
        raise CmocError("merge 失敗時の競合 path を特定できません。", [], "")
    conflict_paths = set(conflicts)
    refactor_relative = refactor_state_path(root).relative_to(root).as_posix()
    managed = conflict_paths & {refactor_relative}
    content_conflicts = sorted(conflict_paths - managed)
    result: dict[str, Any] = {
        "initial_conflicts": conflicts,
        "content_conflicts": content_conflicts,
        "agent_status": "not_confirmed" if content_conflicts else "not_needed",
        "agent_report": None,
        "call_log": None,
        "incidental_paths": [],
    }
    update_primary_report_fields(conflict_resolution=result)
    if record_result is not None:
        record_result(result)
    if content_conflicts:
        # 管理物だけの競合では、使わない prompt と path context を構築しない。
        parameter = build_parameter()
        before = _status_snapshot(root, conflict_paths)
        output = (codex_exec or run_codex_exec)(
            parameter, root=repo_root(root), purpose=purpose
        )
        report = getattr(output, "output_text", "")
        result["agent_report"] = report
        log = getattr(output, "call_log_path", None)
        result["call_log"] = str(log) if log is not None else None
        # 自由文は報告用に保存する。call の終了と Git の機械検査を区別する。
        result["agent_status"] = "completed"
        if record_result is not None:
            record_result(result)
        update_primary_report_fields(
            conflict_resolution_status=result["agent_status"],
            conflict_agent_report=report,
            conflict_call_log=result["call_log"],
        )
        if before_commit is not None:
            before_commit()
        after = _status_snapshot(root, conflict_paths)
        changed = {
            path
            for path in before.keys() | after.keys()
            if before.get(path) != after.get(path)
        }
        # 付随編集の観測は report 用。受理条件は下記正本の検証境界に従う。
        # {{work-root}}/spec/app_spec/codex_common_rule.md の「agent call の差分検証」
        result["incidental_paths"] = sorted(changed)
        if record_result is not None:
            record_result(result)
    if refactor_relative in managed:
        merge_refactor_states(
            root, ("HEAD", "MERGE_HEAD"), sync_entries=sync_managed_entries
        )
    run_git(["add", "-A"], root)
    _check_staged_merge(root)
    run_git(["commit", "--no-edit"], root)
    return result


def _status_snapshot(
    root: Path, initial_conflicts: set[str]
) -> dict[str, tuple[str, str | None]]:
    """初期競合以外の付随編集を、差分 path の再編集も含めて捕捉する。"""
    snapshot: dict[str, tuple[str, str | None]] = {}
    for status, path in status_path_statuses(
        root, untracked_all=True, include_rename_sources=True
    ):
        name = path.relative_to(root).as_posix()
        # 初期競合は付随編集の報告対象外。内容検査は staging 後の marker 検査が担う。
        if name in initial_conflicts:
            continue
        if path.is_symlink():
            content = str(path.readlink()).encode()
        elif path.is_file():
            content = path.read_bytes()
        else:
            content = None
        snapshot[name] = (
            status,
            hashlib.sha256(content).hexdigest() if content is not None else None,
        )
    return snapshot


def _check_staged_merge(root: Path) -> None:
    """同じ index 一覧から未統合 entry と regular text の残存 marker を拒否する。"""
    # rename を削除・追加に分け、status と path の二項を NUL 区切りで取得する。
    fields = run_git(
        ["diff", "--cached", "--name-status", "--no-renames", "-z"], root
    ).stdout.split("\0")
    staged = list(zip(fields[::2], fields[1::2]))
    remaining = [relative for status, relative in staged if status == "U"]
    if remaining:
        raise CmocError("unmerged path が残っています。", [], "\n".join(remaining))
    for _status, relative in staged:
        path = root / relative
        if path.is_symlink() or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            continue
        if _has_conflict_marker_block(text):
            raise CmocError("conflict marker が残っています。", [], relative)


def _has_conflict_marker_block(text: str) -> bool:
    """行頭の Git marker を検出し、Markdown の bare separator を許す。"""
    # marker のない本文では、全行の分割と行頭の走査を省く。
    markers = ("<<<<<<<", "|||||||", ">>>>>>>")
    if not any(marker in text for marker in markers):
        return False
    return any(line.startswith(markers) for line in text.splitlines())
