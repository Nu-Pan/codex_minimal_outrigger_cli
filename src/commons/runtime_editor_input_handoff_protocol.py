"""editor input handoff の共有 schema・routing・transport 定義。"""

import hmac
import json
import os
import secrets
import socket
import stat
import time
from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import TYPE_CHECKING, Any

from oracle.editor_input_handoff.body import EditorInputHandoffSource

from .runtime_ids import is_common_id, new_id
from .runtime_logging import current_execution_id
from .runtime_paths import untracked_data_dir

if TYPE_CHECKING:
    from jsonschema.validators import Draft202012Validator

EDITOR_INPUT_REPOSITORY_ENV = "CMOC_EDITOR_INPUT_REPOSITORY"
EDITOR_INPUT_SOURCE_ENV = "CMOC_EDITOR_INPUT_SOURCE"
EDITOR_INPUT_HANDOFF_PROTOCOL_VERSION = "2"
EDITOR_INPUT_HANDOFF_HOST = "127.0.0.1"
EDITOR_INPUT_HANDOFF_TOKEN_BYTES = 16
EDITOR_INPUT_HANDOFF_UNAUTHENTICATED_TIMEOUT_SECONDS = 1.0
EDITOR_INPUT_HANDOFF_AUTHENTICATED_TIMEOUT_SECONDS = 10.0
_HANDOFF_NONCE_BYTES = 32
_HANDOFF_PROOF_BYTES = 32
_HANDOFF_RESPONSE_LIMIT = 64 * 1024
_CLIENT_PROOF_CONTEXT = b"cmoc-editor-input-handoff-v2/client\0"
_SERVER_PROOF_CONTEXT = b"cmoc-editor-input-handoff-v2/server\0"


@lru_cache(maxsize=3)
def handoff_schema(name: str) -> dict[str, Any]:
    """oracle package resource から handoff の入出力 schema を読む。"""
    # 呼び出し側が指定する正本 resource を共用する。
    schema_text = (
        resources.files("oracle.editor_input_handoff")
        .joinpath(f"{name}.json")
        .read_text(encoding="utf-8")
    )
    loaded = json.loads(schema_text)
    if not isinstance(loaded, dict):
        raise TypeError("editor input handoff schema must be a JSON object")
    return loaded


@lru_cache(maxsize=3)
def _handoff_validator(name: str) -> "Draft202012Validator":
    """正本 schema から受け入れ検査用 validator を構築する。"""
    from jsonschema.validators import Draft202012Validator

    schema = handoff_schema(name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def handoff_payload_is_valid(name: str, payload: object) -> bool:
    """content 本文をエラーへ複製せず、正本 schema への適合だけを返す。"""
    return not any(_handoff_validator(name).iter_errors(payload))


def editor_input_handoff_subprocess_env(
    base: dict[str, str],
    repository: Path,
    source: EditorInputHandoffSource | None,
) -> dict[str, str]:
    """この TUI process の repository と送信元だけを MCP 環境へ渡す。"""
    # 親 process の送信元を引き継がず、この呼び出しの値で置換する。
    environment = {
        **base,
        EDITOR_INPUT_REPOSITORY_ENV: str(repository.resolve()),
    }
    environment.pop(EDITOR_INPUT_SOURCE_ENV, None)
    if source is not None:
        environment[EDITOR_INPUT_SOURCE_ENV] = json.dumps(
            {
                "subcommand": source.subcommand,
                "execution_id": source.execution_id,
                "codex_call_id": source.codex_call_id,
                "sub_command_log_path": str(source.sub_command_log_path),
            }
        )
    return environment


def editor_input_handoff_source_from_env() -> EditorInputHandoffSource:
    """MCP の起動元が供給した送信元を、推定や値の補完なしで検査する。"""
    # transport の形状を検査し、値の意味は正本の型へ委譲する。
    value = json.loads(os.environ.get(EDITOR_INPUT_SOURCE_ENV, "null"))
    fields = {"subcommand", "execution_id", "codex_call_id", "sub_command_log_path"}
    if (
        not isinstance(value, dict)
        or value.keys() != fields
        or not all(isinstance(item, str) for item in value.values())
    ):
        raise ValueError("editor input handoff source is unavailable")
    return EditorInputHandoffSource(
        subcommand=value["subcommand"],
        execution_id=value["execution_id"],
        codex_call_id=value["codex_call_id"],
        sub_command_log_path=Path(value["sub_command_log_path"]),
    )


def _route_directory(repository: Path) -> Path:
    """active target の一時 route だけを保持する directory を返す。"""
    return untracked_data_dir(repository) / "state" / "editor_input_handoff"


def build_editor_input_handoff_target_id(
    repository: Path,
    port: int,
    token: bytes,
    *,
    execution_id: str | None = None,
) -> str:
    """target ID を発行し、同じ repository の一時 route へ登録する。"""
    if type(port) is not int or not 1 <= port <= 65535:
        raise ValueError("editor input handoff port is invalid")
    if len(token) != EDITOR_INPUT_HANDOFF_TOKEN_BYTES:
        raise ValueError("editor input handoff token is invalid")
    owner = execution_id or current_execution_id(repository)
    if not is_common_id(owner, "exec"):
        raise ValueError("editor input handoff execution ID is invalid")
    target_id = new_id(repository, "eit")
    directory = _route_directory(repository)
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    route_path = directory / f"{target_id}.json"
    descriptor = os.open(route_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as route_file:
            json.dump(
                {"port": port, "token": token.hex(), "execution_id": owner},
                route_file,
            )
            route_file.flush()
    except BaseException:
        route_path.unlink(missing_ok=True)
        raise
    return target_id


def remove_editor_input_handoff_target_route(repository: Path, target_id: str) -> None:
    """無効化済み target の route を削除する。"""
    if is_common_id(target_id, "eit"):
        (_route_directory(repository) / f"{target_id}.json").unlink(missing_ok=True)


def parse_editor_input_handoff_target_id(
    repository: Path,
    target_id: str,
) -> tuple[tuple[str, int], bytes] | None:
    """同じ repository の active target から loopback route を得る。"""
    target_id.encode("utf-8")
    if not is_common_id(target_id, "eit"):
        return None
    path = _route_directory(repository) / f"{target_id}.json"
    try:
        if not stat.S_ISREG(path.lstat().st_mode):
            return None
        route = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError):
        return None
    if not isinstance(route, dict) or set(route) != {
        "port",
        "token",
        "execution_id",
    }:
        return None
    try:
        port = route["port"]
        token_hex = route["token"]
        if not isinstance(token_hex, str):
            return None
        token = bytes.fromhex(token_hex)
    except (TypeError, ValueError):
        return None
    if (
        type(port) is not int
        or not 1 <= port <= 65535
        or len(token) != EDITOR_INPUT_HANDOFF_TOKEN_BYTES
        or token_hex != token.hex()
        or not is_common_id(route["execution_id"], "exec")
    ):
        return None
    return (EDITOR_INPUT_HANDOFF_HOST, port), token


def _set_deadline_timeout(connection: socket.socket, deadline: float) -> None:
    """次の socket operation を共有 absolute deadline 内に制限する。"""
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError("editor input handoff deadline exceeded")
    connection.settimeout(remaining)


def _sendall_before_deadline(
    connection: socket.socket,
    data: bytes,
    deadline: float,
) -> None:
    """共有 absolute deadline を維持して固定 frame を送る。"""
    _set_deadline_timeout(connection, deadline)
    connection.sendall(data)


def _read_exact(
    connection: socket.socket,
    size: int,
    deadline: float,
) -> bytes | None:
    """固定長 authentication frame を EOF まで考慮して読む。"""
    received = bytearray()
    while len(received) < size:
        _set_deadline_timeout(connection, deadline)
        chunk = connection.recv(size - len(received))
        if not chunk:
            return None
        received.extend(chunk)
    return bytes(received)


def _handoff_proof(token: bytes, context: bytes, nonce: bytes) -> bytes:
    """role-separated HMAC-SHA256 proof を構築する。"""
    return hmac.digest(token, context + nonce, "sha256")


def authenticate_editor_input_handoff_server(
    connection: socket.socket,
    token: bytes,
    timeout_seconds: float,
) -> bool:
    """request body の受信前に client を認証し、server proof を返す。"""
    deadline = time.monotonic() + timeout_seconds
    nonce = secrets.token_bytes(_HANDOFF_NONCE_BYTES)
    _sendall_before_deadline(connection, nonce, deadline)
    client_proof = _read_exact(connection, _HANDOFF_PROOF_BYTES, deadline)
    expected = _handoff_proof(token, _CLIENT_PROOF_CONTEXT, nonce)
    if client_proof is None or not hmac.compare_digest(client_proof, expected):
        return False
    _sendall_before_deadline(
        connection,
        _handoff_proof(token, _SERVER_PROOF_CONTEXT, nonce),
        deadline,
    )
    return True


def authenticate_editor_input_handoff_client(
    connection: socket.socket,
    token: bytes,
    timeout_seconds: float,
) -> bool:
    """content 送信前に capability を証明し、server proof を検証する。"""
    deadline = time.monotonic() + timeout_seconds
    nonce = _read_exact(connection, _HANDOFF_NONCE_BYTES, deadline)
    if nonce is None:
        return False
    _sendall_before_deadline(
        connection,
        _handoff_proof(token, _CLIENT_PROOF_CONTEXT, nonce),
        deadline,
    )
    server_proof = _read_exact(connection, _HANDOFF_PROOF_BYTES, deadline)
    expected = _handoff_proof(token, _SERVER_PROOF_CONTEXT, nonce)
    return server_proof is not None and hmac.compare_digest(server_proof, expected)


def read_handoff_response(
    connection: socket.socket,
    timeout_seconds: float,
    *,
    max_bytes: int | None = _HANDOFF_RESPONSE_LIMIT,
) -> dict[str, object] | None:
    """期限内に newline-framed response を読み、任意の受信量上限を適用する。"""
    deadline = time.monotonic() + timeout_seconds
    response = b""
    while b"\n" not in response:
        _set_deadline_timeout(connection, deadline)
        chunk = connection.recv(8192)
        if not chunk:
            break
        response += chunk
        if max_bytes is not None and len(response) > max_bytes:
            return None
    try:
        value = json.loads(response.split(b"\n", 1)[0])
    except (UnicodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None
