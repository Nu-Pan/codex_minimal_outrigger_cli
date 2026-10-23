"""feedback の pending observation、active state、atomic publication を検証する。

agent-facing reporter から raw store、intake wave、remediation、current pointer、cleanup
までを同じ repository fixture で追跡する。publication 後に compact active state だけが
残ることを外部境界として検証する。

session fork と live collector の結合は後続 wave の test に残す。保存済み入力を使う
publication・中断・破損検査は feedback_publication_session から始め、doctor の修復、
TCP と実 fsync を繰り返さない。

対応する oracle file:

- `{{work-root}}/spec/app_spec/feedback_observation.md`
- `{{work-root}}/spec/app_spec/console_and_file_log.md`
- `{{work-root}}/spec/app_spec/feedback_state.md`
- `{{work-root}}/spec/app_spec/sub_command/feedback_report.md`
- `{{work-root}}/reference/src/oracle/acp_builder/feedback/normalize_issue.json`
- `{{work-root}}/reference/src/oracle/acp_builder/feedback/remediate_issue.json`
"""

import errno
import hashlib
import itertools
import json
import os
import signal
import socket
import threading
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any, NoReturn
from unittest.mock import Mock

import oracle.other.path_model as path_model_module
import pytest
from _acp_builder_support import oracle_schema_path
from _cli_support import runner, seed_search_config, terminal_primary_report
from _git_support import SESSION_ID, current_branch, make_repo, run_git
from _report_support import assert_report_layout, report_metadata, report_section
from oracle.acp_builder.feedback.normalize_issue import (
    build_feedback_issue_normalization_request as _build_canonical_normalize_parameter,
)
from oracle.acp_builder.feedback.remediate_issue import (
    build_feedback_issue_remediation_request as _build_canonical_remediate_parameter,
)

import commons.runtime_feedback as feedback_module
import commons.runtime_feedback_history as feedback_history_module
import commons.runtime_feedback_protocol as feedback_protocol_module
import commons.runtime_feedback_reporter as reporter_module
import commons.runtime_feedback_state as feedback_state_module
import commons.runtime_feedback_store as feedback_store_module
import commons.runtime_logging as logging_module
import commons.runtime_run_join as run_join_module
import sub_commands.feedback.close as feedback_close_module
import sub_commands.feedback.decision as decision_module
import sub_commands.feedback.recovery as recovery_module
import sub_commands.feedback.remediation as remediation_module
import sub_commands.feedback.report as feedback_report_module
import sub_commands.run.abandon as run_abandon_module
from acp.builder.feedback.normalize_issue import (
    build_feedback_issue_normalization_request,
)
from acp.builder.feedback.remediate_issue import (
    build_feedback_issue_remediation_request,
)
from basic.acp import AgentCallParameter, FileAccessMode
from cmoc_runtime import CmocError, load_state_for_branch
from commons.runtime_feedback import (
    FeedbackInvocation,
    ReporterAvailabilityError,
    begin_feedback_call,
    start_feedback_invocation,
)
from commons.runtime_feedback_close_state import load_close_work
from commons.runtime_feedback_protocol import (
    FEEDBACK_CAPABILITY_ENV,
    FEEDBACK_COLLECTOR_HOST,
    FEEDBACK_COLLECTOR_PORT_ENV,
    FEEDBACK_PROTOCOL_ENV,
    REPORTER_PROTOCOL_VERSION,
)
from commons.runtime_feedback_state import (
    current_pointer_path,
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
from commons.runtime_state import state_path
from main import app


@pytest.fixture
def feedback_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """保存・path・受付の検査に不要な Git と永続採番を準備しない。"""
    root = tmp_path / "repo"
    root.mkdir()
    # 永続採番は test_runtime_ids.py、process 間の共有は test_codex_runtime_paths.py、
    # collector と実採番の結合は validates_context_rate_and_durable_observation に残す。
    ids = itertools.count()

    def in_memory_id(repository: Path, prefix: str) -> str:
        assert repository.resolve() == root.resolve()
        assert prefix in {"exec", "fbo"}
        return f"{prefix}_{next(ids):06d}_2000-01-01_00-00"

    monkeypatch.setattr(feedback_store_module, "new_id", in_memory_id)
    monkeypatch.setattr(logging_module, "new_id", in_memory_id)
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
        "head_commit": (
            head_commit
            if head_commit is not None
            else run_git(root, "rev-parse", "HEAD").stdout.strip()
        ),
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
def stored_feedback_context(
    feedback_directory: Path, monkeypatch: pytest.MonkeyPatch
) -> dict[str, object]:
    """受付・保存内容の検査に、実 evidence file と同期待ちのない context を用意する。"""
    # HEAD の取得は collector test、Git lifecycle は CLI test で検証する。
    # flush の順序・失敗・再保存は test_feedback_store.py、実同期との結合は
    # validates_context_rate_and_durable_observation と後続 wave の test に残す。
    # raw・receipt の write・rename・hash 検査と、TCP の drain・call 分離は実行する。
    monkeypatch.setattr(os, "fsync", lambda _fd: None)
    (feedback_directory / "README.md").write_text("# repo\n")
    return _context(feedback_directory, head_commit="a" * 40)


@pytest.fixture
def collector_directory(
    feedback_directory: Path,
    stored_feedback_context: dict[str, object],
    monkeypatch: pytest.MonkeyPatch,
) -> Path:
    """collector の検査には Git 読み取り結果だけを渡す。"""
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
    """repository を active session の ready 状態にする。"""
    monkeypatch.chdir(root)
    # 管理物の修復・索引同期は session fork 自身の doctor preprocess で行う。
    seed_search_config(root)
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
            "human_action": (
                "README の設定を修正する。" if verdict == "human_required" else None
            ),
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


def _store_agent_issue(root: Path, session_id: str | None) -> tuple[str, Path, str]:
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
    current = feedback_report_module._active_state_input(root, state)
    readers = (
        (lambda: load_active_state(root), state),
        (
            lambda: feedback_state_module._validate_report_cut_current_input(
                root, current, root / "cut.json", allow_missing=False
            ),
            None,
        ),
    )
    reads = []

    def replace_after_read(target):
        content = original_read(target)
        if target == path:
            reads.append(target)
            target.write_bytes(b"{}\n")
        return content

    # active の読込と次の cut の固定入力検査で、同じ publication の準備を共有する。
    for read_state, expected in readers:
        reads.clear()
        try:
            with monkeypatch.context() as snapshot_patch:
                snapshot_patch.setattr(Path, "read_bytes", replace_after_read)
                assert read_state() == expected
                assert reads == [path]
                with pytest.raises(CmocError, match="SHA256"):
                    read_state()
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
        os.pathsep.join(str(source_root / path) for path in ("src", "reference/src")),
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


def test_reporter_availability_propagates_schema_interrupt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """schema 読み込み中の中断を reporter 利用不能へ変換せず伝播する。"""
    # doctor 側の中断伝播は test_doctor_cli.py で確認し、修復・索引同期を重ねない。
    interruption = KeyboardInterrupt()

    def interrupt() -> None:
        raise interruption

    monkeypatch.setattr(feedback_store_module, "reporter_input_schema", interrupt)

    with pytest.raises(KeyboardInterrupt) as caught:
        feedback_module.validate_feedback_reporter_availability()

    assert caught.value is interruption


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


def test_feedback_normalization_preserves_json_and_excludes_search_hint(
    feedback_prompt_directory: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """同じ正本 builder の結果で、JSON 境界・hint 除外・起動設定を検査する。"""
    root = feedback_prompt_directory
    nested = "before\n```\ninside\n```\nafter"
    observation_id = "fbo_000001_2026-08-01_00-00"
    candidate_id = "fbi_" + "a" * 26
    observation = {
        "observation_id": observation_id,
        "payload": {
            "schema_version": 2,
            "category": "tooling",
            "summary": nested,
            "impact": "候補検索用の hint を含む。",
            "evidence": [{"kind": "file", "path": "README.md"}],
        },
    }
    expected_observation = deepcopy(observation)
    observation["payload"]["deduplication_hint"] = "候補検索だけに使う文字列"
    candidate = {
        "candidate_id": candidate_id,
        "origin": "agent_report",
        "category": "tooling",
        "summary": nested,
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
        assert not parameter.enable_feedback_reporting
        assert "cmoc_feedback.submit_observation" not in parameter.prompt
        assert "# routing policy" in parameter.prompt
        assert "# oracle and realization basic" in parameter.prompt
        captured_prompts.append(parameter.prompt)
        return SimpleNamespace(
            output_json={"result": {"decision": "new", "existing_issue_id": None}}
        )

    monkeypatch.setattr(feedback_report_module, "run_codex_exec", fake_run_codex_exec)
    # 保存・読戻し・破損検査は test_feedback_reconfirmation.py に残す。
    monkeypatch.setattr(
        feedback_report_module, "write_immutable_artifact", lambda *_args: {}
    )
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
    prompt = captured_prompts[0]
    assert "deduplication_hint" not in prompt
    assert "候補検索だけに使う文字列" not in prompt

    # JSON 境界と入力保存の検査にも同じ構築結果を使い、prompt の再描画を省く。
    observation_start = prompt.index("# 構造化済み observation")
    observation_end = prompt.index("\n\n# 既存 issue candidate", observation_start)
    candidate_start = observation_end + 2
    candidate_end = prompt.index("\n\n# place holder definition", candidate_start)
    observation_section = prompt[observation_start:observation_end]
    candidate_section = prompt[candidate_start:candidate_end]
    for section, heading, expected in (
        (observation_section, "構造化済み observation", expected_observation),
        (candidate_section, "既存 issue candidate", [candidate]),
    ):
        prefix = f"# {heading}\n\n````json\n"
        suffix = "\n````"
        assert section.startswith(prefix)
        assert section.endswith(suffix)
        assert json.loads(section[len(prefix) : -len(suffix)]) == expected


def test_feedback_remediate_builder_disables_reporting(
    feedback_prompt_directory: Path,
) -> None:
    """remediation は追加報告を無効化し、prompt からも報告指示を外す。"""
    root = feedback_prompt_directory
    parameter = build_feedback_issue_remediation_request(
        json.dumps({"issue_id": "fbi_" + "a" * 26}),
        root,
    )

    assert not parameter.enable_feedback_reporting
    assert "cmoc_feedback.submit_observation" not in parameter.prompt


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
        build_feedback_issue_normalization_request
        is _build_canonical_normalize_parameter
    )
    assert (
        build_feedback_issue_remediation_request is _build_canonical_remediate_parameter
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
    original_inventory = os.scandir
    reads = []
    inventories = []

    def replace_after_read(path):
        value = original_read(path)
        if path == raw:
            reads.append(path)
            path.write_bytes(canonical_json_bytes(changed))
        return value

    def inventory(path):
        if path == raw.parent:
            inventories.append(path)
        return original_inventory(path)

    def load():
        if reader == "pending":
            entries, observations = feedback_report_module._pending_observations(root)
            assert entries == [entry]
            return observations
        return feedback_report_module._read_cut_observations(
            root, {"inputs": {"observations": [entry]}}
        )

    monkeypatch.setattr(Path, "read_bytes", replace_after_read)
    monkeypatch.setattr(os, "scandir", inventory)

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


def test_pending_observations_rejects_undefined_raw_json_artifact(
    feedback_directory: Path,
) -> None:
    """命名外 JSON を無視せず拒否し、raw の内容と診断 path を保持する。"""
    # CLI の未公開・error report は test_invalid_raw_observation_blocks_publication に残す。
    root = feedback_directory
    unknown = feedback_root(root) / "observation" / "v1" / "unknown.json"
    unknown.parent.mkdir(parents=True)
    raw_content = b"{}\n"
    unknown.write_bytes(raw_content)

    with pytest.raises(CmocError, match="raw store の検査") as error:
        feedback_report_module._pending_observations(root)

    assert str(unknown) in error.value.detail
    assert unknown.read_bytes() == raw_content


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
    references = [
        {
            "reference_id": "ref:readme",
            "kind": "repository_content",
            "subjects": [observation["observation_id"]],
            "path": "README.md",
            "state": "hashed",
            "sha256": "b" * 64,
        }
    ]

    current_cut = feedback_report_module._report_cut_fingerprint_pairs(
        Path("/repo"), references, observation
    )
    exact, comparison = feedback_report_module._agent_comparison_candidates(
        observation,
        {str(candidate["candidate_id"]): candidate},
        current_cut_fingerprint_pairs=current_cut,
    )

    assert exact is None
    assert comparison == [candidate]


def test_report_cut_without_fingerprints_skips_path_resolution(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """path fingerprint がなければ参照解決を省き、後の照合では現在の入力を使う。"""
    observation = {
        "observation_id": "fbo_000001_2026-08-01_00-00",
        "evidence_fingerprints": [],
    }
    fingerprint = {
        "normalized_path": str(tmp_path / "README.md"),
        "state": "hashed",
        "sha256": "a" * 64,
    }
    references = [
        {
            "kind": "repository_content",
            "subjects": [observation["observation_id"]],
            "path": "README.md",
            "state": fingerprint["state"],
            "sha256": fingerprint["sha256"],
        }
    ]
    resolve_path = Mock(wraps=feedback_report_module._repository_path)
    monkeypatch.setattr(feedback_report_module, "_repository_path", resolve_path)

    assert (
        feedback_report_module._report_cut_fingerprint_pairs(
            tmp_path, references, observation
        )
        == []
    )
    resolve_path.assert_not_called()

    observation["evidence_fingerprints"].append(fingerprint)
    assert feedback_report_module._report_cut_fingerprint_pairs(
        tmp_path, references, observation
    ) == [(fingerprint["normalized_path"], "hashed", "a" * 64)]


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
    committed_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """loopback reporter 経由の受理、rate limit、失効を確認する。"""
    # 実 HEAD と evidence file は残し、履歴内容を使わない準備を省く。
    root = committed_repository
    (root / "README.md").write_text("# repo\n")
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
    feedback_directory: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """timeout に頼らず接続待ちを解除し、停止を障害として記録しない。"""
    root = feedback_directory
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
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


def test_collector_protocol_probe_does_not_report_expected_degradation(
    feedback_directory: Path,
) -> None:
    """実 TCP の transport probe と通常停止で warning を追加しない。"""
    root = feedback_directory
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    invocation.start()
    try:
        assert invocation.collector_port is not None
        feedback_module._validate_collector_protocol(invocation.collector_port)
    finally:
        invocation.stop()
    assert invocation._server_thread is not None
    assert not invocation._server_thread.is_alive()
    assert logger.warning_messages == []


def test_collector_stop_handles_unavailable_shutdown_without_degradation(
    feedback_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """shutdown 失敗後の accept timeout と thread 回収を実時間の待機なしで検査する。"""
    root = feedback_directory
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    accept_started = threading.Event()
    shutdown_attempted = threading.Event()

    # 実 TCP の probe は上のケースに残し、OS の timeout だけを決定論的に発生させる。
    # collector の start・serve・stop と実 thread の終了は置換しない。
    def accept_until_timeout(listener: socket.socket) -> NoReturn:
        assert listener is invocation._listener
        accept_started.set()
        assert shutdown_attempted.wait(timeout=2)
        raise TimeoutError("injected accept timeout")

    def fail_shutdown(listener: socket.socket, _how: int) -> NoReturn:
        assert listener is invocation._listener
        shutdown_attempted.set()
        raise OSError("injected shutdown failure")

    monkeypatch.setattr(socket.socket, "accept", accept_until_timeout)
    monkeypatch.setattr(socket.socket, "shutdown", fail_shutdown)
    invocation.start()
    try:
        assert accept_started.wait(timeout=2)
        invocation.stop()

        assert shutdown_attempted.is_set()
        assert invocation._server_thread is not None
        assert not invocation._server_thread.is_alive()
        assert invocation._listener is None
        assert invocation.collector_port is None
        assert logger.warning_messages == []
    finally:
        # assertion が失敗しても accept を解除し、test の thread を残さない。
        shutdown_attempted.set()
        invocation.stop()


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
    close_progress = threading.Event()
    close_finished = threading.Event()
    submission_result: dict[str, object] = {}
    submission_errors: list[BaseException] = []
    close_errors: list[BaseException] = []
    submission_thread: threading.Thread | None = None
    close_thread: threading.Thread | None = None
    original_store = feedback_module.store_agent_observation
    original_wait = invocation._condition.wait

    def observe_drain_wait(timeout: float | None = None) -> bool:
        # 固定時間ではなく、実際の drain 待機を観測する。lock の解放・再取得は実物に任せる。
        close_progress.set()
        return original_wait(timeout)

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

    monkeypatch.setattr(invocation._condition, "wait", observe_drain_wait)
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
            try:
                if stop_invocation:
                    invocation.stop()
                else:
                    invocation.close_call(call)
            except BaseException as exc:
                close_errors.append(exc)
            finally:
                close_finished.set()
                # drain を省いて終了する回帰でも親 thread を起こし、即座に失敗させる。
                close_progress.set()

        submission_thread = threading.Thread(target=submit)
        submission_thread.start()
        assert storage_started.wait(timeout=2)
        close_thread = threading.Thread(target=close_context)
        close_thread.start()
        assert close_progress.wait(timeout=2)
        with invocation._condition:
            assert not close_finished.is_set()
            assert not call.accepting
            assert call.inflight == 1
            assert call.capability in invocation._calls

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


@pytest.mark.parametrize("stalled", [True, False], ids=["idle", "trickle"])
def test_collector_limits_unauthenticated_request_read_time(
    feedback_directory: Path, monkeypatch: pytest.MonkeyPatch, stalled: bool
) -> None:
    """無応答と小分け受信の両方を、実時間の待機なしで deadline 拒否する。"""
    root = feedback_directory
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    budget = feedback_module._COLLECTOR_IO_TIMEOUT_SECONDS
    clock = SimpleNamespace(now=0.0)
    monkeypatch.setattr(
        feedback_module, "time", SimpleNamespace(monotonic=lambda: clock.now)
    )
    # 受信ごとの timeout は超えないが、二つ目の断片で絶対 deadline を超える。
    # deadline を毎回延長する回帰では、三つ目まで読めて probe が accepted になる。
    chunks = iter(
        [
            b'{"protocol":',
            json.dumps(REPORTER_PROTOCOL_VERSION).encode("utf-8"),
            b',"_protocol_probe":true}\n',
        ]
    )
    read_timeouts = []
    response = bytearray()

    class IncompleteConnection:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def settimeout(self, seconds):
            self.timeout = seconds

        def recv(self, _size):
            read_timeouts.append(self.timeout)
            if stalled and len(read_timeouts) == 2:
                raise TimeoutError("injected idle connection")
            clock.now += budget * 0.75
            return next(chunks)

        def sendall(self, value):
            response.extend(value)

    # framing・拒否応答・warning は実 worker を通す。TCP の結合は受理・drain test に残す。
    invocation._handle_connection(IncompleteConnection())  # type: ignore[arg-type]

    assert read_timeouts == pytest.approx([budget, budget * 0.25])
    assert json.loads(response) == {
        "status": "rejected",
        "code": "transport_unavailable",
        "message": "collector could not process the request",
        "retryable": True,
    }
    assert logger.warning_messages == [
        "feedback submission rejected (transport_unavailable)"
    ]


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


@pytest.mark.parametrize("redaction", ["none", "text", "path"])
def test_agent_payload_shares_repository_resolution(
    feedback_directory, monkeypatch, redaction
):
    """root の解決だけを共有し、置換後の path と次の submission は再検査する。"""
    root = feedback_directory
    repo_alias = root.parent / "repo-link"
    repo_alias.symlink_to(root, target_is_directory=True)
    raw_path = "Authorization:x" if redaction == "path" else "evidence.txt"
    masked_path = "[REDACTED:authorization]" if redaction == "path" else raw_path
    (root / raw_path).write_bytes(b"original evidence\n")
    target = root / masked_path
    if redaction == "path":
        target.write_bytes(b"redacted path evidence\n")
    text = "failure Authorization:x" if redaction == "text" else "evidence"
    payload = {
        **_payload(),
        "evidence": [{"kind": "command", "text": "failed command"}]
        + [
            {"kind": kind, "text": text, "path": raw_path}
            for kind in ("file", "oracle", "log")
        ],
    }
    original = canonical_json_bytes(payload)
    resolve = Path.resolve
    root_resolutions = []

    def resolve_path(path, *args, **kwargs):
        if path in (root, repo_alias):
            root_resolutions.append(path)
        return resolve(path, *args, **kwargs)

    monkeypatch.setattr(Path, "resolve", resolve_path)

    masked, fingerprints, count = validate_agent_payload(payload, repo_alias)

    assert masked["evidence"] == [{"kind": "command", "text": "failed command"}] + [
        {
            "kind": kind,
            "text": "failure [REDACTED:authorization]" if redaction == "text" else text,
            "path": masked_path,
        }
        for kind in ("file", "oracle", "log")
    ]
    assert fingerprints == [
        {
            "evidence_index": index,
            "normalized_path": str(target),
            "state": "hashed",
            "sha256": sha256_bytes(target.read_bytes()),
        }
        for index in (1, 2, 3)
    ]
    assert count == 3 * int(redaction != "none")
    assert canonical_json_bytes(payload) == original
    # evidence ごとの root 解決による filesystem 読み取りの性能回帰を検出する。
    assert len(root_resolutions) == 1

    (root / raw_path).unlink()
    (root / raw_path).symlink_to(root.parent / "outside.txt")
    with pytest.raises(FeedbackRejected) as outside:
        validate_agent_payload(payload, repo_alias)
    assert outside.value.code == "path_outside_repo"


@pytest.mark.parametrize("retarget_during", ["masking", "fingerprinting"])
def test_agent_payload_rechecks_evidence_after_masking(
    feedback_directory, monkeypatch, retarget_during
):
    """処理中に重複 evidence の symlink が repo 外へ変わった場合も拒否する。"""
    root = feedback_directory
    (root / "evidence.txt").write_text("evidence")
    alias = root / "alias"
    alias.symlink_to("evidence.txt")

    def retarget():
        alias.unlink()
        alias.symlink_to(root.parent / "outside.txt")

    if retarget_during == "masking":
        mask = feedback_store_module._mask_payload

        def mask_and_retarget(value):
            retarget()
            monkeypatch.setattr(feedback_store_module, "_mask_payload", mask)
            return mask(value)

        monkeypatch.setattr(feedback_store_module, "_mask_payload", mask_and_retarget)
    else:
        read = Path.read_bytes

        def read_and_retarget(path):
            content = read(path)
            retarget()
            return content

        monkeypatch.setattr(Path, "read_bytes", read_and_retarget)

    payload = _payload(path="alias")
    payload["evidence"] *= 2
    with pytest.raises(FeedbackRejected) as outside:
        validate_agent_payload(payload, root)
    assert outside.value.code == "path_outside_repo"


@pytest.mark.parametrize("state", ["hashed", "missing", "not_file", "unreadable"])
def test_agent_payload_shares_fingerprints_only_within_submission(
    feedback_directory, monkeypatch, state
):
    """同じ正規化先の読み取りを共有し、別 file と次の submission は再取得する。"""
    root = feedback_directory
    target = root / "evidence.txt"
    other = root / "other.txt"
    other.write_bytes(b"other evidence")
    if state == "not_file":
        target.mkdir()
    elif state != "missing":
        target.write_bytes(b"original evidence")
    (root / "alias").symlink_to(target)
    payload = {
        **_payload(),
        "evidence": [
            {"kind": kind, "text": "observed failure", "path": path}
            for kind, path in (
                ("file", "evidence.txt"),
                ("oracle", "./evidence.txt"),
                ("log", "alias"),
                ("file", "other.txt"),
            )
        ],
    }
    original = canonical_json_bytes(payload)
    read = Path.read_bytes
    reads = []
    unreadable = state == "unreadable"

    def read_evidence(path):
        reads.append(path)
        if path == target and unreadable:
            raise PermissionError("injected unreadable evidence")
        return read(path)

    monkeypatch.setattr(Path, "read_bytes", read_evidence)

    for attempt, (current_state, content) in enumerate(
        ((state, b"original evidence"), ("hashed", b"updated evidence"))
    ):
        if attempt:
            if state == "not_file":
                target.rmdir()
            target.write_bytes(content)
            unreadable = False
        reads.clear()

        masked, fingerprints, redactions = validate_agent_payload(payload, root)

        assert masked == payload
        assert redactions == 0
        expected_target = {
            "normalized_path": str(target),
            "state": current_state,
            "sha256": sha256_bytes(content) if current_state == "hashed" else None,
        }
        assert fingerprints == [
            {"evidence_index": index, **expected_target} for index in range(3)
        ] + [
            {
                "evidence_index": 3,
                "normalized_path": str(other),
                "state": "hashed",
                "sha256": sha256_bytes(b"other evidence"),
            }
        ]
        assert reads.count(target) == int(current_state in {"hashed", "unreadable"})
        assert reads.count(other) == 1
        assert canonical_json_bytes(payload) == original


def test_agent_payload_without_path_evidence_skips_repository_resolution(
    feedback_directory, monkeypatch
):
    """path を検査しない submission で filesystem の解決を追加しない。"""
    monkeypatch.setattr(
        Path,
        "resolve",
        lambda *_args, **_kwargs: pytest.fail("unneeded path resolution"),
    )
    payload = _payload(kind="error", path=None)
    assert validate_agent_payload(payload, feedback_directory) == (payload, [], 0)


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

    (root / "[REDACTED:authorization]").symlink_to(outside / "missing.txt")
    with pytest.raises(FeedbackRejected) as redacted_outside:
        store_agent_observation(
            root, stored_feedback_context, _payload(path="Authorization:x")
        )
    assert redacted_outside.value.code == "path_outside_repo"

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


def test_report_cut_references_share_resolution_and_refresh_between_captures(
    feedback_directory, tmp_path, monkeypatch
):
    root = feedback_directory
    readme = root / "README.md"
    readme.write_text("before\n")
    nested = root / "nested"
    nested.mkdir()
    (nested / "subject.md").write_text("inside\n")
    alias = root / "alias"
    alias.symlink_to(nested, target_is_directory=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "subject.md").write_text("must not be read\n")
    observations = {
        "first": {
            "payload": {"summary": "first", "evidence": []},
            "evidence_fingerprints": [
                {"normalized_path": "README.md"},
                {"normalized_path": "README.md"},
                {"normalized_path": None},
            ],
            "source_event": {"log_path": "README.md"},
        },
        "second": {
            "evidence_fingerprints": [
                {"normalized_path": "README.md"},
                {"normalized_path": "./README.md"},
                {"normalized_path": "alias/subject.md"},
                {"normalized_path": "../outside/subject.md"},
            ],
        },
    }
    issues = {
        "active": {
            "reference_targets": [{"path": "README.md"}, {"path": None}],
            "verification": {
                "current_evidence": [
                    {"path": "README.md"},
                    {"path": "alias/subject.md"},
                ]
            },
        }
    }
    resolve = Mock(wraps=feedback_report_module._repository_path)
    monkeypatch.setattr(feedback_report_module, "_repository_path", resolve)
    read = Mock(wraps=Path.read_bytes)
    monkeypatch.setattr(Path, "read_bytes", lambda path: read(path))

    def capture():
        resolve.reset_mock()
        read.reset_mock()
        references = feedback_report_module._capture_report_cut_references(
            root, observations, issues
        )
        resolved = [call.args[1] for call in resolve.call_args_list]
        assert len(resolved) == len(set(resolved)) == 4
        assert set(resolved) == {
            "README.md",
            "./README.md",
            "alias/subject.md",
            "../outside/subject.md",
        }
        observation_refs = {
            reference["reference_id"]: reference
            for reference in references
            if reference["kind"] == "observation"
        }
        assert set(observation_refs) == {"obs:first", "obs:second"}
        assert observation_refs["obs:first"]["summary"] == "first"
        return {
            reference["path"]: reference
            for reference in references
            if reference["kind"] != "observation"
        }

    before = capture()
    assert set(before) == {"README.md", "alias/subject.md"}
    assert before["README.md"]["subjects"] == ["active", "first", "second"]
    assert before["README.md"]["sha256"] == sha256_bytes(b"before\n")
    assert before["alias/subject.md"]["subjects"] == ["active", "second"]
    assert before["alias/subject.md"]["sha256"] == sha256_bytes(b"inside\n")
    assert {call.args[0] for call in read.call_args_list} == {
        readme,
        alias / "subject.md",
    }
    assert read.call_count == 2

    readme.write_text("after\n")
    alias.unlink()
    alias.symlink_to(outside, target_is_directory=True)
    after = capture()
    assert set(after) == {"README.md"}
    assert after["README.md"]["subjects"] == before["README.md"]["subjects"]
    assert after["README.md"]["sha256"] == sha256_bytes(b"after\n")
    read.assert_called_once_with(readme)


def test_candidate_building_skips_empty_comparison_and_merges_resolved_evidence(
    feedback_directory: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """参照の再走査を省き、同じ wave の alias と実体 path は同じ issue にする。"""
    root = feedback_directory
    target_directory = root / "nested"
    target_directory.mkdir()
    target = target_directory / "README.md"
    target.write_text("subject\n")
    (root / "alias").symlink_to(target_directory, target_is_directory=True)

    # raw 保存・receipt 登録は collector と intake/store の test に残す。
    # 保存直前の envelope を使い、path 解決・fingerprint・context の受け渡しを検査する。
    capture = Mock(return_value=root / "observation.json")
    monkeypatch.setattr(feedback_store_module, "_store_observation", capture)
    context = _context(root, head_commit="a" * 40)

    def observation(evidence_path: str) -> dict[str, object]:
        store_agent_observation(
            root,
            context,
            _payload(path=evidence_path),
        )
        return capture.call_args.args[3]

    first = observation("alias/README.md")
    second = observation("nested/README.md")
    fingerprint = second["evidence_fingerprints"][0]
    observations = {item["observation_id"]: item for item in (first, second)}

    class References(list):
        scans = 0

        def __iter__(self):
            self.scans += 1
            return super().__iter__()

    current_reference = {
        "reference_id": "ref:readme",
        "kind": "repository_content",
        "subjects": list(observations),
        "path": "nested/README.md",
        "state": fingerprint["state"],
        "sha256": fingerprint["sha256"],
    }
    shared_reference = {
        "reference_id": "ref:shared",
        "kind": "observation",
        # 同じ参照が複数 subject と重複 subject に属しても、一度だけ採用する。
        "subjects": [*observations, first["observation_id"]],
    }
    references = References(
        [
            current_reference,
            {
                **current_reference,
                "reference_id": "ref:unrelated",
                "subjects": ["other"],
                "sha256": "0" * 64,
            },
            shared_reference,
        ]
    )
    manifest = {
        "cut_at": second["observed_at"],
        "inputs": {"references": references},
    }
    current_cut = Mock(wraps=feedback_report_module._report_cut_fingerprint_pairs)
    monkeypatch.setattr(
        feedback_report_module, "_report_cut_fingerprint_pairs", current_cut
    )

    candidates, aggregates = feedback_report_module._build_candidates(
        root,
        root,
        manifest,
        observations,
        SimpleNamespace(issues={}, machine_aggregates={}),
    )

    [candidate] = candidates.values()
    assert candidate["candidate_id"] == issue_id(f"agent\0{first['observation_id']}")
    assert candidate["occurrence_count"] == 2
    assert candidate["source_observation_ids"] == sorted(observations)
    assert candidate["reference_targets"] == [
        {"path": "nested/README.md", "kind": "file", "location": None}
    ]
    assert candidate["reference_ids"] == ["ref:readme", "ref:shared"]
    assert aggregates == {}
    assert references.scans == 1
    current_cut.assert_called_once_with(
        root, [current_reference, shared_reference], second
    )


def test_candidate_references_follow_subjects_and_refresh_between_waves(
    tmp_path: Path,
) -> None:
    """candidate と観測の参照を合併し、他候補との分離と wave ごとの更新を保つ。"""
    first, second = (
        {
            "candidate_id": issue_id(f"agent\0{index}"),
            "origin": "agent_report",
            "source_observation_ids": [f"fbo_{index:06d}_2026-10-08_00-00"],
            "reference_ids": ["ref:stale"],
        }
        for index in range(2)
    )
    candidates = {item["candidate_id"]: item for item in (first, second)}
    manifest = {
        "cut_at": "2026-10-08T00:00:00Z",
        "inputs": {
            "references": [
                {"reference_id": "ref:z", "subjects": [first["candidate_id"]]},
                {
                    "reference_id": "ref:m",
                    "subjects": [
                        first["candidate_id"],
                        *first["source_observation_ids"],
                        second["candidate_id"],
                    ],
                },
                {"reference_id": "ref:a", "subjects": first["source_observation_ids"]},
                {"reference_id": "ref:unrelated", "subjects": ["unrelated"]},
            ]
        },
    }

    def build():
        return feedback_report_module._build_candidates(
            tmp_path,
            tmp_path,
            manifest,
            {},
            SimpleNamespace(issues={}, machine_aggregates={}),
            previous_candidates=candidates,
        )

    build()
    assert first["reference_ids"] == ["ref:a", "ref:m", "ref:z"]
    assert second["reference_ids"] == ["ref:m"]

    manifest["inputs"]["references"] = [
        {"reference_id": "ref:next", "subjects": second["source_observation_ids"]}
    ]
    build()
    assert first["reference_ids"] == []
    assert second["reference_ids"] == ["ref:next"]


def test_report_reference_rechecks_kind_and_content_without_repeated_stat(
    feedback_directory, monkeypatch
):
    """種類照会を重ねず、次回の capture では種類・本文・取得失敗を取り直す。"""
    root = feedback_directory
    path = root / "reference"
    original_stat = Path.stat
    original_read = Path.read_bytes
    inspections = []
    reads = []
    stat_error = None
    read_error = None

    def inspect(target, *args, **kwargs):
        if target == path:
            inspections.append(target)
            if stat_error:
                raise stat_error
        return original_stat(target, *args, **kwargs)

    def read(target):
        reads.append(target)
        assert target == path
        if read_error:
            raise read_error
        return original_read(target)

    monkeypatch.setattr(Path, "stat", inspect)
    monkeypatch.setattr(Path, "read_bytes", read)

    def capture(state, content=None):
        inspections.clear()
        reads.clear()
        reference = feedback_report_module._capture_repository_reference(
            root, path, ["subject"]
        )
        assert reference["path"] == "reference"
        assert reference["subjects"] == ["subject"]
        assert reference["state"] == state
        assert reference["sha256"] == (
            sha256_bytes(content) if content is not None else None
        )
        assert reference["kind"] == (
            "repository_content" if content == b"text\n" else "current_fingerprint"
        )
        assert reads == ([path] if content is not None or read_error else [])
        assert len(inspections) <= 1
        return reference

    capture("missing")
    path.mkdir()
    capture("not_file")
    path.rmdir()
    path.write_bytes(b"text\n")
    assert capture("hashed", b"text\n")["content"] == "text\n"
    path.write_bytes(b"\xff")
    capture("hashed", b"\xff")
    # metadata 取得失敗と、種類確認後の読取失敗を区別して注入する。
    stat_error = PermissionError("injected stat failure")
    capture("unreadable")
    for code in (errno.ENOENT, errno.ENOTDIR, errno.EBADF, errno.ELOOP):
        stat_error = OSError(code, "injected missing path")
        capture("missing")
    stat_error = None
    for read_error in (PermissionError("unreadable"), FileNotFoundError("removed")):
        capture("unreadable")
    read_error = None
    target = root / "target"
    path.rename(target)
    path.symlink_to(target)
    capture("unreadable")
    target.unlink()
    capture("unreadable")
    path.unlink()
    capture("missing")


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
    committed_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """対象 event でだけ context を取得し、再検出を同じ raw 一件へ収束させる。"""
    # 検証対象は実 HEAD と log event なので、追跡 file は用意しない。
    root = committed_repository
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
    head_query.assert_called_once_with(root)
    invocation.detect_event(event, logger.path)
    assert head_query.call_count == 2

    [path] = iter_observation_paths(root)
    observation = read_json_object(path)
    assert validate_observation_envelope(observation) == []
    assert observation["source_event"]["event_id"] == event["event_id"]
    assert observation["context"]["head_commit"] == original_head(root)
    assert observation["context"]["subcommand_invocation_id"] == logger.execution_id


def test_machine_detector_masks_secret_in_event_values_and_keys(
    collector_directory: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """値だけ・キーだけの secret を、共通 collector の独立 event で検証する。"""
    root = collector_directory
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    secret = "Authorization: Bearer abcdefghijklmnopqrstuvwxyz"
    cases = {
        "evt_machine_secret_value": (
            {"header": secret},
            {"header": "[REDACTED:authorization]"},
            "a" * 40,
        ),
        "evt_machine_secret_key": (
            {secret: "value"},
            {"[REDACTED:authorization]": "value"},
            "b" * 40,
        ),
    }
    # 後続 event の HEAD も取り直すことを、追加の Git 準備や保存なしで検査する。
    monkeypatch.setattr(
        feedback_module,
        "head_commit",
        Mock(side_effect=[commit for _, _, commit in cases.values()]),
    )
    for event_id, (diagnostic, _, _) in cases.items():
        invocation.detect_event(
            {
                "event_schema_version": 1,
                "event_id": event_id,
                "event_type": "feedback.reporter_unavailable",
                "occurred_at": rfc3339_now(),
                "subcommand_invocation_id": logger.execution_id,
                "component": "collector",
                "failure_code": "protocol_error",
                "diagnostic": diagnostic,
            },
            logger.path,
        )

    paths = iter_observation_paths(root)
    assert len(paths) == len(cases)
    for path in paths:
        observation = read_json_object(path)
        _, expected_diagnostic, expected_head = cases[
            observation["source_event"]["event_id"]
        ]
        assert secret not in path.read_text(encoding="utf-8")
        assert (
            observation["payload"]["event_fields"]["diagnostic"] == expected_diagnostic
        )
        assert observation["context"]["head_commit"] == expected_head
        assert validate_observation_envelope(observation) == []


def test_completion_count_reports_only_pending_raw_observations(
    feedback_directory: Path, stored_feedback_context: dict[str, object]
) -> None:
    """正常 report 前は raw store の pending 件数一値だけを返す。"""
    root = feedback_directory
    store_agent_observation(root, stored_feedback_context, _payload())

    assert feedback_completion_counts(root) == (1, [])


def test_completion_count_threshold_stops_unneeded_reads(tmp_path, monkeypatch):
    """同じ pending 集合へ一件追加し、件数境界の通知と読み取り抑制を検証する。"""
    now = datetime(2030, 1, 8, tzinfo=timezone.utc)
    monkeypatch.setattr(
        feedback_store_module,
        "datetime",
        SimpleNamespace(now=lambda _zone: now, fromisoformat=datetime.fromisoformat),
    )
    read = Mock(return_value={"observed_at": now.isoformat()})
    monkeypatch.setattr(feedback_store_module, "read_json_object", read)

    # 実 inventory・JSON 読取との結合は reports_only_pending_raw_observations、
    # 不正 artifact と消費済み raw の除外は専用ケースに残す。通知境界には一覧だけを渡す。
    for count, expected_warning, max_reads in ((99, False, 99), (100, True, 0)):
        paths = [
            tmp_path / f"fbo_{index:06d}_2030-01-08_00-00.json"
            for index in range(count)
        ]
        monkeypatch.setattr(
            feedback_store_module, "unprocessed_observation_paths", lambda _root: paths
        )
        read.reset_mock()

        pending, warnings = feedback_completion_counts(tmp_path)

        assert pending == count
        assert bool(warnings) is expected_warning
        if warnings:
            assert "cmoc feedback report" in warnings[0]
        assert read.call_count <= max_reads


@pytest.mark.parametrize(
    ("oldest_age", "expected_warning", "max_reads"),
    [
        pytest.param(
            timedelta(days=7) - timedelta(microseconds=1),
            False,
            2,
            id="below-age-limit",
        ),
        pytest.param(timedelta(days=7), True, 1, id="at-age-limit"),
    ],
)
def test_completion_age_threshold_stops_unneeded_reads(
    tmp_path,
    monkeypatch,
    oldest_age,
    expected_warning,
    max_reads,
):
    """経過日数の境界を守り、通知が確定した後の raw 本文読み取りを省く。"""
    now = datetime(2030, 1, 8, tzinfo=timezone.utc)
    observations = {
        tmp_path / "fbo_000000_2030-01-01_00-00.json": (now - oldest_age).isoformat(),
        tmp_path / "fbo_000001_2030-01-08_00-00.json": now.isoformat(),
    }
    # 日時の判定と読取の打ち切りを検査し、保存・inventory の準備を繰り返さない。
    monkeypatch.setattr(
        feedback_store_module,
        "unprocessed_observation_paths",
        lambda _root: list(observations),
    )
    monkeypatch.setattr(
        feedback_store_module,
        "datetime",
        SimpleNamespace(now=lambda _zone: now, fromisoformat=datetime.fromisoformat),
    )
    read = Mock(side_effect=lambda path: {"observed_at": observations[path]})
    monkeypatch.setattr(feedback_store_module, "read_json_object", read)

    pending, warnings = feedback_completion_counts(tmp_path)

    assert pending == 2
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
def test_feedback_output_validation_uses_current_schema_file(
    tmp_path: Path, schema_name: str
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

    # 準備を schema ごとに共有し、各破損からの復旧も同じ file で検査する。
    for change in ("contract", "json", "schema", "missing"):
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

        assert not validate(output, schema_path), change

        schema_path.write_text(schema_text, encoding="utf-8")
        assert validate(output, schema_path), change


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
@pytest.mark.parametrize(
    "link_kind",
    ["file", "parent", "parent_traversal", "dangling", "missing_parent_traversal"],
)
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
    if link_kind in {"parent", "parent_traversal"}:
        alias_parent = expected_root / "alias"
        alias_parent.symlink_to(expected_root, target_is_directory=True)
        # .. の正規化で symlink の要素を消してから検査してはならない。
        alias = (
            alias_parent / ".." / target.name
            if link_kind == "parent_traversal"
            else alias_parent / target.name
        )
    else:
        alias = expected_root / "alias.json"
        alias.symlink_to(
            target
            if link_kind in {"file", "missing_parent_traversal"}
            else expected_root / "missing"
        )
        if link_kind == "missing_parent_traversal":
            # 欠落した親で lstat が失敗しても、正規化先の symlink を見逃さない。
            alias = expected_root / "missing" / ".." / alias.name

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

    def validate(value, expected_root=directory):
        return feedback_state_module._validate_artifact_reference(
            root,
            value,
            expected_root=expected_root,
            description="state artifact",
            allow_missing=allow_missing,
        )

    assert validate(reference) == target
    (directory / "nested").mkdir()
    assert validate({**reference, "path": "artifacts/nested/../record.json"}) == target
    assert validate(reference, directory / "nested/..") == target
    assert (
        validate(reference, directory.relative_to(Path.cwd(), walk_up=True)) == target
    )
    # 期待 root の別表記も解決し、呼び出し間の retarget を cache しない。
    root_alias = root / "root-alias"
    root_alias.symlink_to(directory, target_is_directory=True)
    assert validate(reference, root_alias) == target
    root_alias.unlink()
    root_alias.symlink_to(root / "elsewhere", target_is_directory=True)
    with pytest.raises(CmocError, match="期待 root 外"):
        validate(reference, root_alias)
    with pytest.raises(CmocError, match="期待 root 外"):
        validate({**reference, "path": "artifacts-neighbor/record.json"})
    with pytest.raises(CmocError, match="期待 root 外"):
        validate({**reference, "path": "artifacts/../outside.json"})
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


@pytest.mark.parametrize(
    "artifact", ["unknown", "file_symlink", "directory_symlink", "dangling", "fifo"]
)
def test_completion_count_warns_instead_of_ignoring_invalid_raw_artifact(
    feedback_directory: Path, artifact: str
) -> None:
    """raw store inventory が不正なら件数を推測せず unavailable warning を返す。"""
    root = feedback_directory
    invalid = feedback_root(root) / "observation" / "v1" / "2030/01/02/fbo_invalid.json"
    invalid.parent.mkdir(parents=True, exist_ok=True)
    if artifact == "unknown":
        invalid = invalid.with_name("unexpected.tmp")
        invalid.write_text("partial")
    elif artifact == "fifo":
        os.mkfifo(invalid)
    else:
        target = root / "target"
        if artifact == "file_symlink":
            target.write_text("{}\n")
        elif artifact == "directory_symlink":
            target.mkdir()
        invalid.symlink_to(target, target_is_directory=artifact == "directory_symlink")

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


@pytest.mark.parametrize("location", ["root", "nested"])
def test_pending_inventory_rejects_unreadable_directory(
    feedback_directory, monkeypatch, location
):
    """列挙失敗を空の入力として通知・report に渡さない。"""
    root = feedback_directory
    raw_root = feedback_store_module.observation_root(root)
    nested = raw_root / "2030/01/02"
    nested.mkdir(parents=True)
    (nested / "fbo_invalid.json").write_text("{}\n")
    blocked = raw_root if location == "root" else nested
    original_scan = os.scandir

    def scan(path):
        if path == blocked:
            raise PermissionError(13, "injected unreadable directory", str(path))
        return original_scan(path)

    monkeypatch.setattr(os, "scandir", scan)

    pending, warnings = feedback_completion_counts(root)
    assert pending is None
    assert warnings
    with pytest.raises(CmocError, match="raw store の検査"):
        feedback_report_module._pending_observations(root)


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
    feedback_publication_session: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """candidate がなくても ok report と空 active generation を atomic publication する。"""
    root = feedback_publication_session
    log_dir = root / ".cmoc/gu/log/sub_command"
    previous_logs = set(log_dir.glob("*.jsonl"))
    monkeypatch.setattr(
        feedback_report_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: pytest.fail("empty report must not call Codex"),
    )
    # journal 作成を含む終了処理全体で、cleanup manifest と初期 state の重複読込を検出する。
    finish = recovery_module.finish_feedback_run
    original_read = Path.read_bytes
    original_read_text = Path.read_text
    save_invocation = feedback_report_module.save_feedback_invocation_report
    cleanup_reads = []
    session_reads = []
    invocation_saves = []

    def finish_with_read_count(context, manifest, result):
        manifest_path = feedback_state_module.report_cut_manifest_path(
            root, manifest["report_cut_id"]
        )

        def read(candidate):
            if candidate == manifest_path:
                cleanup_reads.append(candidate)
            return original_read(candidate)

        def read_text(candidate, *args, **kwargs):
            if candidate == context.state_path:
                session_reads.append(candidate)
            return original_read_text(candidate, *args, **kwargs)

        def save(*args, **kwargs):
            if not invocation_saves:
                # identity 検証と state_before は同じ lock 内の snapshot を使う。
                assert session_reads == [context.state_path]
            invocation_saves.append(True)
            return save_invocation(*args, **kwargs)

        with monkeypatch.context() as finalization_patch:
            finalization_patch.setattr(Path, "read_bytes", read)
            finalization_patch.setattr(Path, "read_text", read_text)
            finalization_patch.setattr(
                feedback_report_module, "save_feedback_invocation_report", save
            )
            return finish(context, manifest, result)

    monkeypatch.setattr(recovery_module, "finish_feedback_run", finish_with_read_count)

    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert len(cleanup_reads) == 1
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


@pytest.mark.usefixtures("feedback_without_transport", "nonpersistent_feedback_ids")
def test_feedback_preconditions_preserve_existing_changes_and_raw(
    ready_content_session: tuple[Path, str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """不適合な session から run を開始せず、既存差分をそのまま保持する。"""
    # doctor の修復・公開 session fork との結合は後続 wave test に残す。
    # ここでは準備済み session を使い、doctor 成功後の事前条件と保持を検査する。
    root, session_branch, _state_path = ready_content_session
    # 採番の永続性は test_runtime_ids.py、同期順序・失敗は test_feedback_store.py、
    # 実同期との結合は collector 受理と後続 wave test に残す。
    # 拒否前後の write・rename・raw 本文・Git 差分の検査は実行する。
    monkeypatch.setattr(os, "fsync", lambda _fd: None)
    doctor = Mock()
    monkeypatch.setattr(remediation_module, "doctor_preprocess_for_join", doctor)
    run_git(root, "switch", "-c", "outside-session")
    original_head = run_git(root, "rev-parse", "HEAD").stdout
    # 観測時点の session 有無と複数 raw の保持を、全拒否条件で同じ入力から検査する。
    # branch 切替・本文編集・stage は HEAD を変えないため、比較基準も一度だけ取得する。
    for session_id in (None, SESSION_ID):
        store_agent_observation(
            root,
            _context(root, session_id=session_id, head_commit=original_head.strip()),
            _payload(),
        )
    original_raw = {path: path.read_bytes() for path in iter_observation_paths(root)}
    # 拒否後の保持を確認してから同じ入力を次の境界へ進め、Git/session の準備を共有する。
    # collector の受理・拒否・保存は transport と後続 wave の結合 test で検証する。
    for condition in ("inactive", "dirty_worktree", "dirty_index"):
        if condition == "dirty_worktree":
            run_git(root, "switch", session_branch)
            (root / "README.md").write_text("user change\n")
        elif condition == "dirty_index":
            run_git(root, "add", "README.md")
        original_status = run_git(root, "status", "--porcelain").stdout

        result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

        doctor.assert_called_once_with(rollback_on_interruption=True)
        doctor.reset_mock()
        assert result.exit_code == 1, (condition, result.output)
        expected_error = (
            "feedback report は active session branch 上で実行してください。"
            if condition == "inactive"
            else "git 未コミット差分が存在します。"
        )
        assert expected_error in result.output, (condition, result.output)
        assert run_git(root, "rev-parse", "HEAD").stdout == original_head, condition
        assert (
            run_git(root, "status", "--porcelain").stdout == original_status
        ), condition
        assert {
            path: path.read_bytes() for path in iter_observation_paths(root)
        } == original_raw, condition
        assert load_report_cut(root) is None, condition


def test_feedback_repairs_sequential_waves_and_preserves_late_intake(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """修復中の新 issue を最新 tree で処理し、最終境界後の raw は残す。"""
    # 両分類を同じ後続 wave に入れ、Git/session・修復・publication の準備を共有する。
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _, first_raw, first_id = _store_agent_issue(root, session_id)
    calls: list[str] = []
    raw_paths = [first_raw]
    later_statuses: dict[str, str] = {}

    def fake_call(parameter: Any, **kwargs: Any) -> SimpleNamespace:
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
            with begin_feedback_call(
                agent_call_id="ac_000011_2026-09-29_15-04",
                agent_call_kind=parameter.agent_call_kind,
                codex_call_id="cc_000013_2026-09-29_15-04",
                log_paths=[],
                agent_call_cwd=worktree,
            ) as feedback_call:
                environment = feedback_call.subprocess_env({})
                for last_status in ("human_required", "inconclusive"):
                    accepted = _submit_to_feedback_collector(
                        int(environment[FEEDBACK_COLLECTOR_PORT_ENV]),
                        environment[FEEDBACK_CAPABILITY_ENV],
                        _payload(
                            kind="other", path=None, text=f"別の issue: {last_status}"
                        ),
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
                    later_statuses[later_id] = last_status
                    raw_paths.append(path)
            # 完全重複の observation は新しい issue call を増やさない。
            _, duplicate = store_agent_observation(
                root, _context(root, session_id=session_id), _payload()
            )
            raw_paths.append(duplicate)
        else:
            assert identity in later_statuses
            assert (worktree / "README.md").read_text() == "repaired\n"
            assert run_git(worktree, "status", "--porcelain").stdout == ""
            output = _remediation_output(identity, later_statuses[identity])
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
    assert calls == [first_id, *sorted(later_statuses)]
    assert (root / "README.md").read_text() == "repaired\n"
    assert run_git(root, "status", "--porcelain").stdout == ""
    assert load_report_cut(root) is None
    assert all(path.exists() for path in late_paths)
    state = load_active_state(root)
    assert set(state.issues) == set(later_statuses)
    assert {
        identity: issue["verification"]["status"]
        for identity, issue in state.issues.items()
    } == later_statuses
    assert state.current is not None
    assert state.current["result"] == "incomplete"
    assert all(not path.exists() for path in raw_paths)


# rollback 済み error の手動終了は、障害原因によらず同じ入力状態を扱う。
# 各障害の rollback を検査し、checkpoint 保存済み error では両操作を残す。
# doctor の修復・索引同期と公開 session fork の結合は wave test に残す。
# 準備済み session を使い、Git 差分・rollback・手動終了を実行する。
# 手動 join/abandon と実 doctor の結合は test_editing_run_cli.py の
# test_run_join_from_run_worktree_tracks_main_doctor_repairs と
# test_run_join_preserves_active_state_when_cleanup_fails に残す。
@pytest.mark.parametrize(
    ("fault", "operation"),
    [
        ("unreported_change", "join"),
        ("forbidden_change", "abandon"),
        ("checkpoint", "join"),
        ("checkpoint_reference", "join"),
        ("checkpoint_reference", "abandon"),
    ],
)
def test_failed_feedback_unit_rolls_back_and_manual_completion_keeps_raw(
    feedback_publication_session: Path,
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
    operation: str,
) -> None:
    """未確定 issue の差分を戻し、明示終了で publication せず raw を保持する。"""
    root = feedback_publication_session
    _, raw, identity = _store_agent_issue(root, SESSION_ID)
    initial = (root / "README.md").read_text()

    def fake_call(parameter: Any, **kwargs: Any) -> SimpleNamespace:
        worktree = parameter.agent_call_cwd
        target = "oracle/bad.md" if fault == "forbidden_change" else "README.md"
        (worktree / target).parent.mkdir(parents=True, exist_ok=True)
        (worktree / target).write_text("unconfirmed change\n")
        output = _remediation_output(identity, "fixed")
        output["result"]["changed_paths"] = (
            [] if fault == "unreported_change" else [target]
        )
        return _fake_result(root, output)

    def checkpoint_failure(*_args: Any, **_kwargs: Any) -> None:
        raise OSError("injected checkpoint failure")

    monkeypatch.setattr(feedback_report_module, "run_codex_exec", fake_call)
    if fault == "checkpoint":
        original_write = remediation_module.write_immutable_artifact

        def write_artifact(repo, path, value):
            # wave 保存は通し、修復後の checkpoint 保存失敗を注入する。
            if path.parent.name == "remediation":
                checkpoint_failure()
            return original_write(repo, path, value)

        monkeypatch.setattr(
            remediation_module, "write_immutable_artifact", write_artifact
        )
    elif fault == "checkpoint_reference":
        monkeypatch.setattr(
            feedback_report_module, "_record_checkpoint", checkpoint_failure
        )
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert result.exit_code == 1, result.output
    manifest, _ = load_report_cut(root)
    _, _, session = load_state_for_branch(
        root, manifest["run"]["identity"]["session_branch"]
    )
    assert session.run.state == "error"
    assert manifest["processing"]["status"] == "failed"
    run_worktree = Path(manifest["run"]["identity"]["run_worktree"])
    assert (run_worktree / "README.md").read_text() == (
        "unconfirmed change\n" if fault == "checkpoint_reference" else initial
    )
    assert run_git(run_worktree, "status", "--porcelain").stdout == ""
    assert manifest["processing"]["remediation_checkpoints"] == []

    # doctor 本体だけを省き、join の復旧検査・journal と前処理の呼出契約は保つ。
    preprocess = Mock()
    preprocess_module = run_join_module if operation == "join" else run_abandon_module
    monkeypatch.setattr(preprocess_module, "run_doctor_preprocess", preprocess)
    completed = runner.invoke(app, ["run", operation], catch_exceptions=False)
    assert completed.exit_code == 0, completed.output
    if operation == "join":
        preprocess.assert_called_once_with(root, sync_refactor_entries=False)
    else:
        preprocess.assert_called_once_with(root)
    assert (root / "README.md").read_text() == (
        "unconfirmed change\n"
        if fault == "checkpoint_reference" and operation == "join"
        else initial
    )
    assert raw.exists()
    assert load_active_state(root).current is None
    assert load_report_cut(root) is None


def test_feedback_interrupt_after_run_start_reports_retained_run(
    feedback_publication_session: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """run 公開直後の中断でも joinable state と run identity を report する。"""
    root = feedback_publication_session
    session_path = state_path(root, SESSION_ID)
    original_start = remediation_module.start_editing_run

    def start_then_interrupt(kind: str) -> Any:
        """run の state 公開後、context 返却前の中断を再現する。"""
        original_start(kind)
        raise KeyboardInterrupt()

    monkeypatch.setattr(remediation_module, "start_editing_run", start_then_interrupt)
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    session_state = json.loads(session_path.read_text())
    assert session_state["run"]["state"] == "ready"
    report_text = terminal_primary_report(result).read_text()
    assert 'terminal_classification: "user_interruption"' in report_text
    assert 'run_kind: "feedback_report"' in report_text
    assert 'state_before: "ready"' in report_text
    assert 'state_after: "ready"' in report_text
    assert "cmoc run join" not in result.output


def test_feedback_interruption_joins_commits_and_next_report_reconfirms(
    feedback_publication_session,
    monkeypatch,
):
    """中断は publication せず checkpoint を残し、次の report は全入力を再確認する。"""
    root = feedback_publication_session
    initial = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert initial.exit_code == 0, initial.output
    pointer = current_pointer_path(root).read_bytes()
    inputs = []
    for path in ("README.md", "oracle/spec.md"):
        accepted, raw = store_agent_observation(
            root, _context(root, session_id=SESSION_ID), _payload(path=path)
        )
        inputs.append((issue_id(f"agent\0{accepted['observation_id']}"), raw, path))
    by_id = {identity: path for identity, _raw, path in inputs}
    handled = []

    def repair_then_interrupt(parameter, **_kwargs):
        if handled:
            signal.raise_signal(signal.SIGINT)
            pytest.fail("issue resumed after interruption")
        identity = sorted(by_id)[0]
        handled.append(identity)
        (parameter.agent_call_cwd / "README.md").write_text("confirmed repair\n")
        output = _remediation_output(identity, "fixed", reference_path=by_id[identity])
        output["result"]["changed_paths"] = ["README.md"]
        return _fake_result(root, output)

    monkeypatch.setattr(feedback_report_module, "run_codex_exec", repair_then_interrupt)
    interrupted = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert interrupted.exit_code == 0, interrupted.output
    assert current_pointer_path(root).read_bytes() == pointer
    assert (root / "README.md").read_text() == "confirmed repair\n"
    assert all(raw.exists() for _identity, raw, _path in inputs)
    assert load_report_cut(root) is None

    [receipt] = (root / ".cmoc/gu/feedback/work").glob("*/join_result.json")
    manifest_path = receipt.parent / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    [checkpoint] = manifest["processing"]["remediation_checkpoints"]
    checkpoint_path = root / checkpoint["path"]
    checkpoint_content = checkpoint_path.read_bytes()
    text = terminal_primary_report(interrupted).read_text()
    assert 'state_after: "ready"' in text
    assert 'terminal_classification: "user_interruption"' in text
    assert "publication は行っていません" in text
    assert not Path(
        json.loads(receipt.read_text())["identity"]["run_worktree"]
    ).exists()
    assert "cmoc run join" not in report_section(text, "次の操作")

    rechecked = []

    def reconfirm(parameter, **_kwargs):
        assert (
            parameter.agent_call_cwd / "README.md"
        ).read_text() == "confirmed repair\n"
        identity = sorted(by_id)[len(rechecked)]
        rechecked.append(identity)
        return _fake_result(
            root,
            _remediation_output(
                identity, "already_resolved", reference_path=by_id[identity]
            ),
        )

    monkeypatch.setattr(feedback_report_module, "run_codex_exec", reconfirm)
    completed = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert completed.exit_code == 0, completed.output
    assert rechecked == sorted(by_id)
    assert current_pointer_path(root).read_bytes() != pointer
    assert all(not raw.exists() for _identity, raw, _path in inputs)
    assert checkpoint_path.read_bytes() == checkpoint_content
    assert load_report_cut(root) is None


def test_feedback_outer_report_failure_retains_publication_recovery(
    feedback_publication_session, monkeypatch
):
    """最後の invocation 保存失敗でも journal と immutable な publication を残す。"""
    import commons.runtime_primary_report as primary_report

    root = feedback_publication_session
    original = primary_report.rewrite_primary_report
    with monkeypatch.context() as failing:
        failing.setattr(
            primary_report,
            "rewrite_primary_report",
            lambda *_args: (_ for _ in ()).throw(OSError("outer report save failed")),
        )
        failed = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert failed.exit_code == 1, failed.output
    assert primary_report.rewrite_primary_report is original
    state = load_active_state(root)
    publication = root / state.current["report_path"]
    saved_publication = publication.read_bytes()
    assert (feedback_root(root) / "finalization.json").is_file()
    assert (
        json.loads(state_path(root, SESSION_ID).read_text())["run"]["state"] == "error"
    )
    assert "cmoc feedback report" in failed.output
    assert "cmoc run abandon" not in failed.output
    monkeypatch.setattr(
        feedback_report_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: pytest.fail("recovery must not start a call"),
    )
    recovered = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert recovered.exit_code == 0, recovered.output
    assert publication.read_bytes() == saved_publication
    assert not (feedback_root(root) / "finalization.json").exists()
    assert (
        json.loads(state_path(root, SESSION_ID).read_text())["run"]["state"] == "ready"
    )


def test_feedback_interrupt_after_report_cut_write_recovers_manifest(
    feedback_publication_session: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """manifest 保存直後の中断を記録し、未完了の cut を close で追い越さない。"""
    root = feedback_publication_session
    session_path = state_path(root, SESSION_ID)
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
    session_state = json.loads(session_path.read_text())
    assert session_state["run"]["state"] == "ready"
    assert load_report_cut(root) is None
    [manifest_path] = (root / ".cmoc/gu/feedback/work").glob("*/manifest.json")
    manifest = json.loads(manifest_path.read_text())
    assert (manifest_path.parent / "join_result.json").is_file()
    assert manifest["processing"]["status"] == "interrupted"
    assert 'terminal_classification: "user_interruption"' in (
        terminal_primary_report(result).read_text()
    )

    # 保存済み cut を使い、close の事前条件だけのために別の report/run を作らない。
    saved_manifest = manifest_path.read_bytes()
    saved_session = session_path.read_bytes()
    before = load_active_state(root)
    rejected = runner.invoke(
        app,
        [
            "feedback",
            "close",
            "fbc_000000_2026-10-08_00-00",
            "--reason",
            "外部で解決を確認した",
        ],
        catch_exceptions=False,
    )
    assert rejected.exit_code == 1, rejected.output
    assert "未完了の feedback run/publication/cleanup" not in rejected.stderr
    assert "feedback/invocation" in str(terminal_primary_report(rejected))
    assert load_close_work(root) is None
    assert load_active_state(root) == before
    assert manifest_path.read_bytes() == saved_manifest
    assert session_path.read_bytes() == saved_session


def test_feedback_interrupt_cleanup_failure_sets_error_and_reports(
    feedback_publication_session: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """中断 cleanup の失敗を user interruption へ変換せず error にする。"""
    root = feedback_publication_session
    session_path = state_path(root, SESSION_ID)
    _store_agent_issue(root, SESSION_ID)

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
    session_state = json.loads(session_path.read_text())
    assert session_state["run"]["state"] == "error"
    report_text = terminal_primary_report(result).read_text()
    assert 'terminal_classification: "error"' in report_text
    assert 'state_after: "error"' in report_text
    assert "rollback failed" in result.output
    manifest, _ = load_report_cut(root)
    assert manifest["processing"]["status"] == "failed"


# 復旧の障害検査は修復済み session から始め、doctor の修復・索引同期と
# transport の結合は後続 wave の検査に残す。
@pytest.mark.parametrize(
    "fault",
    [
        "publication",
        "raw_cleanup",
        "cleanup",
        "branch_cleanup",
        "merge_reference",
        "completion_reference",
    ],
)
def test_feedback_recovers_after_auto_join_without_new_calls(
    feedback_publication_session: Path,
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    """自動 join 後の失敗は修復 commit と公開入力を保持して同じ run を完了する。"""
    import commons.runtime_feedback_run_state as run_state_module
    import commons.runtime_run_join as join_runtime
    import sub_commands.feedback.recovery as recovery_module

    root = feedback_publication_session
    _, raw, identity = _store_agent_issue(root, SESSION_ID)

    def fake_call(parameter: Any, **_kwargs: Any) -> SimpleNamespace:
        (parameter.agent_call_cwd / "README.md").write_text("joined repair\n")
        output = _remediation_output(identity, "fixed")
        output["result"]["changed_paths"] = ["README.md"]
        return _fake_result(root, output)

    target = feedback_report_module if fault == "publication" else recovery_module
    name = "publish_current_pointer" if fault == "publication" else "cleanup_joined_run"
    if fault == "branch_cleanup":
        target = join_runtime
        name = "delete_branch"
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
    report_text = terminal_primary_report(result).read_text()
    publication_status = (
        "completed"
        if fault in {"raw_cleanup", "cleanup", "branch_cleanup"}
        else "not_completed"
    )
    for field, label, expected in (
        ("normal_publication_status", "正常 publication", publication_status),
        ("incomplete_diagnostic_status", "incomplete 診断", "not_completed"),
        ("current_pointer_update_status", "current pointer 更新", publication_status),
    ):
        assert f'{field}: "{expected}"' in report_text
        assert f"- {label}: `{expected}`" in report_text
    joined_head = run_git(root, "rev-parse", "HEAD").stdout
    saved_report = None
    if fault in {"raw_cleanup", "cleanup", "branch_cleanup"}:
        published = load_active_state(root)
        assert published.current is not None
        saved_report = root / published.current["report_path"]
        saved_content = saved_report.read_bytes()
        (root / "README.md").write_text("changed after publication\n")
        assert feedback_completion_counts(root)[0] == 0
        if fault == "raw_cleanup":
            assert raw.exists()
        assert "publication_established: true" in report_text
    # 手動操作の拒否は merge 記録（参照回復を含む）と finalization journal の両経路で検査する。
    # completion/publication の障害種別や raw cleanup の進捗は、この拒否条件を変えない。
    if fault in {"merge_reference", "cleanup", "branch_cleanup"}:
        # doctor の修復・索引同期は test_doctor_cli.py、abandon との結合は
        # test_editing_run_cli.py の preserves_active_state_when_cleanup_fails に残す。
        # join は取り込み済み記録を検証して doctor を省く経路をそのまま通す。
        preprocess = Mock()
        monkeypatch.setattr(run_abandon_module, "run_doctor_preprocess", preprocess)
        for operation in ("join", "abandon"):
            rejected = runner.invoke(app, ["run", operation], catch_exceptions=False)
            assert rejected.exit_code == 1, rejected.output
            assert "feedback run は自動 join 済みです。" in rejected.output
            rejected_report = terminal_primary_report(rejected).read_text(
                encoding="utf-8"
            )
            assert 'run_kind: "feedback_report"' in rejected_report
            assert 'state_before: "error"' in rejected_report
            assert 'state_after: "error"' in rejected_report
        preprocess.assert_called_once_with(root)
    monkeypatch.setattr(target, name, original)
    monkeypatch.setattr(
        feedback_report_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: pytest.fail("recovery must not call Codex"),
    )
    recovered = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert recovered.exit_code == 0, recovered.output
    invocation = terminal_primary_report(recovered)
    assert invocation.parent == root / ".cmoc/gu/report/feedback/invocation"
    assert invocation != terminal_primary_report(result)
    metadata = report_metadata(invocation.read_text())
    assert metadata["execution_id"] == invocation.stem
    assert metadata["publication_execution_id"] == terminal_primary_report(result).stem
    assert metadata["state_before"] == "error"
    assert metadata["state_after"] == "ready"
    assert metadata["cleanup"] == "completed"
    assert metadata["publication_established"] is True
    assert (
        Path(metadata["publication_report"]).stem
        == metadata["publication_execution_id"]
    )
    assert_report_layout(invocation.read_text())
    assert run_git(root, "rev-parse", "HEAD").stdout == joined_head
    assert not raw.exists()
    assert load_report_cut(root) is None
    assert not (feedback_root(root) / "finalization.json").exists()
    assert load_active_state(root).current["result"] == "ok"
    if saved_report is not None:
        assert saved_report.read_bytes() == saved_content
        assert (root / "README.md").read_text() == "changed after publication\n"


@pytest.fixture
def feedback_fixed_input_session(feedback_publication_session, monkeypatch):
    """本文を変更しない状態遷移の検査では、判定入力の収集を前後一回ずつにする。"""
    # 入力変更による再確認・封印後の拒否は test_feedback_reconfirmation.py、
    # 実 Git との結合は後続 wave と feedback_basis_includes_oracle_changes に残す。
    # evidence・threshold・checkpoint・publication・履歴は実処理を通す。
    root = feedback_publication_session
    collect = decision_module.worktree_inputs
    before = collect(root)
    monkeypatch.setattr(
        decision_module, "worktree_inputs", lambda _worktree: before.copy()
    )
    yield root
    # 想定外の本文・設定・mode の変更を固定入力で隠さない。
    assert collect(root) == before


def test_agent_issues_are_compacted_then_removed_for_terminal_verdicts(
    feedback_fixed_input_session: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """両終了判定で active・一覧から除き、履歴を残して手動 close を拒否する。"""
    # 異なる subject の案件を同時に用意し、Git/session と二回の publication を共有する。
    root = feedback_fixed_input_session
    cases = {}
    for terminal_verdict, kind, reference_path in (
        ("already_resolved", "file", "README.md"),
        ("not_actionable", "oracle", "oracle/spec.md"),
    ):
        accepted, raw_path = store_agent_observation(
            root,
            _context(root, session_id=SESSION_ID),
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
    assert first_state.current is not None
    assert first_state.current["result"] == "attention"
    first_text = terminal_primary_report(first).read_text()
    for identity, case in cases.items():
        assert not case["raw_path"].exists()
        issue = first_state.issues[identity]
        assert issue["occurrence_count"] == 1
        assert issue["verification"]["human_action"] == "README の設定を修正する。"
        expected_evidence = [
            {
                "kind": "repository_content",
                "path": case["reference_path"],
                "location": f"{case['reference_path']}:1",
                "finding": "report cut で現在状態を確認した。",
            }
        ]
        assert issue["verification"]["current_evidence"] == expected_evidence
        event = next(
            event
            for event in first_state.history[-1]["events"]
            if event["issue_id"] == identity
        )
        assert event["agent_result"]["current_evidence"] == expected_evidence
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
    # 終了 publication を共有し、close の拒否だけのために report を重ねない。
    # close と doctor の結合は test_feedback_close.py の reported_case に残す。
    monkeypatch.setattr(
        feedback_close_module, "run_doctor_preprocess", lambda _root: None
    )
    for issue in first_state.issues.values():
        rejected = runner.invoke(
            app,
            ["feedback", "close", issue["case_id"], "--reason", "外部で解決を確認した"],
            catch_exceptions=False,
        )
        assert rejected.exit_code == 1, rejected.output
        assert "agent の判定により終了しており close の対象外" in rejected.output
        assert load_active_state(root) == second_state


def test_feedback_basis_includes_oracle_changes_but_ignores_refactor_state(
    cli_repository: Path,
) -> None:
    """oracle file の変更を根拠へ含め、管理 state だけを除外する。"""
    # 判定根拠は履歴を参照しないため、実 Git の index だけを用意する。
    root = cli_repository
    document = root / "oracle/notes.md"
    spec = root / "oracle/spec.md"
    state = root / ".cmoc/gt/realization/refactor/state.json"
    document.parent.mkdir()
    state.parent.mkdir(parents=True)
    document.write_text("first document\n")
    spec.write_text("# spec\n")
    state.write_text("{}\n")
    run_git(root, "add", "oracle", ".cmoc/gt/realization/refactor/state.json")
    baseline = decision_module.worktree_inputs(root)
    assert set(baseline) == {"oracle/notes.md", "oracle/spec.md"}

    # 実 Git との結合は更新・未変更入力・state 除外を二つの snapshot で確認する。
    # 個々の入力を一つずつ変更する検査は test_feedback_decision.py に残す。
    document.write_text("updated document\n")
    state.write_text('{"entry": {}}\n')
    after_document = decision_module.worktree_inputs(root)
    assert set(after_document) == set(baseline)
    assert after_document["oracle/notes.md"] != baseline["oracle/notes.md"]
    assert after_document["oracle/spec.md"] == baseline["oracle/spec.md"]


def _reporter_unavailable_observation(root, context, index, occurred_at):
    """同じ rule の observation を異なる recurrence scope で保存する。"""
    log_path = root / ".cmoc/gu/log/sub_command/exec_000000_2026-09-29_15-04.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text('{"event":"reporter unavailable"}\n')
    context = {
        **context,
        "cmoc_session_id": f"sess_{index:06d}_2026-09-29_15-04",
        "subcommand_invocation_id": f"exec_{index:06d}_2026-09-29_15-04",
    }
    event = {
        "event_schema_version": 1,
        "event_id": f"evt_{index}",
        "event_type": "feedback.reporter_unavailable",
        "occurred_at": occurred_at,
        "subcommand_invocation_id": context["subcommand_invocation_id"],
        "component": "reporter",
        "failure_code": "missing",
    }
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
    return read_json_object(raw_path)


def test_machine_threshold_counts_distinct_scopes_within_one_day(
    feedback_directory, stored_feedback_context
):
    """同じ日への追加入力も distinct scope として集約し、threshold を判定する。"""
    root = feedback_directory
    cut_at = "2026-09-29T15:04:00Z"
    aggregate = None
    for index in range(2):
        observation = _reporter_unavailable_observation(
            root, stored_feedback_context, index, cut_at
        )
        aggregate = feedback_report_module._merge_machine_aggregate(
            root, aggregate, [observation], cut_at, machine_canonical_key(observation)
        )

        assert aggregate is not None
        assert len(aggregate["time_buckets"]) == 1
        assert aggregate["occurrence_count"] == index + 1
        assert aggregate["threshold_counts"]["recurrence_scope"] == index + 1
        assert feedback_report_module._machine_threshold_met(aggregate) == (index == 1)


def test_machine_issue_lifecycle_keeps_threshold_state_after_window_expires(
    feedback_fixed_input_session: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """閾値未満・案件化・全件失効の公開 state と、失効の両分岐を検証する。"""
    # 案件化までの Git/session と publication を、期限切れ検査の準備にも使う。
    root = feedback_fixed_input_session
    context = _context(root)
    base = datetime.now(timezone.utc).replace(microsecond=0)
    cut_at = base.isoformat().replace("+00:00", "Z")
    # recurrence window の基準は manifest 作成側、publication の日時は表示側に属する。
    monkeypatch.setattr(remediation_module, "rfc3339_now", lambda: cut_at)
    monkeypatch.setattr(feedback_report_module, "rfc3339_now", lambda: cut_at)

    for index, age_days in enumerate((20, 1)):
        occurred_at = (
            (base - timedelta(days=age_days)).isoformat().replace("+00:00", "Z")
        )
        observation = _reporter_unavailable_observation(
            root, context, index, occurred_at
        )
        canonical_key = machine_canonical_key(observation)
        if index == 0:
            monkeypatch.setattr(
                feedback_report_module,
                "run_codex_exec",
                lambda *_args, **_kwargs: pytest.fail(
                    "threshold 未満で verification してはならない"
                ),
            )
        else:
            candidate_id = issue_id(canonical_key)

            def fake_remediation(parameter, **_kwargs):
                return _fake_result(
                    root,
                    _remediation_output(
                        candidate_id,
                        "human_required",
                        reference_path=".cmoc/gu/log/test.jsonl",
                    ),
                )

            remediation = Mock(side_effect=fake_remediation)
            monkeypatch.setattr(feedback_report_module, "run_codex_exec", remediation)
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
            assert set(state.issues) == {candidate_id}
            assert state.issues[candidate_id]["occurrence_count"] == 2
            remediation.assert_called_once()

    threshold_state = deepcopy(state.issues[candidate_id]["machine_state"])
    assert isinstance(threshold_state, dict)
    # 部分・全件失効で候補が消えたり閾値未満 state に上書きされたりしないことを、
    # 公開済み state からの候補構築で確かめる。CLI の再確認・publication は下で一度通す。
    for elapsed_days in (11, 31):
        cut_at = (
            (base + timedelta(days=elapsed_days)).isoformat().replace("+00:00", "Z")
        )
        remaining = feedback_report_module._merge_machine_aggregate(
            root, deepcopy(threshold_state), [], cut_at, canonical_key
        )
        if elapsed_days == 11:
            assert remaining is not None
            assert remaining["occurrence_count"] == 1
            assert not feedback_report_module._machine_threshold_met(remaining)
        else:
            assert remaining is None

        candidates, aggregates = feedback_report_module._build_candidates(
            root,
            root,
            {"cut_at": cut_at, "inputs": {"references": []}},
            {},
            deepcopy(state),
        )
        assert aggregates == {}
        assert set(candidates) == {candidate_id}
        assert candidates[candidate_id]["machine_state"] == threshold_state
        assert candidates[candidate_id]["occurrence_count"] == 2
    remediation.assert_called_once()

    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert remediation.call_count == 2
    state = load_active_state(root)
    assert state.current is not None
    assert (
        f'report_cut_at: "{cut_at}"'
        in (root / state.current["report_path"]).read_text()
    )
    assert state.machine_aggregates == {}
    assert set(state.issues) == {candidate_id}
    assert state.issues[candidate_id]["machine_state"] == threshold_state


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
    feedback_publication_session: Path,
) -> None:
    """validation 不通過 raw を処理済みにせず、正常 report を publication しない。"""
    root = feedback_publication_session
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


def test_cleanup_corruption_is_a_required_recovery_failure(
    feedback_publication_session: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """publication 後の state corruption は warning ではなく終了コード 1 にする。"""
    root = feedback_publication_session
    _observation_id, _raw_path, candidate_id = _store_agent_issue(root, SESSION_ID)
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
    # 同じ invocation の snapshot だけを共有し、次回 recovery は改変を再検査する。
    pointer_path = feedback_state_module.current_pointer_path(root)
    pointer_content = pointer_path.read_bytes()
    corrupted_content = cut_path.read_bytes()
    recovered = runner.invoke(app, ["feedback", "report"])
    assert recovered.exit_code == 1, recovered.output
    assert "SHA256" in recovered.output
    assert pointer_path.read_bytes() == pointer_content
    assert cut_path.read_bytes() == corrupted_content
    assert (feedback_root(root) / "finalization.json").is_file()
