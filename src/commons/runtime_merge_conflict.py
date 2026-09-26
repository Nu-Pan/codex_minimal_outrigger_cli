"""join 中の内容統合と cmoc 管理物の解消を分担する。"""

import hashlib
import json
from pathlib import Path
from typing import Any

from oracle.acp_builder.basic import AgentCallParameter, FileAccessMode

from .runtime_codex import run_codex_exec
from .runtime_errors import CmocError
from .runtime_git import (
    is_realization_file_path,
    literal_pathspec,
    run_git,
    status_path_statuses,
)
from .runtime_paths import refactor_state_path, repo_root
from .runtime_primary_report import update_primary_report_fields
from .runtime_refactor import sync_refactor_state, write_refactor_state
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
    parameter: AgentCallParameter | None,
    *,
    codex_exec: CodexExecCallable | None = None,
    purpose: str,
) -> dict[str, Any]:
    """内容を agent に委ね、refactor state と全変更を merge commit に収める。"""
    conflicts = unmerged_paths(root)
    if not conflicts:
        raise CmocError("merge 失敗時の競合 path を特定できません。", [], "")
    refactor_relative = refactor_state_path(root).relative_to(root).as_posix()
    managed = {path for path in conflicts if path == refactor_relative}
    content_conflicts = sorted(set(conflicts) - managed)
    result: dict[str, Any] = {
        "initial_conflicts": conflicts,
        "content_conflicts": content_conflicts,
        "agent_status": "not_needed",
        "agent_report": None,
        "call_log": None,
        "incidental_paths": [],
    }
    if content_conflicts:
        if parameter is None:
            raise CmocError(
                "内容競合の agent call を構築できません。",
                [],
                "\n".join(content_conflicts),
            )
        before = _status_snapshot(root)
        output = (codex_exec or run_codex_exec)(
            parameter, root=repo_root(root), purpose=purpose
        )
        report = getattr(output, "output_text", "")
        result["agent_report"] = report
        log = getattr(output, "call_log_path", None)
        result["call_log"] = str(log) if log is not None else None
        result["agent_status"] = (
            "resolved"
            if report.splitlines()[:1] == ["merge_resolution: resolved"]
            else "unresolved"
        )
        update_primary_report_fields(
            conflict_resolution_status=result["agent_status"],
            conflict_agent_report=report,
            conflict_call_log=result["call_log"],
        )
        after = _status_snapshot(root)
        changed = {
            path
            for path in before.keys() | after.keys()
            if before.get(path) != after.get(path)
        }
        if refactor_relative in changed:
            raise CmocError(
                "競合解消 agent が cmoc 管理物を編集しました。",
                [],
                refactor_relative,
            )
        if parameter.file_access_mode == FileAccessMode.REALIZATION_WRITE:
            forbidden = [
                path
                for path in sorted(changed)
                if not (
                    is_realization_file_path(root, root / path, branch="HEAD")
                    or is_realization_file_path(root, root / path, branch="MERGE_HEAD")
                )
            ]
            if forbidden:
                raise CmocError(
                    "競合解消 agent が編集範囲外を変更しました。",
                    [],
                    "\n".join(forbidden),
                )
        result["incidental_paths"] = sorted(
            path for path in changed if path not in conflicts
        )
        if result["agent_status"] != "resolved":
            raise CmocError(
                "競合解消 agent が完了を確認できませんでした。",
                ["Codex call log の未解消理由と検証結果を確認してください。"],
                report,
            )
    if refactor_relative in managed:
        _merge_refactor_state(root, refactor_relative)
    if refactor_relative in managed:
        sync_refactor_state(root)
    run_git(["add", "-A"], root)
    remaining = unmerged_paths(root)
    if remaining:
        raise CmocError("unmerged path が残っています。", [], "\n".join(remaining))
    _check_conflict_markers(root)
    run_git(["commit", "--no-edit"], root)
    return result


def _status_snapshot(root: Path) -> dict[str, tuple[str, str | None]]:
    """agent の付随編集を、既に差分にある path の再編集も含めて捕捉する。"""
    snapshot: dict[str, tuple[str, str | None]] = {}
    for status, path in status_path_statuses(
        root, untracked_all=True, include_rename_sources=True
    ):
        name = path.relative_to(root).as_posix()
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


def _merge_refactor_state(root: Path, path: str) -> None:
    """両 branch の調査履歴と調査要求を失わず、後続の集合同期へ渡す。"""
    sides: list[dict[str, Any]] = []
    for stage in (2, 3):
        content = run_git(["show", f":{stage}:{path}"], root, check=False)
        if content.returncode == 0:
            value = json.loads(content.stdout)
            if not isinstance(value, dict):
                raise CmocError("refactor state の競合内容が不正です。", [], path)
            sides.append(value)
    merged: dict[str, Any] = {}
    for side in sides:
        for name, entry in side.items():
            previous = merged.get(name)
            if previous is None:
                merged[name] = entry
            elif isinstance(previous, dict) and isinstance(entry, dict):
                newer = max(
                    (previous, entry),
                    key=lambda item: item.get("last_investigated_at") or "",
                )
                merged[name] = {
                    **newer,
                    "investigation_required": previous.get(
                        "investigation_required", True
                    )
                    or entry.get("investigation_required", True),
                }
            else:
                raise CmocError("refactor state の競合内容が不正です。", [], name)
    write_refactor_state(root, merged)
    run_git(["add", "--", literal_pathspec(path)], root)


def _check_conflict_markers(root: Path) -> None:
    """staging 対象の regular text に残った Git marker block を拒否する。"""
    paths = run_git(["diff", "--cached", "--name-only", "-z"], root).stdout.split("\0")
    for relative in paths:
        if not relative:
            continue
        path = root / relative
        if path.is_symlink() or not path.is_file():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeError:
            continue
        if _has_conflict_marker_block("\n".join(lines)):
            raise CmocError("conflict marker が残っています。", [], relative)


def _has_conflict_marker_block(text: str) -> bool:
    """Markdown の bare separator と Git conflict marker を区別する。"""
    state = 0
    for line in text.splitlines():
        if line.startswith("<<<<<<<"):
            state = 1
        elif line.startswith(("|||||||", ">>>>>>>")):
            return True
        elif state == 1 and len(line) >= 7 and set(line) == {"="}:
            state = 2
    return state != 0
