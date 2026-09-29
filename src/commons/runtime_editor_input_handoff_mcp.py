"""Codex TUI が起動する editor input handoff 用 stdio MCP server。"""

import json
import os
import socket
import sys
from pathlib import Path

from oracle.editor_input_handoff.body import build_editor_input_handoff_body
from oracle.other.doc_ref_model import DocRef

from .runtime_editor_input_handoff_protocol import (
    EDITOR_INPUT_HANDOFF_AUTHENTICATED_TIMEOUT_SECONDS,
    EDITOR_INPUT_HANDOFF_PROTOCOL_VERSION,
    EDITOR_INPUT_HANDOFF_UNAUTHENTICATED_TIMEOUT_SECONDS,
    EDITOR_INPUT_REPOSITORY_ENV,
    authenticate_editor_input_handoff_client,
    editor_input_handoff_source_from_env,
    handoff_payload_is_valid,
    handoff_schema,
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


def _rejected(code: str, message: str, retryable: bool) -> dict[str, object]:
    """content を含まない agent-facing domain failure を返す。"""
    return {
        "status": "rejected",
        "code": code,
        "message": message,
        "retryable": retryable,
    }


def _validated_target_result(value: object, *, guide: bool) -> dict[str, object] | None:
    """ガイド取得の正本 schema と本文を返さない上書き結果を検査する。"""
    if guide:
        if not handoff_payload_is_valid("get_handoff_guide_result", value):
            return None
        assert isinstance(value, dict)
        return value
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
    """項目別入力と送信元から本文を生成し、同じ repository の target へ渡す。"""
    return _call_target(payload, tool_name="overwrite")


def _get_handoff_guide(payload: object) -> dict[str, object]:
    """指定された active target の保持済みガイドだけを取得する。"""
    # 共通 transport の失敗も、正本が定める取得結果の形へ収める。
    result = _call_target(payload, tool_name="get_handoff_guide")
    if handoff_payload_is_valid("get_handoff_guide_result", result):
        return result
    return {"status": "error", "message": result["message"]}


def _call_target(payload: object, *, tool_name: str) -> dict[str, object]:
    """入力を検証し、認証した同一 repository の target に要求を送る。"""
    # 取得と上書きで repository と target の検証、認証 transport を共用する。
    repository_value = os.environ.get(EDITOR_INPUT_REPOSITORY_ENV)
    if repository_value is None:
        return _rejected(
            "target_unavailable",
            "editor input handoff context is unavailable",
            True,
        )
    if not handoff_payload_is_valid(f"{tool_name}_input", payload):
        return _rejected("invalid_input", "tool input does not match schema", False)
    assert isinstance(payload, dict)
    target_id = payload["target_id"]
    assert isinstance(target_id, str)
    repository = Path(repository_value).resolve()
    try:
        route = parse_editor_input_handoff_target_id(repository, target_id)
    except (UnicodeError, TypeError):
        return _rejected("invalid_input", "tool input does not match schema", False)
    if route is None:
        return _rejected("target_unavailable", "target is not active", False)
    guide = tool_name == "get_handoff_guide"
    target_payload = {"target_id": target_id}
    if not guide:
        # 送信元は tool input や受信先から推測せず、起動時の context だけを使う。
        try:
            source = editor_input_handoff_source_from_env()
        except (ValueError, TypeError):
            return _rejected(
                "source_unavailable",
                "editor input handoff source is unavailable",
                False,
            )
        try:
            references = [
                DocRef(Path(reference["file_path"]), reference["loc_desc"])
                for reference in payload["oracle_references"]
            ]
            content = build_editor_input_handoff_body(
                goal=payload["goal"],
                instructions=payload["instructions"],
                background=payload["background"],
                decisions=payload["decisions"],
                open_questions=payload["open_questions"],
                oracle_references=references,
                source=source,
            )
            content.encode("utf-8")
        except Exception:
            # builder や検証器の例外には入力本文が含まれ得るため転記しない。
            return _rejected("invalid_input", "handoff body could not be built", False)
        target_payload["content"] = content
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
                "payload": target_payload,
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
            if guide:
                # 完全 prompt を含むガイドは、小さな上書き結果の上限で切り詰めない。
                value = read_handoff_response(
                    connection,
                    EDITOR_INPUT_HANDOFF_AUTHENTICATED_TIMEOUT_SECONDS,
                    max_bytes=None,
                )
            else:
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
    validated = _validated_target_result(value, guide=guide)
    if validated is None:
        if guide:
            return {
                "status": "error",
                "message": "handoff guide could not be retrieved",
            }
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
        "isError": result.get("status") not in ("accepted", "ok"),
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
            "serverInfo": {"name": _SERVER_NAME, "version": _SERVER_VERSION},
        }
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {
            "tools": [
                {
                    "name": "get_handoff_guide",
                    "description": "指定された active target の handoff ガイドを取得する。",
                    "inputSchema": handoff_schema("get_handoff_guide_input"),
                    "outputSchema": handoff_schema("get_handoff_guide_result"),
                    "annotations": {
                        "readOnlyHint": True,
                        "openWorldHint": False,
                    },
                },
                {
                    "name": "overwrite",
                    "description": "active な prompt editor input file 全体を置換する。",
                    "inputSchema": handoff_schema("overwrite_input"),
                    "annotations": {
                        "readOnlyHint": False,
                        "destructiveHint": True,
                        "idempotentHint": False,
                        "openWorldHint": False,
                    },
                },
            ]
        }
    elif method == "tools/call":
        parameters = request.get("params")
        if not isinstance(parameters, dict):
            return _invalid_params(request_id)
        name = parameters.get("name")
        if name not in ("get_handoff_guide", "overwrite"):
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32602, "message": "Unknown tool"},
            }
        handler = _get_handoff_guide if name == "get_handoff_guide" else _submit
        result = _tool_result(handler(parameters.get("arguments")))
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
