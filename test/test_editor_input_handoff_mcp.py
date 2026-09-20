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
from _handoff_support import handoff_body, handoff_input

import commons.runtime_editor_input_handoff_mcp as handoff_mcp
from commons.runtime_editor_input_handoff import start_editor_input_handoff
from commons.runtime_editor_input_handoff_protocol import (
    EDITOR_INPUT_REPOSITORY_ENV,
    EDITOR_INPUT_SOURCE_ENV,
    build_editor_input_handoff_target_id,
)

pytestmark = pytest.mark.usefixtures("handoff_source")


def test_handoff_mcp_exposes_only_overwrite_with_canonical_schema() -> None:
    """tool 一つだけを公開し、正本 schema を複製せず返す。"""
    initialized = handoff_mcp._response(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1"},
            },
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
            "params": {
                "protocolVersion": requested,
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1"},
            },
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


@pytest.mark.parametrize(
    "params",
    [
        {
            "protocolVersion": "2025-06-18",
            "clientInfo": {"name": "client", "version": "1"},
        },
        {"protocolVersion": "2025-06-18", "capabilities": {}},
        {
            "protocolVersion": "2025-06-18",
            "capabilities": [],
            "clientInfo": {"name": "client", "version": "1"},
        },
        {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "client"},
        },
    ],
)
def test_handoff_mcp_requires_initialize_capabilities_and_client_info(
    params: dict[str, object],
) -> None:
    """initialize の capabilities と clientInfo を必須として扱う。"""
    response = handoff_mcp._response(
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": params}
    )
    assert response == {
        "jsonrpc": "2.0",
        "id": 1,
        "error": {"code": -32602, "message": "Invalid params"},
    }


def test_handoff_mcp_marks_domain_failure_as_tool_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """submission failure は MCP tool result の isError へ反映する。"""
    monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, "/tmp/repository")
    response = handoff_mcp._response(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "overwrite",
                "arguments": {"target_id": "target", "content": []},
            },
        }
    )
    assert response is not None
    result = response["result"]
    assert result["structuredContent"]["status"] == "rejected"
    assert result["isError"] is True


def test_handoff_mcp_rejects_invalid_input_without_returning_content(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """schema 違反と transport 不可能な文字列を content 非表示で拒否する。"""
    monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, "/tmp/repository")
    payloads: tuple[object, ...] = (
        {"target_id": "target", "content": ["private content"]},
        handoff_input("\ud800", "private content"),
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
    handoff_source,
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
                    "arguments": handoff_input(target.target_id, "private content"),
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
    assert work.read_text(encoding="utf-8") == handoff_body(
        "private content", handoff_source
    )


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
        handoff_input(
            build_editor_input_handoff_target_id(tmp_path, 1234, b"x" * 16),
            "private content",
        )
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
        handoff_input(
            build_editor_input_handoff_target_id(tmp_path, 1234, b"x" * 16),
            "private content",
        )
    )

    assert result == {
        "status": "rejected",
        "code": "write_failed",
        "message": "editor input overwrite failed",
        "retryable": False,
    }
    assert "private content" not in json.dumps(result)


@pytest.mark.parametrize(
    "change",
    [
        {"goal": "  \n"},
        {"instructions": None},
        {"instructions": "\ud800private input"},
        {"background": ""},
        {"decisions": []},
        {"open_questions": "\t"},
        {"oracle_references": None},
        {"oracle_references": [{"file_path": "relative.md", "loc_desc": None}]},
        {"oracle_references": [{"file_path": "/oracle.md", "loc_desc": ""}]},
        {"oracle_references": [{"file_path": "/oracle.md"}]},
        {"source": {"execution_id": "forged"}},
        {"content": "private input"},
    ],
)
def test_invalid_handoff_fields_leave_target_untouched(tmp_path, change):
    work = tmp_path / ".cmoc/gu/editor_input/input.md"
    work.parent.mkdir(parents=True)
    work.write_text("initial")
    target = start_editor_input_handoff(tmp_path, work)
    try:
        with pytest.MonkeyPatch.context() as patch:
            patch.setenv(EDITOR_INPUT_REPOSITORY_ENV, str(tmp_path))
            result = handoff_mcp._submit(
                {**handoff_input(target.target_id, "private input"), **change}
            )
        assert result["code"] == "invalid_input"
        assert "private input" not in json.dumps(result)
        assert work.read_text() == "initial"
    finally:
        target.close()


@pytest.mark.parametrize(
    "source_change",
    [
        None,
        "malformed-json",
        {},
        {"execution_id": ""},
        {"subcommand": []},
        {"codex_call_id": "  "},
        {"sub_command_log_path": "relative.jsonl"},
    ],
)
def test_missing_or_invalid_source_refuses_handoff(
    tmp_path, monkeypatch, source_change
):
    work = tmp_path / ".cmoc/gu/editor_input/input.md"
    work.parent.mkdir(parents=True)
    work.write_text("initial")
    target = start_editor_input_handoff(tmp_path, work)
    try:
        monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, str(tmp_path))
        if isinstance(source_change, dict) and source_change:
            source = json.loads(handoff_mcp.os.environ[EDITOR_INPUT_SOURCE_ENV])
            source.update(source_change)
            value = json.dumps(source)
        else:
            value = (
                json.dumps(source_change)
                if source_change != "malformed-json"
                else source_change
            )
        monkeypatch.setenv(EDITOR_INPUT_SOURCE_ENV, value)
        result = handoff_mcp._submit(handoff_input(target.target_id, "private input"))
        assert result["code"] == "source_unavailable"
        assert work.read_text() == "initial"
        assert "private input" not in json.dumps(result)
    finally:
        target.close()


def test_handoff_uses_canonical_body_and_typed_references(
    tmp_path, monkeypatch, handoff_source
):
    from oracle.editor_input_handoff.body import build_editor_input_handoff_body
    from oracle.other.doc_ref_model import DocRef

    work = tmp_path / ".cmoc/gu/editor_input/input.md"
    work.parent.mkdir(parents=True)
    work.write_text("initial")
    target = start_editor_input_handoff(tmp_path, work)
    monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, str(tmp_path))
    reference_path = tmp_path / "oracle/doc/spec.md"
    fields = handoff_input(target.target_id, "本文を保持する <!-- コメント -->\n続き")
    fields["oracle_references"] = [
        {"file_path": str(reference_path), "loc_desc": None},
        {"file_path": str(reference_path), "loc_desc": "対象の見出し"},
    ]
    expected = build_editor_input_handoff_body(
        **{
            key: value
            for key, value in fields.items()
            if key not in {"target_id", "oracle_references"}
        },
        oracle_references=[
            DocRef(reference_path, None),
            DocRef(reference_path, "対象の見出し"),
        ],
        source=handoff_source,
    )
    try:
        for _ in range(2):
            assert handoff_mcp._submit(fields) == {"status": "accepted"}
            assert work.read_text() == expected
        assert "<!-- コメント -->" in expected
        assert str(reference_path) in expected
        assert handoff_source.codex_call_id in expected
        assert target.target_id not in expected
    finally:
        target.close()


def test_handoff_builder_failure_does_not_leak_input_or_write(tmp_path, monkeypatch):
    work = tmp_path / ".cmoc/gu/editor_input/input.md"
    work.parent.mkdir(parents=True)
    work.write_text("initial")
    target = start_editor_input_handoff(tmp_path, work)
    monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, str(tmp_path))

    def fail(**_kwargs):
        raise RuntimeError("private input")

    monkeypatch.setattr(handoff_mcp, "build_editor_input_handoff_body", fail)
    try:
        result = handoff_mcp._submit(handoff_input(target.target_id, "private input"))
        assert result["status"] == "rejected"
        assert "private input" not in json.dumps(result)
        assert work.read_text() == "initial"
    finally:
        target.close()
