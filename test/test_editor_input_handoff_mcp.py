"""editor input handoff の agent-facing MCP interface を検証する。

正本仕様:
- {{work-root}}/oracle/doc/app_spec/editor_input_handoff.md
- {{work-root}}/oracle/src/oracle/editor_input_handoff/overwrite_input.json
"""

import json
from importlib import resources

import pytest

import commons.runtime_editor_input_handoff_mcp as handoff_mcp
from commons.runtime_editor_input_handoff_protocol import EDITOR_INPUT_REPOSITORY_ENV


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
