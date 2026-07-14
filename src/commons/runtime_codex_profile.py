"""Codex CLI 起動前後の argv/env/schema/error 判定をまとめる境界。

このファイルは 16,000 文字を超えるが、責務境界は Codex CLI に渡す実行環境と
Codex CLI から返る機械的な実行結果の解釈に閉じている。sandbox/argv/cwd、
CODEX_HOME、child process tracking、schema 配置、JSONL error 判定は同じ
subprocess 境界の不変条件を共有するため、分割すると呼び出し側が同時に読むべき
失敗時文脈が増える。現状は Codex subprocess 境界として一箇所に保つ方が凝集性が高い。
根拠: {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import fcntl
import json
import os
import select
import signal
import subprocess
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from basic.acp import AgentCallParameter, FileAccessMode
from config.cmoc_config import CmocConfig

from commons.runtime_content import write_hashed_file
from commons.runtime_errors import CmocError
from commons.runtime_git import (
    is_oracle_file_path,
    is_untracked_git_ignored,
    run_git,
)
from commons.runtime_paths import agent_read_dirs, logs_dir, schema_store_dir

APPLY_PROCESS_TRACKING_ENV = "CMOC_APPLY_PROCESS_ID_PATH"
_active_apply_process_tracking_path: Path | None = None
_CODEX_BLOCKED_ROOT_NAMES = {
    ".agents",
    ".codex",
    ".git",
    ".pytest_cache",
    "AGENTS.md",
    "INDEX.md",
    "memo",
}
_REPO_WRITE_BLOCKED_ROOT_NAMES = _CODEX_BLOCKED_ROOT_NAMES
_CONFLICT_WRITE_BLOCKED_ROOT_NAMES = {
    ".agents",
    ".cmoc",
    ".codex",
    ".git",
    "memo",
}
_DENIED_WRITE_FILE_NAMES = {"AGENTS.md", "INDEX.md"}
_STANDARD_REALIZATION_WRITE_PATHS = ("src", "test", "bin", ".gitignore")
_OLLAMA_PROVIDER_ID = "cmoc_managed_ollama"
_CMOC_PERMISSION_PROFILE = "cmoc"
_PERMISSION_PROFILE_WRITE_MODES = frozenset(
    {
        FileAccessMode.REALIZATION_WRITE,
        FileAccessMode.PURE_ORACLE_WRITE,
        FileAccessMode.REPO_WRITE,
        FileAccessMode.NO_RULE,
    }
)


@contextmanager
def apply_process_id_file_lock(path: Path) -> Iterator[None]:
    """apply process pid file の読み書きを直列化する。"""
    lock_path = path.with_name(f"{path.name}.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock_file:
        # {{work-root}}/oracle/doc/app_spec/sub_command/apply_abandon.md
        # abandon が Codex child 起動直後の未記録状態を読まないよう、
        # parent/child pid file 操作は同じ advisory lock に集約する。
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def open_process_fd(process_id: int, process_name: str = "apply process") -> int | None:
    """pidfd 対応環境でだけ race を避けた process 参照を開く。"""
    if not (hasattr(os, "pidfd_open") and hasattr(signal, "pidfd_send_signal")):
        raise CmocError(
            f"{process_name} の同一性を安全に確認できません。",
            [f"{process_name} を手動で停止してから再実行してください。"],
            f"pid: {process_id}",
        )
    try:
        return os.pidfd_open(process_id)
    except ProcessLookupError:
        return None
    except PermissionError as exc:
        raise CmocError(
            f"実行中 {process_name} の確認権限がありません。",
            [f"{process_name} を手動で確認してから再実行してください。"],
            f"pid: {process_id}",
        ) from exc


def send_process_signal(
    process_fd: int,
    process_id: int,
    sig: signal.Signals,
    process_name: str = "apply process",
) -> None:
    """pidfd 経由で process へ signal を送り、PID reuse を避ける。"""
    try:
        signal.pidfd_send_signal(process_fd, sig)
    except ProcessLookupError:
        return
    except PermissionError as exc:
        raise CmocError(
            f"実行中 {process_name} を停止する権限がありません。",
            [f"{process_name} を手動で停止してから再実行してください。"],
            f"pid: {process_id}",
        ) from exc


def wait_process_fd_exit(process_fd: int, timeout_sec: float) -> bool:
    """pidfd の readable 化を process 終了として待つ。"""
    readable, _, _ = select.select([process_fd], [], [], timeout_sec)
    return bool(readable)


def _process_stat(process_id: int) -> list[str] | None:
    try:
        stat = Path(f"/proc/{process_id}/stat").read_text()
    except OSError:
        return None
    try:
        fields = stat.rsplit(") ", 1)[1].split()
    except IndexError:
        return None
    return fields if len(fields) > 19 else None


def process_start_time(process_id: int) -> int | None:
    """pid 再利用を検出するため Linux proc stat の starttime を読む。"""
    fields = _process_stat(process_id)
    if fields is None:
        return None
    try:
        return int(fields[19])
    except ValueError:
        return None


def process_group_members(
    process_group_id: int,
) -> tuple[tuple[int, int], ...] | None:
    """group 内の非 zombie process を PID と starttime の組で列挙する。"""
    proc = Path("/proc")
    if not proc.is_dir():
        return None
    members: list[tuple[int, int]] = []
    try:
        entries = tuple(proc.iterdir())
    except OSError:
        return None
    for path in entries:
        if not path.name.isdigit():
            continue
        fields = _process_stat(int(path.name))
        if fields is None:
            continue
        try:
            state = fields[0]
            member_group_id = int(fields[2])
            start_time = int(fields[19])
        except ValueError:
            continue
        if member_group_id == process_group_id and state != "Z":
            members.append((int(path.name), start_time))
    return tuple(members)


def process_group_has_running_member(process_group_id: int) -> bool:
    """group 内に停止対象となる process が残っているか確認する。"""
    members = process_group_members(process_group_id)
    return members is None or bool(members)


def wait_process_group_exit(process_group_id: int, timeout_sec: float) -> bool:
    """数値 PGID へ signal を送らず、group が空になるまで待つ。"""
    deadline = time.monotonic() + timeout_sec
    while process_group_has_running_member(process_group_id):
        if time.monotonic() >= deadline:
            return False
        time.sleep(0.05)
    return True


def signal_process_group_members(
    process_group_id: int, sig: signal.Signals
) -> None:
    """group member を個別 pidfd で再検証して signal を送る。"""
    members = process_group_members(process_group_id)
    if members is None:
        raise CmocError(
            "実行中 Codex subprocess の process group を確認できません。",
            ["Codex subprocess を手動で停止してから再実行してください。"],
            f"pgid: {process_group_id}",
        )
    for process_id, expected_start_time in members:
        process_fd = open_process_fd(process_id, "Codex subprocess")
        if process_fd is None:
            continue
        try:
            # stat 読み取りと pidfd_open の間の PID reuse も signal 前に捨てる。
            if process_start_time(process_id) != expected_start_time:
                continue
            send_process_signal(
                process_fd,
                process_id,
                sig,
                "Codex subprocess",
            )
        finally:
            os.close(process_fd)


def stop_process_group(process_group_id: int) -> None:
    """Codex group を個別 pidfd で SIGTERM、必要なら SIGKILL する。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/apply_abandon.md
    # PGID は member discovery にだけ使い、signal delivery は pidfd に固定する。
    signal_process_group_members(process_group_id, signal.SIGTERM)
    if wait_process_group_exit(process_group_id, 5.0):
        return
    signal_process_group_members(process_group_id, signal.SIGKILL)
    if wait_process_group_exit(process_group_id, 5.0):
        return
    raise CmocError(
        "実行中 Codex subprocess を停止できません。",
        ["Codex subprocess を確認して停止後に再実行してください。"],
        f"pgid: {process_group_id}",
    )


def file_access_to_sandbox_mode(mode: FileAccessMode) -> str:
    """cmoc の file access policy を Codex CLI が理解する sandbox 名へ落とす。"""
    match mode:
        case FileAccessMode.READONLY | FileAccessMode.PURE_ORACLE_READ:
            return "read-only"
        case (
            FileAccessMode.REALIZATION_WRITE
            | FileAccessMode.PURE_ORACLE_WRITE
            | FileAccessMode.REPO_WRITE
            | FileAccessMode.NO_RULE
        ):
            return "workspace-write"
        case _:
            raise CmocError("不明な FileAccessMode です。", [], str(mode))


def parameter_codex_cwd(parameter: AgentCallParameter, codex_work_root: Path) -> Path:
    """AgentCallParameter.cwd を優先し、対象 work root 外の古い呼び出しを補正する。"""
    parameter_cwd = parameter.cwd.resolve()
    work = codex_work_root.resolve()
    if parameter_cwd.is_relative_to(work):
        return parameter_cwd
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # Older call paths may still pass the repo root while launching against a
    # linked worktree; Codex must run inside the target work root.
    return work


def _is_read_path_allowed(mode: FileAccessMode, root: Path, path: Path) -> bool:
    """prompt 上の読み取り禁止領域を追加 read path にも適用する。"""
    if not path.is_relative_to(root):
        return False
    if path.is_relative_to(root / "memo"):
        return False
    if _is_tui_complete_prompt_path(root, path):
        # {{work-root}}/oracle/doc/app_spec/sub_command/tui.md
        # PURE_ORACLE_READ の Codex cwd は oracle に閉じるが、TUI の完全
        # prompt だけは起動指示そのものなので `.cmoc` 側から読ませる。
        return True
    if mode in {FileAccessMode.PURE_ORACLE_READ, FileAccessMode.PURE_ORACLE_WRITE}:
        return path.is_relative_to(root / "oracle")
    return True


def _is_repo_agent_read_path(root: Path, path: Path) -> bool:
    """repo 側の agent 読み取り専用領域に含まれるか判定する。"""
    return any(
        path.is_relative_to(read_root)
        for read_root in _repo_agent_read_roots(root)
    )


def _repo_agent_read_roots(root: Path) -> tuple[Path, Path]:
    """linked worktree から例外的に読める repo 側 directory 群を返す。"""
    return tuple(path.resolve() for path in agent_read_dirs(root))


def _is_tui_complete_prompt_path(root: Path, path: Path) -> bool:
    return path.parent == logs_dir(root).parent / "tui" and path.name.endswith(
        "_cmpl.md"
    )


def _validate_extra_read_paths(
    mode: FileAccessMode,
    root: Path,
    extra_read_paths: list[Path] | None,
    extra_read_root: Path | None = None,
) -> None:
    """Codex argv に足す read path が cmoc の許可境界内か検査する。"""
    extra_repo_root = (
        extra_read_root.resolve() if extra_read_root is not None else None
    )
    for path in extra_read_paths or []:
        resolved = path.resolve()
        if not _is_read_path_allowed(mode, root, resolved) and not (
            extra_repo_root is not None
            and extra_repo_root != root
            and _is_repo_agent_read_path(extra_repo_root, resolved)
        ):
            raise CmocError(
                "追加読み取り許可 path が FileAccessMode の許可領域外にあります。",
                [
                    "file access mode で読み取り可能な work root 配下の path を指定してください。"
                ],
                f"mode: {mode.value}\npath: {resolved}",
            )


def _toml_string(value: str) -> str:
    """TOML string として安全な JSON 互換 quote へ寄せる。"""
    return json.dumps(value, ensure_ascii=False)


def _toml_inline_table(values: dict[str, Any]) -> str:
    """ネストした値を Codex の inline TOML table に変換する。"""
    rendered: list[str] = []
    for key, value in sorted(values.items()):
        if isinstance(value, dict):
            value_text = _toml_inline_table(value)
        elif isinstance(value, int):
            value_text = str(value)
        else:
            value_text = _toml_string(value)
        rendered.append(f"{_toml_string(key)} = {value_text}")
    return "{ " + ", ".join(rendered) + " }"


def _writable_roots(
    mode: FileAccessMode,
    root: Path,
    extra_writable_paths: list[Path] | None,
    allow_oracle_conflict_writes: bool = False,
) -> list[Path]:
    """Codex sandbox に渡せる書き込み root を作る。"""
    root = root.resolve()
    match mode:
        case FileAccessMode.READONLY:
            # {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
            # READONLY は oracle/realization file を書き込み禁止にするため、
            # positive-only permission 設定では既存の隙間を列挙して表現する。
            paths = _readonly_gap_writable_roots(root)
        case FileAccessMode.PURE_ORACLE_READ:
            # {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
            # realization file 読み書き禁止と oracle file 書き込み禁止は保ち、
            # READONLY と同じくルール上の隙間だけ permission 設定で開く。
            paths = _readonly_gap_writable_roots(root)
        case FileAccessMode.REALIZATION_WRITE:
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
            # The permission profile opens work-root itself so a new root-level
            # realization file has a parent write root. Narrower read/deny
            # entries below keep reserved trees and oracle outside that scope.
            paths = _top_level_writable_roots(mode, root)
        case FileAccessMode.REPO_WRITE:
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
            # The root write entry is paired with narrower protected entries in
            # `_permission_profile_filesystem_overrides`.
            paths = _top_level_writable_roots(mode, root)
        case FileAccessMode.PURE_ORACLE_WRITE:
            paths = [root / "oracle"]
        case FileAccessMode.NO_RULE:
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # NO_RULE omits the prompt rule; `.cmoc/g*/ar` and Codex-reserved
            # trees stay blocked in the argv permission profile.
            paths = _top_level_writable_roots(mode, root)
        case _:
            paths = []
    if allow_oracle_conflict_writes:
        # {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
        # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        # Conflict resolution exposes only explicit targets before launch.
        paths = []
    result: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        _append_writable_path(result, seen, mode, root, resolved)
    for path in extra_writable_paths or []:
        resolved = path.resolve()
        if not _is_writable_path_allowed(
            mode, root, resolved, allow_oracle_conflict_writes
        ):
            raise CmocError(
                "追加書き込み許可 path が FileAccessMode の許可領域外にあります。",
                [
                    "file access mode で書き込み可能な work root 配下の path を指定してください。"
                ],
                f"mode: {mode.value}\npath: {resolved}",
            )
        _append_writable_path(
            result,
            seen,
            mode,
            root,
            _existing_or_target_writable_root(resolved),
            allow_oracle_conflict_writes,
        )
    return result


def _top_level_writable_roots(mode: FileAccessMode, root: Path) -> list[Path]:
    """permission profile 用の top-level write root を返す。"""
    if mode in {FileAccessMode.REALIZATION_WRITE, FileAccessMode.REPO_WRITE}:
        # {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
        # New root-level files cannot be named in advance. Codex permission
        # entries use most-specific matching, so the root write is safe only
        # together with the protected descendants added below.
        return [root]
    paths: list[Path] = []
    candidates = [root / name for name in _STANDARD_REALIZATION_WRITE_PATHS]
    if mode == FileAccessMode.REPO_WRITE:
        candidates.append(root / "oracle")
    if root.exists():
        candidates.extend(root.iterdir())
    for path in candidates:
        resolved = path.resolve()
        if resolved not in paths and _is_writable_path_allowed(mode, root, resolved):
            paths.append(resolved)
    return paths


def _readonly_gap_writable_roots(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return [path.resolve() for path in root.iterdir()]


def _existing_or_target_writable_root(path: Path) -> Path:
    # {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
    # 未存在の deep path は、最初に作る必要がある directory までを sandbox
    # root にする。既存 parent 直下の未存在 file はその file path のまま渡す。
    if path.exists() or path.parent.exists():
        return path
    return _existing_or_target_writable_root(path.parent)


def _append_writable_path(
    result: list[Path],
    seen: set[Path],
    mode: FileAccessMode,
    root: Path,
    path: Path,
    allow_oracle_conflict_writes: bool = False,
) -> None:
    if (
        mode in {FileAccessMode.READONLY, FileAccessMode.PURE_ORACLE_READ}
        and path.is_dir()
        and not _is_writable_path_allowed(mode, root, path)
    ):
        for child in sorted(path.iterdir()):
            _append_writable_path(
                result,
                seen,
                mode,
                root,
                child.resolve(),
                allow_oracle_conflict_writes,
            )
        return
    if not _is_writable_path_allowed(mode, root, path, allow_oracle_conflict_writes):
        return
    if path.is_dir():
        if (
            _should_expand_writable_directory(
                mode, root, path, allow_oracle_conflict_writes
            )
            or (
                mode not in {FileAccessMode.READONLY, FileAccessMode.PURE_ORACLE_READ}
                and is_untracked_git_ignored(root, path / ".__cmoc_ignore_probe__")
            )
        ):
            # {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
            # {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
            # Codex permission settings have only positive writable roots. A directory that
            # contains denied routing files or would ignore new children cannot
            # be opened as one root; expand existing children instead.
            for child in sorted(path.iterdir()):
                _append_writable_path(
                    result,
                    seen,
                    mode,
                    root,
                    child.resolve(),
                    allow_oracle_conflict_writes,
                )
            return
    _append_writable_root(result, seen, path)


def _should_expand_writable_directory(
    mode: FileAccessMode,
    root: Path,
    path: Path,
    allow_oracle_conflict_writes: bool,
) -> bool:
    if (
        mode in {FileAccessMode.READONLY, FileAccessMode.PURE_ORACLE_READ}
        and _has_denied_write_file(path)
    ):
        return True
    if mode not in {FileAccessMode.READONLY, FileAccessMode.PURE_ORACLE_READ}:
        if path.resolve() == (root / ".cmoc").resolve():
            # {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
            # Keep non-ignored .cmoc files addressable without opening runtime state.
            return True
        return False
    if not is_untracked_git_ignored(root, path):
        return True
    return any(
        not _is_writable_path_allowed(
            mode, root, child.resolve(), allow_oracle_conflict_writes
        )
        for child in path.iterdir()
    )


def _has_denied_write_file(path: Path) -> bool:
    return any((path / name).exists() for name in _DENIED_WRITE_FILE_NAMES)


def _append_writable_root(result: list[Path], seen: set[Path], path: Path) -> None:
    """親子関係で冗長な writable root を持たないように追加する。"""
    _append_access_root(result, seen, path)


def _append_access_root(result: list[Path], seen: set[Path], path: Path) -> None:
    """親子関係で冗長な permission filesystem root を持たないように追加する。"""
    resolved = path.resolve()
    if resolved in seen or any(resolved.is_relative_to(parent) for parent in seen):
        return
    redundant = [existing for existing in seen if existing.is_relative_to(resolved)]
    if redundant:
        result[:] = [existing for existing in result if existing not in redundant]
        seen.difference_update(redundant)
    seen.add(resolved)
    result.append(resolved)


def _is_writable_path_allowed(
    mode: FileAccessMode,
    root: Path,
    path: Path,
    allow_oracle_conflict_writes: bool = False,
) -> bool:
    """FileAccessMode の禁止領域を追加 writable path にも適用する。"""
    if not path.is_relative_to(root):
        return False
    # {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # 追加 writable path は、prompt で伝える禁止領域を広げない範囲だけ許可する。
    relative = path.relative_to(root)
    if path.name in _DENIED_WRITE_FILE_NAMES:
        return False
    if (
        mode not in {FileAccessMode.READONLY, FileAccessMode.PURE_ORACLE_READ}
        and is_untracked_git_ignored(root, path)
    ):
        return False
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # `.cmoc/g*/ar` は git tracking の有無を問わず agent 読み取り専用である。
    if any(path.is_relative_to(read_root) for read_root in agent_read_dirs(root)):
        return False
    if allow_oracle_conflict_writes:
        # {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
        # session join の conflict 解消は oracle file も git conflict 対象なら編集する。
        # runtime 管理領域と root 禁止 file は sandbox 側でも開かない。
        return (
            bool(relative.parts)
            and relative.parts[0] not in _CONFLICT_WRITE_BLOCKED_ROOT_NAMES
        )
    blocked_root_names = _REPO_WRITE_BLOCKED_ROOT_NAMES
    if relative.parts and relative.parts[0] in blocked_root_names:
        return False
    if mode == FileAccessMode.REALIZATION_WRITE:
        return not is_oracle_file_path(root, path)
    if mode == FileAccessMode.PURE_ORACLE_WRITE:
        return path.is_relative_to(root / "oracle")
    if mode in {FileAccessMode.READONLY, FileAccessMode.PURE_ORACLE_READ}:
        return not (
            is_oracle_file_path(root, path) or _is_realization_file_path(root, path)
        )
    return mode in {FileAccessMode.REPO_WRITE, FileAccessMode.NO_RULE}


def _is_realization_file_path(root: Path, path: Path) -> bool:
    # {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
    # READONLY 系では git ignored 一時 file を realization file から外し、
    # oracle と同じ正本定義に合わせて隙間だけを writable に残す。
    try:
        relative = path.absolute().relative_to(root.absolute())
    except ValueError:
        return False
    if not relative.parts or relative.parts[0] in {
        "oracle",
        "memo",
        ".git",
        ".agents",
        ".codex",
        ".cmoc",
    }:
        return False
    return path.name not in _DENIED_WRITE_FILE_NAMES and not is_untracked_git_ignored(
        root, path
    )


def _config_override(key: str, toml_value: str) -> list[str]:
    """Codex CLI の単一 config override を argv fragment にする。"""
    return ["--config", f"{key}={toml_value}"]


def _read_roots_for_permission_profile(
    mode: FileAccessMode,
    root: Path,
    extra_read_paths: list[Path] | None,
    extra_read_root: Path | None,
) -> list[Path]:
    """Codex permission profile に渡す読み取り root を作る。"""
    roots = (
        [root / "oracle"]
        if mode in {FileAccessMode.PURE_ORACLE_READ, FileAccessMode.PURE_ORACLE_WRITE}
        else _top_level_read_roots(mode, root)
    )
    if (
        mode != FileAccessMode.NO_RULE
        and extra_read_root is not None
        and extra_read_root != root
    ):
        # {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
        # linked worktree の規則文は repo 側 `.cmoc/g*/ar` を read 例外にする。
        roots.extend(_repo_agent_read_roots(extra_read_root))
    for path in extra_read_paths or []:
        resolved = path.resolve()
        if any(resolved.is_relative_to(read_root) for read_root in roots):
            continue
        if extra_read_root is not None and _is_repo_agent_read_path(
            extra_read_root, resolved
        ):
            roots.extend(_repo_agent_read_roots(extra_read_root))
        else:
            roots.append(resolved)
    result: list[Path] = []
    seen: set[Path] = set()
    for path in roots:
        _append_access_root(result, seen, path)
    return result


def _top_level_read_roots(mode: FileAccessMode, root: Path) -> list[Path]:
    # {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
    # Codex permission filesystem is positive-only; READONLY cannot use
    # {{work-root}} itself because that would also grant the memo read denied by
    # the base file access rule.
    if mode != FileAccessMode.READONLY:
        return [root]
    if not root.exists():
        return []
    return [
        path.resolve()
        for path in sorted(root.iterdir())
        if _is_read_path_allowed(mode, root, path.resolve())
    ]


def _iter_worktree_paths(root: Path) -> Iterator[Path]:
    """work-root 配下を symlink の解決先へ降りずに列挙する。"""
    if not root.is_dir() or root.is_symlink():
        return
    try:
        paths = sorted(root.iterdir())
    except OSError:
        return
    for path in paths:
        yield path
        if path.is_dir() and not path.is_symlink():
            yield from _iter_worktree_paths(path)


def _git_tracked_paths(root: Path) -> set[Path]:
    """tracked descendant の復元に使う index path を一度だけ取得する。"""
    result = run_git(["ls-files", "-z", "--"], root, check=False)
    if result.returncode != 0:
        return set()
    return {root / relative for relative in result.stdout.split("\0") if relative}


def _is_ignored_directory(root: Path, path: Path) -> bool:
    return is_untracked_git_ignored(root, path) or is_untracked_git_ignored(
        root, path / ".__cmoc_ignore_probe__"
    )


def _ignored_path_overrides(mode: FileAccessMode, root: Path) -> dict[str, str]:
    """ignored directory を read にし、内部の tracked file だけ write に戻す。"""
    # {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
    # git check-ignore が対象外と判定する tracked file は realization/oracle の
    # 定義に残るため、ignored directory 全体の read rule で巻き込まない。
    overrides: dict[str, str] = {}
    ignored_directories: list[Path] = []
    for path in _iter_worktree_paths(root):
        resolved = path.resolve()
        if not resolved.is_relative_to(root):
            continue
        if path.is_dir() and not path.is_symlink():
            if _is_ignored_directory(root, path):
                overrides[str(resolved)] = "read"
                ignored_directories.append(path)
        elif is_untracked_git_ignored(root, path):
            overrides[str(resolved)] = "read"

    tracked_paths = _git_tracked_paths(root)
    for path in tracked_paths:
        if not any(path.is_relative_to(directory) for directory in ignored_directories):
            continue
        resolved = path.resolve()
        if resolved.is_relative_to(root) and _is_writable_path_allowed(
            mode, root, path
        ):
            overrides[str(resolved)] = "write"
    return overrides


def _external_symlink_overrides(
    root: Path, extra_read_root: Path | None
) -> dict[str, str]:
    """work-root 外へ解決する symlink の target を deny にする。"""
    # {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
    # work-root 外は読み書き禁止で、例外は repo-root/.cmoc/g*/ar の read だけ。
    allowed_read_roots = (
        _repo_agent_read_roots(extra_read_root)
        if extra_read_root is not None
        else ()
    )
    overrides: dict[str, str] = {}
    for path in _iter_worktree_paths(root):
        if not path.is_symlink():
            continue
        resolved = path.resolve()
        if resolved.is_relative_to(root) or any(
            resolved.is_relative_to(read_root)
            for read_root in allowed_read_roots
        ):
            continue
        overrides[str(resolved)] = "deny"
    return overrides


def _permission_profile_filesystem_overrides(
    mode: FileAccessMode,
    root: Path,
    extra_read_root: Path | None = None,
) -> dict[str, Any]:
    """permission profile に、将来の path にも効く保護 rule を追加する。"""
    overrides: dict[str, Any] = {}
    if mode in _PERMISSION_PROFILE_WRITE_MODES:
        # {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
        # memo は広い read root に含まれるため deny し、routing file は Codex が
        # 受理する exact な :workspace_roots rule で read のまま write だけ防ぐ。
        routing_rules = {name: "read" for name in _DENIED_WRITE_FILE_NAMES}
        overrides.update(
            {
                str((root / "memo").resolve()): "deny",
                ":workspace_roots": routing_rules,
            }
        )
        if mode in {FileAccessMode.REALIZATION_WRITE, FileAccessMode.REPO_WRITE}:
            # {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
            # A root write is required for unknown, non-protected root-level
            # realization files. Codex selects the most specific filesystem rule,
            # so protect the fixed reserved roots explicitly instead of relying on
            # a later diff check (which is not an access control mechanism).
            overrides.update(
                {
                    str(root.resolve() / name): "read"
                    for name in (".agents", ".codex", ".git", ".pytest_cache")
                }
            )
            overrides.update(
                {str(path.resolve()): "read" for path in agent_read_dirs(root)}
            )
            if mode == FileAccessMode.REALIZATION_WRITE:
                overrides[str((root / "oracle").resolve())] = "read"
            overrides.update(
                {
                    str((root / name).resolve()): "read"
                    for name in _DENIED_WRITE_FILE_NAMES
                }
            )
        overrides.update(_ignored_path_overrides(mode, root))
        if mode in {
            FileAccessMode.REALIZATION_WRITE,
            FileAccessMode.REPO_WRITE,
            FileAccessMode.NO_RULE,
        }:
            # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
            # `.cmoc/g*/ar` は runtime/config の agent 読み取り専用領域である。
            overrides.update(
                {str(path.resolve()): "read" for path in agent_read_dirs(root)}
            )
    # Keep this rule for read-only modes too: their read roots can contain a
    # nested symlink even though they do not have a work-root write entry.
    overrides.update(_external_symlink_overrides(root, extra_read_root))
    return overrides


def _permission_profile_override_args(
    read_roots: list[Path],
    writable_roots: list[Path],
    protected_paths: list[Path],
    filesystem_overrides: dict[str, Any] | None = None,
) -> list[str]:
    """Codex beta permission profile を config override argv で渡す。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/tui.md
    # {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # sandbox_mode cannot express "read this root but never make the primary
    # workspace writable"; permission profiles can.
    entries = {str(path): "read" for path in read_roots}
    entries.update({str(path): "write" for path in writable_roots})
    # A parent write grant is needed for new files.  A narrower read grant
    # keeps existing AGENTS.md/INDEX.md files protected inside that parent.
    entries.update({str(path): "read" for path in protected_paths})
    entries.update(filesystem_overrides or {})
    filesystem = _toml_inline_table(entries)
    permission = (
        f'{{ extends = ":workspace", filesystem = {filesystem} }}'
    )
    return [
        *_config_override(
            "default_permissions", _toml_string(_CMOC_PERMISSION_PROFILE)
        ),
        *_config_override(
            f"permissions.{_CMOC_PERMISSION_PROFILE}", permission
        ),
    ]


def _protected_writable_paths(writable_roots: list[Path]) -> list[Path]:
    """書き込み root 配下の AGENTS.md/INDEX.md を具体的な read rule にする。"""
    # {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
    paths: set[Path] = set()
    for root in writable_roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.name not in _DENIED_WRITE_FILE_NAMES:
                continue
            resolved = path.resolve()
            if resolved.is_relative_to(root.resolve()):
                paths.add(resolved)
    return sorted(paths)


def _ollama_provider_override_args() -> list[str]:
    """cmoc managed ollama provider を argv config override にする。"""
    provider_key = f"model_providers.{_OLLAMA_PROVIDER_ID}"
    return [
        # {{work-root}}/oracle/doc/app_spec/cmoc_managed_ollama.md
        # Codex enables non-function web-search and multi-agent tool types by
        # default, while Ollama's Responses endpoint accepts function tools.
        # Keep the managed local provider on their common tool subset.
        "--disable",
        "multi_agent",
        *_config_override("web_search", _toml_string("disabled")),
        *_config_override("model_provider", _toml_string(_OLLAMA_PROVIDER_ID)),
        *_config_override(
            f"{provider_key}.name", _toml_string("cmoc managed ollama")
        ),
        *_config_override(
            f"{provider_key}.base_url",
            _toml_string("http://127.0.0.1:11434/v1"),
        ),
        *_config_override(f"{provider_key}.wire_api", _toml_string("responses")),
    ]


def build_codex_override_args(
    parameter: AgentCallParameter,
    config: CmocConfig,
    root: Path | None = None,
    extra_read_paths: list[Path] | None = None,
    extra_writable_paths: list[Path] | None = None,
    *,
    extra_read_root: Path | None = None,
    allow_oracle_conflict_writes: bool = False,
) -> list[str]:
    """AgentCallParameter と worktree config から Codex CLI 上書き argv を作る。"""
    model_spec = config.codex.model[parameter.model_class]
    reasoning_effort = config.codex.reasoning_effort[parameter.reasoning_effort]
    args = [
        "--model",
        model_spec.model,
        *_config_override(
            "model_reasoning_effort", _toml_string(reasoning_effort)
        ),
    ]
    use_cmoc_managed_ollama = model_spec.model_provider == "cmoc"
    if use_cmoc_managed_ollama:
        args.extend(_ollama_provider_override_args())
    if root is not None:
        root = root.resolve()
        read_root = (extra_read_root or root).resolve()
        _validate_extra_read_paths(
            parameter.file_access_mode,
            root,
            extra_read_paths,
            extra_read_root=read_root,
        )
    else:
        sandbox_mode = file_access_to_sandbox_mode(parameter.file_access_mode)
        args.extend(["--sandbox", sandbox_mode])
    if root is not None:
        writable_roots = _writable_roots(
            parameter.file_access_mode,
            root,
            extra_writable_paths,
            allow_oracle_conflict_writes,
        )
        args.extend(
            _permission_profile_override_args(
                _read_roots_for_permission_profile(
                    parameter.file_access_mode, root, extra_read_paths, read_root
                ),
                writable_roots,
                _protected_writable_paths(writable_roots),
                _permission_profile_filesystem_overrides(
                    parameter.file_access_mode, root, extra_read_root=read_root
                ),
            )
        )
    return args


def resolve_codex_home(cwd: Path | None = None) -> Path:
    """CODEX_HOME の相対指定を Codex subprocess の cwd 基準で解決する。"""
    value = os.environ.get("CODEX_HOME")
    if value is not None:
        raw_path = Path(value)
        return raw_path if raw_path.is_absolute() else (cwd or Path.cwd()) / raw_path
    return (Path.home() / ".codex").resolve()


def validate_codex_home(codex_home: Path) -> None:
    """Codex 起動前に通常利用に必要な home と auth.json の存在を検査する。"""
    if not codex_home.exists():
        raise CmocError(
            "Codex home が存在しません。",
            [
                "Codex CLI の通常利用環境を初期化してください。",
                "既存の Codex home を指すように CODEX_HOME を設定してください。",
            ],
            f"CODEX_HOME: {codex_home}\nfailed condition: CODEX_HOME exists",
        )
    if not codex_home.is_dir():
        raise CmocError(
            "Codex home がディレクトリではありません。",
            [
                "CODEX_HOME が既存ディレクトリを指すように修正してください。",
                "CODEX_HOME のファイル種別を確認してください。",
            ],
            f"CODEX_HOME: {codex_home}\nfailed condition: CODEX_HOME is directory",
        )
    auth_path = codex_home / "auth.json"
    if not auth_path.is_file():
        raise CmocError(
            "Codex CLI 認証情報が存在しません。",
            [
                "Codex CLI の通常利用環境を初期化してください。",
                "既存の Codex home を指すように CODEX_HOME を設定してください。",
            ],
            f"CODEX_HOME: {codex_home}\nfailed condition: {auth_path} is file",
        )


def prepare_codex_override_args(
    parameter: AgentCallParameter,
    config: CmocConfig | None = None,
    root: Path | None = None,
    extra_read_paths: list[Path] | None = None,
    extra_writable_paths: list[Path] | None = None,
    *,
    extra_read_root: Path | None = None,
    allow_oracle_conflict_writes: bool = False,
) -> list[str]:
    """必要なら local provider を準備し、Codex CLI 上書き argv を返す。"""
    if (
        (config or CmocConfig()).codex.model[parameter.model_class].model_provider
        == "cmoc"
        and root is not None
    ):
        from commons.runtime_doctor import run_doctor_preprocess

        run_doctor_preprocess(root, config)
    return build_codex_override_args(
        parameter,
        config or CmocConfig(),
        root,
        extra_read_paths,
        extra_writable_paths,
        extra_read_root=extra_read_root,
        allow_oracle_conflict_writes=allow_oracle_conflict_writes,
    )


def codex_subprocess_env(codex_home: Path) -> dict[str, str]:
    """Codex subprocess に渡す CODEX_HOME を、利用者指定があればそのまま保つ。"""
    value = os.environ.get("CODEX_HOME")
    if value is None:
        value = str(codex_home)
    return {**os.environ, "CODEX_HOME": value}


def run_codex_subprocess(
    argv: list[str], **kwargs: Any
) -> subprocess.CompletedProcess[Any]:
    """Codex CLI 不在を Python の生例外ではなく cmoc の実行時エラーにそろえる。"""
    try:
        # {{work-root}}/oracle/doc/app_spec/sub_command/apply_abandon.md
        # Tracking is apply-run internal state; an inherited env var alone must
        # not redirect unrelated Codex calls to a stale or foreign pid file.
        if _active_apply_process_tracking_path is not None and argv[:1] == ["codex"]:
            return run_tracked_codex_subprocess(
                argv, _active_apply_process_tracking_path, **kwargs
            )
        return subprocess.run(argv, **kwargs)
    except FileNotFoundError as exc:
        if argv[:1] != ["codex"]:
            raise
        # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        # Codex CLI missing は想定外の exec 失敗として即時に利用者向け失敗にする。
        raise CmocError(
            "Codex CLI が見つかりません。",
            ["Codex CLI をインストールし、PATH に codex を含めてください。"],
            f"argv: {argv}\nerror: {exc}",
        ) from exc


def set_apply_process_tracking_path(path: Path | None) -> Path | None:
    """apply 実行中だけ有効な process-local tracking path を差し替える。"""
    global _active_apply_process_tracking_path
    old_path = _active_apply_process_tracking_path
    _active_apply_process_tracking_path = path
    return old_path


def run_tracked_codex_subprocess(
    argv: list[str], tracking_path: Path, **kwargs: Any
) -> subprocess.CompletedProcess[Any]:
    """apply abandon が止められるよう Codex subprocess group を pid file に記録する。"""
    input_data = kwargs.pop("input", None)
    capture_output = kwargs.pop("capture_output", False)
    check = kwargs.pop("check", False)
    if input_data is not None:
        if kwargs.get("stdin") is not None:
            raise ValueError("stdin and input arguments may not both be used.")
        kwargs["stdin"] = subprocess.PIPE
    if capture_output:
        kwargs.setdefault("stdout", subprocess.PIPE)
        kwargs.setdefault("stderr", subprocess.PIPE)
    process: subprocess.Popen[Any] | None = None
    # {{work-root}}/oracle/doc/app_spec/sub_command/apply_abandon.md
    # Popen と child 行の登録だけを遅延させ、exec 後の child は通常の SIGTERM を受ける。
    previous_sigterm_handler = signal.getsignal(signal.SIGTERM)
    sigterm_pending = False

    def defer_sigterm(_signum: int, _frame: Any) -> None:
        nonlocal sigterm_pending
        sigterm_pending = True

    signal.signal(signal.SIGTERM, defer_sigterm)
    try:
        try:
            with apply_process_id_file_lock(tracking_path):
                process = subprocess.Popen(argv, start_new_session=True, **kwargs)
                _record_tracked_child_process(
                    tracking_path, process.pid, process_group_id=process.pid
                )
        except OSError as exc:
            if process is None:
                raise
            try:
                stop_process_group(process.pid)
            except CmocError as cleanup_exc:
                raise CmocError(
                    "apply process tracking を更新できません。",
                    [
                        "apply process pid file の権限と保存先を確認してください。",
                        "Codex subprocess の停止にも失敗しました。",
                    ],
                    f"path: {tracking_path}\nerror: {exc}\ncleanup: {cleanup_exc}",
                ) from exc
            raise CmocError(
                "apply process tracking を更新できません。",
                ["apply process pid file の権限と保存先を確認してください。"],
                f"path: {tracking_path}\nerror: {exc}",
            ) from exc
    finally:
        signal.signal(signal.SIGTERM, previous_sigterm_handler)
    if sigterm_pending and previous_sigterm_handler != signal.SIG_IGN:
        # Popen と pid file 更新の間だけ遅らせ、登録後は通常の中断処理へ戻す。
        os.kill(os.getpid(), signal.SIGTERM)
    try:
        stdout, stderr = process.communicate(input_data)
        result = subprocess.CompletedProcess(argv, process.returncode, stdout, stderr)
        if check and result.returncode:
            raise subprocess.CalledProcessError(
                result.returncode,
                argv,
                output=stdout,
                stderr=stderr,
            )
        return result
    finally:
        # {{work-root}}/oracle/doc/app_spec/sub_command/apply_abandon.md
        # leader 終了後も descendant が group に残る間は tracking を保持する。
        if process.poll() is not None and not process_group_has_running_member(process.pid):
            try:
                remove_tracked_child_process(tracking_path, process.pid)
            except OSError as exc:
                raise CmocError(
                    "apply process tracking を更新できません。",
                    ["apply process pid file の権限と保存先を確認してください。"],
                    f"path: {tracking_path}\nerror: {exc}",
                ) from exc


def record_tracked_child_process(
    path: Path, process_id: int, process_group_id: int | None = None
) -> None:
    """apply process pid file へ Codex child process の同一性情報を追記する。"""
    with apply_process_id_file_lock(path):
        _record_tracked_child_process(path, process_id, process_group_id)


def _record_tracked_child_process(
    path: Path, process_id: int, process_group_id: int | None = None
) -> None:
    start_time = process_start_time(process_id)
    if start_time is None:
        raise OSError(f"process {process_id} start time is unavailable")
    path.parent.mkdir(parents=True, exist_ok=True)
    current = path.read_text() if path.exists() else ""
    lines = [line for line in current.splitlines() if line.strip()]
    group_id = process_id if process_group_id is None else process_group_id
    child_line = f"child {process_id} {start_time} {group_id}"
    lines = [line for line in lines if not line.startswith(f"child {process_id} ")]
    lines.append(child_line)
    path.write_text("\n".join(lines) + "\n")


def remove_tracked_child_process(path: Path, process_id: int) -> None:
    """終了した Codex child process を apply process pid file から除く。"""
    with apply_process_id_file_lock(path):
        if not path.exists():
            return
        lines = [
            line
            for line in path.read_text().splitlines()
            if not line.startswith(f"child {process_id} ")
        ]
        path.write_text(("\n".join(lines) + "\n") if lines else "")


def prepare_schema(root: Path, schema_source_path: Path | None) -> Path | None:
    """Structured Output schema を指定 root の内容 hash store へ配置する。"""
    if schema_source_path is None:
        return None
    schema_text = schema_source_path.read_text()
    return write_hashed_file(schema_store_dir(root), "", ".json", schema_text)


def read_output_json(path: Path) -> Any:
    """schema なしの Codex output が空または不正 JSON の場合は None を返す。"""
    if not path.exists() or not path.read_text().strip():
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return None


def codex_error_text(stdout_text: str, stderr_text: str) -> str:
    """Codex の stderr と JSONL event 内 message を利用者向け detail に束ねる。"""
    fragments: list[str] = [stderr_text]
    for line in stdout_text.splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # Keep the original line visible even when it is blank; malformed
            # stdout is a protocol failure, not an ignorable diagnostic.
            fragments.append(f"malformed JSONL event (invalid JSON): {line}")
            continue
        if not isinstance(item, dict):
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # Known JSONL events are objects; preserve malformed output in
            # error detail so the caller takes the non-retryable failure path.
            fragments.append(f"malformed JSONL event (expected object): {line}")
            continue
        message = item.get("message")
        if isinstance(message, str):
            fragments.append(message)
        error = item.get("error")
        if isinstance(error, dict) and isinstance(error.get("message"), str):
            fragments.append(error["message"])
    return "\n".join(fragments)


def extract_resume_token(stdout_text: str) -> str | None:
    """quota retry で resume できる thread id を Codex JSONL stdout から拾う。"""
    for line in stdout_text.splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(item, dict):
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # A non-object event cannot carry a resume token.
            continue
        if item.get("type") != "thread.started":
            continue
        value = item.get("thread_id")
        if isinstance(value, str) and value:
            return value
    return None


def _codex_jsonl_error_messages(stdout_text: str) -> list[str | None]:
    """Codex JSONL の error event message を retry 判定用に抽出する。"""
    messages: list[str | None] = []
    for line in stdout_text.splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # A JSONL protocol violation is unexpected even when the process
            # returned zero and the output-last-message file is valid.
            messages.append(None)
            continue
        if not isinstance(item, dict):
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # A malformed event is an unexpected error, never a retry signal.
            messages.append(None)
            continue
        if item.get("type") == "error":
            message = item.get("message")
            messages.append(message if isinstance(message, str) else None)
        elif item.get("type") == "turn.failed":
            error = item.get("error")
            message = error.get("message") if isinstance(error, dict) else None
            messages.append(message if isinstance(message, str) else None)
    return messages


_CAPACITY_ERROR_MARKER = "Selected model is at capacity"
_QUOTA_ERROR_MARKERS = (
    "Quota exceeded",
    "You've hit your usage limit",
    "out of credits",
    "You hit your spend cap",
)


def is_capacity_error(stdout_text: str) -> bool:
    """Codex JSONL 上の model capacity error だけを retry 対象として判定する。"""
    return any(
        isinstance(message, str) and _CAPACITY_ERROR_MARKER in message
        for message in _codex_jsonl_error_messages(stdout_text)
    )


def is_quota_error(stdout_text: str) -> bool:
    """usage limit 系の Codex JSONL error を quota 待機対象として判定する。"""
    return any(
        isinstance(message, str) and marker in message
        for message in _codex_jsonl_error_messages(stdout_text)
        for marker in _QUOTA_ERROR_MARKERS
    )


def is_unexpected_error(stdout_text: str) -> bool:
    """既知の capacity/quota 以外の Codex JSONL error を検出する。"""
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # Only capacity and quota events have recovery paths; malformed or other
    # error events must not be hidden by a zero subprocess return code.
    return any(
        not isinstance(message, str)
        or (
            _CAPACITY_ERROR_MARKER not in message
            and not any(marker in message for marker in _QUOTA_ERROR_MARKERS)
        )
        for message in _codex_jsonl_error_messages(stdout_text)
    )
