"""feedback の pending observation、active state、atomic publication を検証する。

agent-facing reporter から raw store、intake wave、remediation、current pointer、cleanup
までを同じ repository fixture で追跡する。publication 後に compact active state だけが
残ることを外部境界として検証する。

対応する oracle file:

- `{{work-root}}/oracle/doc/app_spec/feedback_observation.md`
- `{{work-root}}/oracle/doc/app_spec/console_and_file_log.md`
- `{{work-root}}/oracle/doc/app_spec/feedback_state.md`
- `{{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md`
- `{{work-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.json`
- `{{work-root}}/oracle/src/oracle/acp_builder/feedback/remediate_issue.json`
"""

import hashlib
import json
import os
import socket
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any, NoReturn
from unittest.mock import Mock

import oracle.other.path_model as path_model_module
import pytest
from _acp_builder_support import oracle_schema_path
from _cli_support import run_doctor, runner, terminal_primary_report
from _git_support import SESSION_ID, current_branch, make_repo, run_git
from oracle.acp_builder.feedback.normalize_issue import (
    build_feedback_normalize_issue_parameter as _build_canonical_normalize_parameter,
)
from oracle.acp_builder.feedback.remediate_issue import (
    build_feedback_remediate_issue_parameter as _build_canonical_remediate_parameter,
)

import commons.runtime_feedback as feedback_module
import commons.runtime_feedback_history as feedback_history_module
import commons.runtime_feedback_protocol as feedback_protocol_module
import commons.runtime_feedback_reporter as reporter_module
import commons.runtime_feedback_state as feedback_state_module
import commons.runtime_feedback_store as feedback_store_module
import sub_commands.feedback.decision as decision_module
import sub_commands.feedback.remediation as remediation_module
import sub_commands.feedback.report as feedback_report_module
from acp.builder.feedback.normalize_issue import (
    build_feedback_normalize_issue_parameter,
)
from acp.builder.feedback.remediate_issue import (
    build_feedback_remediate_issue_parameter,
)
from basic.acp import AgentCallParameter, FileAccessMode
from cmoc_runtime import CmocError, load_state_for_branch
from commons.runtime_feedback import (
    FeedbackInvocation,
    ReporterAvailabilityError,
    begin_feedback_call,
    start_feedback_invocation,
)
from commons.runtime_feedback_protocol import (
    FEEDBACK_CAPABILITY_ENV,
    FEEDBACK_COLLECTOR_HOST,
    FEEDBACK_COLLECTOR_PORT_ENV,
    FEEDBACK_PROTOCOL_ENV,
    REPORTER_PROTOCOL_VERSION,
)
from commons.runtime_feedback_state import (
    feedback_writer_lock,
    issue_id,
    load_active_state,
    load_report_cut,
    machine_canonical_key,
    validate_feedback_state,
    validate_observation_envelope,
)
from commons.runtime_feedback_store import (
    FeedbackRejected,
    canonical_json_bytes,
    feedback_completion_counts,
    feedback_root,
    iter_observation_paths,
    observation_path,
    read_json_object,
    reporter_input_schema,
    rfc3339_now,
    sha256_bytes,
    store_agent_observation,
    store_machine_observation,
    validate_agent_payload,
)
from commons.runtime_logging import SubcommandLogger
from main import app


@pytest.fixture
def feedback_directory(tmp_path: Path) -> Path:
    """Git を参照しない保存・path・lock 検査には通常 directory だけを用意する。"""
    root = tmp_path / "repo"
    root.mkdir()
    return root


@pytest.fixture
def feedback_prompt_directory(
    feedback_directory: Path, monkeypatch: pytest.MonkeyPatch
) -> Path:
    """prompt 検査では Git 探索結果だけを置換し、builder と renderer を実行する。"""

    # 実 Git metadata の解決は test_basic_runtime.py と feedback wave 統合 test に残す。
    def resolve_worktree_roots(agent_call_cwd: Path) -> tuple[Path, Path]:
        assert agent_call_cwd == feedback_directory.resolve()
        return agent_call_cwd, agent_call_cwd

    monkeypatch.setattr(
        path_model_module, "_resolve_git_worktree_roots", resolve_worktree_roots
    )
    return feedback_directory


def _payload(
    *,
    text: str = "README の内容から反復する問題を確認した。",
    kind: str = "file",
    path: str | None = "README.md",
) -> dict[str, object]:
    """正本 reporter schema に適合する最小 payload を返す。"""
    evidence: dict[str, object] = {"kind": kind, "text": text}
    if path is not None:
        evidence["path"] = path
    return {
        "schema_version": 2,
        "category": "tooling",
        "severity": "moderate",
        "summary": "反復する feedback test issue",
        "impact": "同じ作業を再実行する必要がある。",
        "workload_limitation": "tooling の設定確認が必要である。",
        "cause": {"certainty": "suspected", "description": "設定差の可能性がある。"},
        "evidence": [evidence],
        "continuation": "continued",
    }


def _context(
    root: Path,
    *,
    session_id: str | None = None,
    head_commit: str | None = None,
) -> dict[str, object]:
    """collector が付与する version 1 context と同形の fixture を返す。"""
    return {
        "repo_root": str(root.resolve()),
        "work_root": str(root.resolve()),
        "head_commit": head_commit
        if head_commit is not None
        else run_git(root, "rev-parse", "HEAD").stdout.strip(),
        "cmoc_session_id": session_id,
        "run_id": None,
        "run_kind": None,
        "subcommand": "feedback test",
        "subcommand_invocation_id": "exec_000000_2026-09-29_15-04",
        "agent_call_id": "ac_000002_2026-09-29_15-04",
        "agent_call_kind": "build_feedback_test_parameter",
        "codex_call_id": "cc_000002_2026-09-29_15-04",
        "codex_session_id": None,
        "log_paths": [
            str(
                (
                    root / ".cmoc/gu/log/sub_command/exec_000000_2026-09-29_15-04.jsonl"
                ).resolve()
            )
        ],
    }


@pytest.fixture
def stored_feedback_context(feedback_directory: Path) -> dict[str, object]:
    """保存検査には、collector 確定済みの context と実 evidence file を渡す。"""
    # HEAD の取得は collector test、Git lifecycle は CLI test で検証する。
    (feedback_directory / "README.md").write_text("# repo\n")
    return _context(feedback_directory, head_commit="a" * 40)


@pytest.fixture
def collector_directory(
    feedback_directory: Path,
    stored_feedback_context: dict[str, object],
    monkeypatch: pytest.MonkeyPatch,
) -> Path:
    """transport・保存・call lifecycle の検査には Git 読み取り結果だけを渡す。"""
    # 実 Git の context 取得は context/rate test と linked worktree の wave test で検証する。
    monkeypatch.setattr(feedback_module, "current_branch", lambda _root: "main")
    monkeypatch.setattr(
        feedback_module,
        "head_commit",
        lambda _root: stored_feedback_context["head_commit"],
    )
    return feedback_directory


def _submit_to_feedback_collector(
    port: int,
    capability: str,
    payload: object,
) -> dict[str, object]:
    """実 TCP transport で capability 付き request を送信する。"""
    request = {
        "protocol": REPORTER_PROTOCOL_VERSION,
        "capability": capability,
        "payload": payload,
    }
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
        connection.settimeout(5)
        connection.connect((FEEDBACK_COLLECTOR_HOST, port))
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
    result = json.loads(response.split(b"\n", 1)[0])
    assert isinstance(result, dict)
    return result


def _active_session(root: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    """doctor 済み repository を active session の ready 状態にする。"""
    monkeypatch.chdir(root)
    run_doctor(root)
    result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    branch = current_branch(root)
    assert branch.startswith("cmoc/session/")
    return branch.removeprefix("cmoc/session/")


def _remediation_output(
    candidate_id: str, verdict: str, *, reference_path: str = "README.md"
) -> dict[str, object]:
    """README current reference を根拠にする正式な remediation output を返す。"""
    if verdict == "inconclusive":
        evidence: list[dict[str, str]] = []
    else:
        evidence = [
            {
                "path": reference_path,
                "location": f"{reference_path}:1",
                "finding": "report cut で現在状態を確認した。",
            }
        ]
    return {
        "result": {
            "issue_id": candidate_id,
            "status": verdict,
            "changed_paths": [],
            "verification": [
                {"method": "inspection", "status": "passed", "summary": "確認済み"}
            ],
            "current_evidence": evidence,
            "human_action": "README の設定を修正する。"
            if verdict == "human_required"
            else None,
            "reason": "固定済み README 参照から現在状態を判定した。",
        }
    }


def _fake_result(root: Path, output: dict[str, object]) -> SimpleNamespace:
    directory = root / ".cmoc/gu/log/feedback_test"
    directory.mkdir(parents=True, exist_ok=True)
    log = directory / f"call-{len(list(directory.iterdir()))}.json"
    log.write_text(json.dumps(output, ensure_ascii=False))
    return SimpleNamespace(output_json=output, returncode=0, call_log_path=log)


def _install_codex_outputs(
    monkeypatch: pytest.MonkeyPatch, *outputs: dict[str, object]
) -> None:
    """feedback 専用 Codex call の正式 output を呼出順で返す。"""
    remaining = iter(outputs)

    def fake_run_codex_exec(*_args: object, **_kwargs: object) -> SimpleNamespace:
        return _fake_result(Path.cwd(), next(remaining))

    monkeypatch.setattr(feedback_report_module, "run_codex_exec", fake_run_codex_exec)


def _store_agent_issue(root: Path, session_id: str) -> tuple[str, Path, str]:
    """README を evidence とする agent observation と issue ID を返す。"""
    accepted, raw_path = store_agent_observation(
        root,
        _context(root, session_id=session_id),
        _payload(),
    )
    observation_id = str(accepted["observation_id"])
    return observation_id, raw_path, issue_id(f"agent\0{observation_id}")


def _assert_hash_verified_state_snapshot(root, state, path, monkeypatch):
    """一度読んだ artifact の hash と内容を使い、次回は改変を検出する。"""
    original_read = Path.read_bytes
    original_content = original_read(path)
    reads = []

    def replace_after_read(target):
        content = original_read(target)
        if target == path:
            reads.append(target)
            target.write_bytes(b"{}\n")
        return content

    try:
        with monkeypatch.context() as snapshot_patch:
            snapshot_patch.setattr(Path, "read_bytes", replace_after_read)
            assert load_active_state(root) == state
            assert reads == [path]
            with pytest.raises(CmocError, match="SHA256"):
                load_active_state(root)
            assert reads == [path, path]
    finally:
        path.write_bytes(original_content)


def test_reporter_exposes_only_canonical_submission_tool(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """stdio MCP discovery と collector 転送を一つの agent-facing tool に限定する。"""
    listed = reporter_module._response(
        {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
    )
    assert listed is not None
    assert listed["result"]["tools"] == [
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
    sent: list[bytes] = []
    connected: list[tuple[str, int]] = []

    class FakeSocket:
        def __enter__(self) -> "FakeSocket":
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def settimeout(self, _seconds: int) -> None:
            return None

        def connect(self, address: tuple[str, int]) -> None:
            connected.append(address)

        def sendall(self, value: bytes) -> None:
            sent.append(value)

        def recv(self, _size: int) -> bytes:
            return b'{"status":"accepted","observation_id":"fbo_000001_2026-08-01_00-00","redaction_count":0}\n'

    monkeypatch.setattr(reporter_module.socket, "socket", lambda *_args: FakeSocket())
    monkeypatch.setenv(FEEDBACK_COLLECTOR_PORT_ENV, "43210")
    monkeypatch.setenv(FEEDBACK_CAPABILITY_ENV, "secret-capability")
    monkeypatch.setenv(FEEDBACK_PROTOCOL_ENV, "1")

    result = reporter_module._submit(_payload())

    assert result["status"] == "accepted"
    request = json.loads(sent[0])
    assert connected == [(FEEDBACK_COLLECTOR_HOST, 43210)]
    assert request["capability"] == "secret-capability"
    assert request["payload"] == _payload()


def test_reporter_discovery_supports_editable_namespace_package(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """editable namespace package でも discovery に正本 schema を渡す。"""
    expected_schema = reporter_input_schema()
    original_files = feedback_protocol_module.resources.files

    def raise_namespace_resource_error(package: str):
        if package == "oracle.feedback":
            raise NotADirectoryError(package)
        return original_files(package)

    monkeypatch.setattr(
        feedback_protocol_module.resources, "files", raise_namespace_resource_error
    )
    feedback_protocol_module.load_reporter_input_schema.cache_clear()
    try:
        response = reporter_module._response(
            {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
        )
        assert response is not None
        assert response["result"]["tools"][0]["inputSchema"] == expected_schema
    finally:
        feedback_protocol_module.load_reporter_input_schema.cache_clear()


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
def test_reporter_rejects_invalid_jsonrpc_request(
    message: dict[str, object],
) -> None:
    """JSON-RPC 2.0 の request 形状を満たさない入力を実行しない。"""
    assert reporter_module._response(message) == {
        "jsonrpc": "2.0",
        "id": None,
        "error": {"code": -32600, "message": "Invalid Request"},
    }


@pytest.mark.parametrize(
    "message",
    [
        {"jsonrpc": "1.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "method": 1},
        {"jsonrpc": "2.0", "method": "notifications/initialized", "params": []},
    ],
)
def test_reporter_does_not_reply_to_invalid_notifications(
    message: dict[str, object],
) -> None:
    """不正な Request 形状の notification にも response を返さない。"""
    assert reporter_module._response(message) is None


@pytest.mark.parametrize("requested", ["2024-11-05", "future-version"])
def test_reporter_negotiates_only_supported_mcp_protocol_version(
    requested: str,
) -> None:
    """未対応の MCP protocol version をそのまま採用しない。"""
    response = reporter_module._response(
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


def test_reporter_requires_initialize_parameters() -> None:
    """initialize の必須 parameter 欠落を method error にする。"""
    response = reporter_module._response(
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
    )
    assert response == {
        "jsonrpc": "2.0",
        "id": 1,
        "error": {"code": -32602, "message": "Invalid params"},
    }


def test_reporter_strips_unexpected_collector_result_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """collector response の余分な field を agent-facing result へ転送しない。"""

    class FakeSocket:
        def __enter__(self) -> "FakeSocket":
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def settimeout(self, _seconds: int) -> None:
            return None

        def connect(self, _address: tuple[str, int]) -> None:
            return None

        def sendall(self, _value: bytes) -> None:
            return None

        def recv(self, _size: int) -> bytes:
            return (
                b'{"status":"rejected","code":"schema_invalid",'
                b'"message":"invalid","retryable":false,'
                b'"secret":"must-not-be-forwarded"}\n'
            )

    monkeypatch.setattr(reporter_module.socket, "socket", lambda *_args: FakeSocket())
    monkeypatch.setenv(FEEDBACK_COLLECTOR_PORT_ENV, "43210")
    monkeypatch.setenv(FEEDBACK_CAPABILITY_ENV, "secret-capability")
    monkeypatch.setenv(FEEDBACK_PROTOCOL_ENV, "1")

    assert reporter_module._submit(_payload()) == {
        "status": "rejected",
        "code": "schema_invalid",
        "message": "invalid",
        "retryable": False,
    }


def test_reporter_escapes_surrogates_on_stdio_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """collector result に不正な Unicode があっても stdio framing を壊さない。"""

    class Utf8Stdout:
        def __init__(self) -> None:
            self.writes: list[bytes] = []

        def write(self, value: str) -> int:
            encoded = value.encode("utf-8")
            self.writes.append(encoded)
            return len(value)

        def flush(self) -> None:
            return None

    stdout = Utf8Stdout()
    monkeypatch.setattr(
        reporter_module,
        "_submit",
        lambda _payload: {
            "status": "rejected",
            "code": "schema_invalid",
            "message": "bad \ud800",
            "retryable": False,
        },
    )
    monkeypatch.setattr(
        reporter_module.sys,
        "stdin",
        [
            '{"jsonrpc":"2.0","id":1,"method":"tools/call",'
            '"params":{"name":"submit_observation","arguments":{}}}\n'
        ],
    )
    monkeypatch.setattr(reporter_module.sys, "stdout", stdout)

    assert reporter_module.main() == 0
    assert b"bad \\ud800" in b"".join(stdout.writes)


def test_reporter_returns_rejection_for_non_utf8_payload_text(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """UTF-8 化できない JSON 文字列も collector の rejected へ到達させる。"""
    sent: list[bytes] = []

    class FakeSocket:
        def __enter__(self) -> "FakeSocket":
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def settimeout(self, _seconds: int) -> None:
            return None

        def connect(self, _address: tuple[str, int]) -> None:
            return None

        def sendall(self, value: bytes) -> None:
            sent.append(value)

        def recv(self, _size: int) -> bytes:
            return (
                b'{"status":"rejected","code":"schema_invalid",'
                b'"message":"payload is not valid UTF-8","retryable":false}\n'
            )

    monkeypatch.setattr(reporter_module.socket, "socket", lambda *_args: FakeSocket())
    monkeypatch.setenv(FEEDBACK_COLLECTOR_PORT_ENV, "43210")
    monkeypatch.setenv(FEEDBACK_CAPABILITY_ENV, "secret-capability")
    monkeypatch.setenv(FEEDBACK_PROTOCOL_ENV, "1")

    result = reporter_module._submit(_payload(text="\ud800"))

    assert result["status"] == "rejected"
    assert json.loads(sent[0])["payload"]["evidence"][0]["text"] == "\ud800"


@pytest.mark.parametrize(
    "collector_port",
    [None, "", "0", "65536", "000080", "not-a-port", " 123", "+123", "１２３"],
)
def test_reporter_rejects_malformed_collector_port(
    monkeypatch: pytest.MonkeyPatch, collector_port: str | None
) -> None:
    """範囲外または不正な port へ接続せず unavailable result を返す。"""
    if collector_port is None:
        monkeypatch.delenv(FEEDBACK_COLLECTOR_PORT_ENV, raising=False)
    else:
        monkeypatch.setenv(FEEDBACK_COLLECTOR_PORT_ENV, collector_port)
    monkeypatch.setenv(FEEDBACK_CAPABILITY_ENV, "secret-capability")
    monkeypatch.setenv(FEEDBACK_PROTOCOL_ENV, "1")
    monkeypatch.setattr(
        reporter_module.socket,
        "socket",
        lambda *_args: pytest.fail("invalid collector port reached socket creation"),
    )

    assert reporter_module._submit(_payload()) == {
        "status": "rejected",
        "code": "collector_unavailable",
        "message": "feedback collector context is unavailable",
        "retryable": True,
    }


def test_reporter_availability_probe_checks_stdio_process_and_collector(
    feedback_directory, monkeypatch, real_stdio_reporter_probe
) -> None:
    """実 stdio process と TCP collector の事前検証が raw を保存せず成功する。"""
    # 子 process も現在の worktree の実装を読み、利用者の HOME は使わない。
    root = feedback_directory
    source_root = Path(__file__).parents[1]
    monkeypatch.setenv("HOME", str(root))
    monkeypatch.setenv(
        "PYTHONPATH",
        os.pathsep.join(str(source_root / path) for path in ("src", "oracle/src")),
    )
    probed_roots: list[Path] = []

    def check_stdio(schema, reporter_cwd):
        real_stdio_reporter_probe(schema, reporter_cwd)
        probed_roots.append(reporter_cwd)

    monkeypatch.setattr(feedback_module, "_validate_stdio_reporter", check_stdio)
    logger = SubcommandLogger(root, "feedback test")
    invocation, token = start_feedback_invocation(root, root, "feedback test", logger)
    try:
        assert invocation is not None
        feedback_module.validate_feedback_reporter_availability()
        assert root in probed_roots
        assert logger.warning_messages == []
        assert iter_observation_paths(root) == []
    finally:
        feedback_module.stop_feedback_invocation(invocation, token)


@pytest.mark.parametrize("schema", [[], {"type": "invalid"}])
def test_reporter_availability_rejects_invalid_input_schema(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, schema: object
) -> None:
    """読み取りと discovery を分離しても doctor は不正な schema を検出する。"""
    (tmp_path / "reporter_input.json").write_text(json.dumps(schema), encoding="utf-8")
    monkeypatch.setattr(
        feedback_protocol_module.resources, "files", lambda _pkg: tmp_path
    )
    feedback_protocol_module.load_reporter_input_schema.cache_clear()
    feedback_store_module.reporter_input_schema.cache_clear()
    try:
        with pytest.raises(
            ReporterAvailabilityError, match="schema is invalid"
        ) as error:
            feedback_module.validate_feedback_reporter_availability()
        assert error.value.component == "reporter"
        assert error.value.failure_code == "version_mismatch"
    finally:
        feedback_protocol_module.load_reporter_input_schema.cache_clear()
        feedback_store_module.reporter_input_schema.cache_clear()


def test_reporter_probe_rejects_non_object_mcp_response(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, real_stdio_reporter_probe
) -> None:
    """不正な JSON object 形状を reporter protocol error として扱う。"""
    monkeypatch.setattr(
        feedback_module.subprocess,
        "run",
        lambda *_args, **_kwargs: SimpleNamespace(
            returncode=0,
            stdout="[1]\n",
            stderr="",
        ),
    )

    with pytest.raises(ReporterAvailabilityError, match="invalid MCP data") as error:
        real_stdio_reporter_probe({}, tmp_path)

    assert error.value.component == "reporter"
    assert error.value.failure_code == "protocol_error"


@pytest.mark.parametrize(
    "response",
    [
        b'{"status":"accepted"}\n',
        b'{"status":"accepted","observation_id":"invalid-observation-id","redaction_count":0}\n',
        b'{"status":"rejected","code":"schema_invalid","message":"invalid","retryable":true}\n',
        b'{"status":"rejected","code":[],"message":"invalid","retryable":false}\n',
    ],
)
def test_reporter_rejects_invalid_collector_result(
    monkeypatch: pytest.MonkeyPatch, response: bytes
) -> None:
    """collector の不正な domain result を MCP result として転送しない。"""

    class FakeSocket:
        def __enter__(self) -> "FakeSocket":
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def settimeout(self, _seconds: int) -> None:
            return None

        def connect(self, _address: tuple[str, int]) -> None:
            return None

        def sendall(self, _value: bytes) -> None:
            return None

        def recv(self, _size: int) -> bytes:
            return response

    monkeypatch.setattr(reporter_module.socket, "socket", lambda *_args: FakeSocket())
    monkeypatch.setenv(FEEDBACK_COLLECTOR_PORT_ENV, "43210")
    monkeypatch.setenv(FEEDBACK_CAPABILITY_ENV, "secret-capability")
    monkeypatch.setenv(FEEDBACK_PROTOCOL_ENV, "1")

    assert reporter_module._submit(_payload()) == {
        "status": "rejected",
        "code": "protocol_mismatch",
        "message": "invalid collector response",
        "retryable": False,
    }


def test_feedback_normalize_builder_protects_nested_code_fences(
    feedback_prompt_directory: Path,
) -> None:
    """normalization の動的 JSON が prompt section の境界を閉じないことを検証する。"""
    root = feedback_prompt_directory
    nested = "before\n```\ninside\n```\nafter"
    observation_json = json.dumps({"payload": {"summary": nested}})
    candidate_json = json.dumps(
        [{"candidate_id": "fbi_" + "a" * 26, "summary": nested}]
    )

    parameter = build_feedback_normalize_issue_parameter(
        observation_json,
        candidate_json,
        root,
    )

    observation_start = parameter.prompt.index("# 構造化済み observation")
    observation_end = parameter.prompt.index(
        "\n\n# 既存 issue candidate", observation_start
    )
    candidate_start = observation_end + 2
    candidate_end = parameter.prompt.index(
        "\n\n# place holder definition", candidate_start
    )
    observation_section = parameter.prompt[observation_start:observation_end]
    candidate_section = parameter.prompt[candidate_start:candidate_end]
    assert observation_section.startswith("# 構造化済み observation\n\n````json\n")
    assert observation_section.endswith("\n````")
    assert candidate_section.startswith("# 既存 issue candidate\n\n````json\n")
    assert candidate_section.endswith("\n````")
    assert observation_json in observation_section
    assert candidate_json in candidate_section


def test_feedback_normalization_excludes_candidate_search_hint(
    feedback_prompt_directory: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """候補検索専用 hint を normalization agent の入力へ渡さない。"""
    root = feedback_prompt_directory
    observation_id = "fbo_000001_2026-08-01_00-00"
    candidate_id = "fbi_" + "a" * 26
    observation = {
        "observation_id": observation_id,
        "payload": {
            "schema_version": 2,
            "category": "tooling",
            "summary": "同一性判断の入力",
            "impact": "候補検索用の hint を含む。",
            "deduplication_hint": "候補検索だけに使う文字列",
            "evidence": [{"kind": "file", "path": "README.md"}],
        },
    }
    candidate = {
        "candidate_id": candidate_id,
        "origin": "agent_report",
        "category": "tooling",
        "summary": "既存候補",
        "impact": "既存候補の影響",
        "representative_evidence": [],
        "reference_targets": [],
        "latest_fingerprints": [],
    }
    captured_prompts: list[str] = []

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **_kwargs: object
    ) -> SimpleNamespace:
        assert parameter.agent_call_cwd == root
        assert parameter.file_access_mode == FileAccessMode.READONLY
        assert parameter.enable_document_search_mcp is True
        assert "# routing policy" in parameter.prompt
        assert "# oracle and realization basic" in parameter.prompt
        captured_prompts.append(parameter.prompt)
        return SimpleNamespace(
            output_json={"result": {"decision": "new", "existing_issue_id": None}}
        )

    monkeypatch.setattr(feedback_report_module, "run_codex_exec", fake_run_codex_exec)
    monkeypatch.setattr(
        feedback_report_module,
        "_record_checkpoint",
        lambda *_args, **_kwargs: None,
    )

    manifest = {
        "report_cut_id": "fbc_00000000-0000-7000-8000-000000000001",
        "inputs": {"versions": {"normalization_builder": "0" * 64}},
        "processing": {"normalization_checkpoints": []},
    }

    assert (
        feedback_report_module._normalize_issue_identity(
            root, root, manifest, observation, [candidate]
        )
        is None
    )
    assert len(captured_prompts) == 1
    assert "deduplication_hint" not in captured_prompts[0]
    assert "候補検索だけに使う文字列" not in captured_prompts[0]


def test_feedback_issue_builders_disable_reporting(
    feedback_prompt_directory: Path,
) -> None:
    """normalization と remediation は同じ追加報告を prompt から外す。"""
    root = feedback_prompt_directory
    parameters = (
        build_feedback_normalize_issue_parameter("{}", "[]", root),
        build_feedback_remediate_issue_parameter(
            json.dumps({"issue_id": "fbi_" + "a" * 26}),
            root,
        ),
    )

    assert all(not parameter.enable_feedback_reporting for parameter in parameters)
    assert all(
        "cmoc_feedback.submit_observation" not in parameter.prompt
        for parameter in parameters
    )


def test_feedback_processing_versions_hash_canonical_builders() -> None:
    """checkpoint version は prompt 構築 builder とその依存を識別する。"""
    normalize_path = feedback_report_module._builder_source_path(
        _build_canonical_normalize_parameter
    )
    verify_path = feedback_report_module._builder_source_path(
        _build_canonical_remediate_parameter
    )
    renderer_path = feedback_report_module._builder_source_path(
        feedback_report_module.render_sd_node_as_markdown
    )

    assert (
        build_feedback_normalize_issue_parameter is _build_canonical_normalize_parameter
    )
    assert (
        build_feedback_remediate_issue_parameter is _build_canonical_remediate_parameter
    )
    versions = feedback_report_module._processing_versions()
    normalization_version = feedback_report_module._builder_version_hash(
        normalize_path,
        (renderer_path,),
    )
    assert versions["normalization_builder"] == normalization_version
    verification_version = feedback_report_module._builder_version_hash(
        verify_path,
        (renderer_path,),
    )
    assert versions["remediation_builder"] == verification_version


def test_pending_observations_rejects_symlinked_root(
    tmp_path: Path, feedback_directory: Path
) -> None:
    """symlink 化された raw root を空の初期 state として扱わない。"""
    root = feedback_directory
    observation_parent = feedback_root(root) / "observation"
    observation_parent.mkdir(parents=True)
    (observation_parent / "v1").symlink_to(
        tmp_path / "missing-observations", target_is_directory=True
    )

    with pytest.raises(CmocError, match="observation root"):
        feedback_report_module._pending_observations(root)


@pytest.mark.parametrize("reader", ["pending", "cut"])
def test_raw_observation_reader_uses_one_snapshot(
    feedback_directory, stored_feedback_context, monkeypatch, reader
):
    root = feedback_directory
    accepted, raw = store_agent_observation(root, stored_feedback_context, _payload())
    original = read_json_object(raw)
    content = canonical_json_bytes(original)
    changed = {
        **original,
        "payload": {**original["payload"], "summary": "置換後の観測"},
    }
    entry = {
        "observation_id": accepted["observation_id"],
        "path": raw.relative_to(root).as_posix(),
        "sha256": sha256_bytes(content),
    }
    original_read = Path.read_bytes
    original_inventory = Path.rglob
    reads = []
    inventories = []

    def replace_after_read(path):
        value = original_read(path)
        if path == raw:
            reads.append(path)
            path.write_bytes(canonical_json_bytes(changed))
        return value

    def inventory(path, pattern):
        if path == feedback_root(root) / "observation/v1":
            inventories.append(path)
        return original_inventory(path, pattern)

    def load():
        if reader == "pending":
            entries, observations = feedback_report_module._pending_observations(root)
            assert entries == [entry]
            return observations
        return feedback_report_module._read_cut_observations(
            root, {"inputs": {"observations": [entry]}}
        )

    monkeypatch.setattr(Path, "read_bytes", replace_after_read)
    monkeypatch.setattr(Path, "rglob", inventory)

    # hash・canonical・schema を検査した byte 列を使い、読込後の置換を混ぜない。
    assert load() == {raw.stem: original}
    assert reads == [raw]
    assert len(inventories) == (1 if reader == "pending" else 0)
    if reader == "cut":
        # 同じ参照の次回読込では置換を検出し、呼び出し間の cache は持たない。
        with pytest.raises(CmocError, match="raw observation hash"):
            load()
        assert reads == [raw, raw]
    else:
        entry["sha256"] = sha256_bytes(canonical_json_bytes(changed))
        assert load() == {raw.stem: changed}
        assert reads == [raw, raw]
        assert len(inventories) == 2


@pytest.mark.parametrize("raw_content", [b"not-json\n", b'{"x": NaN}\n'])
def test_pending_observations_rejects_invalid_json(feedback_directory, raw_content):
    # publication の阻止と invocation report は CLI の一ケースで確認する。
    root = feedback_directory
    raw = observation_path(root, "fbo_000099_2026-08-01_00-00", "2030-01-02T00:00:00Z")
    raw.parent.mkdir(parents=True)
    raw.write_bytes(raw_content)

    with pytest.raises(CmocError, match="raw observation validation") as error:
        feedback_report_module._pending_observations(root)
    assert str(raw) in error.value.detail
    assert raw.read_bytes() == raw_content


def test_agent_candidate_comparison_requires_evidence_subject_type() -> None:
    """同じ path でも異なる evidence subject type を同一候補へ絞り込まない。"""
    observation = {
        "context": {"repo_root": "/repo"},
        "payload": {
            "category": "tooling",
            "evidence": [{"kind": "oracle", "path": "README.md"}],
        },
        "evidence_fingerprints": [
            {
                "evidence_index": 0,
                "normalized_path": "/repo/README.md",
                "state": "hashed",
                "sha256": "a" * 64,
            }
        ],
    }
    candidate = {
        "candidate_id": "fbi_" + "b" * 26,
        "category": "tooling",
        "latest_fingerprints": observation["evidence_fingerprints"],
        "reference_targets": [{"path": "README.md", "kind": "file", "location": None}],
        "deduplication_hints": [],
    }

    exact, comparison = feedback_report_module._agent_comparison_candidates(
        observation, {str(candidate["candidate_id"]): candidate}
    )

    assert exact is None
    assert comparison == []


def test_agent_candidate_exact_match_requires_report_cut_fingerprint() -> None:
    """observation 時点と異なる cut fingerprint では exact merge しない。"""
    observation = {
        "observation_id": "fbo_000001_2026-08-01_00-00",
        "context": {"repo_root": "/repo"},
        "payload": {
            "category": "tooling",
            "evidence": [{"kind": "oracle", "path": "README.md"}],
        },
        "evidence_fingerprints": [
            {
                "evidence_index": 0,
                "normalized_path": "/repo/README.md",
                "state": "hashed",
                "sha256": "a" * 64,
            }
        ],
    }
    candidate = {
        "candidate_id": "fbi_" + "b" * 26,
        "category": "tooling",
        "latest_fingerprints": observation["evidence_fingerprints"],
        "reference_targets": [
            {"path": "README.md", "kind": "oracle", "location": None}
        ],
        "deduplication_hints": [],
    }
    manifest = {
        "inputs": {
            "references": [
                {
                    "reference_id": "ref:readme",
                    "kind": "repository_content",
                    "subjects": [observation["observation_id"]],
                    "path": "README.md",
                    "state": "hashed",
                    "sha256": "b" * 64,
                }
            ]
        }
    }

    current_cut = feedback_report_module._report_cut_fingerprint_pairs(
        Path("/repo"), manifest, observation
    )
    exact, comparison = feedback_report_module._agent_comparison_candidates(
        observation,
        {str(candidate["candidate_id"]): candidate},
        current_cut_fingerprint_pairs=current_cut,
    )

    assert exact is None
    assert comparison == [candidate]


def test_issue_id_collision_stops_candidate_building(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """異なる agent canonical key が同じ issue ID になった場合は候補を上書きしない。"""
    observations = {
        observation_id: {
            "observation_id": observation_id,
            "source": "agent_report",
            "observed_at": observed_at,
            "context": {},
            "payload": {
                "category": "tooling",
                "summary": "同じ issue ID を持つ候補",
                "impact": "候補 identity の衝突を検出する。",
                "evidence": [{"kind": "other", "text": observation_id}],
            },
            "evidence_fingerprints": [],
        }
        for observation_id, observed_at in (
            ("fbo_000001_2026-08-01_00-00", "2026-08-01T00:00:00Z"),
            ("fbo_000002_2026-08-01_00-00", "2026-08-02T00:00:00Z"),
        )
    }
    monkeypatch.setattr(
        feedback_report_module, "issue_id", lambda _canonical_key: "fbi_" + "a" * 26
    )

    with pytest.raises(CmocError, match="collision"):
        feedback_report_module._build_candidates(
            tmp_path,
            tmp_path,
            {"inputs": {"references": []}, "cut_at": "2026-08-02T00:00:00Z"},
            observations,
            SimpleNamespace(issues={}, machine_aggregates={}),
        )


def test_merge_observation_keeps_latest_fingerprint_for_older_observation() -> None:
    """遅れて到着した古い observation が latest fingerprint を巻き戻さない。"""
    newer = {
        "observation_id": "fbo_000001_2026-08-02_00-00",
        "source": "agent_report",
        "observed_at": "2026-08-02T00:00:00Z",
        "context": {"cmoc_session_id": SESSION_ID},
        "payload": {
            "category": "tooling",
            "summary": "new",
            "impact": "impact",
            "evidence": [{"kind": "file", "path": "README.md", "text": "new"}],
        },
        "evidence_fingerprints": [
            {
                "evidence_index": 0,
                "normalized_path": "/repo/README.md",
                "state": "hashed",
                "sha256": "b" * 64,
            }
        ],
    }
    older = {
        **newer,
        "observation_id": "fbo_000000_2026-08-01_00-00",
        "observed_at": "2026-08-01T00:00:00Z",
        "payload": {
            **newer["payload"],
            "summary": "old",
            "evidence": [{"kind": "file", "path": "README.md", "text": "old"}],
        },
        "evidence_fingerprints": [
            {
                "evidence_index": 0,
                "normalized_path": "/repo/README.md",
                "state": "hashed",
                "sha256": "a" * 64,
            }
        ],
    }
    candidate = feedback_report_module._new_candidate(
        newer, "agent\0fbo_000001_2026-08-02_00-00"
    )
    feedback_report_module._merge_observation(Path("/repo"), candidate, newer)
    feedback_report_module._merge_observation(Path("/repo"), candidate, older)

    assert candidate["last_observed_at"] == newer["observed_at"]
    assert candidate["latest_fingerprints"] == newer["evidence_fingerprints"]


def test_collector_validates_context_rate_and_durable_observation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """loopback reporter 経由の受理、rate limit、失効を確認する。"""
    root = make_repo(tmp_path)
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    invocation.start()
    try:
        call = invocation.register_call(
            agent_call_id="ac_000005_2026-09-29_15-04",
            agent_call_kind="build_one",
            codex_call_id="cc_000005_2026-09-29_15-04",
            codex_session_id="session_one",
            log_paths=[
                root
                / f".cmoc/gu/log/codex/{logger.execution_id}/cc_000005_2026-09-29_15-04_call.json"
            ],
        )
        assert invocation.collector_port is not None
        assert invocation._listener is not None
        assert invocation._listener.getsockname() == (
            FEEDBACK_COLLECTOR_HOST,
            invocation.collector_port,
        )
        feedback_call = feedback_module.FeedbackCall(invocation, call)
        reporter_environment = feedback_call.subprocess_env({})
        for name, value in reporter_environment.items():
            monkeypatch.setenv(name, value)

        accepted = [reporter_module._submit(_payload()) for _index in range(3)]

        assert all(result["status"] == "accepted" for result in accepted)
        paths = iter_observation_paths(root)
        assert len(paths) == 3
        envelope = read_json_object(paths[0])
        assert validate_observation_envelope(envelope) == []
        assert envelope["context"]["repo_root"] == str(root)
        assert envelope["context"]["work_root"] == str(root)
        assert (
            envelope["context"]["head_commit"]
            == run_git(root, "rev-parse", "HEAD").stdout.strip()
        )
        assert envelope["context"]["subcommand_invocation_id"] == logger.execution_id
        assert envelope["context"]["agent_call_id"] == "ac_000005_2026-09-29_15-04"
        assert reporter_module._submit(_payload())["code"] == "rate_limited"
        feedback_call.close()
        assert reporter_module._submit(_payload())["code"] == "context_invalid"
        invocation.stop()
        assert reporter_module._submit(_payload())["code"] == "collector_unavailable"
    finally:
        invocation.stop()


def test_disabled_feedback_call_does_not_register_capability(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """明示的に無効な call は collector context や capability を作らない。"""

    class Invocation:
        """登録経路へ誤って進んだ場合に失敗する collector double。"""

        def register_call(self, **_kwargs: object) -> object:
            raise AssertionError("disabled feedback call registered a context")

    monkeypatch.setattr(
        feedback_module, "current_feedback_invocation", lambda: Invocation()
    )
    feedback_call = begin_feedback_call(
        agent_call_id="ac_000000_2026-09-29_15-04",
        agent_call_kind="build_disabled",
        codex_call_id="cc_000000_2026-09-29_15-04",
        log_paths=[],
        enable_feedback_reporting=False,
    )

    assert feedback_call.codex_call_id is None
    assert feedback_call.subprocess_env({}) == {}
    feedback_call.close()


def test_collector_stop_wakes_blocked_listener(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """timeout に頼らず接続待ちを解除し、停止を障害として記録しない。"""
    logger = SubcommandLogger(tmp_path, "feedback test")
    invocation = FeedbackInvocation(tmp_path, tmp_path, "feedback test", logger)
    accept_started = threading.Event()
    accepting_sockets: list[socket.socket] = []
    original_accept = socket.socket.accept

    def blocking_accept(listener: socket.socket) -> tuple[socket.socket, object]:
        # 元の FD の close だけでは解除できない接続待ちを、同じ socket に保持する。
        with listener.dup() as accepting_socket:
            accepting_socket.settimeout(None)
            accepting_sockets.append(accepting_socket)
            accept_started.set()
            return original_accept(accepting_socket)

    monkeypatch.setattr(socket.socket, "accept", blocking_accept)
    invocation.start()
    try:
        assert accept_started.wait(timeout=2)
        invocation.stop()

        assert invocation._server_thread is not None
        assert not invocation._server_thread.is_alive()
        assert invocation._listener is None
        assert invocation.collector_port is None
        assert logger.warning_messages == []
    finally:
        # 回帰時にも blocking accept を解除し、test の thread を残さない。
        for accepting_socket in accepting_sockets:
            try:
                accepting_socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
        invocation.stop()


@pytest.mark.parametrize("shutdown_unavailable", [False, True])
def test_collector_protocol_probe_does_not_report_expected_degradation(
    feedback_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
    shutdown_unavailable: bool,
) -> None:
    """transport probe と通常・shutdown 不可の停止で warning を追加しない。"""
    root = feedback_directory
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    if shutdown_unavailable:

        def fail_shutdown(_listener: socket.socket, _how: int) -> None:
            raise OSError("injected shutdown failure")

        monkeypatch.setattr(socket.socket, "shutdown", fail_shutdown)
    invocation.start()
    try:
        assert invocation.collector_port is not None
        feedback_module._validate_collector_protocol(invocation.collector_port)
    finally:
        invocation.stop()
    assert invocation._server_thread is not None
    assert not invocation._server_thread.is_alive()
    assert logger.warning_messages == []


def test_collector_records_rejected_submission_as_degraded_warning(
    collector_directory: Path,
) -> None:
    """collector の rejected result を本命 workload と分離した warning に残す。"""
    root = collector_directory
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    invocation.start()
    try:
        call = invocation.register_call(
            agent_call_id="ac_000009_2026-09-29_15-04",
            agent_call_kind="build_rejected_warning",
            codex_call_id="cc_000010_2026-09-29_15-04",
            log_paths=[],
        )
        assert invocation.collector_port is not None
        rejected = _submit_to_feedback_collector(
            invocation.collector_port,
            call.capability,
            {**_payload(), "summary": ""},
        )

        assert rejected["status"] == "rejected"
        assert rejected["code"] == "schema_invalid"
        assert logger.warning_messages == [
            "feedback submission rejected (schema_invalid)"
        ]
        assert any(
            event.get("event") == "warning"
            and event.get("message") == "feedback submission rejected (schema_invalid)"
            for event in logger.event_records()
        )
        invocation.close_call(call)
    finally:
        invocation.stop()


def test_collector_records_unexpected_listener_failure_as_degraded_warning(
    feedback_directory: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """停止処理以外の listener failure を黙って collector 終了にしない。"""
    root = feedback_directory
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)

    def fail_accept(_listener: socket.socket) -> tuple[socket.socket, object]:
        raise OSError("injected listener failure")

    monkeypatch.setattr(socket.socket, "accept", fail_accept)
    invocation.start()
    try:
        assert invocation._server_thread is not None
        invocation._server_thread.join(timeout=2)
        assert not invocation._server_thread.is_alive()
        assert logger.warning_messages == [
            "feedback submission rejected (transport_unavailable)"
        ]
        assert any(
            event.get("event") == "warning"
            and event.get("message")
            == "feedback submission rejected (transport_unavailable)"
            for event in logger.event_records()
        )
    finally:
        invocation.stop()


def test_collector_handles_response_timeout_failure_as_degraded_warning(
    feedback_directory: Path,
) -> None:
    """response 送信時の timeout 設定失敗を worker 例外へ漏らさない。"""
    root = feedback_directory
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)

    class FailingTimeoutConnection:
        def __enter__(self) -> "FailingTimeoutConnection":
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def settimeout(self, _seconds: float) -> None:
            raise OSError("injected timeout failure")

    invocation._handle_connection(FailingTimeoutConnection())  # type: ignore[arg-type]

    assert logger.warning_messages == [
        "feedback submission rejected (transport_unavailable)"
    ]


def test_collector_accepts_utf8_payload_at_wire_size_over_64_kib(
    collector_directory: Path,
) -> None:
    """UTF-8 payload の制限を JSON ASCII escape の wire size で狭めない。"""
    root = collector_directory
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    invocation.start()
    try:
        call = invocation.register_call(
            agent_call_id="ac_000012_2026-09-29_15-04",
            agent_call_kind="build_utf8_wire_size",
            codex_call_id="cc_000014_2026-09-29_15-04",
            log_paths=[],
        )
        assert invocation.collector_port is not None
        payload = {
            **_payload(),
            "evidence": [{"kind": "other", "text": "😀" * 900} for _index in range(8)],
        }
        assert len(canonical_json_bytes(payload)) - 1 <= 32 * 1024
        assert (
            len(
                json.dumps(
                    {
                        "protocol": REPORTER_PROTOCOL_VERSION,
                        "capability": call.capability,
                        "payload": payload,
                    },
                    ensure_ascii=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            )
            > 64 * 1024
        )

        result = _submit_to_feedback_collector(
            invocation.collector_port, call.capability, payload
        )
        assert result["status"] == "accepted"
        invocation.close_call(call)
    finally:
        invocation.stop()


def test_collector_rejects_surrogate_payload_with_protocol_safe_response(
    collector_directory: Path,
) -> None:
    """不正な Unicode payload の rejected result を response として返せる。"""
    root = collector_directory
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    invocation.start()
    try:
        call = invocation.register_call(
            agent_call_id="ac_000010_2026-09-29_15-04",
            agent_call_kind="build_surrogate_response",
            codex_call_id="cc_000012_2026-09-29_15-04",
            log_paths=[],
        )
        assert invocation.collector_port is not None
        result = _submit_to_feedback_collector(
            invocation.collector_port,
            call.capability,
            {**_payload(), "summary": "bad \ud800"},
        )
        assert result == {
            "status": "rejected",
            "code": "schema_invalid",
            "message": "payload must be valid UTF-8 JSON",
            "retryable": False,
        }
        invocation.close_call(call)
    finally:
        invocation.stop()


@pytest.mark.parametrize("stop_invocation", [False, True], ids=["call", "invocation"])
def test_feedback_shutdown_drains_accepted_tcp_request(
    collector_directory: Path, monkeypatch: pytest.MonkeyPatch, stop_invocation: bool
) -> None:
    """call 終了と collector 停止は、受付済み request の保存後にだけ完了する。"""
    root = collector_directory
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    storage_started = threading.Event()
    release_storage = threading.Event()
    close_started = threading.Event()
    close_finished = threading.Event()
    submission_result: dict[str, object] = {}
    submission_errors: list[BaseException] = []
    close_errors: list[BaseException] = []
    submission_thread: threading.Thread | None = None
    close_thread: threading.Thread | None = None
    original_store = feedback_module.store_agent_observation

    def blocking_store(
        repo: Path,
        context: dict[str, Any],
        payload: object,
    ) -> tuple[dict[str, object], Path]:
        """close 中も accepted request を保存途中に留める。"""
        storage_started.set()
        if not release_storage.wait(timeout=5):
            raise RuntimeError("test did not release feedback storage")
        return original_store(repo, context, payload)

    monkeypatch.setattr(feedback_module, "store_agent_observation", blocking_store)
    invocation.start()
    try:
        call = invocation.register_call(
            agent_call_id="ac_000001_2026-09-29_15-04",
            agent_call_kind="build_drain",
            codex_call_id="cc_000001_2026-09-29_15-04",
            log_paths=[],
        )
        assert invocation.collector_port is not None

        def submit() -> None:
            """実 transport の結果または例外を親 thread へ渡す。"""
            try:
                submission_result.update(
                    _submit_to_feedback_collector(
                        invocation.collector_port,
                        call.capability,
                        _payload(),
                    )
                )
            except BaseException as exc:
                submission_errors.append(exc)

        def close_context() -> None:
            """call 終了または invocation 停止の完了を親 thread へ通知する。"""
            close_started.set()
            try:
                if stop_invocation:
                    invocation.stop()
                else:
                    invocation.close_call(call)
            except BaseException as exc:
                close_errors.append(exc)
            finally:
                close_finished.set()

        submission_thread = threading.Thread(target=submit)
        submission_thread.start()
        assert storage_started.wait(timeout=2)
        close_thread = threading.Thread(target=close_context)
        close_thread.start()
        assert close_started.wait(timeout=2)
        assert not close_finished.wait(timeout=0.05)

        release_storage.set()
        submission_thread.join(timeout=5)
        close_thread.join(timeout=5)

        assert not submission_thread.is_alive()
        assert not close_thread.is_alive()
        assert submission_errors == []
        assert close_errors == []
        assert submission_result["status"] == "accepted"
        assert len(iter_observation_paths(root)) == 1
        if stop_invocation:
            assert invocation.collector_port is None
            assert call.capability not in invocation._calls
            assert invocation._server_thread is not None
            assert not invocation._server_thread.is_alive()
            assert not invocation._worker_threads
        else:
            rejected = _submit_to_feedback_collector(
                invocation.collector_port,
                call.capability,
                _payload(),
            )
            assert rejected["code"] == "context_invalid"
    finally:
        release_storage.set()
        if submission_thread is not None:
            submission_thread.join(timeout=5)
        if close_thread is not None:
            close_thread.join(timeout=5)
        invocation.stop()


def test_parallel_feedback_call_lifecycles_are_isolated(
    collector_directory: Path,
) -> None:
    """並行 call の片方を閉じても他方の request を継続受理する。"""
    root = collector_directory
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    invocation.start()
    try:
        first = invocation.register_call(
            agent_call_id="ac_000006_2026-09-29_15-04",
            agent_call_kind="build_parallel_one",
            codex_call_id="cc_000006_2026-09-29_15-04",
            log_paths=[],
        )
        second = invocation.register_call(
            agent_call_id="ac_000007_2026-09-29_15-04",
            agent_call_kind="build_parallel_two",
            codex_call_id="cc_000007_2026-09-29_15-04",
            log_paths=[],
        )
        assert invocation.collector_port is not None
        start_submissions = threading.Event()
        results: dict[str, dict[str, object] | BaseException] = {}

        def submit(label: str, capability: str) -> None:
            """二つの capability を同時に実 TCP collector へ送る。"""
            start_submissions.wait(timeout=2)
            try:
                results[label] = _submit_to_feedback_collector(
                    invocation.collector_port,
                    capability,
                    _payload(text=f"{label} call の observation"),
                )
            except BaseException as exc:
                results[label] = exc

        threads = [
            threading.Thread(target=submit, args=("first", first.capability)),
            threading.Thread(target=submit, args=("second", second.capability)),
        ]
        for thread in threads:
            thread.start()
        start_submissions.set()
        for thread in threads:
            thread.join(timeout=5)

        assert all(not thread.is_alive() for thread in threads)
        first_result = results.get("first")
        second_result = results.get("second")
        assert isinstance(first_result, dict)
        assert isinstance(second_result, dict)
        assert first_result["status"] == "accepted"
        assert second_result["status"] == "accepted"

        invocation.close_call(first)
        first_rejected = _submit_to_feedback_collector(
            invocation.collector_port,
            first.capability,
            _payload(),
        )
        second_accepted = _submit_to_feedback_collector(
            invocation.collector_port,
            second.capability,
            _payload(text="second call remains active"),
        )

        assert first_rejected["code"] == "context_invalid"
        assert second_accepted["status"] == "accepted"
        paths = iter_observation_paths(root)
        assert len(paths) == 3
        contexts = {
            read_json_object(path)["context"]["agent_call_id"] for path in paths
        }
        assert contexts == {"ac_000006_2026-09-29_15-04", "ac_000007_2026-09-29_15-04"}
        invocation.close_call(second)
    finally:
        invocation.stop()


def test_collector_limits_unauthenticated_request_read_time(
    feedback_directory: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """改行前で停止した未認証接続を短い絶対 deadline で終了する。"""
    root = feedback_directory
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    monkeypatch.setattr(feedback_module, "_COLLECTOR_IO_TIMEOUT_SECONDS", 0.05)
    invocation.start()
    try:
        assert invocation.collector_port is not None
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(1)
            connection.connect((FEEDBACK_COLLECTOR_HOST, invocation.collector_port))
            connection.sendall(b"{")
            response = json.loads(connection.recv(8192).split(b"\n", 1)[0])

        assert response["code"] == "transport_unavailable"
    finally:
        invocation.stop()


def test_collector_rejects_observation_without_current_head(
    feedback_directory: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """current HEAD を取得できない場合は invalid context を保存しない。"""
    root = feedback_directory
    logger = SubcommandLogger(root, "feedback test")

    def fail_head_commit(_root: Path) -> str:
        """collector context の HEAD 取得失敗を再現する。"""
        raise RuntimeError("git is unavailable")

    monkeypatch.setattr(feedback_module, "head_commit", fail_head_commit)
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    call = invocation.register_call(
        agent_call_id="ac_000003_2026-09-29_15-04",
        agent_call_kind="build_head_failure",
        codex_call_id="cc_000003_2026-09-29_15-04",
        log_paths=[],
    )

    with pytest.raises(FeedbackRejected) as error:
        invocation._submit_request(
            {"protocol": "1", "capability": call.capability, "payload": _payload()}
        )

    assert error.value.code == "context_invalid"
    assert iter_observation_paths(root) == []
    invocation.close_call(call)


def test_feedback_degradation_preserves_keyboard_interrupt(
    feedback_directory: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """collector の degraded fallback はユーザー中断を握り潰さない。"""
    root = feedback_directory
    logger = SubcommandLogger(root, "feedback test")

    def interrupt_start(_self: FeedbackInvocation) -> None:
        """collector 起動中のユーザー中断を再現する。"""
        raise KeyboardInterrupt()

    original_start = FeedbackInvocation.start
    monkeypatch.setattr(FeedbackInvocation, "start", interrupt_start)
    with pytest.raises(KeyboardInterrupt):
        start_feedback_invocation(root, root, "feedback test", logger)
    monkeypatch.setattr(FeedbackInvocation, "start", original_start)

    class InterruptingInvocation:
        """call context 登録を中断する collector double。"""

        def register_call(self, **_kwargs: object) -> object:
            """call context 登録中のユーザー中断を再現する。"""
            raise KeyboardInterrupt()

    invocation = InterruptingInvocation()
    monkeypatch.setattr(
        feedback_module, "current_feedback_invocation", lambda: invocation
    )

    with pytest.raises(KeyboardInterrupt):
        begin_feedback_call(
            agent_call_id="ac_000004_2026-09-29_15-04",
            agent_call_kind="build_interrupt",
            codex_call_id="cc_000004_2026-09-29_15-04",
            log_paths=[],
        )


def test_agent_store_rejects_outside_path_and_masks_secret(
    tmp_path: Path, feedback_directory: Path, stored_feedback_context: dict[str, object]
) -> None:
    """repository path boundary と secret masking を raw publication 前に適用する。"""
    root = feedback_directory
    with pytest.raises(FeedbackRejected) as outside:
        store_agent_observation(
            root,
            stored_feedback_context,
            _payload(path=str(tmp_path / "outside.txt")),
        )
    assert outside.value.code == "path_outside_repo"
    with pytest.raises(FeedbackRejected) as masked_outside:
        store_agent_observation(
            root,
            stored_feedback_context,
            _payload(
                path="Authorization: Bearer abcdefghijklmnopqrstuvwxyz/../../outside.txt"
            ),
        )
    assert masked_outside.value.code == "path_outside_repo"

    (root / "loop").symlink_to("loop")
    with pytest.raises(FeedbackRejected) as malformed:
        store_agent_observation(root, stored_feedback_context, _payload(path="loop"))
    assert malformed.value.code == "path_outside_repo"

    outside = tmp_path / "outside"
    outside.mkdir()
    (root / "outside-link").symlink_to(outside, target_is_directory=True)
    with pytest.raises(FeedbackRejected) as missing_outside:
        store_agent_observation(
            root, stored_feedback_context, _payload(path="outside-link/missing.txt")
        )
    assert missing_outside.value.code == "path_outside_repo"

    redacted = _payload(
        text="request failed before Authorization: Bearer abcdefghijklmnopqrstuvwxyz",
        kind="error",
        path=None,
    )
    result, path = store_agent_observation(root, stored_feedback_context, redacted)

    assert result["redaction_count"] == 1
    assert "[REDACTED:authorization]" in path.read_text()
    assert "abcdefghijklmnopqrstuvwxyz" not in path.read_text()


def test_report_reference_rejects_symlinked_parent_outside(
    tmp_path: Path, feedback_directory: Path
) -> None:
    """report cut reference が symlink 親経由の repository 外 path を読まない。"""
    root = feedback_directory
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_text("SECRET\n")
    (root / "link").symlink_to(outside, target_is_directory=True)

    assert feedback_report_module._repository_path(root, "link/secret.txt") is None


def test_report_reference_targets_use_resolved_evidence_path(
    feedback_directory: Path, stored_feedback_context: dict[str, object]
) -> None:
    """同じ file への symlink alias と実体 path を同じ issue subject にする。"""
    root = feedback_directory
    target_directory = root / "nested"
    target_directory.mkdir()
    target = target_directory / "README.md"
    target.write_text("subject\n")
    (root / "alias").symlink_to(target_directory, target_is_directory=True)

    _, first_path = store_agent_observation(
        root, stored_feedback_context, _payload(path="alias/README.md")
    )
    first = read_json_object(first_path)
    candidate = feedback_report_module._new_candidate(
        first, f"agent\0{first['observation_id']}"
    )
    feedback_report_module._merge_observation(root, candidate, first)

    _, second_path = store_agent_observation(
        root, stored_feedback_context, _payload(path="nested/README.md")
    )
    second = read_json_object(second_path)
    fingerprint = second["evidence_fingerprints"][0]
    exact, comparison = feedback_report_module._agent_comparison_candidates(
        second,
        {candidate["candidate_id"]: candidate},
        current_cut_fingerprint_pairs=[
            (fingerprint["normalized_path"], "hashed", fingerprint["sha256"])
        ],
    )

    assert exact is candidate
    assert comparison == [candidate]


def test_report_reference_masks_secret_across_content_limit(
    feedback_directory: Path,
) -> None:
    """capture 上限をまたぐ private key block の断片を保存しない。"""
    root = feedback_directory
    path = root / "secret.txt"
    private_key = (
        "-----BEGIN PRIVATE KEY-----\n" + "A" * 256 + "\n-----END PRIVATE KEY-----"
    )
    path.write_text(
        "x"
        * (
            feedback_report_module._REFERENCE_CONTENT_LIMIT
            - len("[REDACTED:private_key]")
            - 10
        )
        + private_key
    )

    reference = feedback_report_module._capture_repository_reference(
        root, path, ["subject"]
    )

    assert reference["kind"] == "repository_content"
    assert reference["truncated"] is True
    assert "[REDACTED:private_key]" in reference["content"]
    assert "A" * 50 not in reference["content"]


def test_machine_detector_observation_id_is_idempotent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """対象 event でだけ context を取得し、再検出を同じ raw 一件へ収束させる。"""
    root = make_repo(tmp_path)
    logger = SubcommandLogger(root, "feedback test")
    original_head = feedback_module.head_commit
    branch_query = Mock(wraps=feedback_module.current_branch)
    head_query = Mock(wraps=original_head)
    monkeypatch.setattr(feedback_module, "current_branch", branch_query)
    monkeypatch.setattr(feedback_module, "head_commit", head_query)
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    event = {
        "event_schema_version": 1,
        "event_id": "evt_reporter_unavailable",
        "event_type": "feedback.reporter_unavailable",
        "occurred_at": rfc3339_now(),
        "subcommand_invocation_id": logger.execution_id,
        "component": "collector",
        "failure_code": "protocol_error",
    }

    for excluded_fields in (
        {"event_type": "unregistered.event"},
        {"subcommand_invocation_id": "other-invocation"},
        {"component": "unknown"},
    ):
        invocation.detect_event({**event, **excluded_fields}, logger.path)
    FeedbackInvocation(root, root, "feedback report", logger).detect_event(
        event, logger.path
    )
    branch_query.assert_not_called()
    head_query.assert_not_called()

    invocation.detect_event(event, logger.path)
    invocation.detect_event(event, logger.path)

    [path] = iter_observation_paths(root)
    observation = read_json_object(path)
    assert validate_observation_envelope(observation) == []
    assert observation["source_event"]["event_id"] == event["event_id"]
    assert observation["context"]["head_commit"] == original_head(root)
    assert observation["context"]["subcommand_invocation_id"] == logger.execution_id


def test_machine_detector_masks_secret_in_event_fields(tmp_path: Path) -> None:
    """detector payload の追加 field も raw publication 前に secret masking する。"""
    root = make_repo(tmp_path)
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    secret = "Authorization: Bearer abcdefghijklmnopqrstuvwxyz"
    event = {
        "event_schema_version": 1,
        "event_id": "evt_machine_secret",
        "event_type": "feedback.reporter_unavailable",
        "occurred_at": rfc3339_now(),
        "subcommand_invocation_id": logger.execution_id,
        "component": "collector",
        "failure_code": "protocol_error",
        "diagnostic": {"header": secret},
    }

    invocation.detect_event(event, logger.path)

    [path] = iter_observation_paths(root)
    observation = read_json_object(path)
    raw_text = path.read_text(encoding="utf-8")
    assert secret not in raw_text
    assert (
        observation["payload"]["event_fields"]["diagnostic"]["header"]
        == "[REDACTED:authorization]"
    )
    assert validate_observation_envelope(observation) == []


def test_machine_detector_masks_secret_in_event_field_keys(tmp_path: Path) -> None:
    """detector payload の object key に含まれる secret も raw に残さない。"""
    root = make_repo(tmp_path)
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    secret_key = "Authorization: Bearer abcdefghijklmnopqrstuvwxyz"
    event = {
        "event_schema_version": 1,
        "event_id": "evt_machine_secret_key",
        "event_type": "feedback.reporter_unavailable",
        "occurred_at": rfc3339_now(),
        "subcommand_invocation_id": logger.execution_id,
        "component": "collector",
        "failure_code": "protocol_error",
        "diagnostic": {secret_key: "value"},
    }

    invocation.detect_event(event, logger.path)

    [path] = iter_observation_paths(root)
    observation = read_json_object(path)
    raw_text = path.read_text(encoding="utf-8")
    assert secret_key not in raw_text
    assert observation["payload"]["event_fields"]["diagnostic"] == {
        "[REDACTED:authorization]": "value"
    }
    assert validate_observation_envelope(observation) == []


def test_completion_count_reports_only_pending_raw_observations(
    feedback_directory: Path, stored_feedback_context: dict[str, object]
) -> None:
    """正常 report 前は raw store の pending 件数一値だけを返す。"""
    root = feedback_directory
    store_agent_observation(root, stored_feedback_context, _payload())

    assert feedback_completion_counts(root) == (1, [])


@pytest.mark.parametrize(
    ("count", "oldest_age", "expected_warning", "max_reads"),
    [
        pytest.param(99, timedelta(0), False, 99, id="below-count-limit"),
        pytest.param(100, timedelta(0), True, 0, id="at-count-limit"),
        pytest.param(
            2,
            timedelta(days=7) - timedelta(microseconds=1),
            False,
            2,
            id="below-age-limit",
        ),
        pytest.param(2, timedelta(days=7), True, 1, id="at-age-limit"),
    ],
)
def test_completion_count_retention_thresholds_stop_unneeded_reads(
    feedback_directory,
    stored_feedback_context,
    monkeypatch,
    count,
    oldest_age,
    expected_warning,
    max_reads,
):
    """通知の境界を守り、通知が確定した後の raw 本文読み取りを省く。"""
    root = feedback_directory
    now = datetime(2030, 1, 8, tzinfo=timezone.utc)
    _, first_path = store_agent_observation(
        root,
        stored_feedback_context,
        _payload(),
        observation_id="fbo_000000_2030-01-08_00-00",
        observed_at=(now - oldest_age).isoformat(),
    )
    observation = read_json_object(first_path)
    # 保存・receipt の検査は専用ケースへ委ね、件数用の追加 raw だけを作る。
    for index in range(1, count):
        identity = f"fbo_{index:06d}_2030-01-08_00-00"
        observation.update(observation_id=identity, observed_at=now.isoformat())
        path = observation_path(root, identity, now.isoformat())
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(canonical_json_bytes(observation))
    monkeypatch.setattr(
        feedback_store_module,
        "datetime",
        SimpleNamespace(now=lambda _zone: now, fromisoformat=datetime.fromisoformat),
    )
    read = Mock(wraps=feedback_store_module.read_json_object)
    monkeypatch.setattr(feedback_store_module, "read_json_object", read)

    pending, warnings = feedback_completion_counts(root)

    assert pending == count
    assert bool(warnings) is expected_warning
    if warnings:
        assert "cmoc feedback report" in warnings[0]
    assert read.call_count <= max_reads


def test_agent_store_rejects_non_directory_observation_parent(
    feedback_directory: Path, stored_feedback_context: dict[str, object]
) -> None:
    """raw storage の非 directory parent を domain rejection として返す。"""
    root = feedback_directory
    invalid_parent = feedback_root(root) / "observation" / "v1" / "2030"
    invalid_parent.parent.mkdir(parents=True)
    invalid_parent.write_text("not a directory")

    with pytest.raises(FeedbackRejected) as rejected:
        store_agent_observation(
            root,
            stored_feedback_context,
            _payload(),
            observed_at="2030-01-02T00:00:00Z",
        )

    assert rejected.value.code == "context_invalid"


@pytest.mark.parametrize("redacted", [False, True], ids=["plain", "redacted"])
@pytest.mark.parametrize("exceeds_limit", [False, True], ids=["at-limit", "over-limit"])
def test_agent_payload_summary_limit_after_redaction(
    feedback_directory: Path, redacted: bool, exceeds_limit: bool
) -> None:
    """未置換と置換後の summary で、文字数上限を同じように適用する。"""
    payload = _payload(kind="error", path=None)
    limit = reporter_input_schema()["properties"]["summary"]["maxLength"]
    marker = "[REDACTED:authorization]"
    suffix = " Authorization:x" if redacted else ""
    masked_suffix = " " + marker if redacted else ""
    prefix = "s" * (limit + int(exceeds_limit) - len(masked_suffix))
    payload["summary"] = prefix + suffix
    original = canonical_json_bytes(payload)

    if exceeds_limit:
        with pytest.raises(FeedbackRejected) as error:
            validate_agent_payload(payload, feedback_directory)
        assert error.value.code == "schema_invalid"
        assert "/summary" in error.value.message
    else:
        masked, _, count = validate_agent_payload(payload, feedback_directory)
        assert masked["summary"] == prefix + masked_suffix
        assert count == int(redacted)
    assert canonical_json_bytes(payload) == original


@pytest.mark.parametrize("redacted", [False, True], ids=["plain", "redacted"])
@pytest.mark.parametrize("exceeds_limit", [False, True], ids=["at-limit", "over-limit"])
def test_agent_payload_utf8_size_limit_after_redaction(
    feedback_directory: Path, redacted: bool, exceeds_limit: bool
) -> None:
    """各 field が schema 内でも、UTF-8 合計の 32 KiB 上限を置換後まで守る。"""
    payload = _payload(kind="error", path=None)
    payload["evidence"] = [{"kind": "error", "text": "é" * 1950} for _ in range(8)]
    if redacted:
        payload["summary"] = "failure Authorization:x"
    growth = len("[REDACTED:authorization]") - len("Authorization:x") if redacted else 0
    size = len(canonical_json_bytes(payload)) - 1
    payload["impact"] = str(payload["impact"]) + "x" * (
        32 * 1024 + int(exceeds_limit) - size - growth
    )
    original = canonical_json_bytes(payload)
    assert len(original) - 1 + growth == 32 * 1024 + int(exceeds_limit)

    if exceeds_limit:
        with pytest.raises(FeedbackRejected) as error:
            validate_agent_payload(payload, feedback_directory)
        assert error.value.code == "payload_too_large"
        if redacted:
            assert error.value.message == "redacted payload exceeds 32 KiB"
    else:
        masked, _, count = validate_agent_payload(payload, feedback_directory)
        assert len(canonical_json_bytes(masked)) - 1 == 32 * 1024
        assert count == int(redacted)
    assert canonical_json_bytes(payload) == original


@pytest.mark.parametrize("text", ["Authorization:x", "[REDACTED:authorization]", " "])
def test_agent_payload_requires_meaningful_evidence(
    feedback_directory: Path, text: str
) -> None:
    """置換の有無にかかわらず、marker や空白だけの evidence を受理しない。"""
    with pytest.raises(FeedbackRejected) as error:
        validate_agent_payload(
            _payload(text=text, kind="error", path=None), feedback_directory
        )
    assert error.value.code == "suspected_secret"


def test_stored_invalid_reporter_schema_is_rejected_without_rewriting(
    feedback_directory: Path, stored_feedback_context: dict[str, object]
) -> None:
    """旧 input version の raw を intake で拒否し、元の byte 列を保持する。"""
    # CLI の publication 阻止・エラー report は invalid raw のケースで検証する。
    root = feedback_directory
    _, raw = store_agent_observation(root, stored_feedback_context, _payload())
    invalid = read_json_object(raw)
    invalid["payload"]["schema_version"] = 1
    content = canonical_json_bytes(invalid)
    raw.write_bytes(content)
    (feedback_root(root) / "intake.json").unlink()
    with pytest.raises(CmocError, match="raw observation validation") as error:
        feedback_report_module._pending_observations(root)
    assert str(raw) in error.value.detail
    assert "/schema_version" in error.value.detail
    assert raw.read_bytes() == content
    assert load_active_state(root).current is None


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_canonical_json_rejects_non_json_numbers(value: float) -> None:
    """raw と state に標準 JSON でない数値を保存しない。"""
    with pytest.raises(ValueError):
        canonical_json_bytes({"value": value})


@pytest.mark.parametrize("content", [b'{"value":NaN}\n', b'{"value":"\\ud800"}\n'])
def test_state_reader_wraps_noncanonical_json_values(
    tmp_path: Path, content: bytes
) -> None:
    """state reader が canonical 化時の JSON value 例外を corruption にする。"""
    path = tmp_path / "state.json"
    path.write_bytes(content)

    with pytest.raises(CmocError, match="canonical JSON object"):
        feedback_state_module._read_canonical_object(path, "feedback state")


@pytest.mark.parametrize("schema_name", ["normalize_issue", "remediate_issue"])
@pytest.mark.parametrize("change", ["contract", "json", "schema", "missing"])
def test_feedback_output_validation_uses_current_schema_file(
    tmp_path: Path, schema_name: str, change: str
) -> None:
    """再利用時も各 output と現在の schema を検査し、更新・破損・消失を拒否する。"""
    schema_text = oracle_schema_path("feedback", f"{schema_name}.json").read_text(
        encoding="utf-8"
    )
    schema_path = tmp_path / f"{schema_name}.json"
    schema_path.write_text(schema_text, encoding="utf-8")
    output = (
        {"result": {"decision": "existing", "existing_issue_id": "fbi_" + "a" * 26}}
        if schema_name == "normalize_issue"
        else _remediation_output("fbi_" + "a" * 26, "not_actionable")
    )
    validate = feedback_report_module._structured_output_matches_schema

    assert validate(output, schema_path)
    assert not validate({}, schema_path)

    if change == "contract":
        schema = json.loads(schema_text)
        schema["properties"]["new_field"] = {"type": "null"}
        schema["required"].append("new_field")
        schema_path.write_text(json.dumps(schema), encoding="utf-8")
    elif change == "json":
        schema_path.write_text("{", encoding="utf-8")
    elif change == "schema":
        schema_path.write_text('{"type": "invalid"}', encoding="utf-8")
    else:
        schema_path.unlink()

    assert not validate(output, schema_path)

    schema_path.write_text(schema_text, encoding="utf-8")
    assert validate(output, schema_path)


def test_normalization_schema_supports_editable_namespace_package(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """editable namespace package でも oracle schema を読み込める。"""
    original_files = feedback_state_module.resources.files

    def raise_namespace_resource_error(package: str):
        if package == "oracle.acp_builder.feedback":
            raise NotADirectoryError(package)
        return original_files(package)

    monkeypatch.setattr(
        feedback_state_module.resources, "files", raise_namespace_resource_error
    )
    feedback_state_module._normalization_validator.cache_clear()

    assert feedback_state_module._normalization_output_matches_schema(
        {"result": {"decision": "new", "existing_issue_id": None}}
    )


@pytest.mark.parametrize("allow_missing", [False, True])
@pytest.mark.parametrize("link_kind", ["file", "parent", "dangling"])
def test_state_reference_rejects_in_repository_symlink_alias(
    feedback_directory: Path,
    allow_missing: bool,
    link_kind: str,
) -> None:
    """cleanup でも file・親 directory・dangling symlink を受理しない。"""
    root = feedback_directory
    expected_root = root / ".cmoc/gu/feedback/active/generation"
    expected_root.mkdir(parents=True)
    target = expected_root / "manifest.json"
    content = b"artifact\n"
    target.write_bytes(content)
    if link_kind == "parent":
        alias_parent = expected_root / "alias"
        alias_parent.symlink_to(expected_root, target_is_directory=True)
        alias = alias_parent / target.name
    else:
        alias = expected_root / "alias.json"
        alias.symlink_to(target if link_kind == "file" else expected_root / "missing")

    with pytest.raises(CmocError, match="symlink"):
        feedback_state_module._validate_artifact_reference(
            root,
            {
                "path": alias.relative_to(root).as_posix(),
                "sha256": hashlib.sha256(content).hexdigest(),
            },
            expected_root=expected_root,
            description="state artifact",
            allow_missing=allow_missing,
        )


@pytest.mark.parametrize("allow_missing", [False, True])
def test_state_reference_cleanup_relaxes_only_file_existence(
    feedback_directory: Path, allow_missing: bool
) -> None:
    """削除済みの許容は path・hash 検証と、現存する通常 file の条件を変えない。"""
    root = feedback_directory
    directory = root / "artifacts"
    directory.mkdir()
    target = directory / "record.json"
    content = b"artifact\n"
    target.write_bytes(content)
    reference = {
        "path": target.relative_to(root).as_posix(),
        "sha256": hashlib.sha256(content).hexdigest(),
    }

    def validate(value):
        return feedback_state_module._validate_artifact_reference(
            root,
            value,
            expected_root=directory,
            description="state artifact",
            allow_missing=allow_missing,
        )

    assert validate(reference) == target
    target.write_bytes(b"changed\n")
    with pytest.raises(CmocError, match="SHA256"):
        validate(reference)
    target.unlink()
    if allow_missing:
        assert validate(reference) == target
    else:
        with pytest.raises(CmocError, match="通常 file"):
            validate(reference)
    with pytest.raises(CmocError, match="SHA256"):
        validate({**reference, "sha256": "invalid"})
    with pytest.raises(CmocError, match="期待 root 外"):
        validate({**reference, "path": "outside.json"})
    target.mkdir()
    with pytest.raises(CmocError, match="通常 file"):
        validate(reference)


def test_completion_count_warns_instead_of_ignoring_unknown_raw_artifact(
    feedback_directory: Path,
) -> None:
    """raw store inventory が不正なら件数を推測せず unavailable warning を返す。"""
    root = feedback_directory
    invalid = feedback_root(root) / "observation" / "v1" / "unexpected.tmp"
    invalid.parent.mkdir(parents=True, exist_ok=True)
    invalid.write_text("partial")

    pending, warnings = feedback_completion_counts(root)

    assert pending is None
    assert warnings == [
        "repository-local feedback state を安全に検証できないため件数を計算できません。"
    ]


@pytest.mark.parametrize("invalid_parent", ["dangling_symlink", "file"])
def test_completion_count_rejects_invalid_observation_parent(
    tmp_path: Path,
    feedback_directory: Path,
    invalid_parent: str,
) -> None:
    """不正な observation 親を空の初期 state として扱わない。"""
    root = feedback_directory
    observation_parent = feedback_root(root) / "observation"
    observation_parent.parent.mkdir(parents=True)
    if invalid_parent == "dangling_symlink":
        observation_parent.symlink_to(
            tmp_path / "missing-observations", target_is_directory=True
        )
    else:
        observation_parent.write_text("not a directory")

    pending, warnings = feedback_completion_counts(root)

    assert pending is None
    assert warnings


def test_feedback_writer_lock_rejects_concurrent_writer(
    feedback_directory: Path,
) -> None:
    """同じ repository で二つ目の report writer を開始しない。"""
    root = feedback_directory
    with feedback_writer_lock(root):
        with pytest.raises(CmocError, match="別の feedback writer"):
            with feedback_writer_lock(root):
                pass


def test_empty_report_publishes_current_generation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """candidate がなくても ok report と空 active generation を atomic publication する。"""
    root = make_repo(tmp_path)
    _active_session(root, monkeypatch)
    log_dir = root / ".cmoc/gu/log/sub_command"
    previous_logs = set(log_dir.glob("*.jsonl"))
    monkeypatch.setattr(
        feedback_report_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: pytest.fail("empty report must not call Codex"),
    )

    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    [log_path] = set(log_dir.glob("*.jsonl")) - previous_logs
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    [publication_event] = [
        event for event in events if event["event"] == "feedback_report_published"
    ]
    assert Path(publication_event["generation_manifest_path"]).is_absolute()
    assert Path(publication_event["report_path"]).is_absolute()

    # 履歴の再走査は publication のたびに増えるので、一回の state 読込では一巡に抑える。
    history_loads = []
    original_load_history = feedback_history_module.load_history

    def observed_load_history(repo, references):
        history_loads.append(references)
        return original_load_history(repo, references)

    monkeypatch.setattr(feedback_history_module, "load_history", observed_load_history)
    state = validate_feedback_state(root)
    assert len(history_loads) <= 1
    assert state.history == [
        read_json_object(root / reference["path"])
        for reference in state.generation_manifest["history"]
    ]
    assert state.current is not None
    assert state.current["result"] == "ok"
    assert state.issues == {}
    assert state.machine_aggregates == {}
    assert load_report_cut(root) is None
    [report] = (root / ".cmoc/gu/report/feedback").glob("*.md")
    text = report.read_text()
    assert 'result: "ok"' in text
    assert "human_required_issue_count: 0" in text
    assert (
        state.generation_manifest["session_commit"]
        == run_git(root, "rev-parse", "HEAD").stdout.strip()
    )


@pytest.mark.parametrize("condition", ["dirty_worktree", "dirty_index", "inactive"])
def test_feedback_preconditions_preserve_existing_changes_and_raw(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    condition: str,
) -> None:
    """不適合な session から run を開始せず、既存差分をそのまま保持する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    session_id = None
    if condition == "inactive":
        run_doctor(root)
    else:
        session_id = _active_session(root, monkeypatch)
        (root / "README.md").write_text("user change\n")
        if condition == "dirty_index":
            run_git(root, "add", "README.md")
    _, raw = store_agent_observation(
        root, _context(root, session_id=session_id), _payload()
    )
    original_head = run_git(root, "rev-parse", "HEAD").stdout
    original_status = run_git(root, "status", "--porcelain").stdout
    original_raw = raw.read_bytes()
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert result.exit_code == 1, result.output
    assert run_git(root, "rev-parse", "HEAD").stdout == original_head
    assert run_git(root, "status", "--porcelain").stdout == original_status
    assert raw.read_bytes() == original_raw
    assert load_report_cut(root) is None


@pytest.mark.parametrize("last_status", ["human_required", "inconclusive"])
def test_feedback_repairs_sequential_waves_and_preserves_late_intake(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, last_status: str
) -> None:
    """修復中の新 issue を最新 tree で処理し、最終境界後の raw は残す。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _, first_raw, first_id = _store_agent_issue(root, session_id)
    calls: list[str] = []
    raw_paths = [first_raw]
    later_id: str | None = None

    def fake_call(parameter: Any, **kwargs: Any) -> SimpleNamespace:
        nonlocal later_id
        identity = (
            kwargs["purpose"]
            .removeprefix("feedback issue remediation (")
            .removesuffix(")")
        )
        calls.append(identity)
        worktree = parameter.agent_call_cwd
        assert worktree != root
        assert parameter.file_access_mode == FileAccessMode.REALIZATION_WRITE
        if identity == first_id:
            (worktree / "README.md").write_text("repaired\n")
            output = _remediation_output(identity, "fixed")
            output["result"]["changed_paths"] = ["README.md"]
            payload = _payload(kind="other", path=None, text="別の issue")
            with begin_feedback_call(
                agent_call_id="ac_000011_2026-09-29_15-04",
                agent_call_kind=parameter.agent_call_kind,
                codex_call_id="cc_000013_2026-09-29_15-04",
                log_paths=[],
                agent_call_cwd=worktree,
            ) as feedback_call:
                environment = feedback_call.subprocess_env({})
                accepted = _submit_to_feedback_collector(
                    int(environment[FEEDBACK_COLLECTOR_PORT_ENV]),
                    environment[FEEDBACK_CAPABILITY_ENV],
                    payload,
                )
            assert accepted["status"] == "accepted"
            path = next(
                path
                for path in iter_observation_paths(root)
                if path.stem == accepted["observation_id"]
            )
            context = read_json_object(path)["context"]
            assert context["work_root"] == str(worktree)
            assert context["run_kind"] == "feedback_report"
            assert context["run_id"] is not None
            assert (
                context["head_commit"]
                == run_git(worktree, "rev-parse", "HEAD").stdout.strip()
            )
            later_id = issue_id(f"agent\0{accepted['observation_id']}")
            raw_paths.append(path)
            # 完全重複の observation は新しい issue call を増やさない。
            _, duplicate = store_agent_observation(
                root, _context(root, session_id=session_id), _payload()
            )
            raw_paths.append(duplicate)
        else:
            assert identity == later_id
            assert (worktree / "README.md").read_text() == "repaired\n"
            assert run_git(worktree, "status", "--porcelain").stdout == ""
            output = _remediation_output(identity, last_status)
        return _fake_result(root, output)

    original_seal = remediation_module._seal
    late_paths: list[Path] = []

    def seal_then_receive(*args: Any) -> None:
        original_seal(*args)
        _, late = store_agent_observation(
            root,
            _context(root, session_id=session_id),
            _payload(text="最終境界後の observation"),
        )
        late_paths.append(late)

    monkeypatch.setattr(feedback_report_module, "run_codex_exec", fake_call)
    monkeypatch.setattr(remediation_module, "_seal", seal_then_receive)
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert calls == [first_id, later_id]
    assert (root / "README.md").read_text() == "repaired\n"
    assert run_git(root, "status", "--porcelain").stdout == ""
    assert load_report_cut(root) is None
    assert all(path.exists() for path in late_paths)
    state = load_active_state(root)
    assert set(state.issues) == {later_id}
    assert state.issues[later_id]["verification"]["status"] == last_status
    assert all(not path.exists() for path in raw_paths)


# rollback 済み error の手動終了は、障害原因によらず同じ入力状態を扱う。
# 各障害を検査し、error（rollback 済み／checkpoint 保存済み）と joinable で両操作を残す。
@pytest.mark.parametrize(
    ("fault", "operation"),
    [
        ("unreported_change", "join"),
        ("forbidden_change", "abandon"),
        ("checkpoint", "join"),
        ("checkpoint_reference", "join"),
        ("checkpoint_reference", "abandon"),
        ("interrupt", "join"),
        ("interrupt", "abandon"),
    ],
)
def test_failed_feedback_unit_rolls_back_and_manual_completion_keeps_raw(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, fault: str, operation: str
) -> None:
    """未確定 issue の差分を戻し、明示終了で publication せず raw を保持する。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _, raw, identity = _store_agent_issue(root, session_id)
    initial = (root / "README.md").read_text()

    def fake_call(parameter: Any, **kwargs: Any) -> SimpleNamespace:
        worktree = parameter.agent_call_cwd
        target = "oracle/bad.md" if fault == "forbidden_change" else "README.md"
        (worktree / target).parent.mkdir(parents=True, exist_ok=True)
        (worktree / target).write_text("unconfirmed change\n")
        if fault == "interrupt":
            raise KeyboardInterrupt
        output = _remediation_output(identity, "fixed")
        output["result"]["changed_paths"] = (
            [] if fault == "unreported_change" else [target]
        )
        return _fake_result(root, output)

    def checkpoint_failure(*_args: Any, **_kwargs: Any) -> None:
        raise OSError("injected checkpoint failure")

    monkeypatch.setattr(feedback_report_module, "run_codex_exec", fake_call)
    if fault == "checkpoint":
        monkeypatch.setattr(remediation_module, "write_checkpoint", checkpoint_failure)
    elif fault == "checkpoint_reference":
        monkeypatch.setattr(
            feedback_report_module, "_record_checkpoint", checkpoint_failure
        )
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert result.exit_code == (0 if fault == "interrupt" else 1), result.output
    manifest, _ = load_report_cut(root)
    _, _, session = load_state_for_branch(
        root, manifest["run"]["identity"]["session_branch"]
    )
    assert session.run.state == ("joinable" if fault == "interrupt" else "error")
    assert manifest["processing"]["status"] == (
        "interrupted" if fault == "interrupt" else "failed"
    )
    run_worktree = Path(manifest["run"]["identity"]["run_worktree"])
    assert (run_worktree / "README.md").read_text() == (
        "unconfirmed change\n" if fault == "checkpoint_reference" else initial
    )
    assert run_git(run_worktree, "status", "--porcelain").stdout == ""
    assert manifest["processing"]["remediation_checkpoints"] == []
    completed = runner.invoke(app, ["run", operation], catch_exceptions=False)
    assert completed.exit_code == 0, completed.output
    assert (root / "README.md").read_text() == (
        "unconfirmed change\n"
        if fault == "checkpoint_reference" and operation == "join"
        else initial
    )
    assert raw.exists()
    assert load_active_state(root).current is None
    assert load_report_cut(root) is None


def test_feedback_interrupt_after_run_start_reports_retained_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """run 公開直後の中断でも joinable state と run identity を report する。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    original_start = remediation_module.start_editing_run

    def start_then_interrupt(kind: str) -> Any:
        """run の state 公開後、context 返却前の中断を再現する。"""
        original_start(kind)
        raise KeyboardInterrupt()

    monkeypatch.setattr(remediation_module, "start_editing_run", start_then_interrupt)
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    session_state = json.loads(
        (root / ".cmoc" / "gu" / "session" / f"{session_id}.json").read_text()
    )
    assert session_state["run"]["state"] == "joinable"
    report_text = terminal_primary_report(result).read_text()
    assert 'terminal_classification: "user_interruption"' in report_text
    assert 'run_kind: "feedback_report"' in report_text
    assert 'state_before: "ready"' in report_text
    assert 'state_after: "joinable"' in report_text
    assert "保持した feedback run" in result.output


def test_feedback_interrupt_after_report_cut_write_recovers_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """manifest の atomic write 後に中断しても interrupted 状態を保存する。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    original_write = remediation_module.write_report_cut_manifest

    def write_then_interrupt(repository: Path, manifest: dict[str, Any]) -> NoReturn:
        """write の戻り値を受け取る前の中断を再現する。"""
        original_write(repository, manifest)
        raise KeyboardInterrupt()

    monkeypatch.setattr(
        remediation_module, "write_report_cut_manifest", write_then_interrupt
    )
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    session_state = json.loads(
        (root / ".cmoc" / "gu" / "session" / f"{session_id}.json").read_text()
    )
    assert session_state["run"]["state"] == "joinable"
    manifest, _ = load_report_cut(root)
    assert manifest["processing"]["status"] == "interrupted"
    assert 'terminal_classification: "user_interruption"' in (
        terminal_primary_report(result).read_text()
    )


def test_feedback_interrupt_cleanup_failure_sets_error_and_reports(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """中断 cleanup の失敗を user interruption へ変換せず error にする。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _store_agent_issue(root, session_id)

    def interrupting_agent(parameter: Any, **_kwargs: Any) -> NoReturn:
        """差分を作成した issue 処理単位の中断を再現する。"""
        (parameter.agent_call_cwd / "README.md").write_text("interrupted\n")
        raise KeyboardInterrupt()

    def fail_rollback(_worktree: Path) -> NoReturn:
        """中断後の run-level rollback 失敗を再現する。"""
        raise RuntimeError("rollback failed")

    monkeypatch.setattr(feedback_report_module, "run_codex_exec", interrupting_agent)
    monkeypatch.setattr(remediation_module, "rollback_work_unit", fail_rollback)
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert result.exit_code == 1, result.output
    session_state = json.loads(
        (root / ".cmoc" / "gu" / "session" / f"{session_id}.json").read_text()
    )
    assert session_state["run"]["state"] == "error"
    report_text = terminal_primary_report(result).read_text()
    assert 'terminal_classification: "error"' in report_text
    assert 'state_after: "error"' in report_text
    assert "rollback failed" in result.output
    manifest, _ = load_report_cut(root)
    assert manifest["processing"]["status"] == "failed"


@pytest.mark.parametrize(
    "fault",
    [
        "publication",
        "raw_cleanup",
        "cleanup",
        "merge_reference",
        "completion_reference",
    ],
)
def test_feedback_recovers_after_auto_join_without_new_calls(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, fault: str
) -> None:
    """自動 join 後の失敗は修復 commit と公開入力を保持して同じ run を完了する。"""
    import commons.runtime_feedback_run_state as run_state_module
    import sub_commands.feedback.recovery as recovery_module

    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _, raw, identity = _store_agent_issue(root, session_id)

    def fake_call(parameter: Any, **_kwargs: Any) -> SimpleNamespace:
        (parameter.agent_call_cwd / "README.md").write_text("joined repair\n")
        output = _remediation_output(identity, "fixed")
        output["result"]["changed_paths"] = ["README.md"]
        return _fake_result(root, output)

    target = feedback_report_module if fault == "publication" else recovery_module
    name = "publish_current_pointer" if fault == "publication" else "cleanup_joined_run"
    if fault == "raw_cleanup":
        target = feedback_state_module
        name = "_unlink_artifact_reference"
    if fault.endswith("_reference"):
        target = run_state_module
        name = "write_report_cut_manifest"
    original = getattr(target, name)

    def fail(*args: Any, **kwargs: Any) -> Any:
        if fault.endswith("_reference"):
            key = "merged" if fault == "merge_reference" else "completion"
            if args[1]["run"][key] is None:
                return original(*args, **kwargs)
        raise OSError("injected finalization failure")

    monkeypatch.setattr(feedback_report_module, "run_codex_exec", fake_call)
    monkeypatch.setattr(target, name, fail)
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert result.exit_code == 1, result.output
    assert (root / "README.md").read_text() == "joined repair\n"
    joined_head = run_git(root, "rev-parse", "HEAD").stdout
    saved_report = None
    if fault in {"raw_cleanup", "cleanup"}:
        published = load_active_state(root)
        assert published.current is not None
        saved_report = root / published.current["report_path"]
        saved_content = saved_report.read_bytes()
        (root / "README.md").write_text("changed after publication\n")
        assert feedback_completion_counts(root)[0] == 0
        if fault == "raw_cleanup":
            assert raw.exists()
        report_text = terminal_primary_report(result).read_text()
        assert "publication_established: true" in report_text
    for operation in ("join", "abandon"):
        rejected = runner.invoke(app, ["run", operation], catch_exceptions=False)
        assert rejected.exit_code == 1, rejected.output
        rejected_report = terminal_primary_report(rejected).read_text(encoding="utf-8")
        assert 'run_kind: "feedback_report"' in rejected_report
        assert 'state_before: "error"' in rejected_report
        assert 'state_after: "error"' in rejected_report
    monkeypatch.setattr(target, name, original)
    monkeypatch.setattr(
        feedback_report_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: pytest.fail("recovery must not call Codex"),
    )
    recovered = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert recovered.exit_code == 0, recovered.output
    assert run_git(root, "rev-parse", "HEAD").stdout == joined_head
    assert not raw.exists()
    assert load_report_cut(root) is None
    assert not (feedback_root(root) / "finalization.json").exists()
    assert load_active_state(root).current["result"] == "ok"
    if saved_report is not None:
        assert saved_report.read_bytes() == saved_content
        assert (root / "README.md").read_text() == "changed after publication\n"


def test_agent_issues_are_compacted_then_removed_for_terminal_verdicts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """両方の終了判定で active と一覧から除き、各案件の履歴を残す。"""
    # 異なる subject の案件を同時に用意し、Git/session と二回の publication を共有する。
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    cases = {}
    for terminal_verdict, kind, reference_path in (
        ("already_resolved", "file", "README.md"),
        ("not_actionable", "oracle", "oracle/spec.md"),
    ):
        accepted, raw_path = store_agent_observation(
            root,
            _context(root, session_id=session_id),
            _payload(kind=kind, path=reference_path),
        )
        identity = issue_id(f"agent\0{accepted['observation_id']}")
        cases[identity] = {
            "raw_path": raw_path,
            "reference_path": reference_path,
            "terminal_verdict": terminal_verdict,
        }
    verdicts = {identity: "human_required" for identity in cases}

    def fake_call(*_args: Any, **kwargs: Any) -> SimpleNamespace:
        identity = (
            kwargs["purpose"]
            .removeprefix("feedback issue remediation (")
            .removesuffix(")")
        )
        return _fake_result(
            root,
            _remediation_output(
                identity,
                verdicts[identity],
                reference_path=cases[identity]["reference_path"],
            ),
        )

    monkeypatch.setattr(feedback_report_module, "run_codex_exec", fake_call)

    first = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert first.exit_code == 0, first.output
    first_state = load_active_state(root)
    assert set(first_state.issues) == set(cases)
    first_text = terminal_primary_report(first).read_text()
    for identity, case in cases.items():
        assert not case["raw_path"].exists()
        issue = first_state.issues[identity]
        assert issue["occurrence_count"] == 1
        assert issue["verification"]["human_action"] == "README の設定を修正する。"
        assert "reference_id" not in json.dumps(
            issue["verification"], ensure_ascii=False
        )
        assert identity in first_text
    assert feedback_completion_counts(root) == (0, [])

    verdicts.update(
        {identity: case["terminal_verdict"] for identity, case in cases.items()}
    )
    second = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert second.exit_code == 0, second.output
    second_state = load_active_state(root)
    assert second_state.issues == {}
    events = {event["issue_id"]: event for event in second_state.history[-1]["events"]}
    assert set(events) == set(cases)
    for identity, case in cases.items():
        event = events[identity]
        assert event["kind"] == "resolved"
        assert event["before"] == first_state.issues[identity]
        assert event["after"] is None
        assert event["agent_result"]["status"] == case["terminal_verdict"]
    reports = list((root / ".cmoc/gu/report/feedback").glob("*.md"))
    assert len(reports) == 2
    assert second_state.current is not None
    current_report = root / str(second_state.current["report_path"])
    current_text = current_report.read_text()
    assert all(identity not in current_text for identity in cases)
    assert "human_required_issue_count: 0" in current_text
    assert "未終了の案件はありません。" in current_text
    generation_directories = list(
        (feedback_root(root) / "active" / "generation").iterdir()
    )
    assert len(generation_directories) == 1


def test_feedback_basis_includes_oracle_changes_but_ignores_refactor_state(
    tmp_path: Path,
) -> None:
    """oracle file の変更を根拠へ含め、管理 state だけを除外する。"""
    root = make_repo(tmp_path)
    document = root / "oracle/notes.md"
    state = root / ".cmoc/gt/realization/refactor/state.json"
    state.parent.mkdir(parents=True)
    document.write_text("first document\n")
    state.write_text("{}\n")
    run_git(root, "add", "oracle/notes.md", ".cmoc/gt/realization/refactor/state.json")
    baseline = decision_module.worktree_inputs(root)

    document.write_text("updated document\n")
    state.write_text('{"entry": {}}\n')
    after_document = decision_module.worktree_inputs(root)
    assert after_document != baseline
    state.write_text('{"another": {}}\n')
    assert decision_module.worktree_inputs(root) == after_document

    (root / "oracle/spec.md").write_text("# updated spec\n")
    assert decision_module.worktree_inputs(root) != baseline


def test_machine_observation_stays_bounded_until_recurrence_threshold(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """threshold 未満は bounded aggregate、到達後は remediation candidate にする。"""
    root = make_repo(tmp_path)
    _active_session(root, monkeypatch)
    log_path = root / ".cmoc/gu/log/sub_command/exec_000000_2026-09-29_15-04.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text('{"event":"reporter unavailable"}\n')
    canonical_key: str | None = None
    # 集約の threshold を確認するため、壁時計が数秒戻っても window 内の時刻を使う。
    observed_at = (
        (datetime.now(timezone.utc) - timedelta(minutes=5))
        .isoformat()
        .replace("+00:00", "Z")
    )

    for index in range(2):
        event = {
            "event_schema_version": 1,
            "event_id": f"evt_{index}",
            "event_type": "feedback.reporter_unavailable",
            "occurred_at": observed_at,
            "subcommand_invocation_id": f"exec_{index:06d}_2026-09-29_15-04",
            "component": "reporter",
            "failure_code": "missing",
        }
        context = _context(root, session_id=f"sess_{index:06d}_2026-09-29_15-04")
        context["subcommand_invocation_id"] = event["subcommand_invocation_id"]
        _observation_id, raw_path = store_machine_observation(
            root,
            context,
            rule_id="feedback.reporter_unavailable.v1",
            category="tooling",
            subject_type="reporter_component",
            normalized_subject_id="reporter:missing",
            summary="feedback reporter が反復して利用できない。",
            impact="agent observation が欠落する。",
            human_action="reporter を確認する。",
            event=event,
            log_path=log_path,
        )
        raw = read_json_object(raw_path)
        canonical_key = machine_canonical_key(raw)
        if index == 0:
            monkeypatch.setattr(
                feedback_report_module,
                "run_codex_exec",
                lambda *_args, **_kwargs: pytest.fail(
                    "threshold 未満で verification してはならない"
                ),
            )
        else:
            assert canonical_key is not None
            candidate_id = issue_id(canonical_key)
            _install_codex_outputs(
                monkeypatch,
                _remediation_output(
                    candidate_id,
                    "human_required",
                    reference_path=".cmoc/gu/log/test.jsonl",
                ),
            )
        result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
        assert result.exit_code == 0, result.output
        state = load_active_state(root)
        if index == 0:
            assert set(state.machine_aggregates) == {canonical_key}
            assert state.issues == {}
            [reference] = state.generation_manifest["machine_aggregates"]
            _assert_hash_verified_state_snapshot(
                root, state, root / reference["path"], monkeypatch
            )
        else:
            assert state.machine_aggregates == {}
            assert set(state.issues) == {issue_id(str(canonical_key))}
            assert state.issues[issue_id(str(canonical_key))]["occurrence_count"] == 2


def test_active_machine_issue_keeps_threshold_state_after_window_expires(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """window 外で threshold 未満になった active machine issue を最後の state で再検証する。"""
    root = make_repo(tmp_path)
    _active_session(root, monkeypatch)
    log_path = root / ".cmoc/gu/log/sub_command/exec_000000_2026-09-29_15-04.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text('{"event":"reporter unavailable"}\n')
    canonical_key: str | None = None
    base = datetime.now(timezone.utc)

    for index in range(2):
        occurred_at = base - timedelta(days=1 if index == 0 else 20)
        event = {
            "event_schema_version": 1,
            "event_id": f"evt_expiry_{index}",
            "event_type": "feedback.reporter_unavailable",
            "occurred_at": occurred_at.isoformat(timespec="seconds").replace(
                "+00:00", "Z"
            ),
            "subcommand_invocation_id": f"exec_{index:06d}_2026-09-29_15-04",
            "component": "reporter",
            "failure_code": "missing",
        }
        context = _context(root, session_id=f"sess_{index:06d}_2026-09-29_15-04")
        context["subcommand_invocation_id"] = event["subcommand_invocation_id"]
        _observation_id, raw_path = store_machine_observation(
            root,
            context,
            rule_id="feedback.reporter_unavailable.v1",
            category="tooling",
            subject_type="reporter_component",
            normalized_subject_id="reporter:missing",
            summary="feedback reporter が反復して利用できない。",
            impact="agent observation が欠落する。",
            human_action="reporter を確認する。",
            event=event,
            log_path=log_path,
        )
        canonical_key = machine_canonical_key(read_json_object(raw_path))

    assert canonical_key is not None
    candidate_id = issue_id(canonical_key)
    _install_codex_outputs(
        monkeypatch,
        _remediation_output(
            candidate_id,
            "human_required",
            reference_path=".cmoc/gu/log/test.jsonl",
        ),
    )
    first = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert first.exit_code == 0, first.output
    first_state = load_active_state(root)
    assert set(first_state.issues) == {candidate_id}
    assert isinstance(first_state.issues[candidate_id]["machine_state"], dict)

    partially_expired = (
        (base + timedelta(days=11)).isoformat(timespec="seconds").replace("+00:00", "Z")
    )
    monkeypatch.setattr(
        feedback_report_module, "rfc3339_now", lambda: partially_expired
    )
    _install_codex_outputs(
        monkeypatch,
        _remediation_output(
            candidate_id,
            "human_required",
            reference_path=".cmoc/gu/log/test.jsonl",
        ),
    )
    second = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert second.exit_code == 0, second.output
    second_state = load_active_state(root)
    assert set(second_state.issues) == {candidate_id}
    assert isinstance(second_state.issues[candidate_id]["machine_state"], dict)

    fully_expired = (
        (base + timedelta(days=31)).isoformat(timespec="seconds").replace("+00:00", "Z")
    )
    monkeypatch.setattr(feedback_report_module, "rfc3339_now", lambda: fully_expired)
    _install_codex_outputs(
        monkeypatch,
        _remediation_output(
            candidate_id,
            "human_required",
            reference_path=".cmoc/gu/log/test.jsonl",
        ),
    )
    third = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert third.exit_code == 0, third.output
    third_state = load_active_state(root)
    assert set(third_state.issues) == {candidate_id}
    assert isinstance(third_state.issues[candidate_id]["machine_state"], dict)


def test_machine_threshold_excludes_expired_scope_in_boundary_bucket() -> None:
    """日次 bucket が window 境界をまたぐ場合は occurrence ごと破棄する。"""
    canonical_key = (
        "feedback.reporter_unavailable.v1\0reporter_component\0reporter:missing"
    )
    previous = {
        "rule_id": "feedback.reporter_unavailable.v1",
        "category": "tooling",
        "summary": "summary",
        "impact": "impact",
        "human_action": "action",
        "time_buckets": [
            {
                "day": "2026-01-02",
                "count": 2,
                "first_observed_at": "2026-01-02T11:00:00Z",
                "last_observed_at": "2026-01-02T13:00:00Z",
                "scope_digest": [
                    {
                        "value": "a" * 64,
                        "last_observed_at": "2026-01-02T11:00:00Z",
                    },
                    {
                        "value": "b" * 64,
                        "last_observed_at": "2026-01-02T13:00:00Z",
                    },
                ],
                "agent_call_digest": [],
            }
        ],
        "representative_evidence": [],
        "latest_fingerprints": [],
    }

    aggregate = feedback_report_module._merge_machine_aggregate(
        Path("/unused"),
        previous,
        [],
        "2026-02-01T12:00:00Z",
        canonical_key,
    )

    assert aggregate is None


def test_invalid_raw_observation_blocks_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """validation 不通過 raw を処理済みにせず、正常 report を publication しない。"""
    root = make_repo(tmp_path)
    _active_session(root, monkeypatch)
    observation_id = "fbo_000099_2026-08-01_00-00"
    raw_path = observation_path(root, observation_id, "2030-01-02T00:00:00Z")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_content = "not-json\n"
    raw_path.write_text(raw_content)

    result = runner.invoke(app, ["feedback", "report"])

    assert result.exit_code == 1
    assert raw_path.read_text() == raw_content
    assert str(raw_path) in result.output
    assert not (feedback_root(root) / "active" / "current.json").exists()
    assert not list((root / ".cmoc/gu/report/feedback").glob("*.md"))
    invocation_report = terminal_primary_report(result)
    assert invocation_report.parent.name == "invocation"
    assert 'terminal_classification: "error"' in invocation_report.read_text()


def test_undefined_raw_json_artifact_blocks_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """raw store の observation 命名外 JSON を無視して正常 publication しない。"""
    root = make_repo(tmp_path)
    _active_session(root, monkeypatch)
    unknown = feedback_root(root) / "observation" / "v1" / "unknown.json"
    unknown.parent.mkdir(parents=True, exist_ok=True)
    unknown.write_text("{}\n")

    result = runner.invoke(app, ["feedback", "report"])

    assert result.exit_code == 1
    assert unknown.exists()
    assert not (feedback_root(root) / "active" / "current.json").exists()


def test_cleanup_corruption_is_a_required_recovery_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """publication 後の state corruption は warning ではなく終了コード 1 にする。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _observation_id, _raw_path, candidate_id = _store_agent_issue(root, session_id)
    _install_codex_outputs(
        monkeypatch, _remediation_output(candidate_id, "human_required")
    )

    def fail_cleanup(_path: Path) -> None:
        raise CmocError(
            "cleanup state is corrupt",
            ["inspect the cleanup manifest"],
            str(_path),
        )

    monkeypatch.setattr(feedback_state_module, "_durable_unlink", fail_cleanup)
    result = runner.invoke(app, ["feedback", "report"])

    assert result.exit_code == 1
    assert "cleanup は未完了" not in result.output
    state = validate_feedback_state(root)
    assert state.current is not None
    assert state.cleanup_manifest is not None
    cut_path = state.cleanup_manifest_path
    assert cut_path is not None
    changed = {**state.cleanup_manifest, "created_at": "2026-01-01T00:00:00Z"}
    cut_path.write_bytes(canonical_json_bytes(changed))
    with pytest.raises(CmocError, match="SHA256"):
        load_active_state(root)
