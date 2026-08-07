"""Codex が起動する call-scoped stdio MCP feedback reporter/client。

対応する oracle file:
`{{work-root}}/oracle/doc/app_spec/feedback_observation.md`。
"""

import json
import os
import socket
import sys

from .runtime_feedback import (
    FEEDBACK_CAPABILITY_ENV,
    FEEDBACK_COLLECTOR_ENV,
    FEEDBACK_PROTOCOL_ENV,
)
from .runtime_feedback_store import (
    REPORTER_PROTOCOL_VERSION,
    reporter_input_schema,
)

MCP_PROTOCOL_VERSION = REPORTER_PROTOCOL_VERSION
_SERVER_NAME = "cmoc-feedback-reporter"


def _rejected(code: str, message: str, retryable: bool) -> dict[str, object]:
    """collector 到達前の transport failure を domain result にする。"""
    return {
        "status": "rejected",
        "code": code,
        "message": message,
        "retryable": retryable,
    }


def _submit(payload: object) -> dict[str, object]:
    """tool payload を capability envelope と分離して collector へ転送する。"""
    socket_path = os.environ.get(FEEDBACK_COLLECTOR_ENV)
    capability = os.environ.get(FEEDBACK_CAPABILITY_ENV)
    protocol = os.environ.get(FEEDBACK_PROTOCOL_ENV)
    if not socket_path or not capability:
        return _rejected(
            "collector_unavailable", "feedback collector context is unavailable", True
        )
    if protocol != REPORTER_PROTOCOL_VERSION:
        return _rejected("protocol_mismatch", "feedback protocol mismatch", False)
    request = {
        "protocol": REPORTER_PROTOCOL_VERSION,
        "capability": capability,
        "payload": payload,
    }
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
            connection.settimeout(10)
            connection.connect(socket_path)
            connection.sendall(
                json.dumps(request, ensure_ascii=False, separators=(",", ":")).encode(
                    "utf-8"
                )
                + b"\n"
            )
            response = b""
            while b"\n" not in response:
                chunk = connection.recv(8192)
                if not chunk:
                    break
                response += chunk
                if len(response) > 64 * 1024:
                    return _rejected(
                        "transport_unavailable", "collector response is too large", True
                    )
    except OSError:
        return _rejected(
            "collector_unavailable", "feedback collector is unavailable", True
        )
    try:
        value = json.loads(response.split(b"\n", 1)[0])
    except (UnicodeError, json.JSONDecodeError):
        return _rejected("protocol_mismatch", "invalid collector response", False)
    if not isinstance(value, dict) or value.get("status") not in {
        "accepted",
        "rejected",
    }:
        return _rejected("protocol_mismatch", "invalid collector response", False)
    return value


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
        # notification は状態を持たない reporter では応答不要である。
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
            "serverInfo": {"name": _SERVER_NAME, "version": REPORTER_PROTOCOL_VERSION},
        }
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {
            "tools": [
                {
                    "name": "submit_observation",
                    "description": "人間対応が必要な問題の observation を cmoc collector へ送信する。",
                    "inputSchema": reporter_input_schema(),
                    "annotations": {
                        "readOnlyHint": False,
                        "destructiveHint": False,
                        "idempotentHint": False,
                        "openWorldHint": False,
                    },
                }
            ]
        }
    elif method == "tools/call":
        parameters = request.get("params")
        if (
            not isinstance(parameters, dict)
            or parameters.get("name") != "submit_observation"
        ):
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
