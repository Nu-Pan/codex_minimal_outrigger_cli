"""editor input handoff の agent-facing MCP interface を検証する。

正本仕様:
- {{work-root}}/oracle/doc/app_spec/editor_input_handoff.md
- {{work-root}}/oracle/src/oracle/editor_input_handoff/overwrite_input.json
"""

import json
import socket
import threading
from contextlib import nullcontext
from importlib import resources
from pathlib import Path
from unittest.mock import Mock

import pytest
from _handoff_support import handoff_body, handoff_input
from jsonschema.validators import Draft202012Validator
from oracle.editor_input_handoff.guide import build_editor_input_handoff_guide

import commons.runtime_editor_input_handoff_mcp as handoff_mcp
from commons.runtime_editor_input_handoff import start_editor_input_handoff
from commons.runtime_editor_input_handoff_protocol import (
    _HANDOFF_RESPONSE_LIMIT,
    EDITOR_INPUT_REPOSITORY_ENV,
    EDITOR_INPUT_SOURCE_ENV,
    read_handoff_message,
)

pytestmark = pytest.mark.usefixtures("handoff_source")


@pytest.fixture
def handoff_transport(tmp_path, monkeypatch):
    """MCP 側の検証では受信 thread を起動せず、上書き要求の送信を観測する。"""
    # 採番・route 登録は lifecycle test で検証し、ここでは解決結果だけを使う。
    target_id = "eit_000000_2026-09-29_15-04"
    connection = Mock()
    monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, str(tmp_path))
    monkeypatch.setattr(
        handoff_mcp,
        "parse_editor_input_handoff_target_id",
        lambda *_args: (("127.0.0.1", 1234), b"x" * 16),
    )
    monkeypatch.setattr(
        handoff_mcp.socket, "socket", lambda *_args: nullcontext(connection)
    )
    monkeypatch.setattr(
        handoff_mcp,
        "authenticate_editor_input_handoff_client",
        lambda *_args: True,
    )
    monkeypatch.setattr(
        handoff_mcp, "read_handoff_message", lambda *_args: {"status": "accepted"}
    )
    return target_id, connection


def _get_guide_result(arguments):
    response = handoff_mcp._response(
        {
            "jsonrpc": "2.0",
            "id": "guide",
            "method": "tools/call",
            "params": {"name": "get_handoff_guide", "arguments": arguments},
        }
    )
    result = response["result"]
    value = result["structuredContent"]
    schema = json.loads(
        resources.files("oracle.editor_input_handoff")
        .joinpath("get_handoff_guide_result.json")
        .read_text(encoding="utf-8")
    )
    Draft202012Validator(schema).validate(value)
    assert json.loads(result["content"][0]["text"]) == value
    assert result["isError"] is (value["status"] == "error")
    return value


def test_handoff_guide_returns_complete_large_receiver_template(tmp_path, monkeypatch):
    monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, str(tmp_path))
    work = tmp_path / ".cmoc/gu/log/editor_input/input.md"
    work.parent.mkdir(parents=True)
    work.write_text("private editor content")
    # 上書き応答の上限を超える境界を、過剰な本文量なしで検証する。
    line = "受信先の制約"
    repeat_count = _HANDOFF_RESPONSE_LIMIT // len(line.encode("utf-8")) + 1
    skeleton = f"{line}\r\n" * repeat_count + "{{original-prompt-here}}"
    expected_guide = build_editor_input_handoff_guide(skeleton)
    assert len(expected_guide.encode("utf-8")) > _HANDOFF_RESPONSE_LIMIT
    target = start_editor_input_handoff(tmp_path, work, skeleton)
    monkeypatch.delenv(EDITOR_INPUT_SOURCE_ENV)
    try:
        result = _get_guide_result({"target_id": target.target_id})
        assert result == {
            "status": "ok",
            "guide_text": expected_guide,
        }
        assert "private editor content" not in json.dumps(result)
        assert work.read_text() == "private editor content"
    finally:
        target.close()
    assert not target.handoff_guide_path.exists()


def test_unavailable_guide_never_returns_editor_content(tmp_path, monkeypatch):
    """同じ active target で各取得失敗と復帰を検証し、登録・受信 thread を共用する。"""
    monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, str(tmp_path))
    work = tmp_path / ".cmoc/gu/log/editor_input/input.md"
    work.parent.mkdir(parents=True)
    work.write_text("private editor content")
    target = start_editor_input_handoff(tmp_path, work, "{{original-prompt-here}}")
    try:
        guide_bytes = target.handoff_guide_path.read_bytes()
        for damage in ("missing", "invalid_utf8", "symlink"):
            target.handoff_guide_path.unlink()
            if damage == "invalid_utf8":
                target.handoff_guide_path.write_bytes(b"\xff")
            elif damage == "symlink":
                target.handoff_guide_path.symlink_to(work)
            result = _get_guide_result({"target_id": target.target_id})
            assert result["status"] == "error", damage
            assert "private editor content" not in json.dumps(result), damage
            assert work.read_text() == "private editor content", damage

            # 正常取得へ戻し、前の失敗結果の使い回しが次の故障を隠さないようにする。
            target.handoff_guide_path.unlink(missing_ok=True)
            target.handoff_guide_path.write_bytes(guide_bytes)
            assert _get_guide_result({"target_id": target.target_id}) == {
                "status": "ok",
                "guide_text": guide_bytes.decode("utf-8"),
            }, damage
    finally:
        target.close()


@pytest.mark.parametrize(
    "arguments",
    [
        None,
        {},
        {"target_id": " "},
        {"target_id": 1},
        {"target_id": "unknown"},
        {"target_id": "\ud800"},
        {"target_id": "unknown", "content": "private input"},
        {"target_id": "unknown", "file_path": "private input"},
    ],
)
def test_handoff_guide_rejects_invalid_or_unknown_target_without_input_leak(
    tmp_path, monkeypatch, arguments
):
    monkeypatch.setenv(EDITOR_INPUT_REPOSITORY_ENV, str(tmp_path))
    result = _get_guide_result(arguments)
    assert result["status"] == "error"
    assert "private input" not in json.dumps(result)


@pytest.mark.parametrize(
    "target_result",
    [
        None,
        {"status": "ok"},
        {"status": "error", "message": " "},
        {"status": "ok", "guide_text": "public guide", "content": "private input"},
    ],
)
def test_handoff_guide_rejects_invalid_target_result_without_input_leak(
    monkeypatch, handoff_transport, target_result
):
    """欠落・不正・余分な本文を含む受信応答はガイドとして返さない。"""
    target_id, connection = handoff_transport
    monkeypatch.setattr(
        handoff_mcp,
        "read_handoff_message",
        lambda *_args, **_kwargs: target_result,
    )
    result = _get_guide_result({"target_id": target_id})
    assert result["status"] == "error"
    assert "private input" not in json.dumps(result)
    connection.sendall.assert_called_once()


def test_handoff_mcp_exposes_only_guide_and_overwrite_with_canonical_schemas() -> None:
    """取得と上書きだけを公開し、正本 schema を複製せず返す。"""
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
    assert [tool["name"] for tool in tools] == ["get_handoff_guide", "overwrite"]
    for tool in tools:
        expected_schema = json.loads(
            resources.files("oracle.editor_input_handoff")
            .joinpath(f"{tool['name']}_input.json")
            .read_text(encoding="utf-8")
        )
        assert tool["inputSchema"] == expected_schema
    assert tools[0]["outputSchema"] == json.loads(
        resources.files("oracle.editor_input_handoff")
        .joinpath("get_handoff_guide_result.json")
        .read_text(encoding="utf-8")
    )

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


def test_handoff_response_loss_reports_unknown_while_write_completes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    handoff_source,
) -> None:
    """受付済み上書きの応答を失っても、非 active や未反映とは報告しない。"""
    work = tmp_path / ".cmoc/gu/log/editor_input/input.md"
    work.parent.mkdir(parents=True)
    work.write_text("initial", encoding="utf-8")
    target = start_editor_input_handoff(tmp_path, work, "{{original-prompt-here}}")
    entered = threading.Event()
    release = threading.Event()
    overwrite = target._overwrite
    read_response = handoff_mcp.read_handoff_message

    def delayed_overwrite(content: str) -> None:
        entered.set()
        assert release.wait(5)
        overwrite(content)

    def lose_response(connection: socket.socket, timeout: float) -> object:
        assert entered.wait(2)
        # EOF で応答だけを失わせる。timeout の結果判定は transport 境界で検証する。
        connection.shutdown(socket.SHUT_RD)
        return read_response(connection, timeout)

    monkeypatch.setattr(target, "_overwrite", delayed_overwrite)
    monkeypatch.setattr(handoff_mcp, "read_handoff_message", lose_response)
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
        ("recv", TimeoutError(), "unknown", False),
    ],
)
def test_handoff_transport_errors_distinguish_submission_uncertainty(
    monkeypatch: pytest.MonkeyPatch,
    handoff_transport,
    stage: str,
    error: OSError,
    status: str,
    retryable: bool,
) -> None:
    """送信前の失敗と、送信中・応答喪失による結果不明を区別する。"""
    target_id, connection = handoff_transport
    authenticate = Mock(return_value=True)
    if stage == "authenticate":
        authenticate.side_effect = error
    else:
        getattr(connection, stage).side_effect = error
    if stage == "recv":
        # 受信器を通した timeout を待機なしで起こし、応答喪失の unknown 判定を守る。
        monkeypatch.setattr(handoff_mcp, "read_handoff_message", read_handoff_message)
    monkeypatch.setattr(
        handoff_mcp, "authenticate_editor_input_handoff_client", authenticate
    )
    result = handoff_mcp._submit(handoff_input(target_id, "private content"))
    assert result["status"] == status
    assert result["code"] == "transport_unavailable"
    assert result["retryable"] is retryable
    assert "not active" not in result["message"]
    assert "private content" not in json.dumps(result)
    if stage == "recv":
        connection.sendall.assert_called_once()


def test_handoff_mcp_strips_unexpected_target_result_fields(
    monkeypatch: pytest.MonkeyPatch,
    handoff_transport,
) -> None:
    """target response の余分な field を agent-facing result へ転送しない。"""
    target_id, _connection = handoff_transport
    monkeypatch.setattr(
        handoff_mcp,
        "read_handoff_message",
        lambda *_args: {
            "status": "rejected",
            "code": "write_failed",
            "message": "editor input overwrite failed",
            "retryable": False,
            "content": "private content",
        },
    )
    result = handoff_mcp._submit(handoff_input(target_id, "private content"))

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
def test_invalid_handoff_fields_leave_target_untouched(handoff_transport, change):
    """不正入力は拒否され、受信側へ上書き要求が届かない。"""
    target_id, connection = handoff_transport
    result = handoff_mcp._submit(
        {**handoff_input(target_id, "private input"), **change}
    )
    assert result["code"] == "invalid_input"
    assert "private input" not in json.dumps(result)
    connection.sendall.assert_not_called()


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
    monkeypatch, handoff_transport, source_change
):
    """送信元情報の欠落・破損時は上書き要求を送信しない。"""
    target_id, connection = handoff_transport
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
    result = handoff_mcp._submit(handoff_input(target_id, "private input"))
    assert result["code"] == "source_unavailable"
    assert "private input" not in json.dumps(result)
    connection.sendall.assert_not_called()


def test_handoff_uses_canonical_body_and_typed_references(
    tmp_path, handoff_transport, handoff_source
):
    """本文・参照の構築を送信境界で検証し、実書き込みは lifecycle test に委ねる。"""
    from oracle.editor_input_handoff.body import build_editor_input_handoff_body
    from oracle.other.doc_ref_model import DocRef

    target_id, connection = handoff_transport
    reference_path = tmp_path / "oracle/doc/spec.md"
    fields = handoff_input(target_id, "本文を保持する <!-- コメント -->\n続き")
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
    for _ in range(2):
        connection.sendall.reset_mock()
        assert handoff_mcp._submit(fields) == {"status": "accepted"}
        sent = b"".join(call.args[0] for call in connection.sendall.call_args_list)
        request = json.loads(sent)
        assert request["payload"] == {"target_id": target_id, "content": expected}
    assert "<!-- コメント -->" in expected
    assert str(reference_path) in expected
    assert handoff_source.codex_call_id in expected
    assert target_id not in expected


def test_handoff_builder_failure_does_not_leak_input_or_write(
    monkeypatch, handoff_transport
):
    """本文生成の例外は入力を漏らさず拒否し、上書き要求を送信しない。"""
    target_id, connection = handoff_transport

    def fail(**_kwargs):
        raise RuntimeError("private input")

    monkeypatch.setattr(handoff_mcp, "build_editor_input_handoff_body", fail)
    result = handoff_mcp._submit(handoff_input(target_id, "private input"))
    assert result["status"] == "rejected"
    assert "private input" not in json.dumps(result)
    connection.sendall.assert_not_called()
