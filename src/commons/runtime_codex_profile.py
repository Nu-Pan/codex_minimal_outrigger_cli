"""Codex CLI 起動前後の profile/env/schema/error 判定をまとめる境界。

このファイルは 16,000 文字を超えるが、責務境界は Codex CLI に渡す実行環境と
Codex CLI から返る機械的な実行結果の解釈に閉じている。sandbox/profile/cwd、
CODEX_HOME、child process tracking、schema 配置、JSONL error 判定は同じ
subprocess 境界の不変条件を共有するため、分割すると呼び出し側が同時に読むべき
失敗時文脈が増える。現状は Codex profile 境界として一箇所に保つ方が凝集性が高い。
根拠: <work-root>/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import fcntl
import json
import os
import subprocess
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from basic.acp import AgentCallParameter, FileAccessMode, ModelClass
from config.cmoc_config import CmocConfig

from commons.runtime_content import write_hashed_file, write_hashed_file_in_existing_dir
from commons.runtime_errors import CmocError
from commons.runtime_git import is_oracle_file_path
from commons.runtime_paths import logs_dir, schema_store_dir

APPLY_PROCESS_TRACKING_ENV = "CMOC_APPLY_PROCESS_ID_PATH"
_active_apply_process_tracking_path: Path | None = None
_PROFILE_BLOCKED_ROOT_NAMES = {
    ".agents",
    ".cmoc",
    ".codex",
    ".git",
    "AGENTS.md",
    "INDEX.md",
    "memo",
}
_REPO_WRITE_BLOCKED_ROOT_NAMES = _PROFILE_BLOCKED_ROOT_NAMES
_CONFLICT_WRITE_BLOCKED_ROOT_NAMES = {
    ".agents",
    ".cmoc",
    ".codex",
    ".git",
    "memo",
}
_STANDARD_REALIZATION_WRITE_PATHS = ("src", "test", "bin", ".gitignore")
_OLLAMA_PROVIDER_ID = "cmoc_managed_ollama"
_CMOC_PERMISSION_PROFILE = "cmoc"


@contextmanager
def apply_process_id_file_lock(path: Path) -> Iterator[None]:
    """apply process pid file の読み書きを直列化する。"""
    lock_path = path.with_name(f"{path.name}.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock_file:
        # <work-root>/oracle/doc/app_spec/sub_command/apply_abandon.md
        # abandon が Codex child 起動直後の未記録状態を読まないよう、
        # parent/child pid file 操作は同じ advisory lock に集約する。
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def file_access_to_sandbox_mode(mode: FileAccessMode) -> str:
    """cmoc の file access policy を Codex CLI が理解する sandbox 名へ落とす。"""
    match mode:
        case (
            FileAccessMode.READONLY
            | FileAccessMode.PURE_ORACLE_READ
            | FileAccessMode.REALIZATION_WRITE
            | FileAccessMode.PURE_ORACLE_WRITE
            | FileAccessMode.REPO_WRITE
            | FileAccessMode.NO_RULE
        ):
            return "workspace-write"
        case _:
            raise CmocError("不明な FileAccessMode です。", [], str(mode))


def file_access_to_codex_cwd(mode: FileAccessMode, root: Path) -> Path:
    """旧互換 API。Codex 作業 root は AgentCallParameter.cwd が正本。"""
    root = root.resolve()
    return root


def _is_read_path_allowed(mode: FileAccessMode, root: Path, path: Path) -> bool:
    """prompt 上の読み取り禁止領域を追加 read path にも適用する。"""
    if not path.is_relative_to(root):
        return False
    if path.is_relative_to(root / "memo") or path.is_relative_to(root / ".agents"):
        return False
    if _is_tui_complete_prompt_path(root, path):
        # <work-root>/oracle/doc/app_spec/sub_command/tui.md
        # PURE_ORACLE_READ の Codex cwd は oracle に閉じるが、TUI の完全
        # prompt だけは起動指示そのものなので `.cmoc` 側から読ませる。
        return True
    if mode in {FileAccessMode.PURE_ORACLE_READ, FileAccessMode.PURE_ORACLE_WRITE}:
        return path.is_relative_to(root / "oracle")
    return True


def _is_repo_local_read_path(root: Path, path: Path) -> bool:
    return path.is_relative_to(logs_dir(root).parent.parent)


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
    """Codex profile に足す read path が cmoc の許可境界内か検査する。"""
    extra_log_root = extra_read_root.resolve() if extra_read_root is not None else None
    for path in extra_read_paths or []:
        resolved = path.resolve()
        if not _is_read_path_allowed(mode, root, resolved) and not (
            extra_log_root is not None
            and extra_log_root != root
            and _is_repo_local_read_path(extra_log_root, resolved)
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
            # <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
            # READONLY は cmoc 上の論理的な読み取り専用であり、Codex CLI
            # sandbox は pytest cache などの一時生成物を許せるよう workspace
            # に寄せる。
            paths = _top_level_writable_roots(mode, root)
        case FileAccessMode.PURE_ORACLE_READ:
            # <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
            # READONLY より狭い読み取り系モードなので、oracle tree も
            # sandbox writable root には渡さない。
            paths = _top_level_writable_roots(mode, root)
        case FileAccessMode.REALIZATION_WRITE:
            # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
            # <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
            # `.agents` is a Codex-reserved tree, so opening <work-root> itself
            # would grant a write path that codex exec cannot safely mediate.
            paths = _top_level_writable_roots(mode, root)
        case FileAccessMode.REPO_WRITE:
            # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
            # <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
            # Keep the sandbox roots positive-only; root itself would include
            # `.agents`, `.git`, `.codex`, memo, and cmoc runtime state.
            paths = _top_level_writable_roots(mode, root)
        case FileAccessMode.PURE_ORACLE_WRITE:
            paths = [root / "oracle"]
        case FileAccessMode.NO_RULE:
            paths = [root]
        case _:
            paths = []
    result: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        _append_writable_path(result, seen, mode, root, resolved)
    for path in extra_writable_paths or []:
        resolved = path.resolve()
        if not resolved.exists() or not _is_writable_path_allowed(
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
            resolved,
            allow_oracle_conflict_writes,
        )
    return result


def _top_level_writable_roots(mode: FileAccessMode, root: Path) -> list[Path]:
    """root 自体を開かず、許可済み top-level path だけを候補にする。"""
    paths: list[Path] = []
    candidates = [
        root / name for name in _STANDARD_REALIZATION_WRITE_PATHS if (root / name).exists()
    ]
    if mode == FileAccessMode.REPO_WRITE:
        candidates.append(root / "oracle")
    if root.exists():
        candidates.extend(root.iterdir())
    for path in candidates:
        resolved = path.resolve()
        if resolved not in paths and _is_writable_path_allowed(mode, root, resolved):
            paths.append(resolved)
    return paths


def _append_writable_path(
    result: list[Path],
    seen: set[Path],
    mode: FileAccessMode,
    root: Path,
    path: Path,
    allow_oracle_conflict_writes: bool = False,
) -> None:
    if not _is_writable_path_allowed(mode, root, path, allow_oracle_conflict_writes):
        return
    if not path.exists():
        return
    if path.is_dir():
        # <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
        # Codex profile has no deny rule, so do not open directories that can
        # contain AGENTS.md or INDEX.md; enumerate writable files instead.
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


def _append_writable_root(result: list[Path], seen: set[Path], path: Path) -> None:
    """親子関係で冗長な writable root を持たないように追加する。"""
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
    # <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # 追加 writable path は、prompt で伝える禁止領域を広げない範囲だけ許可する。
    relative = path.relative_to(root)
    if path.name in {"AGENTS.md", "INDEX.md"}:
        return False
    if mode == FileAccessMode.REALIZATION_WRITE and allow_oracle_conflict_writes:
        # <work-root>/oracle/doc/app_spec/sub_command/session_join.md
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
        return False
    return mode in {FileAccessMode.REPO_WRITE, FileAccessMode.NO_RULE}


def _append_workspace_write_section(
    lines: list[str], writable_roots: list[Path]
) -> None:
    """Codex sandbox が理解できる workspace-write section を追加する。"""
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # FileAccessMode の細かい deny は prompt 側にも載せるが、Codex profile
    # で表現できる sandbox 境界はここで必ず渡してから起動する。
    roots = ", ".join(_toml_string(str(path)) for path in writable_roots)
    lines.extend(["[sandbox_workspace_write]", f"writable_roots = [{roots}]"])


def _needs_permission_profile(root: Path, extra_read_paths: list[Path] | None) -> bool:
    """旧 sandbox で表現できない work root 外の読み取り許可だけ profile 化する。"""
    return any(not path.resolve().is_relative_to(root) for path in extra_read_paths or [])


def _read_roots_for_permission_profile(
    root: Path,
    extra_read_paths: list[Path] | None,
    extra_read_root: Path | None,
) -> list[Path]:
    """Codex permission profile に渡す読み取り root を作る。"""
    roots = [root]
    for path in extra_read_paths or []:
        resolved = path.resolve()
        if resolved.is_relative_to(root):
            continue
        if extra_read_root is not None and _is_repo_local_read_path(
            extra_read_root, resolved
        ):
            roots.append(logs_dir(extra_read_root).parent.parent.resolve())
        else:
            roots.append(resolved)
    result: list[Path] = []
    seen: set[Path] = set()
    for path in roots:
        resolved = path.resolve()
        if resolved in seen or any(resolved.is_relative_to(parent) for parent in seen):
            continue
        redundant = [existing for existing in seen if existing.is_relative_to(resolved)]
        if redundant:
            result[:] = [existing for existing in result if existing not in redundant]
            seen.difference_update(redundant)
        seen.add(resolved)
        result.append(resolved)
    return result


def _append_permission_profile_section(
    lines: list[str],
    read_roots: list[Path],
    writable_roots: list[Path],
) -> None:
    """work root 外の read-only root は Codex beta permission profile で渡す。"""
    # <work-root>/oracle/doc/app_spec/sub_command/tui.md
    # <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
    # sandbox_workspace_write has writable_roots only; permission profiles can
    # represent repo-local TUI logs as read without granting write access.
    entries = {str(path): "read" for path in read_roots}
    entries.update({str(path): "write" for path in writable_roots})
    lines.extend(
        [
            f'default_permissions = "{_CMOC_PERMISSION_PROFILE}"',
            "",
            f"[permissions.{_CMOC_PERMISSION_PROFILE}]",
            'extends = ":read-only"',
            "",
            f"[permissions.{_CMOC_PERMISSION_PROFILE}.filesystem]",
        ]
    )
    for path, access in sorted(entries.items()):
        lines.append(f"{_toml_string(path)} = {_toml_string(access)}")


def _append_ollama_provider_section(lines: list[str], root: Path | None) -> None:
    lines.extend(
        [
            f"[model_providers.{_OLLAMA_PROVIDER_ID}]",
            'name = "cmoc managed ollama"',
            'base_url = "http://127.0.0.1:11434/v1"',
            'wire_api = "responses"',
        ]
    )


def build_codex_profile(
    parameter: AgentCallParameter,
    config: CmocConfig,
    root: Path | None = None,
    extra_read_paths: list[Path] | None = None,
    extra_writable_paths: list[Path] | None = None,
    *,
    extra_read_root: Path | None = None,
    allow_oracle_conflict_writes: bool = False,
) -> str:
    """AgentCallParameter と repo config から再利用可能な Codex profile 本文を作る。"""
    model_spec = config.codex.model[parameter.model_class]
    reasoning_effort = config.codex.reasoning_effort[parameter.reasoning_effort]
    lines = [
        f'model = "{model_spec.model}"',
        f'model_reasoning_effort = "{reasoning_effort}"',
    ]
    use_cmoc_managed_ollama = model_spec.model_provider == "cmoc"
    if use_cmoc_managed_ollama:
        lines.append(f'model_provider = "{_OLLAMA_PROVIDER_ID}"')
    use_permission_profile = False
    if root is not None:
        root = root.resolve()
        read_root = (extra_read_root or root).resolve()
        _validate_extra_read_paths(
            parameter.file_access_mode,
            root,
            extra_read_paths,
            extra_read_root=read_root,
        )
        use_permission_profile = _needs_permission_profile(root, extra_read_paths)
    if not use_permission_profile:
        sandbox_mode = file_access_to_sandbox_mode(parameter.file_access_mode)
        lines.append(f'sandbox_mode = "{sandbox_mode}"')
    if root is not None:
        writable_roots = _writable_roots(
            parameter.file_access_mode,
            root,
            extra_writable_paths,
            allow_oracle_conflict_writes,
        )
        if use_permission_profile:
            _append_permission_profile_section(
                lines,
                _read_roots_for_permission_profile(root, extra_read_paths, read_root),
                writable_roots,
            )
        else:
            _append_workspace_write_section(lines, writable_roots)
    if use_cmoc_managed_ollama:
        _append_ollama_provider_section(lines, root)
    lines.append("")
    return "\n".join(lines)


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


def codex_profile_name(profile_path: Path) -> str:
    """hashed profile path から Codex CLI の profile 名だけを取り出す。"""
    suffix = ".config.toml"
    if profile_path.name.endswith(suffix):
        return profile_path.name[: -len(suffix)]
    return profile_path.stem


def prepare_codex_profile(
    parameter: AgentCallParameter,
    config: CmocConfig | None = None,
    codex_home: Path | None = None,
    root: Path | None = None,
    extra_read_paths: list[Path] | None = None,
    extra_writable_paths: list[Path] | None = None,
    *,
    extra_read_root: Path | None = None,
    allow_oracle_conflict_writes: bool = False,
) -> Path:
    """Codex home 内へ内容 hash 名の profile を作り、同一内容なら再利用する。"""
    if (
        (config or CmocConfig()).codex.model[parameter.model_class].model_provider
        == "cmoc"
        and root is not None
    ):
        from commons.runtime_doctor import run_doctor_preprocess

        run_doctor_preprocess(root, config)
    profile = build_codex_profile(
        parameter,
        config or CmocConfig(),
        root,
        extra_read_paths,
        extra_writable_paths,
        extra_read_root=extra_read_root,
        allow_oracle_conflict_writes=allow_oracle_conflict_writes,
    )
    target_home = codex_home or resolve_codex_home()
    try:
        return write_hashed_file_in_existing_dir(
            target_home, "cmoc_", ".config.toml", profile
        )
    except OSError as exc:
        raise CmocError(
            "Codex profile を生成できません。",
            [
                "CODEX_HOME の権限を確認してください。",
                "Codex CLI の通常利用環境を初期化してから再実行してください。",
            ],
            f"CODEX_HOME: {target_home}\nerror: {exc}",
        ) from exc


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
        # <work-root>/oracle/doc/app_spec/sub_command/apply_abandon.md
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
        # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
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
    try:
        with apply_process_id_file_lock(tracking_path):
            process = subprocess.Popen(argv, start_new_session=True, **kwargs)
            _record_tracked_child_process(tracking_path, process.pid)
    except OSError as exc:
        if process is None:
            raise
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        raise CmocError(
            "apply process tracking を更新できません。",
            ["apply process pid file の権限と保存先を確認してください。"],
            f"path: {tracking_path}\nerror: {exc}",
        ) from exc
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
        try:
            remove_tracked_child_process(tracking_path, process.pid)
        except OSError as exc:
            raise CmocError(
                "apply process tracking を更新できません。",
                ["apply process pid file の権限と保存先を確認してください。"],
                f"path: {tracking_path}\nerror: {exc}",
            ) from exc


def record_tracked_child_process(path: Path, process_id: int) -> None:
    """apply process pid file へ Codex child process の同一性情報を追記する。"""
    with apply_process_id_file_lock(path):
        _record_tracked_child_process(path, process_id)


def _record_tracked_child_process(path: Path, process_id: int) -> None:
    start_time = process_start_time(process_id)
    if start_time is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    current = path.read_text() if path.exists() else ""
    lines = [line for line in current.splitlines() if line.strip()]
    child_line = f"child {process_id} {start_time}"
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


def process_start_time(process_id: int) -> int | None:
    """pid 再利用を検出するため Linux proc stat の starttime を読む。"""
    try:
        stat = Path(f"/proc/{process_id}/stat").read_text()
    except OSError:
        return None
    try:
        return int(stat.rsplit(") ", 1)[1].split()[19])
    except (IndexError, ValueError):
        return None


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
            fragments.append(line)
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
        if item.get("type") != "thread.started":
            continue
        value = item.get("thread_id")
        if isinstance(value, str) and value:
            return value
    return None


def _codex_jsonl_error_messages(stdout_text: str) -> list[str]:
    """retry 判定対象を Codex JSONL の error event に限定して抽出する。"""
    messages: list[str] = []
    for line in stdout_text.splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if item.get("type") == "error":
            message = item.get("message")
            if isinstance(message, str):
                messages.append(message)
        elif item.get("type") == "turn.failed":
            error = item.get("error")
            if isinstance(error, dict) and isinstance(error.get("message"), str):
                messages.append(error["message"])
    return messages


def is_capacity_error(stdout_text: str) -> bool:
    """Codex JSONL 上の model capacity error だけを retry 対象として判定する。"""
    return any(
        "Selected model is at capacity" in message
        for message in _codex_jsonl_error_messages(stdout_text)
    )


def is_quota_error(stdout_text: str) -> bool:
    """usage limit 系の Codex JSONL error を quota 待機対象として判定する。"""
    quota_markers = [
        "Quota exceeded",
        "You've hit your usage limit",
        "out of credits",
        "You hit your spend cap",
    ]
    return any(
        marker in message
        for message in _codex_jsonl_error_messages(stdout_text)
        for marker in quota_markers
    )
