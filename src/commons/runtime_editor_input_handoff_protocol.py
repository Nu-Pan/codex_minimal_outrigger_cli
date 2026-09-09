"""editor input handoff の共有 schema・routing・transport 定義。"""

import hashlib
import hmac
import json
import os
import secrets
import socket
import time
from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from jsonschema.validators import Draft202012Validator

EDITOR_INPUT_REPOSITORY_ENV = "CMOC_EDITOR_INPUT_REPOSITORY"
EDITOR_INPUT_HANDOFF_PROTOCOL_VERSION = "2"
EDITOR_INPUT_HANDOFF_HOST = "127.0.0.1"
EDITOR_INPUT_HANDOFF_TOKEN_BYTES = 16
EDITOR_INPUT_HANDOFF_UNAUTHENTICATED_TIMEOUT_SECONDS = 1.0
EDITOR_INPUT_HANDOFF_AUTHENTICATED_TIMEOUT_SECONDS = 10.0
_HANDOFF_NONCE_BYTES = 32
_HANDOFF_PROOF_BYTES = hashlib.sha256().digest_size
_HANDOFF_RESPONSE_LIMIT = 64 * 1024
_CLIENT_PROOF_CONTEXT = b"cmoc-editor-input-handoff-v2/client\0"
_SERVER_PROOF_CONTEXT = b"cmoc-editor-input-handoff-v2/server\0"


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


def _repository_fingerprint(repository: Path) -> str:
    """canonical repository path の固定長 fingerprint を返す。"""
    repository_bytes = os.fsencode(str(repository.resolve()))
    return hashlib.sha256(repository_bytes).hexdigest()[:32]


def build_editor_input_handoff_target_id(
    repository: Path,
    port: int,
    token: bytes,
) -> str:
    """repository route と capability を opaque target ID に符号化する。"""
    if type(port) is not int or not 1 <= port <= 65535:
        raise ValueError("editor input handoff port is invalid")
    if len(token) != EDITOR_INPUT_HANDOFF_TOKEN_BYTES:
        raise ValueError("editor input handoff token is invalid")
    return f"eit_2_{_repository_fingerprint(repository)}_{port:04x}_{token.hex()}"


def parse_editor_input_handoff_target_id(
    repository: Path,
    target_id: str,
) -> tuple[tuple[str, int], bytes] | None:
    """同じ repository 用 target ID から loopback route と capability を得る。"""
    target_id.encode("utf-8")
    parts = target_id.split("_")
    if len(parts) != 5 or parts[:2] != ["eit", "2"]:
        return None
    repository_fingerprint, port_hex, token_hex = parts[2:]
    if (
        len(repository_fingerprint) != 32
        or len(port_hex) != 4
        or len(token_hex) != EDITOR_INPUT_HANDOFF_TOKEN_BYTES * 2
    ):
        return None
    if not hmac.compare_digest(
        repository_fingerprint,
        _repository_fingerprint(repository),
    ):
        return None
    try:
        port = int(port_hex, 16)
        token = bytes.fromhex(token_hex)
    except ValueError:
        return None
    if (
        not 1 <= port <= 65535
        or port_hex != f"{port:04x}"
        or len(token) != EDITOR_INPUT_HANDOFF_TOKEN_BYTES
        or token_hex != token.hex()
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
) -> dict[str, object] | None:
    """MCP client 用に小さな newline-framed response を読む。"""
    deadline = time.monotonic() + timeout_seconds
    response = b""
    while b"\n" not in response:
        _set_deadline_timeout(connection, deadline)
        chunk = connection.recv(8192)
        if not chunk:
            break
        response += chunk
        if len(response) > _HANDOFF_RESPONSE_LIMIT:
            return None
    try:
        value = json.loads(response.split(b"\n", 1)[0])
    except (UnicodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None
