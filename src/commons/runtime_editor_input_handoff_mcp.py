"""Codex TUI が起動する editor input handoff 用 stdio MCP server。"""

import json
import os
import socket
import sys
from pathlib import Path

from .runtime_editor_input_handoff_protocol import (
    EDITOR_INPUT_HANDOFF_AUTHENTICATED_TIMEOUT_SECONDS,
    EDITOR_INPUT_HANDOFF_PROTOCOL_VERSION,
    EDITOR_INPUT_HANDOFF_UNAUTHENTICATED_TIMEOUT_SECONDS,
    EDITOR_INPUT_REPOSITORY_ENV,
    authenticate_editor_input_handoff_client,
    overwrite_input_is_valid,
    overwrite_input_schema,
    parse_editor_input_handoff_target_id,
    read_handoff_response,
)

MCP_PROTOCOL_VERSION = "2025-06-18"
_SERVER_NAME = "cmoc-editor-input-handoff"
_SERVER_VERSION = EDITOR_INPUT_HANDOFF_PROTOCOL_VERSION
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


def _invalid_request() -> dict[str, object]:
    """JSON-RPC request として解釈できない message の response を返す。"""
    return {
        "jsonrpc": "2.0",
        "id": None,
        "error": {"code": -32600, "message": "Invalid Request"},
    }


def _invalid_params(request_id: object) -> dict[str, object]:
    """method-specific params を解釈できない request の response を返す。"""
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32602, "message": "Invalid params"},
    }


def _is_valid_request_id(value: object) -> bool:
    """MCP が許可する string または integer の request ID か検査する。"""
    return isinstance(value, str) or type(value) is int


def _is_valid_jsonrpc_request(request: dict[object, object]) -> bool:
    """MCP の JSON-RPC 2.0 request 形状を副作用なく検査する。"""
    if request.get("jsonrpc") != "2.0" or not isinstance(request.get("method"), str):
        return False
    if "id" in request and not _is_valid_request_id(request["id"]):
        return False
    return "params" not in request or isinstance(request["params"], dict)


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
        return {"status": "accepted"}
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
    return {
        "status": "rejected",
        "code": code,
        "message": message,
        "retryable": retryable,
    }


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
    try:
        route = parse_editor_input_handoff_target_id(repository, target_id)
    except UnicodeError:
        return _rejected("invalid_input", "tool input does not match schema", False)
    if route is None:
        return _rejected("target_unavailable", "target is not active", False)
    address, token = route
    submission_started = False
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(EDITOR_INPUT_HANDOFF_UNAUTHENTICATED_TIMEOUT_SECONDS)
            connection.connect(address)
            if not authenticate_editor_input_handoff_client(
                connection,
                token,
                EDITOR_INPUT_HANDOFF_UNAUTHENTICATED_TIMEOUT_SECONDS,
            ):
                return _rejected(
                    "transport_unavailable",
                    "invalid editor input handoff response",
                    True,
                )
            connection.settimeout(EDITOR_INPUT_HANDOFF_AUTHENTICATED_TIMEOUT_SECONDS)
            request = {
                "protocol": EDITOR_INPUT_HANDOFF_PROTOCOL_VERSION,
                "repository": str(repository),
                "payload": payload,
            }
            request_data = (
                json.dumps(
                    request,
                    ensure_ascii=True,
                    separators=(",", ":"),
                ).encode("utf-8")
                + b"\n"
            )
            # sendall 自体が失敗しても、一部または全体が届いた可能性が残る。
            submission_started = True
            connection.sendall(request_data)
            value = read_handoff_response(
                connection,
                EDITOR_INPUT_HANDOFF_AUTHENTICATED_TIMEOUT_SECONDS,
            )
    except OSError:
        if not submission_started:
            return _rejected(
                "transport_unavailable",
                "editor input handoff connection failed before submission",
                True,
            )
        value = None
    validated = _validated_target_result(value)
    if validated is None:
        # 応答を失っても受付済みの上書きは継続する。未反映とは断定しない。
        return {
            "status": "unknown",
            "code": "transport_unavailable",
            "message": (
                "submission outcome is unknown; content may have been applied; "
                "verify editor input before retrying"
            ),
            "retryable": False,
        }
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
    if not isinstance(request, dict) or not _is_valid_jsonrpc_request(request):
        return _invalid_request()
    method = request.get("method")
    if "id" not in request:
        return None
    request_id = request["id"]
    if method == "initialize":
        parameters = request.get("params")
        if not isinstance(parameters, dict) or not isinstance(
            parameters.get("protocolVersion"), str
        ):
            return _invalid_params(request_id)
        requested_protocol = parameters["protocolVersion"]
        protocol_version = (
            requested_protocol
            if requested_protocol == MCP_PROTOCOL_VERSION
            else MCP_PROTOCOL_VERSION
        )
        result: dict[str, object] = {
            "protocolVersion": protocol_version,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": _SERVER_NAME, "version": _SERVER_VERSION},
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
        if not isinstance(parameters, dict):
            return _invalid_params(request_id)
        if parameters.get("name") != "overwrite":
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
