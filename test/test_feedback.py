"""feedback の pending observation、active state、atomic publication を検証する。

agent-facing reporter から raw store、report cut、verification、current pointer、cleanup
までを同じ repository fixture で追跡する。publication 後に compact active state だけが
残ることを外部境界として検証する。

対応する oracle file:

- `{{work-root}}/oracle/doc/app_spec/feedback_observation.md`
- `{{work-root}}/oracle/doc/app_spec/console_and_file_log.md`
- `{{work-root}}/oracle/doc/app_spec/feedback_state.md`
- `{{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md`
- `{{work-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.json`
- `{{work-root}}/oracle/src/oracle/acp_builder/feedback/verify_issue.json`
"""

import hashlib
import json
from collections.abc import Iterator
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest
from _cli_support import run_doctor, runner
from _git_support import current_branch, make_repo, run_git
from jsonschema import ValidationError, validate
from oracle.acp_builder.feedback.normalize_issue import (
    build_feedback_normalize_issue_parameter as _build_canonical_normalize_parameter,
)
from oracle.acp_builder.feedback.verify_issue import (
    build_feedback_verify_issue_parameter as _build_canonical_verify_parameter,
)

import commons.runtime_codex_preflight as codex_preflight_module
import commons.runtime_feedback as feedback_module
import commons.runtime_feedback_reporter as reporter_module
import commons.runtime_feedback_state as feedback_state_module
import sub_commands.feedback.report as feedback_report_module
from acp.builder.feedback.normalize_issue import (
    build_feedback_normalize_issue_parameter,
)
from acp.builder.feedback.verify_issue import build_feedback_verify_issue_parameter
from basic.acp import FileAccessMode
from cmoc_runtime import CmocError
from commons.runtime_feedback import (
    FeedbackInvocation,
    begin_feedback_call,
    start_feedback_invocation,
)
from commons.runtime_feedback_state import (
    cleanup_published_report,
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
    store_agent_observation,
    store_machine_observation,
)
from commons.runtime_logging import SubcommandLogger
from main import app


@pytest.fixture(autouse=True)
def reset_indexing_preflight() -> Iterator[None]:
    """process-global な indexing preflight を case 間で分離する。"""
    codex_preflight_module.disable_indexing_preflight()
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
        "schema_version": 1,
        "category": "tooling",
        "severity": "moderate",
        "summary": "反復する feedback test issue",
        "impact": "同じ作業を再実行する必要がある。",
        "human_action_reason": "tooling の設定確認が必要である。",
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


def _active_session(root: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    """doctor 済み repository を active session の ready 状態にする。"""
    monkeypatch.chdir(root)
    run_doctor(root)
    result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    branch = current_branch(root)
    assert branch.startswith("cmoc/session/")
    return branch.removeprefix("cmoc/session/")


def _repository_reference_id(path: str) -> str:
    """report cut の repository reference ID と同じ決定関数を返す。"""
    digest = hashlib.sha256(path.encode("utf-8")).hexdigest()[:24]
    return f"ref:{digest}"


def _verification_output(
    candidate_id: str, verdict: str, *, reference_path: str = "README.md"
) -> dict[str, object]:
    """README current reference を根拠にする正式な verification output を返す。"""
    if verdict == "inconclusive":
        evidence: list[dict[str, str]] = []
    else:
        evidence = [
            {
                "reference_id": _repository_reference_id(reference_path),
                "location": f"{reference_path}:1",
                "finding": "report cut で現在状態を確認した。",
            }
        ]
    return {
        "result": {
            "candidate_id": candidate_id,
            "verdict": verdict,
            "current_evidence": evidence,
            "human_action": "README の設定を修正する。"
            if verdict == "unresolved"
            else None,
            "reason": "固定済み README 参照から現在状態を判定した。",
        }
    }


def _install_codex_outputs(
    monkeypatch: pytest.MonkeyPatch, *outputs: dict[str, object]
) -> None:
    """feedback 専用 Codex call の正式 output を呼出順で返す。"""
    remaining = iter(outputs)

    def fake_run_codex_exec(*_args: object, **_kwargs: object) -> SimpleNamespace:
        return SimpleNamespace(output_json=next(remaining))

    monkeypatch.setattr(feedback_report_module, "run_codex_exec", fake_run_codex_exec)


def _install_verification_verdicts(
    monkeypatch: pytest.MonkeyPatch,
    verdicts: dict[str, tuple[str, str]],
    calls: list[str] | None = None,
) -> None:
    """candidate ID ごとに verdict と current reference path を返す。"""

    def fake_run_codex_exec(*_args: object, **kwargs: object) -> SimpleNamespace:
        purpose = kwargs.get("purpose")
        prefix = "feedback issue verification ("
        if not isinstance(purpose, str) or not purpose.startswith(prefix):
            pytest.fail(f"unexpected feedback agent call: {purpose!r}")
        candidate_id = purpose.removeprefix(prefix).removesuffix(")")
        if calls is not None:
            calls.append(candidate_id)
        verdict, reference_path = verdicts[candidate_id]
        return SimpleNamespace(
            output_json=_verification_output(
                candidate_id,
                verdict,
                reference_path=reference_path,
            )
        )

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
    sent: list[bytes] = []

    class FakeSocket:
        def __enter__(self) -> "FakeSocket":
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def settimeout(self, _seconds: int) -> None:
            return None

        def connect(self, _path: str) -> None:
            return None

        def sendall(self, value: bytes) -> None:
            sent.append(value)

        def recv(self, _size: int) -> bytes:
            return b'{"status":"accepted","observation_id":"fbo_test","redaction_count":0}\n'

    monkeypatch.setattr(reporter_module.socket, "socket", lambda *_args: FakeSocket())
    monkeypatch.setenv("CMOC_FEEDBACK_COLLECTOR_SOCKET", "/tmp/collector.sock")
    monkeypatch.setenv("CMOC_FEEDBACK_CAPABILITY", "secret-capability")
    monkeypatch.setenv("CMOC_FEEDBACK_PROTOCOL_VERSION", "1")

    result = reporter_module._submit(_payload())

    assert result["status"] == "accepted"
    request = json.loads(sent[0])
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

        def connect(self, _path: str) -> None:
            return None

        def sendall(self, value: bytes) -> None:
            sent.append(value)

        def recv(self, _size: int) -> bytes:
            return (
                b'{"status":"rejected","code":"schema_invalid",'
                b'"message":"payload is not valid UTF-8","retryable":false}\n'
            )

    monkeypatch.setattr(reporter_module.socket, "socket", lambda *_args: FakeSocket())
    monkeypatch.setenv("CMOC_FEEDBACK_COLLECTOR_SOCKET", "/tmp/collector.sock")
    monkeypatch.setenv("CMOC_FEEDBACK_CAPABILITY", "secret-capability")
    monkeypatch.setenv("CMOC_FEEDBACK_PROTOCOL_VERSION", "1")

    result = reporter_module._submit(_payload(text="\ud800"))

    assert result["status"] == "rejected"
    assert json.loads(sent[0])["payload"]["evidence"][0]["text"] == "\ud800"


@pytest.mark.parametrize(
    "response",
    [
        b'{"status":"accepted"}\n',
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

        def connect(self, _path: str) -> None:
            return None

        def sendall(self, _value: bytes) -> None:
            return None

        def recv(self, _size: int) -> bytes:
            return response

    monkeypatch.setattr(reporter_module.socket, "socket", lambda *_args: FakeSocket())
    monkeypatch.setenv("CMOC_FEEDBACK_COLLECTOR_SOCKET", "/tmp/collector.sock")
    monkeypatch.setenv("CMOC_FEEDBACK_CAPABILITY", "secret-capability")
    monkeypatch.setenv("CMOC_FEEDBACK_PROTOCOL_VERSION", "1")

    assert reporter_module._submit(_payload()) == {
        "status": "rejected",
        "code": "protocol_mismatch",
        "message": "invalid collector response",
        "retryable": False,
    }


def test_feedback_agent_builders_are_readonly_and_schema_scoped(tmp_path: Path) -> None:
    """canonical prompt を保ち、入力だけを使う agent call を構築する。"""
    root = make_repo(tmp_path)
    candidate_id = "fbi_" + "a" * 26
    observation_json = json.dumps({"observation_id": "fbo_input"})
    candidates_json = json.dumps([{"candidate_id": candidate_id}])
    candidate_json = json.dumps({"candidate_id": candidate_id})
    references_json = json.dumps(
        [
            {
                "reference_id": "ref:readme",
                "kind": "repository_content",
                "content": "# repo",
            }
        ]
    )
    normalizer = build_feedback_normalize_issue_parameter(
        observation_json,
        candidates_json,
        root,
    )
    verifier = build_feedback_verify_issue_parameter(
        candidate_json,
        references_json,
        root,
    )

    assert normalizer == _build_canonical_normalize_parameter(
        observation_json,
        candidates_json,
        root,
    )
    assert verifier == _build_canonical_verify_parameter(
        candidate_json,
        references_json,
        root,
    )
    assert normalizer.file_access_mode is FileAccessMode.READONLY
    assert verifier.file_access_mode is FileAccessMode.READONLY
    assert normalizer.structured_output_schema_path is not None
    assert verifier.structured_output_schema_path is not None
    assert "同一性" in normalizer.prompt
    assert "unresolved | resolved | not_actionable | inconclusive" in verifier.prompt
    assert "# routing rule" not in normalizer.prompt
    assert "# routing rule" not in verifier.prompt
    normalize_schema = json.loads(normalizer.structured_output_schema_path.read_text())
    verify_schema = json.loads(verifier.structured_output_schema_path.read_text())
    validate(
        {
            "result": {
                "decision": "existing",
                "existing_issue_id": candidate_id,
            }
        },
        normalize_schema,
    )
    validate(_verification_output(candidate_id, "unresolved"), verify_schema)
    with pytest.raises(ValidationError):
        validate(
            {
                "result": {
                    "decision": "new",
                    "existing_issue_id": candidate_id,
                }
            },
            normalize_schema,
        )


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


def test_feedback_verify_builder_protects_nested_code_fences(
    tmp_path: Path,
) -> None:
    """verification の動的 JSON が prompt section の境界を閉じないことを検証する。"""
    root = make_repo(tmp_path)
    nested = "before\n```\ninside\n```\nafter"
    candidate_json = json.dumps({"candidate_id": "fbi_" + "a" * 26, "summary": nested})
    references_json = json.dumps(
        [
            {
                "reference_id": "ref:readme",
                "kind": "repository_content",
                "content": nested,
            }
        ]
    )

    parameter = build_feedback_verify_issue_parameter(
        candidate_json,
        references_json,
        root,
    )

    candidate_start = parameter.prompt.index("# issue candidate")
    candidate_end = parameter.prompt.index(
        "\n\n# report cut references", candidate_start
    )
    references_start = candidate_end + 2
    references_end = parameter.prompt.index(
        "\n\n# place holder definition", references_start
    )
    candidate_section = parameter.prompt[candidate_start:candidate_end]
    references_section = parameter.prompt[references_start:references_end]
    assert candidate_section.startswith("# issue candidate\n\n````json\n")
    assert candidate_section.endswith("\n````")
    assert references_section.startswith("# report cut references\n\n````json\n")
    assert references_section.endswith("\n````")
    assert candidate_json in candidate_section
    assert references_json in references_section


def test_feedback_processing_versions_hash_canonical_builders() -> None:
    """checkpoint version は prompt 構築 builder とその依存を識別する。"""
    normalize_path = feedback_report_module._builder_source_path(
        _build_canonical_normalize_parameter
    )
    verify_path = feedback_report_module._builder_source_path(
        _build_canonical_verify_parameter
    )
    renderer_path = feedback_report_module._builder_source_path(
        feedback_report_module.render_as_markdown
    )

    assert (
        build_feedback_normalize_issue_parameter is _build_canonical_normalize_parameter
    )
    assert build_feedback_verify_issue_parameter is _build_canonical_verify_parameter
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
    assert versions["verification_builder"] == verification_version


def test_feedback_verification_postcondition_rejects_non_concrete_text() -> None:
    """schema の末尾改行と空白だけの text を verification で受理しない。"""
    candidate_id = "fbi_" + "a" * 26
    reference_id = _repository_reference_id("README.md")
    references = {reference_id: {"kind": "repository_content"}}
    valid = _verification_output(candidate_id, "unresolved")
    assert not feedback_report_module._verification_output_issues(
        valid, candidate_id, set(references), references
    )

    cases: list[tuple[dict[str, object], str]] = [
        (
            {"human_action": " \n"},
            "$.result.human_action",
        ),
        (
            {"human_action": "a" * 1200 + "\n"},
            "$.result.human_action",
        ),
        (
            {"reason": " \n"},
            "$.result.reason",
        ),
        (
            {
                "current_evidence": [
                    {
                        "reference_id": reference_id,
                        "location": "a" * 500 + "\n",
                        "finding": "current finding",
                    }
                ]
            },
            "$.result.current_evidence[0].location",
        ),
        (
            {
                "current_evidence": [
                    {
                        "reference_id": reference_id,
                        "location": "README.md:1",
                        "finding": " \n",
                    }
                ]
            },
            "$.result.current_evidence[0].finding",
        ),
    ]
    for updates, location in cases:
        output = _verification_output(candidate_id, "unresolved")
        result = output["result"]
        assert isinstance(result, dict)
        result.update(updates)
        issues = feedback_report_module._verification_output_issues(
            output, candidate_id, set(references), references
        )
        assert any(issue.location == location for issue in issues)


def test_feedback_verification_accepts_semantic_current_fingerprint() -> None:
    """意味を持つ current fingerprint だけの unresolved evidence を受理する。"""
    candidate_id = "fbi_" + "a" * 26
    reference_id = _repository_reference_id("missing.cfg")
    references = {
        reference_id: {
            "kind": "current_fingerprint",
            "path": "missing.cfg",
            "state": "missing",
            "sha256": None,
        }
    }
    output = _verification_output(
        candidate_id, "unresolved", reference_path="missing.cfg"
    )

    assert not feedback_report_module._verification_output_issues(
        output, candidate_id, set(references), references
    )


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
    tmp_path: Path,
) -> None:
    """call capability の受理、rate limit、失効を raw 保存結果から確認する。"""
    root = make_repo(tmp_path)
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    call = invocation.register_call(
        agent_call_id="agc_one",
        agent_call_kind="build_one",
        codex_call_id="cdc_one",
        codex_session_id="session_one",
        log_paths=[root / ".cmoc/gu/ar/log/codex/call.json"],
    )
    request = {"protocol": "1", "capability": call.capability, "payload": _payload()}

    accepted = [invocation._submit_request(request) for _index in range(3)]

    assert all(result["status"] == "accepted" for result in accepted)
    paths = iter_observation_paths(root)
    assert len(paths) == 3
    envelope = read_json_object(paths[0])
    assert validate_observation_envelope(envelope) == []
    assert envelope["context"]["agent_call_id"] == "agc_one"
    with pytest.raises(FeedbackRejected) as rate_error:
        invocation._submit_request(request)
    assert rate_error.value.code == "rate_limited"
    invocation.close_call(call)
    with pytest.raises(FeedbackRejected) as context_error:
        invocation._submit_request(request)
    assert context_error.value.code == "context_invalid"


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
    assert "unresolved_issue_count: 0" in text


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


def test_agent_issue_is_verified_compacted_then_removed_when_resolved(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """pending raw を unresolved active issue へ集約し、次回 resolved なら active から除く。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _observation_id, raw_path, candidate_id = _store_agent_issue(root, session_id)
    _install_codex_outputs(
        monkeypatch, _verification_output(candidate_id, "unresolved")
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

    _install_codex_outputs(monkeypatch, _verification_output(candidate_id, "resolved"))
    second = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert second.exit_code == 0, second.output
    second_state = load_active_state(root)
    assert second_state.issues == {}
    reports = list((root / ".cmoc/gu/ar/report/feedback").glob("*.md"))
    assert len(reports) == 2
    assert second_state.current is not None
    current_report = root / str(second_state.current["report_path"])
    assert candidate_id not in current_report.read_text()
    assert "unresolved_issue_count: 0" in current_report.read_text()
    generation_directories = list(
        (feedback_root(root) / "active" / "generation").iterdir()
    )
    assert len(generation_directories) == 1


def test_inconclusive_verdict_saves_incomplete_report_without_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """全 verdict を診断し、current/raw を維持したまま次回は新しい cut にする。"""
    # {{work-root}}/oracle/doc/app_spec/feedback_state.md
    # {{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _first_observation_id, _first_raw, readme_candidate_id = _store_agent_issue(
        root, session_id
    )
    other_path = root / "OTHER.md"
    other_path.write_text("current evidence\n")
    accepted, _other_raw = store_agent_observation(
        root,
        _context(root, session_id=session_id),
        _payload(text="OTHER の反復問題を確認した。", path="OTHER.md"),
    )
    other_observation_id = str(accepted["observation_id"])
    other_candidate_id = issue_id(f"agent\0{other_observation_id}")
    reference_paths = {
        readme_candidate_id: "README.md",
        other_candidate_id: "OTHER.md",
    }
    initial_calls: list[str] = []
    _install_verification_verdicts(
        monkeypatch,
        {
            candidate_id: ("unresolved", reference_path)
            for candidate_id, reference_path in reference_paths.items()
        },
        initial_calls,
    )

    first = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert first.exit_code == 0, first.output
    assert initial_calls == sorted(reference_paths)
    first_state = validate_feedback_state(root)
    assert set(first_state.issues) == set(reference_paths)
    pointer_path = feedback_root(root) / "active" / "current.json"
    first_pointer = pointer_path.read_bytes()
    normal_reports = list((root / ".cmoc/gu/ar/report/feedback").glob("*.md"))
    assert len(normal_reports) == 1
    generation_count = len(
        list((feedback_root(root) / "active" / "generation").iterdir())
    )

    _pending_observation_id, pending_raw, _new_candidate_id = _store_agent_issue(
        root, session_id
    )
    inconclusive_id = min(reference_paths)
    unresolved_id = next(
        candidate_id
        for candidate_id in reference_paths
        if candidate_id != inconclusive_id
    )
    incomplete_calls: list[str] = []
    _install_verification_verdicts(
        monkeypatch,
        {
            candidate_id: (
                "inconclusive" if candidate_id == inconclusive_id else "unresolved",
                reference_path,
            )
            for candidate_id, reference_path in reference_paths.items()
        },
        incomplete_calls,
    )

    log_dir = root / ".cmoc/gu/ar/log/sub_command"
    previous_logs = set(log_dir.glob("*.jsonl"))
    incomplete = runner.invoke(app, ["feedback", "report"])

    assert incomplete.exit_code == 0
    [incomplete_log_path] = set(log_dir.glob("*.jsonl")) - previous_logs
    incomplete_events = [
        json.loads(line) for line in incomplete_log_path.read_text().splitlines()
    ]
    [incomplete_event] = [
        event
        for event in incomplete_events
        if event["event"] == "feedback_report_incomplete"
    ]
    assert Path(incomplete_event["report_path"]).is_absolute()
    assert incomplete_calls == sorted(reference_paths)
    assert "result: `incomplete`" in incomplete.output
    assert "verification candidates: `2`" in incomplete.output
    assert "unresolved candidates: `1`" in incomplete.output
    assert "inconclusive candidates: `1`" in incomplete.output
    assert "normal publication: `not completed`" in incomplete.output
    assert pointer_path.read_bytes() == first_pointer
    assert pending_raw.exists()
    assert len(list((root / ".cmoc/gu/ar/report/feedback").glob("*.md"))) == 1
    assert (
        len(list((feedback_root(root) / "active" / "generation").iterdir()))
        == generation_count
    )
    terminal = load_report_cut(root)
    assert terminal is not None
    terminal_manifest, _terminal_path = terminal
    assert terminal_manifest["processing"]["status"] == "incomplete"
    assert terminal_manifest["publication"] is None
    diagnostic = terminal_manifest["diagnostic"]
    assert isinstance(diagnostic, dict)
    diagnostic_report = root / str(diagnostic["report"]["path"])
    text = diagnostic_report.read_text()
    assert 'result: "incomplete"' in text
    assert "active_generation_id" not in text
    assert "verification_candidate_count: 2" in text
    assert "unresolved_candidate_count: 1" in text
    assert "inconclusive_candidate_count: 1" in text
    assert text.index(
        "## 確定済みだが今回未 publication の unresolved candidate"
    ) < text.index("## inconclusive candidate")
    assert f"### {unresolved_id}" in text
    assert f"### {inconclusive_id}" in text
    assert "今回の active generation へ publication されていません" in text
    assert "確認できた current evidence はありません" in text

    rerun_calls: list[str] = []
    _install_verification_verdicts(
        monkeypatch,
        {
            candidate_id: ("resolved", reference_path)
            for candidate_id, reference_path in reference_paths.items()
        },
        rerun_calls,
    )
    rerun = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert rerun.exit_code == 0, rerun.output
    assert rerun_calls == sorted(reference_paths)
    assert load_report_cut(root) is None
    assert not pending_raw.exists()
    assert diagnostic_report.exists()
    assert pointer_path.read_bytes() != first_pointer
    assert validate_feedback_state(root).issues == {}


@pytest.mark.parametrize(
    ("write_error", "first_exit_code"),
    [(OSError("diagnostic write failed"), 1), (KeyboardInterrupt(), 0)],
    ids=("write-error", "user-interruption"),
)
def test_incomplete_report_write_failure_reuses_formal_checkpoints(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    write_error: BaseException,
    first_exit_code: int,
) -> None:
    """診断未完了は staging cut を保持し、再実行で AI call を繰り返さない。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _observation_id, raw_path, candidate_id = _store_agent_issue(root, session_id)
    _install_codex_outputs(
        monkeypatch,
        _verification_output(candidate_id, "inconclusive"),
    )
    original_write = feedback_report_module.write_immutable_bytes

    def fail_diagnostic_write(path: Path, content: bytes) -> str:
        if path.parent.name == "incomplete":
            raise write_error
        return original_write(path, content)

    monkeypatch.setattr(
        feedback_report_module,
        "write_immutable_bytes",
        fail_diagnostic_write,
    )

    failed = runner.invoke(app, ["feedback", "report"])

    assert failed.exit_code == first_exit_code
    staged = load_report_cut(root)
    assert staged is not None
    staged_manifest, _staged_path = staged
    assert staged_manifest["processing"]["status"] == "diagnostic_staging"
    assert len(staged_manifest["processing"]["verification_checkpoints"]) == 1
    diagnostic = staged_manifest["diagnostic"]
    assert isinstance(diagnostic, dict)
    report_path = root / str(diagnostic["report"]["path"])
    assert not report_path.exists()
    assert raw_path.exists()
    assert not (feedback_root(root) / "active" / "current.json").exists()

    monkeypatch.setattr(
        feedback_report_module,
        "write_immutable_bytes",
        original_write,
    )
    monkeypatch.setattr(
        feedback_report_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: pytest.fail(
            "formal verification checkpoint must be reused"
        ),
    )
    resumed = runner.invoke(app, ["feedback", "report"])

    assert resumed.exit_code == 0
    terminal = load_report_cut(root)
    assert terminal is not None
    assert terminal[0]["processing"]["status"] == "incomplete"
    assert report_path.exists()
    assert raw_path.exists()
    assert not (feedback_root(root) / "active" / "current.json").exists()


def test_machine_observation_stays_bounded_until_recurrence_threshold(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """threshold 未満は bounded aggregate、到達後は verification candidate にする。"""
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
                _verification_output(
                    candidate_id,
                    "unresolved",
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
        _verification_output(
            candidate_id,
            "unresolved",
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
        _verification_output(
            candidate_id,
            "unresolved",
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
        _verification_output(
            candidate_id,
            "unresolved",
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


def test_invalid_raw_observation_blocks_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """validation 不通過 raw を処理済みにせず、正常 report を publication しない。"""
    root = make_repo(tmp_path)
    _active_session(root, monkeypatch)
    observation_id = "fbo_00000000-0000-7000-8000-000000000099"
    raw_path = observation_path(root, observation_id, "2030-01-02T00:00:00Z")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text("not-json\n")

    result = runner.invoke(app, ["feedback", "report"])

    assert result.exit_code == 1
    assert raw_path.read_text() == "not-json\n"
    assert not (feedback_root(root) / "active" / "current.json").exists()
    assert not list((root / ".cmoc/gu/ar/report/feedback").glob("*.md"))


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


def test_interruption_reuses_formal_verification_checkpoint(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """中断時は report を出さず、同じ cut の正式 checkpoint から publication を再開する。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _observation_id, raw_path, candidate_id = _store_agent_issue(root, session_id)
    _install_codex_outputs(
        monkeypatch, _verification_output(candidate_id, "unresolved")
    )
    original_publish = feedback_report_module.publish_generation_artifacts

    def interrupt_publication(*_args: object, **_kwargs: object) -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr(
        feedback_report_module,
        "publish_generation_artifacts",
        interrupt_publication,
    )
    interrupted = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert interrupted.exit_code == 0, interrupted.output
    assert "再開対象 report cut" in interrupted.output
    resumable = load_report_cut(root)
    assert resumable is not None
    cut_id = resumable[0]["report_cut_id"]
    assert resumable[0]["processing"]["status"] == "interrupted"
    assert len(resumable[0]["processing"]["verification_checkpoints"]) == 1
    assert raw_path.exists()
    assert not (feedback_root(root) / "active" / "current.json").exists()

    monkeypatch.setattr(
        feedback_report_module,
        "publish_generation_artifacts",
        original_publish,
    )
    monkeypatch.setattr(
        feedback_report_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: pytest.fail("formal checkpoint must be reused"),
    )
    resumed = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert resumed.exit_code == 0, resumed.output
    assert load_active_state(root).current["report_cut_id"] == cut_id
    assert load_report_cut(root) is None
    assert not raw_path.exists()


def test_interruption_during_cut_creation_is_normal_and_resumable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """cut 固定中の Ctrl+C も report を publication せず再開 state を残す。"""
    root = make_repo(tmp_path)
    _active_session(root, monkeypatch)
    original_create = feedback_report_module._create_report_cut

    def interrupt_after_durable_cut(*args: object, **kwargs: object) -> None:
        original_create(*args, **kwargs)
        raise KeyboardInterrupt

    monkeypatch.setattr(
        feedback_report_module, "_create_report_cut", interrupt_after_durable_cut
    )

    interrupted = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert interrupted.exit_code == 0, interrupted.output
    resumable = load_report_cut(root)
    assert resumable is not None
    assert resumable[0]["processing"]["status"] == "interrupted"
    assert not (feedback_root(root) / "active" / "current.json").exists()
    assert not list((root / ".cmoc/gu/ar/report/feedback").glob("*.md"))


def test_interruption_during_preconditions_is_normal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """report cut 固定前の Ctrl+C も feedback report の正常中断にする。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)

    def interrupt_preconditions(*_args: object) -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr(
        feedback_report_module, "_validate_preconditions", interrupt_preconditions
    )
    interrupted = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert interrupted.exit_code == 0, interrupted.output
    assert "ユーザー中断" in interrupted.output
    assert load_report_cut(root) is None
    assert not (feedback_root(root) / "active" / "current.json").exists()


def test_interruption_during_writer_lock_acquisition_is_normal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """report cut 前の writer lock 取得中断を正常終了として扱う。"""
    # {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
    root = make_repo(tmp_path)
    _active_session(root, monkeypatch)

    def interrupt_lock(_repo: Path) -> object:
        """writer lock の取得中にユーザー中断を再現する。"""
        raise KeyboardInterrupt()

    monkeypatch.setattr(feedback_report_module, "feedback_writer_lock", interrupt_lock)

    interrupted = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert interrupted.exit_code == 0, interrupted.output
    assert "ユーザー中断" in interrupted.output
    assert load_report_cut(root) is None
    assert not (feedback_root(root) / "active" / "current.json").exists()


def test_report_cut_rejects_observation_path_mismatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """report cut が observed_at と異なる raw path を固定していないことを検証する。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _observation_id, raw_path, _candidate_id = _store_agent_issue(root, session_id)
    original_create = feedback_report_module._create_report_cut

    def interrupt_after_durable_cut(*args: object, **kwargs: object) -> None:
        original_create(*args, **kwargs)
        raise KeyboardInterrupt

    monkeypatch.setattr(
        feedback_report_module, "_create_report_cut", interrupt_after_durable_cut
    )
    interrupted = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert interrupted.exit_code == 0, interrupted.output
    resumable = load_report_cut(root)
    assert resumable is not None
    manifest, manifest_path = resumable

    forged_path = (
        feedback_root(root) / "observation" / "v1" / "2099" / "01" / raw_path.name
    )
    forged_path.parent.mkdir(parents=True, exist_ok=True)
    forged_path.write_bytes(raw_path.read_bytes())
    observations = manifest["inputs"]["observations"]
    assert isinstance(observations, list) and len(observations) == 1
    assert isinstance(observations[0], dict)
    observations[0]["path"] = forged_path.relative_to(root).as_posix()
    manifest_path.write_bytes(canonical_json_bytes(manifest))

    with pytest.raises(CmocError, match="observation path"):
        load_report_cut(root)
    assert raw_path.exists()
    assert forged_path.exists()


def test_checkpoint_file_is_recovered_before_agent_call_reuse(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """checkpoint 保存後・manifest 更新前の停止でも quota を再消費しない。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _observation_id, raw_path, candidate_id = _store_agent_issue(root, session_id)
    _install_codex_outputs(
        monkeypatch, _verification_output(candidate_id, "unresolved")
    )
    original_record = feedback_report_module._record_checkpoint

    def fail_manifest_update(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("manifest update failed after checkpoint publication")

    monkeypatch.setattr(
        feedback_report_module, "_record_checkpoint", fail_manifest_update
    )
    failed = runner.invoke(app, ["feedback", "report"])

    assert failed.exit_code == 1
    resumable = load_report_cut(root)
    assert resumable is not None
    assert resumable[0]["processing"]["verification_checkpoints"] == []
    checkpoint_path = (
        resumable[1].parent / "checkpoint" / "verification" / f"{candidate_id}.json"
    )
    assert checkpoint_path.is_file()
    assert raw_path.exists()

    monkeypatch.setattr(feedback_report_module, "_record_checkpoint", original_record)
    monkeypatch.setattr(
        feedback_report_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: pytest.fail("formal checkpoint must be recovered"),
    )
    resumed = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert resumed.exit_code == 0, resumed.output
    assert not raw_path.exists()
    assert load_report_cut(root) is None


def test_unlisted_report_cut_artifact_is_corruption(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """report cut manifest が列挙しない work file を無視しない。"""
    root = make_repo(tmp_path)
    _active_session(root, monkeypatch)
    original_create = feedback_report_module._create_report_cut

    def interrupt_after_durable_cut(*args: object, **kwargs: object) -> None:
        original_create(*args, **kwargs)
        raise KeyboardInterrupt

    monkeypatch.setattr(
        feedback_report_module, "_create_report_cut", interrupt_after_durable_cut
    )
    interrupted = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert interrupted.exit_code == 0, interrupted.output
    resumable = load_report_cut(root)
    assert resumable is not None
    unexpected = resumable[1].parent / "unexpected.json"
    unexpected.write_text("{}\n")

    with pytest.raises(CmocError, match="未定義 artifact"):
        load_report_cut(root)


def test_publication_ready_cut_resumes_without_reverification(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """成果物保存後の pointer failure は final manifest hash から切替だけを再開する。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _observation_id, raw_path, candidate_id = _store_agent_issue(root, session_id)
    _install_codex_outputs(
        monkeypatch, _verification_output(candidate_id, "unresolved")
    )
    original_publish = feedback_report_module.publish_current_pointer

    def fail_pointer(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("pointer publication failed")

    monkeypatch.setattr(
        feedback_report_module,
        "publish_current_pointer",
        fail_pointer,
    )
    failed = runner.invoke(app, ["feedback", "report"])

    assert failed.exit_code == 1
    resumable = load_report_cut(root)
    assert resumable is not None
    assert resumable[0]["processing"]["status"] == "publication_ready"
    assert raw_path.exists()
    assert not (feedback_root(root) / "active" / "current.json").exists()

    monkeypatch.setattr(
        feedback_report_module,
        "publish_current_pointer",
        original_publish,
    )
    monkeypatch.setattr(
        feedback_report_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: pytest.fail("publication_ready must not reverify"),
    )
    resumed = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert resumed.exit_code == 0, resumed.output
    assert load_report_cut(root) is None
    assert not raw_path.exists()
    assert load_active_state(root).current is not None


def test_partial_cleanup_keeps_publication_and_excludes_processed_pending(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """pointer 切替後の部分 cleanup は current を維持し、missing target から再開する。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    first_id, _first_path, candidate_id = _store_agent_issue(root, session_id)
    second_id, _second_path, _same_candidate = _store_agent_issue(root, session_id)
    assert first_id != second_id
    _install_codex_outputs(
        monkeypatch, _verification_output(candidate_id, "unresolved")
    )
    original_unlink = feedback_state_module._durable_unlink
    unlink_count = 0

    def fail_second_unlink(path: Path) -> None:
        nonlocal unlink_count
        unlink_count += 1
        if unlink_count == 2:
            raise OSError("cleanup interrupted")
        original_unlink(path)

    monkeypatch.setattr(feedback_state_module, "_durable_unlink", fail_second_unlink)
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert "cleanup は未完了" in result.output
    state = validate_feedback_state(root)
    assert state.current is not None
    assert state.cleanup_manifest is not None
    assert len(iter_observation_paths(root)) == 1
    assert feedback_completion_counts(root) == (0, [])

    monkeypatch.setattr(feedback_state_module, "_durable_unlink", original_unlink)
    assert cleanup_published_report(root) is True
    assert load_report_cut(root) is None
    assert iter_observation_paths(root) == []
    assert load_active_state(root).current is not None


def test_cleanup_keyboard_interrupt_is_reported_as_user_interruption(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """pointer 切替後の cleanup 中断を正常完了と区別して state に残す。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _observation_id, _raw_path, candidate_id = _store_agent_issue(root, session_id)
    _install_codex_outputs(
        monkeypatch, _verification_output(candidate_id, "unresolved")
    )
    original_unlink = feedback_state_module._durable_unlink

    def interrupt_cleanup(_path: Path) -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr(feedback_state_module, "_durable_unlink", interrupt_cleanup)
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert "ユーザー中断" in result.output
    state = validate_feedback_state(root)
    assert state.current is not None
    assert state.cleanup_manifest is not None

    monkeypatch.setattr(feedback_state_module, "_durable_unlink", original_unlink)
    assert cleanup_published_report(root) is True


def test_current_pointer_rejects_publication_cross_reference_mismatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """cleanup manifest の publication artifact が pointer とずれたら停止する。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _observation_id, _raw_path, candidate_id = _store_agent_issue(root, session_id)
    _install_codex_outputs(
        monkeypatch, _verification_output(candidate_id, "unresolved")
    )
    original_unlink = feedback_state_module._durable_unlink

    def fail_cleanup(_path: Path) -> None:
        raise OSError("cleanup interrupted")

    monkeypatch.setattr(
        feedback_state_module,
        "_durable_unlink",
        fail_cleanup,
    )
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    monkeypatch.setattr(feedback_state_module, "_durable_unlink", original_unlink)

    state = load_active_state(root)
    assert state.cleanup_manifest_path is not None
    manifest_path = state.cleanup_manifest_path
    manifest = read_json_object(manifest_path)
    publication = manifest["publication"]
    assert isinstance(publication, dict)
    publication["result"] = "ok"
    manifest_path.write_bytes(canonical_json_bytes(manifest))

    pointer_path = feedback_root(root) / "active" / "current.json"
    pointer = read_json_object(pointer_path)
    pointer["report_cut_manifest_sha256"] = hashlib.sha256(
        manifest_path.read_bytes()
    ).hexdigest()
    pointer_path.write_bytes(canonical_json_bytes(pointer))

    with pytest.raises(CmocError, match="publication artifact"):
        load_active_state(root)


def test_active_generation_hash_mismatch_is_corruption(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """current pointer が列挙する active record の改変を無視して続行しない。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _observation_id, _raw_path, candidate_id = _store_agent_issue(root, session_id)
    _install_codex_outputs(
        monkeypatch, _verification_output(candidate_id, "unresolved")
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
        monkeypatch, _verification_output(candidate_id, "unresolved")
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
