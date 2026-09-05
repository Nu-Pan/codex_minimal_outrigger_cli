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
import socket
import threading
from collections.abc import Iterator
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from _cli_support import run_doctor, runner, terminal_primary_report
from _git_support import current_branch, make_repo, run_git
from oracle.acp_builder.feedback.normalize_issue import (
    build_feedback_normalize_issue_parameter as _build_canonical_normalize_parameter,
)
from oracle.acp_builder.feedback.remediate_issue import (
    build_feedback_remediate_issue_parameter as _build_canonical_remediate_parameter,
)

import commons.runtime_codex_preflight as codex_preflight_module
import commons.runtime_feedback as feedback_module
import commons.runtime_feedback_reporter as reporter_module
import commons.runtime_feedback_state as feedback_state_module
import sub_commands.feedback.remediation as remediation_module
import sub_commands.feedback.report as feedback_report_module
import sub_commands.run.join as run_join_module
from acp.builder.feedback.normalize_issue import (
    build_feedback_normalize_issue_parameter,
)
from acp.builder.feedback.remediate_issue import (
    build_feedback_remediate_issue_parameter,
)
from basic.acp import FileAccessMode
from cmoc_runtime import CmocError
from commons.runtime_feedback import (
    FEEDBACK_CAPABILITY_ENV,
    FEEDBACK_COLLECTOR_HOST,
    FEEDBACK_COLLECTOR_PORT_ENV,
    FEEDBACK_PROTOCOL_ENV,
    FeedbackInvocation,
    ReporterAvailabilityError,
    begin_feedback_call,
    start_feedback_invocation,
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
    REPORTER_PROTOCOL_VERSION,
    FeedbackRejected,
    canonical_json_bytes,
    feedback_completion_counts,
    feedback_root,
    iter_observation_paths,
    observation_path,
    read_json_object,
    reporter_input_schema,
    rfc3339_now,
    store_agent_observation,
    store_machine_observation,
)
from commons.runtime_logging import SubcommandLogger
from main import app


@pytest.fixture(autouse=True)
def reset_indexing_preflight(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """process-global な indexing preflight を case 間で分離する。"""
    codex_preflight_module.disable_indexing_preflight()
    monkeypatch.setattr(
        remediation_module, "run_indexing_preflight", lambda *_args: None
    )
    monkeypatch.setattr(
        remediation_module, "refresh_indexes", lambda *_args, **_kwargs: []
    )
    monkeypatch.setattr(
        run_join_module, "refresh_indexes", lambda *_args, **_kwargs: []
    )
    yield
    codex_preflight_module.disable_indexing_preflight()


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


def _context(root: Path, *, session_id: str | None = None) -> dict[str, object]:
    """collector が付与する version 1 context と同形の fixture を返す。"""
    return {
        "repo_root": str(root.resolve()),
        "work_root": str(root.resolve()),
        "head_commit": run_git(root, "rev-parse", "HEAD").stdout.strip(),
        "cmoc_session_id": session_id,
        "run_id": None,
        "run_kind": None,
        "subcommand": "feedback test",
        "subcommand_invocation_id": "sci_feedback_test",
        "agent_call_id": "agc_feedback_test",
        "agent_call_kind": "build_feedback_test_parameter",
        "codex_call_id": "cdc_feedback_test",
        "codex_session_id": None,
        "log_paths": [str((root / ".cmoc/gu/ar/log/test.jsonl").resolve())],
    }


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
    directory = root / ".cmoc/gu/ar/log/feedback_test"
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
            return b'{"status":"accepted","observation_id":"fbo_00000000-0000-7000-8000-000000000001","redaction_count":0}\n'

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


def test_reporter_probe_rejects_non_object_mcp_response(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
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
        feedback_module._validate_stdio_reporter({}, tmp_path)

    assert error.value.component == "reporter"
    assert error.value.failure_code == "protocol_error"


@pytest.mark.parametrize(
    "response",
    [
        b'{"status":"accepted"}\n',
        b'{"status":"accepted","observation_id":"fbo_test","redaction_count":0}\n',
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


def test_feedback_report_registers_indexing_preflight_before_cli_runtime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """feedback report が本命 agent call 用 preflight を invocation 前に登録する。"""
    events: list[str] = []

    def record_enable_indexing_preflight() -> None:
        """indexing preflight の登録順を記録する。"""
        events.append("enable-indexing")

    def record_run_cli_subcommand(*_args: object, **_kwargs: object) -> None:
        """CLI runtime への委譲順を記録する。"""
        events.append("run-cli")

    monkeypatch.setattr(
        feedback_report_module,
        "enable_indexing_preflight",
        record_enable_indexing_preflight,
    )
    monkeypatch.setattr(
        feedback_report_module,
        "run_cli_subcommand",
        record_run_cli_subcommand,
    )

    feedback_report_module.cmoc_feedback_report_impl()

    assert events == ["enable-indexing", "run-cli"]


def test_feedback_normalize_builder_protects_nested_code_fences(
    tmp_path: Path,
) -> None:
    """normalization の動的 JSON が prompt section の境界を閉じないことを検証する。"""
    root = make_repo(tmp_path)
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
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """候補検索専用 hint を normalization agent の入力へ渡さない。"""
    root = make_repo(tmp_path)
    observation_id = "fbo_00000000-0000-7000-8000-000000000001"
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

    def fake_run_codex_exec(parameter: object, **_kwargs: object) -> SimpleNamespace:
        assert hasattr(parameter, "prompt")
        captured_prompts.append(str(parameter.prompt))
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


def test_pending_observations_rejects_symlinked_root(tmp_path: Path) -> None:
    """symlink 化された raw root を空の初期 state として扱わない。"""
    root = make_repo(tmp_path)
    observation_parent = feedback_root(root) / "observation"
    observation_parent.mkdir(parents=True)
    (observation_parent / "v1").symlink_to(
        tmp_path / "missing-observations", target_is_directory=True
    )

    with pytest.raises(CmocError, match="observation root"):
        feedback_report_module._pending_observations(root)


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
        "observation_id": "fbo_00000000-0000-7000-8000-000000000001",
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
            ("fbo_00000000-0000-7000-8000-000000000001", "2026-08-01T00:00:00Z"),
            ("fbo_00000000-0000-7000-8000-000000000002", "2026-08-02T00:00:00Z"),
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
        "observation_id": "fbo_new",
        "source": "agent_report",
        "observed_at": "2026-08-02T00:00:00Z",
        "context": {"cmoc_session_id": "session"},
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
        "observation_id": "fbo_old",
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
    candidate = feedback_report_module._new_candidate(newer, "agent\0fbo_new")
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
            agent_call_id="agc_one",
            agent_call_kind="build_one",
            codex_call_id="cdc_one",
            codex_session_id="session_one",
            log_paths=[root / ".cmoc/gu/ar/log/codex/call.json"],
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
        assert envelope["context"]["agent_call_id"] == "agc_one"
        assert reporter_module._submit(_payload())["code"] == "rate_limited"
        feedback_call.close()
        assert reporter_module._submit(_payload())["code"] == "context_invalid"
        invocation.stop()
        assert reporter_module._submit(_payload())["code"] == "collector_unavailable"
    finally:
        invocation.stop()


def test_feedback_call_close_drains_accepted_tcp_request(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """受付済み request の保存完了後にだけ capability を失効する。"""
    root = make_repo(tmp_path)
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
            agent_call_id="agc_drain",
            agent_call_kind="build_drain",
            codex_call_id="cdc_drain",
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

        def close_call() -> None:
            """対象 call の drain 完了を親 thread へ通知する。"""
            close_started.set()
            try:
                invocation.close_call(call)
            except BaseException as exc:
                close_errors.append(exc)
            finally:
                close_finished.set()

        submission_thread = threading.Thread(target=submit)
        submission_thread.start()
        assert storage_started.wait(timeout=2)
        close_thread = threading.Thread(target=close_call)
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


def test_parallel_feedback_call_lifecycles_are_isolated(tmp_path: Path) -> None:
    """並行 call の片方を閉じても他方の request を継続受理する。"""
    root = make_repo(tmp_path)
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    invocation.start()
    try:
        first = invocation.register_call(
            agent_call_id="agc_parallel_one",
            agent_call_kind="build_parallel_one",
            codex_call_id="cdc_parallel_one",
            log_paths=[],
        )
        second = invocation.register_call(
            agent_call_id="agc_parallel_two",
            agent_call_kind="build_parallel_two",
            codex_call_id="cdc_parallel_two",
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
        assert contexts == {"agc_parallel_one", "agc_parallel_two"}
        invocation.close_call(second)
    finally:
        invocation.stop()


def test_collector_limits_unauthenticated_request_read_time(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """改行前で停止した未認証接続を短い絶対 deadline で終了する。"""
    root = make_repo(tmp_path)
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
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """current HEAD を取得できない場合は invalid context を保存しない。"""
    root = make_repo(tmp_path)
    logger = SubcommandLogger(root, "feedback test")

    def fail_head_commit(_root: Path) -> str:
        """collector context の HEAD 取得失敗を再現する。"""
        raise RuntimeError("git is unavailable")

    monkeypatch.setattr(feedback_module, "head_commit", fail_head_commit)
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    call = invocation.register_call(
        agent_call_id="agc_head_failure",
        agent_call_kind="build_head_failure",
        codex_call_id="cdc_head_failure",
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
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """collector の degraded fallback はユーザー中断を握り潰さない。"""
    root = make_repo(tmp_path)
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
            agent_call_id="agc_interrupt",
            agent_call_kind="build_interrupt",
            codex_call_id="cdc_interrupt",
            log_paths=[],
        )


def test_agent_store_rejects_outside_path_and_masks_secret(tmp_path: Path) -> None:
    """repository path boundary と secret masking を raw publication 前に適用する。"""
    root = make_repo(tmp_path)
    with pytest.raises(FeedbackRejected) as outside:
        store_agent_observation(
            root,
            _context(root),
            _payload(path=str(tmp_path / "outside.txt")),
        )
    assert outside.value.code == "path_outside_repo"
    with pytest.raises(FeedbackRejected) as masked_outside:
        store_agent_observation(
            root,
            _context(root),
            _payload(
                path="Authorization: Bearer abcdefghijklmnopqrstuvwxyz/../../outside.txt"
            ),
        )
    assert masked_outside.value.code == "path_outside_repo"

    (root / "loop").symlink_to("loop")
    with pytest.raises(FeedbackRejected) as malformed:
        store_agent_observation(root, _context(root), _payload(path="loop"))
    assert malformed.value.code == "path_outside_repo"

    outside = tmp_path / "outside"
    outside.mkdir()
    (root / "outside-link").symlink_to(outside, target_is_directory=True)
    with pytest.raises(FeedbackRejected) as missing_outside:
        store_agent_observation(
            root, _context(root), _payload(path="outside-link/missing.txt")
        )
    assert missing_outside.value.code == "path_outside_repo"

    redacted = _payload(
        text="request failed before Authorization: Bearer abcdefghijklmnopqrstuvwxyz",
        kind="error",
        path=None,
    )
    result, path = store_agent_observation(root, _context(root), redacted)

    assert result["redaction_count"] == 1
    assert "[REDACTED:authorization]" in path.read_text()
    assert "abcdefghijklmnopqrstuvwxyz" not in path.read_text()


def test_report_reference_rejects_symlinked_parent_outside(tmp_path: Path) -> None:
    """report cut reference が symlink 親経由の repository 外 path を読まない。"""
    root = make_repo(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_text("SECRET\n")
    (root / "link").symlink_to(outside, target_is_directory=True)

    assert feedback_report_module._repository_path(root, "link/secret.txt") is None


def test_report_reference_masks_secret_across_content_limit(tmp_path: Path) -> None:
    """capture 上限をまたぐ private key block の断片を保存しない。"""
    root = make_repo(tmp_path)
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


def test_machine_detector_observation_id_is_idempotent(tmp_path: Path) -> None:
    """同じ stable event の再検出を同じ raw observation 一件へ収束させる。"""
    root = make_repo(tmp_path)
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    event = {
        "event_schema_version": 1,
        "event_id": "evt_reporter_unavailable",
        "event_type": "feedback.reporter_unavailable",
        "occurred_at": rfc3339_now(),
        "subcommand_invocation_id": logger.invocation_id,
        "component": "collector",
        "failure_code": "protocol_error",
    }

    invocation.detect_event(event, logger.path)
    invocation.detect_event(event, logger.path)

    [path] = iter_observation_paths(root)
    observation = read_json_object(path)
    assert validate_observation_envelope(observation) == []
    assert observation["source_event"]["event_id"] == event["event_id"]


def test_completion_count_reports_only_pending_raw_observations(tmp_path: Path) -> None:
    """正常 report 前は raw store の pending 件数一値だけを返す。"""
    root = make_repo(tmp_path)
    store_agent_observation(root, _context(root), _payload())

    assert feedback_completion_counts(root) == (1, [])


def test_legacy_raw_is_read_without_rewriting_but_new_v1_submission_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """導入前の v1 raw は assertion として扱い、新しい受付には v2 を要求する。"""
    from commons.runtime_feedback_store import reporter_payload_view

    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _, raw, identity = _store_agent_issue(root, session_id)
    legacy = read_json_object(raw)
    legacy["payload"]["schema_version"] = 1
    legacy["payload"]["human_action_reason"] = legacy["payload"].pop(
        "workload_limitation"
    )
    content = canonical_json_bytes(legacy)
    raw.write_bytes(content)
    (feedback_root(root) / "intake.json").unlink()
    assert validate_observation_envelope(legacy) == []
    view = reporter_payload_view(legacy["payload"])
    assert view["schema_version"] == 2
    assert view["workload_limitation"] == legacy["payload"]["human_action_reason"]
    with pytest.raises(FeedbackRejected, match="human_action_reason"):
        store_agent_observation(root, _context(root), legacy["payload"])

    def fake_call(*_args: Any, **_kwargs: Any) -> SimpleNamespace:
        assert raw.read_bytes() == content
        return _fake_result(root, _remediation_output(identity, "already_resolved"))

    monkeypatch.setattr(feedback_report_module, "run_codex_exec", fake_call)
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    assert load_active_state(root).issues == {}
    assert not raw.exists()


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_canonical_json_rejects_non_json_numbers(value: float) -> None:
    """raw と state に標準 JSON でない数値を保存しない。"""
    with pytest.raises(ValueError):
        canonical_json_bytes({"value": value})


def test_completion_count_warns_instead_of_ignoring_unknown_raw_artifact(
    tmp_path: Path,
) -> None:
    """raw store inventory が不正なら件数を推測せず unavailable warning を返す。"""
    root = make_repo(tmp_path)
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
    invalid_parent: str,
) -> None:
    """不正な observation 親を空の初期 state として扱わない。"""
    root = make_repo(tmp_path)
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


def test_feedback_writer_lock_rejects_concurrent_writer(tmp_path: Path) -> None:
    """同じ repository で二つ目の report writer を開始しない。"""
    root = make_repo(tmp_path)
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
    log_dir = root / ".cmoc/gu/ar/log/sub_command"
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
    state = validate_feedback_state(root)
    assert state.current is not None
    assert state.current["result"] == "ok"
    assert state.issues == {}
    assert state.machine_aggregates == {}
    assert load_report_cut(root) is None
    [report] = (root / ".cmoc/gu/ar/report/feedback").glob("*.md")
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
                agent_call_id="agc_wave",
                agent_call_kind=parameter.agent_call_kind,
                codex_call_id="cdc_wave",
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
    if last_status == "human_required":
        assert set(state.issues) == {later_id}
        assert all(not path.exists() for path in raw_paths)
    else:
        assert state.current is None
        assert all(path.exists() for path in raw_paths)


@pytest.mark.parametrize(
    "fault",
    [
        "unreported_change",
        "forbidden_change",
        "checkpoint",
        "checkpoint_reference",
        "interrupt",
    ],
)
@pytest.mark.parametrize("operation", ["join", "abandon"])
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


@pytest.mark.parametrize(
    "fault", ["publication", "cleanup", "merge_reference", "completion_reference"]
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
    name = (
        "publish_current_pointer" if fault == "publication" else "_cleanup_joined_run"
    )
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
    for operation in ("join", "abandon"):
        rejected = runner.invoke(app, ["run", operation], catch_exceptions=False)
        assert rejected.exit_code == 1, rejected.output
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


def test_current_pointer_rejects_non_markdown_report_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """current pointer が Markdown 以外の report artifact を選べない。"""
    root = make_repo(tmp_path)
    _active_session(root, monkeypatch)
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert result.exit_code == 0, result.output

    pointer_path = feedback_root(root) / "active" / "current.json"
    pointer = read_json_object(pointer_path)
    current_report = root / str(pointer["report_path"])
    invalid_report = current_report.with_suffix(".json")
    invalid_report.write_bytes(current_report.read_bytes())
    pointer["report_path"] = invalid_report.relative_to(root).as_posix()
    pointer["report_sha256"] = hashlib.sha256(invalid_report.read_bytes()).hexdigest()
    pointer_path.write_bytes(canonical_json_bytes(pointer))

    with pytest.raises(CmocError, match="Markdown report path"):
        load_active_state(root)


@pytest.mark.parametrize("terminal_verdict", ["already_resolved", "not_actionable"])
def test_agent_issue_is_verified_compacted_then_removed_for_terminal_verdict(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    terminal_verdict: str,
) -> None:
    """pending raw を active issue へ集約し、terminal verdict なら active から除く。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _observation_id, raw_path, candidate_id = _store_agent_issue(root, session_id)
    _install_codex_outputs(
        monkeypatch, _remediation_output(candidate_id, "human_required")
    )

    first = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert first.exit_code == 0, first.output
    assert not raw_path.exists()
    first_state = load_active_state(root)
    assert set(first_state.issues) == {candidate_id}
    issue = first_state.issues[candidate_id]
    assert issue["occurrence_count"] == 1
    assert issue["verification"]["human_action"] == "README の設定を修正する。"
    assert "reference_id" not in json.dumps(issue["verification"], ensure_ascii=False)
    assert feedback_completion_counts(root) == (0, [])

    _install_codex_outputs(
        monkeypatch, _remediation_output(candidate_id, terminal_verdict)
    )
    second = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert second.exit_code == 0, second.output
    second_state = load_active_state(root)
    assert second_state.issues == {}
    reports = list((root / ".cmoc/gu/ar/report/feedback").glob("*.md"))
    assert len(reports) == 2
    assert second_state.current is not None
    current_report = root / str(second_state.current["report_path"])
    assert candidate_id not in current_report.read_text()
    assert "human_required_issue_count: 0" in current_report.read_text()
    generation_directories = list(
        (feedback_root(root) / "active" / "generation").iterdir()
    )
    assert len(generation_directories) == 1


def test_machine_observation_stays_bounded_until_recurrence_threshold(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """threshold 未満は bounded aggregate、到達後は remediation candidate にする。"""
    root = make_repo(tmp_path)
    _active_session(root, monkeypatch)
    log_path = root / ".cmoc/gu/ar/log/test.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text('{"event":"reporter unavailable"}\n')
    canonical_key: str | None = None

    for index in range(2):
        event = {
            "event_schema_version": 1,
            "event_id": f"evt_{index}",
            "event_type": "feedback.reporter_unavailable",
            "occurred_at": rfc3339_now(),
            "subcommand_invocation_id": f"scope_{index}",
            "component": "reporter",
            "failure_code": "missing",
        }
        context = _context(root, session_id=f"session_{index}")
        context["subcommand_invocation_id"] = f"scope_{index}"
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
                    reference_path=".cmoc/gu/ar/log/test.jsonl",
                ),
            )
        result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
        assert result.exit_code == 0, result.output
        state = load_active_state(root)
        if index == 0:
            assert set(state.machine_aggregates) == {canonical_key}
            assert state.issues == {}
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
    log_path = root / ".cmoc/gu/ar/log/test.jsonl"
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
            "subcommand_invocation_id": f"scope_expiry_{index}",
            "component": "reporter",
            "failure_code": "missing",
        }
        context = _context(root, session_id=f"session_expiry_{index}")
        context["subcommand_invocation_id"] = f"scope_expiry_{index}"
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
            reference_path=".cmoc/gu/ar/log/test.jsonl",
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
            reference_path=".cmoc/gu/ar/log/test.jsonl",
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
            reference_path=".cmoc/gu/ar/log/test.jsonl",
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


@pytest.mark.parametrize("raw_content", ["not-json\n", '{"x": NaN}\n'])
def test_invalid_raw_observation_blocks_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, raw_content: str
) -> None:
    """validation 不通過 raw を処理済みにせず、正常 report を publication しない。"""
    root = make_repo(tmp_path)
    _active_session(root, monkeypatch)
    observation_id = "fbo_00000000-0000-7000-8000-000000000099"
    raw_path = observation_path(root, observation_id, "2030-01-02T00:00:00Z")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(raw_content)

    result = runner.invoke(app, ["feedback", "report"])

    assert result.exit_code == 1
    assert raw_path.read_text() == raw_content
    assert str(raw_path) in result.output
    assert not (feedback_root(root) / "active" / "current.json").exists()
    assert not list((root / ".cmoc/gu/ar/report/feedback").glob("*.md"))
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


def test_active_generation_hash_mismatch_is_corruption(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """current pointer が列挙する active record の改変を無視して続行しない。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _observation_id, _raw_path, candidate_id = _store_agent_issue(root, session_id)
    _install_codex_outputs(
        monkeypatch, _remediation_output(candidate_id, "human_required")
    )
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    state = load_active_state(root)
    assert state.generation_manifest is not None
    [reference] = state.generation_manifest["issues"]
    issue_path = root / reference["path"]
    issue = read_json_object(issue_path)
    issue["summary"] = "改変済み"
    issue_path.write_bytes(canonical_json_bytes(issue))

    with pytest.raises(CmocError, match="SHA256"):
        load_active_state(root)


def test_unlisted_active_generation_artifact_is_corruption(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """manifest が列挙しない active generation file を無視しない。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _observation_id, _raw_path, candidate_id = _store_agent_issue(root, session_id)
    _install_codex_outputs(
        monkeypatch, _remediation_output(candidate_id, "human_required")
    )
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    state = load_active_state(root)
    assert state.current is not None
    manifest_path = root / str(state.current["generation_manifest_path"])
    unexpected = manifest_path.parent / "unexpected.json"
    unexpected.write_text("{}\n")

    with pytest.raises(CmocError, match="未定義 artifact"):
        validate_feedback_state(root)
