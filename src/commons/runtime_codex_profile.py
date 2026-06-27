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


def _validate_extra_read_paths(
    root: Path,
    extra_read_paths: list[Path] | None,
) -> None:
    protected = [root / "memo", root / ".agents"]
    for path in extra_read_paths or []:
        resolved = path.resolve()
        if any(resolved.is_relative_to(base) for base in protected):
            raise CmocError(
                "追加読み取り許可 path が保護領域内にあります。",
                ["memo または .agents 配下ではないファイルを指定してください。"],
                f"path: {resolved}",
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
    # Codex profile は deny を持たないため、FileAccessMode の禁止領域を
    # writable_roots に入れない正リストとして表現する。
    if path.is_relative_to(root / "memo"):
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
        _validate_extra_read_paths(root, extra_read_paths)
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
    """CODEX_HOME の相対指定を呼び出し側 cwd 基準で解決する。"""
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
    try:
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
