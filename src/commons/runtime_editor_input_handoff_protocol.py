"""editor input handoff の共有 schema・routing・transport 定義。"""

import hashlib
import json
import os
import socket
import tempfile
from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from jsonschema.validators import Draft202012Validator

EDITOR_INPUT_REPOSITORY_ENV = "CMOC_EDITOR_INPUT_REPOSITORY"
EDITOR_INPUT_HANDOFF_PROTOCOL_VERSION = "1"
_SOCKET_RESPONSE_LIMIT = 64 * 1024


@lru_cache(maxsize=1)
def overwrite_input_schema() -> dict[str, Any]:
    """oracle package resource から overwrite input schema を読む。"""
    schema_text = (
        resources.files("oracle.editor_input_handoff")
        .joinpath("overwrite_input.json")
        .read_text(encoding="utf-8")
    )
    loaded = json.loads(schema_text)
    if not isinstance(loaded, dict):
        raise TypeError("editor input overwrite schema must be a JSON object")
    return loaded


@lru_cache(maxsize=1)
def _overwrite_input_validator() -> "Draft202012Validator":
    """正本 schema から受け入れ検査用 validator を構築する。"""
    from jsonschema.validators import Draft202012Validator

    schema = overwrite_input_schema()
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def overwrite_input_is_valid(payload: object) -> bool:
    """content 本文をエラーへ複製せず、正本 schema への適合だけを返す。"""
    return not any(_overwrite_input_validator().iter_errors(payload))


def editor_input_handoff_subprocess_env(
    base: dict[str, str],
    repository: Path,
) -> dict[str, str]:
    """MCP process へ渡す repository context を Codex 環境へ追加する。"""
    return {
        **base,
        EDITOR_INPUT_REPOSITORY_ENV: str(repository.resolve()),
    }


def editor_input_handoff_socket_path(repository: Path, target_id: str) -> Path:
    """repository と opaque target ID から短い一時 socket path を導出する。"""
    repository_bytes = os.fsencode(str(repository.resolve()))
    digest = hashlib.sha256(
        repository_bytes + b"\0" + target_id.encode("utf-8")
    ).hexdigest()[:32]
    return Path(tempfile.gettempdir()) / f"cmoc-ei-{os.getuid()}-{digest}.sock"


def read_handoff_response(connection: socket.socket) -> dict[str, object] | None:
    """MCP client 用に小さな newline-framed domain response を読む。"""
    response = b""
    while b"\n" not in response:
        chunk = connection.recv(8192)
        if not chunk:
            break
        response += chunk
        if len(response) > _SOCKET_RESPONSE_LIMIT:
            return None
    try:
        value = json.loads(response.split(b"\n", 1)[0])
    except (UnicodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None
