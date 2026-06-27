import json
import os
import subprocess
from pathlib import Path
from typing import Any

from basic.acp import AgentCallParameter, FileAccessMode
from config.cmoc_config import CmocConfig

from commons.runtime_content import write_hashed_file, write_hashed_file_in_existing_dir
from commons.runtime_errors import CmocError
from commons.runtime_paths import schema_store_dir

APPLY_PROCESS_TRACKING_ENV = "CMOC_APPLY_PROCESS_ID_PATH"


def file_access_to_sandbox_mode(mode: FileAccessMode) -> str:
    """cmoc の file access policy を Codex CLI が理解する sandbox 名へ落とす。"""
    match mode:
        case FileAccessMode.READONLY | FileAccessMode.PURE_ORACLE_READ:
            return "read-only"
        case (
            FileAccessMode.REALIZATION_WRITE
            | FileAccessMode.ORACLE_WRITE
            | FileAccessMode.REPO_WRITE
        ):
            return "workspace-write"
        case _:
            raise CmocError("不明な FileAccessMode です。", [], str(mode))


def file_access_to_codex_cwd(mode: FileAccessMode, root: Path) -> Path:
    """FileAccessMode の読み取り境界に合わせた Codex 作業 root を返す。"""
    root = root.resolve()
    if mode == FileAccessMode.PURE_ORACLE_READ:
        # <work-root>/oracle/src/acp/prompt_parts/file_access_rule.py
        # Codex profile は read-only の読み取り root を分けられないため、
        # 公開済みの --cd/cwd で oracle tree だけを作業 root にする。
        return root / "oracle"
    return root


def _is_read_path_allowed(mode: FileAccessMode, root: Path, path: Path) -> bool:
    if not path.is_relative_to(root):
        return False
    if path.is_relative_to(root / "memo") or path.is_relative_to(root / ".agents"):
        return False
    return mode != FileAccessMode.PURE_ORACLE_READ or path.is_relative_to(
        root / "oracle"
    )


def _validate_extra_read_paths(
    mode: FileAccessMode,
    root: Path,
    extra_read_paths: list[Path] | None,
) -> None:
    for path in extra_read_paths or []:
        resolved = path.resolve()
        if not _is_read_path_allowed(mode, root, resolved):
            raise CmocError(
                "追加読み取り許可 path が FileAccessMode の許可領域外にあります。",
                ["file access mode で読み取り可能な work root 配下の path を指定してください。"],
                f"mode: {mode.value}\npath: {resolved}",
            )


def _toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _writable_roots(
    mode: FileAccessMode,
    root: Path,
    extra_writable_paths: list[Path] | None,
) -> list[Path]:
    if file_access_to_sandbox_mode(mode) == "read-only":
        return []
    root = root.resolve()
    match mode:
        case FileAccessMode.REALIZATION_WRITE:
            paths = [
                path
                for path in root.iterdir()
                if _is_writable_path_allowed(mode, root, path.resolve())
            ]
        case FileAccessMode.ORACLE_WRITE:
            paths = [root / "oracle"]
        case FileAccessMode.REPO_WRITE:
            paths = [
                path
                for path in root.iterdir()
                if _is_writable_path_allowed(mode, root, path.resolve())
            ]
        case _:
            paths = []
    result: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            result.append(resolved)
    for path in extra_writable_paths or []:
        resolved = path.resolve()
        if not _is_writable_path_allowed(mode, root, resolved):
            raise CmocError(
                "追加書き込み許可 path が FileAccessMode の許可領域外にあります。",
                ["file access mode で書き込み可能な work root 配下の path を指定してください。"],
                f"mode: {mode.value}\npath: {resolved}",
            )
        if resolved not in seen:
            seen.add(resolved)
            result.append(resolved)
    return result


def _is_writable_path_allowed(mode: FileAccessMode, root: Path, path: Path) -> bool:
    if not path.is_relative_to(root):
        return False
    # <work-root>/oracle/src/acp/prompt_parts/file_access_rule.py
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # Codex profile は deny を持たないため、FileAccessMode と Codex exec の
    # 禁止領域を writable_roots に入れない正リストとして表現する。
    if path.is_relative_to(root / "memo") or path.is_relative_to(root / ".agents"):
        return False
    if mode == FileAccessMode.REALIZATION_WRITE:
        return not path.is_relative_to(root / "oracle")
    if mode == FileAccessMode.ORACLE_WRITE:
        return path.is_relative_to(root / "oracle")
    return mode == FileAccessMode.REPO_WRITE


def _append_workspace_write_section(lines: list[str], writable_roots: list[Path]) -> None:
    if not writable_roots:
        return
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # FileAccessMode の細かい deny は prompt 側にも載せるが、Codex profile
    # で表現できる sandbox 境界はここで必ず渡してから起動する。
    roots = ", ".join(_toml_string(str(path)) for path in writable_roots)
    lines.extend(["[sandbox_workspace_write]", f"writable_roots = [{roots}]"])


def build_codex_profile(
    parameter: AgentCallParameter,
    config: CmocConfig,
    root: Path | None = None,
    extra_read_paths: list[Path] | None = None,
    extra_writable_paths: list[Path] | None = None,
) -> str:
    """AgentCallParameter と repo config から再利用可能な Codex profile 本文を作る。"""
    model = config.codex.model[parameter.model_class]
    reasoning_effort = config.codex.reasoning_effort[parameter.reasoning_effort]
    lines = [
        f'model = "{model}"',
        f'model_reasoning_effort = "{reasoning_effort}"',
    ]
    if root is not None:
        root = root.resolve()
        _validate_extra_read_paths(
            parameter.file_access_mode, root, extra_read_paths
        )
    sandbox_mode = file_access_to_sandbox_mode(parameter.file_access_mode)
    lines.append(f'sandbox_mode = "{sandbox_mode}"')
    if root is not None:
        _append_workspace_write_section(
            lines,
            _writable_roots(
                parameter.file_access_mode,
                root,
                extra_writable_paths,
            ),
        )
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
) -> Path:
    """Codex home 内へ内容 hash 名の profile を作り、同一内容なら再利用する。"""
    profile = build_codex_profile(
        parameter,
        config or CmocConfig(),
        root,
        extra_read_paths,
        extra_writable_paths,
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
    tracking_path = os.environ.get(APPLY_PROCESS_TRACKING_ENV)
    try:
        if tracking_path and argv[:1] == ["codex"]:
            return run_tracked_codex_subprocess(argv, Path(tracking_path), **kwargs)
        return subprocess.run(argv, **kwargs)
    except FileNotFoundError as exc:
        if argv[:1] != ["codex"]:
            raise
        # <work-root>/oracle/src/commons/runtime_codex.py
        # oracle 断片では Codex CLI missing を専用 fallback で利用者向け失敗にする。
        raise CmocError(
            "Codex CLI が見つかりません。",
            ["Codex CLI をインストールし、PATH に codex を含めてください。"],
            f"argv: {argv}\nerror: {exc}",
        ) from exc


def run_tracked_codex_subprocess(
    argv: list[str], tracking_path: Path, **kwargs: Any
) -> subprocess.CompletedProcess[Any]:
    input_data = kwargs.pop("input", None)
    capture_output = kwargs.pop("capture_output", False)
    check = kwargs.pop("check", False)
    if capture_output:
        kwargs.setdefault("stdout", subprocess.PIPE)
        kwargs.setdefault("stderr", subprocess.PIPE)
    process = subprocess.Popen(argv, start_new_session=True, **kwargs)
    record_tracked_child_process(tracking_path, process.pid)
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
        remove_tracked_child_process(tracking_path, process.pid)


def record_tracked_child_process(path: Path, process_id: int) -> None:
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
    if not path.exists():
        return
    lines = [
        line
        for line in path.read_text().splitlines()
        if not line.startswith(f"child {process_id} ")
    ]
    path.write_text(("\n".join(lines) + "\n") if lines else "")


def process_start_time(process_id: int) -> int | None:
    try:
        stat = Path(f"/proc/{process_id}/stat").read_text()
    except OSError:
        return None
    try:
        return int(stat.rsplit(") ", 1)[1].split()[19])
    except (IndexError, ValueError):
        return None


def prepare_schema(root: Path, schema_source_path: Path | None) -> Path | None:
    """Structured Output schema を work root 側の内容 hash store へ配置する。"""
    if schema_source_path is None:
        return None
    schema_text = schema_source_path.read_text()
    return write_hashed_file(schema_store_dir(root), "", ".json", schema_text)


def read_output_json(path: Path) -> Any:
    """Codex output file が空または不正 JSON の場合は retry 判定側へ None を返す。"""
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
