"""feedback observation の収集、保存、増分 report を検証する。

この file は 16,000 文字を超えるが、reporter input から raw observation、tracked
issue state、増分 report までを同じ fixture ID と Git session で追跡する受け入れ境界
である。分割すると同じ observation の lifecycle assertion が重複するため、一続きの
feedback subsystem test として保つ。

根拠:
- {{work-root}}/oracle/doc/app_spec/feedback_observation.md
- {{work-root}}/oracle/doc/app_spec/feedback_state.md
- {{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md
"""

import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from _cli_support import run_doctor, runner
from _git_support import current_branch, make_repo, run_git

import commons.runtime_codex_preflight as codex_preflight_module
import commons.runtime_feedback_reporter as reporter_module
import sub_commands.feedback.report as feedback_report_module
from acp.builder.feedback.normalize_issue import (
    build_feedback_normalize_issue_parameter,
)
from basic.acp import FileAccessMode
from commons.runtime_feedback import FeedbackInvocation
from commons.runtime_feedback_state import (
    IssueView,
    identity_record,
    issue_id,
    load_issue_views,
    occurrence_record,
    record_path,
    revision_record,
    validate_observation_envelope,
    validate_tracked_feedback_state,
    write_tracked_record,
)
from commons.runtime_feedback_store import (
    FeedbackRejected,
    ingestion_receipt_path,
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


def test_reporter_exposes_only_canonical_submission_tool(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """stdio MCP discovery と転送 envelope が agent-facing 契約に一致する。"""
    listed = reporter_module._response(
        {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
    )
    assert listed is not None
    tools = listed["result"]["tools"]
    assert tools == [
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
        """reporter から collector への一往復だけを記録する socket double。"""

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
    assert "capability" not in request["payload"]


def test_feedback_normalizer_builder_has_call_kind_and_readonly_scope(
    tmp_path: Path,
) -> None:
    """normalization 専用 agent call の識別子、schema、参照範囲を固定する。"""
    root = make_repo(tmp_path)
    parameter = build_feedback_normalize_issue_parameter(
        json.dumps({"observation_id": "fbo_input"}),
        "[]",
        [root / "README.md"],
        root,
    )

    assert parameter.agent_call_kind == "build_feedback_normalize_issue_parameter"
    assert parameter.file_access_mode is FileAccessMode.READONLY
    assert parameter.structured_output_schema_path is not None
    assert parameter.structured_output_schema_path.name == "normalize_issue.json"
    assert parameter.prompt.count("cmoc_feedback.submit_observation") == 1


def test_collector_validates_context_rate_and_durable_observation(
    tmp_path: Path,
) -> None:
    """call capability ごとの受理、rate limit、失効を保存結果から確認する。"""
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
    assert envelope["context"]["codex_call_id"] == "cdc_one"
    assert envelope["context"]["codex_session_id"] == "session_one"
    assert envelope["context"]["log_paths"] == [
        str(logger.path.resolve()),
        str((root / ".cmoc/gu/ar/log/codex/call.json").resolve()),
    ]
    assert envelope["evidence_fingerprints"][0]["state"] == "hashed"
    with pytest.raises(FeedbackRejected) as rate_error:
        invocation._submit_request(request)
    assert rate_error.value.code == "rate_limited"
    assert rate_error.value.retryable is True

    invocation.close_call(call)
    with pytest.raises(FeedbackRejected) as context_error:
        invocation._submit_request(request)
    assert context_error.value.code == "context_invalid"


def test_agent_store_rejects_outside_paths_and_secret_only_evidence(
    tmp_path: Path,
) -> None:
    """path boundary と高確度 secret の拒否を本命処理から独立して行う。"""
    root = make_repo(tmp_path)
    empty_evidence = _payload()
    empty_evidence["evidence"] = []
    with pytest.raises(FeedbackRejected) as empty:
        store_agent_observation(root, _context(root), empty_evidence)
    assert empty.value.code == "evidence_empty"

    with pytest.raises(FeedbackRejected) as outside:
        store_agent_observation(
            root,
            _context(root),
            _payload(path=str(tmp_path / "outside.txt")),
        )
    assert outside.value.code == "path_outside_repo"

    secret_payload = _payload(
        text="Authorization: Bearer abcdefghijklmnopqrstuvwxyz",
        kind="error",
        path=None,
    )
    with pytest.raises(FeedbackRejected) as secret:
        store_agent_observation(root, _context(root), secret_payload)
    assert secret.value.code == "suspected_secret"

    redacted_payload = _payload(
        text="request failed before Authorization: Bearer abcdefghijklmnopqrstuvwxyz",
        kind="error",
        path=None,
    )
    result, path = store_agent_observation(root, _context(root), redacted_payload)
    assert result["redaction_count"] == 1
    assert "[REDACTED:authorization]" in path.read_text()
    assert "abcdefghijklmnopqrstuvwxyz" not in path.read_text()


def test_machine_detector_observation_id_is_idempotent(tmp_path: Path) -> None:
    """同じ stable event の再検出が同じ raw observation 一件へ収束する。"""
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
    assert observation["source"] == "machine_rule"
    assert observation["source_event"]["event_id"] == event["event_id"]


def test_machine_detector_ignores_incomplete_structured_output_event(
    tmp_path: Path,
) -> None:
    """rule 固有 field が欠けた event を raw observation として保存しない。"""
    root = make_repo(tmp_path)
    logger = SubcommandLogger(root, "feedback test")
    invocation = FeedbackInvocation(root, root, "feedback test", logger)
    event = {
        "event_schema_version": 1,
        "event_id": "evt_incomplete_structured_output",
        "event_type": "codex.structured_output_validation_exhausted",
        "occurred_at": rfc3339_now(),
        "subcommand_invocation_id": logger.invocation_id,
        "agent_call_id": "agc_incomplete_structured_output",
        "agent_call_kind": "build_feedback_test_parameter",
        "codex_call_id": "cdc_incomplete_structured_output",
    }

    invocation.detect_event(event, logger.path)

    assert iter_observation_paths(root) == []


def test_agent_candidate_requires_all_fingerprints_for_exact_match(
    tmp_path: Path,
) -> None:
    """一部の evidence だけ一致する候補は normalizer へ残す。"""
    view = IssueView(
        issue_id="fbi_candidate",
        identity={"origin": "agent_report"},
        revision={"category": "tooling"},
        occurrences=[{"observation_id": "fbo_old"}],
        assessment=None,
        disposition=None,
    )
    first_path = str((tmp_path / "README.md").resolve())
    second_path = str((tmp_path / "pyproject.toml").resolve())
    previous = {
        "fbo_old": {
            "payload": {"category": "tooling"},
            "evidence_fingerprints": [
                {"normalized_path": first_path, "sha256": "a" * 64},
                {"normalized_path": second_path, "sha256": "b" * 64},
            ],
        }
    }
    current = {
        "payload": {"category": "tooling"},
        "evidence_fingerprints": [{"normalized_path": first_path, "sha256": "a" * 64}],
    }

    exact, candidates = feedback_report_module._candidate_issues(
        current,
        {view.issue_id: view},
        previous,
    )

    assert exact is None
    assert candidates == [view]


def test_normalizer_presence_keeps_changed_fingerprint_stale(
    tmp_path: Path,
) -> None:
    """normalizer の presence を使っても変更済み fingerprint は再検証扱いにする。"""
    evidence_path = tmp_path / "evidence.txt"
    evidence_path.write_text("current\n")
    observation = {
        "context": {"repo_root": str(tmp_path.resolve())},
        "evidence_fingerprints": [
            {
                "normalized_path": str(evidence_path.resolve()),
                "state": "hashed",
                "sha256": "a" * 64,
            }
        ],
    }

    assessment = feedback_report_module._assessment_for_observation(
        "fbi_candidate",
        rfc3339_now(),
        observation,
        {"presence": "likely_absent", "reason": "current content differs"},
    )

    assert assessment["presence"] == "likely_absent"
    assert assessment["freshness"] == "needs_revalidation"
    assert assessment["reason_code"] == "normalizer_assessment"


def test_feedback_report_is_incremental_and_refreshes_fingerprint(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """初回、再実行、evidence 変更後の report 差分と assessment を検証する。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    _result, raw_path = store_agent_observation(
        root,
        _context(root, session_id=session_id),
        _payload(),
    )
    # raw envelope の schema は JSON の空白表現を固定しない。
    raw_path.write_text(
        json.dumps(read_json_object(raw_path), ensure_ascii=False, indent=2) + "\n"
    )

    first = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert first.exit_code == 0, first.output
    assert raw_path.is_file()
    assert ingestion_receipt_path(root, raw_path.stem).is_file()
    reports = sorted((root / ".cmoc/gu/ar/report/feedback").glob("*.md"))
    assert len(reports) == 1
    assert 'result: "attention"' in reports[-1].read_text()
    assert "代表的な evidence" in reports[-1].read_text()
    assert run_git(root, "status", "--short").stdout.strip() == ""

    second = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert second.exit_code == 0, second.output
    reports = sorted((root / ".cmoc/gu/ar/report/feedback").glob("*.md"))
    assert len(reports) == 2
    assert 'result: "ok"' in reports[-1].read_text()
    assert "既定表示の対象 issue はありません。" in reports[-1].read_text()

    (root / "README.md").write_text("# changed evidence\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "change evidence")
    third = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert third.exit_code == 0, third.output
    reports = sorted((root / ".cmoc/gu/ar/report/feedback").glob("*.md"))
    assert len(reports) == 3
    report_text = reports[-1].read_text()
    assert 'result: "attention"' in report_text
    assert "needs_revalidation_issue_count: 1" in report_text
    assert "unknown / needs_revalidation" in report_text


def test_feedback_report_suppresses_machine_issue_until_threshold(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """machine issue を保存しつつ異なる recurrence scope 二件まで既定表示しない。"""
    root = make_repo(tmp_path)
    _active_session(root, monkeypatch)
    observed_at = rfc3339_now()
    generated_reports: list[Path] = []
    for index in range(2):
        event = {
            "event_schema_version": 1,
            "event_id": f"evt_{index}",
            "event_type": "feedback.reporter_unavailable",
            "occurred_at": observed_at,
            "subcommand_invocation_id": f"scope_{index}",
            "component": "reporter",
            "failure_code": "missing",
        }
        context = _context(root, session_id=f"session_{index}")
        context["subcommand_invocation_id"] = f"scope_{index}"
        store_machine_observation(
            root,
            context,
            rule_id="feedback.reporter_unavailable.v1",
            category="tooling",
            subject_type="reporter_component",
            normalized_subject_id="reporter:missing",
            summary="feedback reporter または collector が反復して利用できない。",
            impact="agent observation が欠落する。",
            human_action="reporter を確認する。",
            event=event,
            log_path=root / ".cmoc/gu/ar/log/test.jsonl",
        )
        report_directory = root / ".cmoc/gu/ar/report/feedback"
        before = set(report_directory.glob("*.md"))
        result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
        assert result.exit_code == 0, result.output
        [generated] = set(report_directory.glob("*.md")) - before
        generated_reports.append(generated)
        if index == 0:
            all_result = runner.invoke(
                app,
                ["feedback", "report", "--all"],
                catch_exceptions=False,
            )
            assert all_result.exit_code == 0, all_result.output
            all_report = max(
                set(report_directory.glob("*.md")) - {*before, generated},
                key=lambda path: path.stat().st_mtime_ns,
            )
            all_text = all_report.read_text()
            assert 'result: "ok"' in all_text
            assert "suppressed_machine_issue_count: 1" in all_text
            assert "feedback reporter または collector" in all_text

    assert 'result: "ok"' in generated_reports[0].read_text()
    assert "suppressed_machine_issue_count: 1" in generated_reports[0].read_text()
    assert 'result: "attention"' in generated_reports[1].read_text()
    assert "recurrent_open_issue_count: 1" in generated_reports[1].read_text()


def test_feedback_report_records_invalid_raw_observation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """schema 不正 raw file を変更せず invalid ingestion receipt へ確定する。"""
    root = make_repo(tmp_path)
    _active_session(root, monkeypatch)
    observation_id = "fbo_00000000000000000000000000000000"
    raw_path = observation_path(root, observation_id, "2026-08-07T00:00:00Z")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text("not-json\n")

    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert raw_path.read_text() == "not-json\n"
    receipt = read_json_object(ingestion_receipt_path(root, observation_id))
    assert receipt["status"] == "invalid"
    assert receipt["issue_ids"] == []
    [report] = (root / ".cmoc/gu/ar/report/feedback").glob("*.md")
    assert "invalid_observation_count: 1" in report.read_text()


def test_effective_revision_uses_source_observation_time(tmp_path: Path) -> None:
    """revision 生成時刻ではなく source の最大 observed_at で effective を選ぶ。"""
    root = make_repo(tmp_path)
    old_observation_id = "fbo_00000000-0000-7000-8000-000000000001"
    new_observation_id = "fbo_00000000-0000-7000-8000-000000000002"
    canonical_key = f"agent\0{old_observation_id}"
    current_issue_id = issue_id(canonical_key)
    old_observation = {
        "observation_id": old_observation_id,
        "observed_at": "2026-01-01T00:00:00Z",
        "context": {
            "cmoc_session_id": "session_old",
            "subcommand_invocation_id": "scope_old",
            "log_paths": [],
        },
    }
    new_observation = {
        "observation_id": new_observation_id,
        "observed_at": "2026-02-01T00:00:00Z",
        "context": {
            "cmoc_session_id": "session_new",
            "subcommand_invocation_id": "scope_new",
            "log_paths": [],
        },
    }
    identity = identity_record(
        current_issue_id,
        canonical_key,
        "agent_report",
        old_observation_id,
        "2026-01-01T00:00:00Z",
    )
    old_occurrence = occurrence_record(current_issue_id, old_observation, "a" * 64)
    new_occurrence = occurrence_record(current_issue_id, new_observation, "b" * 64)
    old_revision = revision_record(
        current_issue_id,
        "2026-12-01T00:00:00Z",
        [old_observation_id],
        "tooling",
        "old summary",
        "old action",
        "old impact",
        {"certainty": "unknown", "description": "old"},
        [],
    )
    new_revision = revision_record(
        current_issue_id,
        "2026-03-01T00:00:00Z",
        [new_observation_id],
        "tooling",
        "new summary",
        "new action",
        "new impact",
        {"certainty": "supported", "description": "new"},
        [],
    )
    records = [
        ("identity", identity),
        ("occurrence", old_occurrence),
        ("occurrence", new_occurrence),
        ("revision", old_revision),
        ("revision", new_revision),
    ]
    for kind, record in records:
        write_tracked_record(record_path(root, record, kind), record)

    validate_tracked_feedback_state(root)
    view = load_issue_views(root)[current_issue_id]

    assert view.revision["summary"] == "new summary"


def test_feedback_report_records_user_interruption_as_normal_completion(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """実行中 unit の Ctrl+C を deferred observation 付き report へ確定する。"""
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    store_agent_observation(
        root,
        _context(root, session_id=session_id),
        _payload(),
    )

    def interrupt(*_args: object, **_kwargs: object) -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr(
        feedback_report_module,
        "_integrate_agent_observation",
        interrupt,
    )

    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert "ユーザー中断要求を受け付けました" in result.output
    [report] = (root / ".cmoc/gu/ar/report/feedback").glob("*.md")
    report_text = report.read_text()
    assert 'result: "interrupted"' in report_text
    assert "deferred_observation_count: 1" in report_text
