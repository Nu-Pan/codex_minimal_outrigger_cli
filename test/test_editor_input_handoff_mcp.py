"""editor input handoff の agent-facing MCP interface を検証する。

正本仕様:
- {{work-root}}/oracle/doc/app_spec/editor_input_handoff.md
- {{work-root}}/oracle/src/oracle/editor_input_handoff/overwrite_input.json
"""

import json
import socket
import threading
from importlib import resources
from pathlib import Path
from unittest.mock import MagicMock

import pytest

import commons.runtime_editor_input_handoff_mcp as handoff_mcp
from commons.runtime_editor_input_handoff import start_editor_input_handoff
from commons.runtime_editor_input_handoff_protocol import (
    EDITOR_INPUT_REPOSITORY_ENV,
    build_editor_input_handoff_target_id,
)


def test_handoff_mcp_exposes_only_overwrite_with_canonical_schema() -> None:
    """tool 一つだけを公開し、正本 schema を複製せず返す。"""
    initialized = handoff_mcp._response(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": "2025-06-18"},
        }
    )
    assert initialized is not None
    assert initialized["result"]["protocolVersion"] == "2025-06-18"
    assert initialized["result"]["capabilities"] == {"tools": {"listChanged": False}}

    listed = handoff_mcp._response(
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
    )
    assert listed is not None
    tools = listed["result"]["tools"]
    assert [tool["name"] for tool in tools] == ["overwrite"]
    expected_schema = json.loads(
        resources.files("oracle.editor_input_handoff")
        .joinpath("overwrite_input.json")
        .read_text(encoding="utf-8")
    )
    assert tools[0]["inputSchema"] == expected_schema

    for method in ("resources/list", "prompts/list"):
        response = handoff_mcp._response(
            {"jsonrpc": "2.0", "id": method, "method": method, "params": {}}
        )
        assert response is not None
        assert response["error"]["code"] == -32601


@pytest.mark.parametrize(
    "message",
    [
        {"jsonrpc": "1.0", "id": 1, "method": "ping"},
        {"jsonrpc": "2.0", "id": True, "method": "ping"},
        {"jsonrpc": "2.0", "id": [], "method": "ping"},
        {"jsonrpc": "2.0", "id": 1, "method": 1},
        {"jsonrpc": "2.0", "id": 1, "method": "ping", "params": "invalid"},
        {"jsonrpc": "2.0", "id": 1, "method": "ping", "params": []},
    ],
)
def test_handoff_mcp_rejects_invalid_jsonrpc_request(
    message: dict[str, object],
) -> None:
    """JSON-RPC 2.0 の request 形状を満たさない入力を実行しない。"""
    assert handoff_mcp._response(message) == {
        "jsonrpc": "2.0",
        "id": None,
        "error": {"code": -32600, "message": "Invalid Request"},
    }


@pytest.mark.parametrize("requested", ["2024-11-05", "future-version"])
def test_handoff_mcp_negotiates_only_supported_protocol_version(
    requested: str,
) -> None:
    """未対応の MCP protocol version をそのまま採用しない。"""
    response = handoff_mcp._response(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": requested},
        }
    )
    assert response is not None
    assert response["result"]["protocolVersion"] == "2025-06-18"


def test_handoff_mcp_requires_initialize_protocol_parameter() -> None:
    """initialize の必須 protocolVersion 欠落を method error にする。"""
    response = handoff_mcp._response(
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
    )
    assert response == {
        "jsonrpc": "2.0",
        "id": 1,
        "error": {"code": -32602, "message": "Invalid params"},
    }


def test_handoff_mcp_rejects_invalid_input_without_returning_content(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """schema 違反と transport 不可能な文字列を content 非表示で拒否する。"""
    monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, "/tmp/repository")
    payloads: tuple[object, ...] = (
        {"target_id": "target", "content": ["private content"]},
        {"target_id": "\ud800", "content": "private content"},
    )

    for payload in payloads:
        result = handoff_mcp._submit(payload)
        rendered = json.dumps(result, ensure_ascii=True)
        assert result["status"] == "rejected"
        assert result["code"] == "invalid_input"
        assert "private content" not in rendered


@pytest.mark.parametrize("failure", ["timeout", "eof"])
def test_handoff_response_loss_reports_unknown_while_write_completes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
) -> None:
    """受付済み上書きの応答を失っても、非 active や未反映とは報告しない。"""
    work = tmp_path / ".cmoc/gu/editor_input/input.md"
    work.parent.mkdir(parents=True)
    work.write_text("initial", encoding="utf-8")
    target = start_editor_input_handoff(tmp_path, work)
    entered = threading.Event()
    release = threading.Event()
    overwrite = target._overwrite
    read_response = handoff_mcp.read_handoff_response

    def delayed_overwrite(content: str) -> None:
        entered.set()
        assert release.wait(5)
        overwrite(content)

    def lose_response(connection: socket.socket, _timeout: float) -> object:
        assert entered.wait(2)
        if failure == "eof":
            connection.shutdown(socket.SHUT_RD)
        return read_response(connection, 0.05)

    monkeypatch.setattr(target, "_overwrite", delayed_overwrite)
    monkeypatch.setattr(handoff_mcp, "read_handoff_response", lose_response)
    monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, str(tmp_path))
    try:
        response = handoff_mcp._response(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "overwrite",
                    "arguments": {
                        "target_id": target.target_id,
                        "content": "private content",
                    },
                },
            }
        )
        assert response is not None
        result = response["result"]["structuredContent"]
        assert result["status"] == "unknown"
        assert result["code"] == "transport_unavailable"
        assert result["retryable"] is False
        assert "may have been applied" in result["message"]
        assert "private content" not in json.dumps(response)
        assert work.read_text(encoding="utf-8") == "initial"
    finally:
        release.set()
        target.close()
    assert work.read_text(encoding="utf-8") == "private content"


@pytest.mark.parametrize(
    ("stage", "error", "status", "retryable"),
    [
        ("connect", PermissionError(), "rejected", True),
        ("authenticate", TimeoutError(), "rejected", True),
        ("sendall", BrokenPipeError(), "unknown", False),
    ],
)
def test_handoff_transport_errors_distinguish_submission_uncertainty(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    stage: str,
    error: OSError,
    status: str,
    retryable: bool,
) -> None:
    """送信前の失敗と、部分送信もあり得る送信中の失敗を区別する。"""
    connection = MagicMock()
    connection.__enter__.return_value = connection
    authenticate = MagicMock(return_value=True)
    if stage == "authenticate":
        authenticate.side_effect = error
    else:
        getattr(connection, stage).side_effect = error
    monkeypatch.setattr(handoff_mcp.socket, "socket", lambda *_args: connection)
    monkeypatch.setattr(
        handoff_mcp, "authenticate_editor_input_handoff_client", authenticate
    )
    monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, str(tmp_path))
    result = handoff_mcp._submit(
        {
            "target_id": build_editor_input_handoff_target_id(
                tmp_path, 1234, b"x" * 16
            ),
            "content": "private content",
        }
    )
    assert result["status"] == status
    assert result["code"] == "transport_unavailable"
    assert result["retryable"] is retryable
    assert "not active" not in result["message"]
    assert "private content" not in json.dumps(result)


def test_handoff_mcp_strips_unexpected_target_result_fields(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """target response の余分な field を agent-facing result へ転送しない。"""
    connection = MagicMock()
    connection.__enter__.return_value = connection
    monkeypatch.setattr(handoff_mcp.socket, "socket", lambda *_args: connection)
    monkeypatch.setattr(
        handoff_mcp,
        "authenticate_editor_input_handoff_client",
        lambda *_args: True,
    )
    monkeypatch.setattr(
        handoff_mcp,
        "read_handoff_response",
        lambda *_args: {
            "status": "rejected",
            "code": "write_failed",
            "message": "editor input overwrite failed",
            "retryable": False,
            "content": "private content",
        },
    )
    monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, str(tmp_path))

    result = handoff_mcp._submit(
        {
            "target_id": build_editor_input_handoff_target_id(
                tmp_path, 1234, b"x" * 16
            ),
            "content": "private content",
        }
    )

    assert result == {
        "status": "rejected",
        "code": "write_failed",
        "message": "editor input overwrite failed",
        "retryable": False,
    }
    assert "private content" not in json.dumps(result)
