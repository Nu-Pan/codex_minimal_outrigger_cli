"""Codex TUI が起動する editor input handoff 用 stdio MCP server。"""

import json
import os
import socket
import sys
from pathlib import Path

from .runtime_editor_input_handoff_protocol import (
    EDITOR_INPUT_HANDOFF_PROTOCOL_VERSION,
    EDITOR_INPUT_REPOSITORY_ENV,
    editor_input_handoff_socket_path,
    overwrite_input_is_valid,
    overwrite_input_schema,
    read_handoff_response,
)

MCP_PROTOCOL_VERSION = EDITOR_INPUT_HANDOFF_PROTOCOL_VERSION
_SERVER_NAME = "cmoc-editor-input-handoff"
_REJECTION_CODES = frozenset(
    {
        "invalid_input",
        "protocol_mismatch",
        "repository_mismatch",
        "target_unavailable",
        "transport_unavailable",
        "write_failed",
    }
)


def _rejected(code: str, message: str, retryable: bool) -> dict[str, object]:
    """content を含まない agent-facing domain failure を返す。"""
    return {
        "status": "rejected",
        "code": code,
        "message": message,
        "retryable": retryable,
    }


def _validated_target_result(value: object) -> dict[str, object] | None:
    """target response が content を持たない domain result か検査する。"""
    if value == {"status": "accepted"}:
        return value
    if not isinstance(value, dict) or value.get("status") != "rejected":
        return None
    code = value.get("code")
    message = value.get("message")
    retryable = value.get("retryable")
    if (
        not isinstance(code, str)
        or code not in _REJECTION_CODES
        or not isinstance(message, str)
        or type(retryable) is not bool
    ):
        return None
    return value


def _submit(payload: object) -> dict[str, object]:
    """tool input を同じ repository の active target へ転送する。"""
    repository_value = os.environ.get(EDITOR_INPUT_REPOSITORY_ENV)
    if repository_value is None:
        return _rejected(
            "target_unavailable",
            "editor input handoff context is unavailable",
            True,
        )
    if not overwrite_input_is_valid(payload):
        return _rejected("invalid_input", "tool input does not match schema", False)
    assert isinstance(payload, dict)
    target_id = payload["target_id"]
    assert isinstance(target_id, str)
    repository = Path(repository_value).resolve()
    request = {
        "protocol": EDITOR_INPUT_HANDOFF_PROTOCOL_VERSION,
        "repository": str(repository),
        "payload": payload,
    }
    try:
        socket_path = editor_input_handoff_socket_path(repository, target_id)
    except UnicodeError:
        return _rejected("invalid_input", "tool input does not match schema", False)
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
            connection.settimeout(10)
            connection.connect(str(socket_path))
            connection.sendall(
                json.dumps(
                    request,
                    ensure_ascii=True,
                    separators=(",", ":"),
                ).encode("utf-8")
                + b"\n"
            )
            value = read_handoff_response(connection)
    except OSError:
        return _rejected("target_unavailable", "target is not active", False)
    validated = _validated_target_result(value)
    if validated is None:
        return _rejected(
            "transport_unavailable",
            "invalid editor input handoff response",
            True,
        )
    return validated


def _tool_result(result: dict[str, object]) -> dict[str, object]:
    """domain result を MCP structuredContent と text の両方で返す。"""
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(result, ensure_ascii=False, separators=(",", ":")),
            }
        ],
        "structuredContent": result,
        "isError": False,
    }


def _response(request: object) -> dict[str, object] | None:
    """一つの MCP JSON-RPC message を処理する。"""
    if not isinstance(request, dict):
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32600, "message": "Invalid Request"},
        }
    method = request.get("method")
    if "id" not in request:
        return None
    request_id = request["id"]
    if method == "initialize":
        parameters = request.get("params")
        requested_protocol = (
            parameters.get("protocolVersion") if isinstance(parameters, dict) else None
        )
        protocol_version = (
            requested_protocol if isinstance(requested_protocol, str) else "2025-06-18"
        )
        result: dict[str, object] = {
            "protocolVersion": protocol_version,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": _SERVER_NAME, "version": MCP_PROTOCOL_VERSION},
        }
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {
            "tools": [
                {
                    "name": "overwrite",
                    "description": "active な prompt editor input file 全体を置換する。",
                    "inputSchema": overwrite_input_schema(),
                    "annotations": {
                        "readOnlyHint": False,
                        "destructiveHint": True,
                        "idempotentHint": False,
                        "openWorldHint": False,
                    },
                }
            ]
        }
    elif method == "tools/call":
        parameters = request.get("params")
        if not isinstance(parameters, dict) or parameters.get("name") != "overwrite":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32602, "message": "Unknown tool"},
            }
        result = _tool_result(_submit(parameters.get("arguments")))
    else:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": "Method not found"},
        }
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def main() -> int:
    """newline-framed stdio MCP server loop を実行する。"""
    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = _response(request)
        except (UnicodeError, json.JSONDecodeError):
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"},
            }
        if response is not None:
            sys.stdout.write(
                json.dumps(response, ensure_ascii=False, separators=(",", ":")) + "\n"
            )
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
