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
    FEEDBACK_COLLECTOR_HOST,
    FEEDBACK_COLLECTOR_PORT_ENV,
    FEEDBACK_PROTOCOL_ENV,
)
from .runtime_feedback_store import (
    REPORTER_PROTOCOL_VERSION,
    is_uuid7_prefixed,
    reporter_input_schema,
)

MCP_PROTOCOL_VERSION = "2025-06-18"
_SERVER_NAME = "cmoc-feedback-reporter"
_REJECTION_CODES = frozenset(
    {
        "schema_invalid",
        "payload_too_large",
        "path_outside_repo",
        "evidence_empty",
        "rate_limited",
        "suspected_secret",
        "context_invalid",
        "collector_unavailable",
        "protocol_mismatch",
        "transport_unavailable",
    }
)
_RETRYABLE_REJECTION_CODES = frozenset(
    {"rate_limited", "collector_unavailable", "transport_unavailable"}
)


def _rejected(code: str, message: str, retryable: bool) -> dict[str, object]:
    """collector 到達前の transport failure を domain result にする。"""
    return {
        "status": "rejected",
        "code": code,
        "message": message,
        "retryable": retryable,
    }


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


def _is_valid_initialize_params(value: object) -> bool:
    """MCP initialize request の必須 parameter shape を検査する。"""
    if not isinstance(value, dict):
        return False
    client_info = value.get("clientInfo")
    return (
        isinstance(value.get("protocolVersion"), str)
        and isinstance(value.get("capabilities"), dict)
        and isinstance(client_info, dict)
        and isinstance(client_info.get("name"), str)
        and isinstance(client_info.get("version"), str)
    )


def _validated_collector_result(value: object) -> dict[str, object] | None:
    """collector の domain result が agent-facing 契約に適合するか検査する。"""
    if not isinstance(value, dict):
        return None
    status = value.get("status")
    if status == "accepted":
        observation_id = value.get("observation_id")
        redaction_count = value.get("redaction_count")
        if (
            not isinstance(observation_id, str)
            or not is_uuid7_prefixed(observation_id, "fbo_")
            or type(redaction_count) is not int
            or redaction_count < 0
        ):
            return None
        return {
            "status": "accepted",
            "observation_id": observation_id,
            "redaction_count": redaction_count,
        }
    if status != "rejected":
        return None
    code = value.get("code")
    message = value.get("message")
    retryable = value.get("retryable")
    if (
        not isinstance(code, str)
        or code not in _REJECTION_CODES
        or not isinstance(message, str)
        or type(retryable) is not bool
        or (retryable and code not in _RETRYABLE_REJECTION_CODES)
    ):
        return None
    return {
        "status": "rejected",
        "code": code,
        "message": message,
        "retryable": retryable,
    }


def _submit(payload: object) -> dict[str, object]:
    """tool payload を capability envelope と分離して collector へ転送する。"""
    collector_port_text = os.environ.get(FEEDBACK_COLLECTOR_PORT_ENV)
    capability = os.environ.get(FEEDBACK_CAPABILITY_ENV)
    protocol = os.environ.get(FEEDBACK_PROTOCOL_ENV)
    if (
        not collector_port_text
        or not collector_port_text.isascii()
        or not collector_port_text.isdecimal()
        or len(collector_port_text) > 5
        or not capability
    ):
        return _rejected(
            "collector_unavailable", "feedback collector context is unavailable", True
        )
    collector_port = int(collector_port_text)
    if not 1 <= collector_port <= 65535:
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
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(10)
            connection.connect((FEEDBACK_COLLECTOR_HOST, collector_port))
            connection.sendall(
                json.dumps(request, ensure_ascii=True, separators=(",", ":")).encode(
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
    validated = _validated_collector_result(value)
    if validated is None:
        return _rejected("protocol_mismatch", "invalid collector response", False)
    return validated


def _tool_result(result: dict[str, object]) -> dict[str, object]:
    """domain result を MCP structuredContent と text の両方で返す。"""
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(result, ensure_ascii=True, separators=(",", ":")),
            }
        ],
        "structuredContent": result,
        "isError": False,
    }


def _response(request: object) -> dict[str, object] | None:
    """一つの MCP JSON-RPC message を処理する。"""
    # JSON-RPC notification は不正な Request であっても応答しない。
    if isinstance(request, dict) and "id" not in request:
        return None
    if not isinstance(request, dict) or not _is_valid_jsonrpc_request(request):
        return _invalid_request()
    method = request.get("method")
    request_id = request["id"]
    if method == "initialize":
        parameters = request.get("params")
        if not _is_valid_initialize_params(parameters):
            return _invalid_params(request_id)
        assert isinstance(parameters, dict)
        requested_protocol = parameters["protocolVersion"]
        protocol_version = (
            requested_protocol
            if requested_protocol == MCP_PROTOCOL_VERSION
            else MCP_PROTOCOL_VERSION
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
                    "description": "現在の workload では解消できない問題を、後続の自動修復または人間対応の候補として cmoc collector へ送信する。",
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
        if not isinstance(parameters, dict):
            return _invalid_params(request_id)
        if parameters.get("name") != "submit_observation":
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
                json.dumps(response, ensure_ascii=True, separators=(",", ":")) + "\n"
            )
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
