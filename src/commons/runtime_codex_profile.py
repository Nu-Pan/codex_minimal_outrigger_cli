import json
import os
from pathlib import Path
from typing import Any

from basic.acp import AgentCallParameter, FileAccessMode
from config.cmoc_config import CmocConfig

from commons.runtime_content import write_hashed_file, write_hashed_file_in_existing_dir
from commons.runtime_errors import CmocError
from commons.runtime_paths import schema_store_dir


def file_access_to_sandbox_mode(mode: FileAccessMode) -> str:
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


def build_codex_profile(parameter: AgentCallParameter, config: CmocConfig) -> str:
    model = config.codex.model[parameter.model_class]
    reasoning_effort = config.codex.reasoning_effort[parameter.reasoning_effort]
    sandbox_mode = file_access_to_sandbox_mode(parameter.file_access_mode)
    return "\n".join(
        [
            f'model = "{model}"',
            f'reasoning_effort = "{reasoning_effort}"',
            f'sandbox_mode = "{sandbox_mode}"',
            "",
        ]
    )


def resolve_codex_home(cwd: Path | None = None) -> Path:
    value = os.environ.get("CODEX_HOME")
    if value is not None:
        raw_path = Path(value)
        return raw_path if raw_path.is_absolute() else (cwd or Path.cwd()) / raw_path
    return (Path.home() / ".codex").resolve()


def validate_codex_home(codex_home: Path) -> None:
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
    suffix = ".config.toml"
    if profile_path.name.endswith(suffix):
        return profile_path.name[: -len(suffix)]
    return profile_path.stem


def prepare_codex_profile(
    parameter: AgentCallParameter,
    config: CmocConfig | None = None,
    codex_home: Path | None = None,
) -> Path:
    profile = build_codex_profile(parameter, config or CmocConfig())
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
    value = os.environ.get("CODEX_HOME")
    if value is None:
        value = str(codex_home)
    return {**os.environ, "CODEX_HOME": value}


def prepare_schema(root: Path, schema_source_path: Path | None) -> Path | None:
    if schema_source_path is None:
        return None
    schema_text = schema_source_path.read_text()
    return write_hashed_file(schema_store_dir(root), "", ".json", schema_text)


def read_output_json(path: Path) -> Any:
    if not path.exists() or not path.read_text().strip():
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return None


def codex_error_text(stdout_text: str, stderr_text: str) -> str:
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
    for line in stdout_text.splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        for key in ("session_id", "conversation_id", "id"):
            value = item.get(key)
            if isinstance(value, str) and value:
                return value
    return None


def is_capacity_error(text: str) -> bool:
    return "Selected model is at capacity" in text


def is_quota_error(text: str) -> bool:
    quota_markers = [
        "Quota exceeded",
        "You've hit your usage limit",
        "out of credits",
        "You hit your spend cap",
    ]
    return any(marker in text for marker in quota_markers)
