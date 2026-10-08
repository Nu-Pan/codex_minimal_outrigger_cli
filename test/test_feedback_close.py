"""案件の publication、手動 close、確定点前後の recovery を検証する。"""

import json

import pytest
from _cli_support import runner, terminal_primary_report
from _git_support import make_repo, run_git
from test_feedback import (
    _active_session,
    _context,
    _fake_result,
    _install_codex_outputs,
    _payload,
    _remediation_output,
    _store_agent_issue,
)

import commons.runtime_feedback_close_state as close_state
import commons.runtime_feedback_state as feedback_state
import sub_commands.feedback.report as report_module
from commons.runtime_feedback_store import (
    canonical_json_bytes,
    feedback_completion_counts,
    read_json_object,
    rfc3339_now,
    store_agent_observation,
    store_machine_observation,
)
from commons.runtime_ids import is_common_id
from commons.runtime_logging import SubcommandLogger
from main import app


@pytest.fixture
def open_case(tmp_path, monkeypatch):
    root = make_repo(tmp_path)
    session_id = _active_session(root, monkeypatch)
    observation_id, raw, identity = _store_agent_issue(root, session_id)
    _install_codex_outputs(monkeypatch, _remediation_output(identity, "inconclusive"))
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    state = feedback_state.validate_feedback_state(root)
    assert state.current["result"] == "incomplete"
    issue = state.issues[identity]
    assert is_common_id(issue["case_id"], "fbc")
    assert not raw.exists()
    assert feedback_completion_counts(root)[0] == 0
    assert state.history[-1]["observations"][0]["observation_id"] == observation_id
    text = terminal_primary_report(result).read_text()
    assert issue["case_id"] in text
    assert "active_generation_id:" in text
    assert "正常 publication ではありません" not in text
    assert "保存時点では publication・cleanup・終了処理は未完了" in text
    monkeypatch.setattr(
        report_module,
        "run_codex_exec",
        lambda *_a, **_k: pytest.fail("close must not call an agent"),
    )
    return root, session_id, issue


def _close(case, reason="外部で解決を確認した"):
    return runner.invoke(
        app,
        ["feedback", "close", case["case_id"], "--reason", reason],
        catch_exceptions=False,
    )


def test_close_publishes_immediately_keeps_pending_and_replay_reason(
    open_case, monkeypatch
):
    root, session_id, issue = open_case
    _, late = store_agent_observation(
        root,
        _context(root, session_id=session_id),
        _payload(text="close 前の未処理入力"),
    )
    previous = feedback_state.load_active_state(root)
    # Close は active session と clean worktree を要求しない。
    run_git(root, "checkout", "-b", "outside-session")
    (root / "README.md").write_text("external fix, still dirty\n")
    state_before = list((root / ".cmoc/gu/session").glob("*.json"))
    result = _close(issue)
    assert result.exit_code == 0, result.output
    assert "closed" in result.output
    state = feedback_state.validate_feedback_state(root)
    assert state.current["result"] == "ok"
    assert state.issues == {}
    assert (
        state.generation_manifest["input_boundary"]
        == previous.generation_manifest["input_boundary"]
    )
    assert state.history[-1]["observations"] == []
    event = state.history[-1]["events"][0]
    assert event["kind"] == "manual_close"
    assert event["agent_result"] is None
    assert event["before"] == issue
    assert late.exists()
    assert feedback_completion_counts(root)[0] == 1
    report = terminal_primary_report(result)
    report_bytes = report.read_bytes()
    pointer = canonical_json_bytes(state.current)
    history = list(state.history)
    repeated = _close(issue, "別の理由")
    assert repeated.exit_code == 0, repeated.output
    assert "already_closed" in repeated.output
    after = feedback_state.validate_feedback_state(root)
    assert canonical_json_bytes(after.current) == pointer
    assert after.history == history
    assert report.read_bytes() == report_bytes
    assert terminal_primary_report(repeated) != report
    assert state_before == list((root / ".cmoc/gu/session").glob("*.json"))


@pytest.mark.parametrize(
    "fault",
    [
        "history",
        "report",
        "pointer_before",
        "pointer_after",
        "cleanup",
        "partial_cleanup",
    ],
)
def test_close_failure_recovers_fixed_targets_and_preserves_confirmed_state(
    open_case, monkeypatch, fault
):
    root, session_id, issue = open_case
    _, late = store_agent_observation(
        root,
        _context(root, session_id=session_id),
        _payload(text="recovery の対象外の新規入力"),
    )
    old = feedback_state.load_active_state(root)
    published = fault in {"pointer_after", "cleanup", "partial_cleanup"}
    if fault in {"history", "report"}:
        name = "write_immutable_bytes"
        original = getattr(close_state, name)

        def broken(path, content):
            if (fault == "history" and path.parent.name == "history") or (
                fault == "report"
                and path.parent.name == "close"
                and path.suffix == ".md"
            ):
                raise OSError("injected save failure")
            return original(path, content)
    elif fault in {"pointer_before", "pointer_after"}:
        name = "publish_current_pointer"
        original = getattr(close_state, name)

        def broken(*args, **kwargs):
            if fault == "pointer_after":
                original(*args, **kwargs)
            raise OSError("injected pointer failure")
    else:
        name = "_unlink_artifact_reference"
        original = getattr(close_state, name)

        def broken(*args, **kwargs):
            if fault == "partial_cleanup":
                original(*args, **kwargs)
            raise OSError("injected cleanup failure")

    monkeypatch.setattr(close_state, name, broken)
    failed = _close(issue)
    assert failed.exit_code == 1, failed.output
    assert "feedback/invocation" in str(terminal_primary_report(failed))
    state = feedback_state.validate_feedback_state(root)
    assert (issue["issue_id"] not in state.issues) == published
    if not published:
        assert state.current == old.current
    fixed = close_state.load_close_work(root)
    assert fixed is not None
    target = root / fixed["report"]["path"]
    saved = target.read_bytes() if target.exists() else None
    assert late.exists()
    assert feedback_completion_counts(root)[0] == 1
    conflict = _close({"case_id": "fbc_zzzzzz_2026-10-08_00-00"})
    assert conflict.exit_code == 1
    if not published:
        assert _close(issue, "異なる理由").exit_code == 1
    blocked_report = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert blocked_report.exit_code == 1
    assert close_state.load_close_work(root) == fixed
    monkeypatch.setattr(close_state, name, original)
    if published:
        (root / "README.md").write_text("state changed after publication\n")
    resumed = _close(issue)
    assert resumed.exit_code == 0, resumed.output
    assert terminal_primary_report(resumed) == target
    if saved is not None:
        assert target.read_bytes() == saved
    assert close_state.load_close_work(root) is None
    final = feedback_state.validate_feedback_state(root)
    assert len(final.history) == len(old.history) + 1
    assert issue["issue_id"] not in final.issues
    assert late.exists()


@pytest.mark.parametrize(
    "arguments",
    [
        [],
        ["not-a-case"],
        ["fbc_zzzzzz_2026-10-08_00-00"],
        ["fbc_zzzzzz_2026-10-08_00-00", "--reason", ""],
        ["fbc_zzzzzz_2026-10-08_00-00", "--reason", "  "],
        ["fbc_zzzzzz_2026-10-08_00-00", "--reason", "external fix"],
        ["fbc_zzzzzz_2026-10-08_00-00", "--reason"],
        ["fbc_zzzzzz_2026-10-08_00-00", "--report", "output.md"],
        ["fbc_zzzzzz_2026-10-08_00-00", "extra", "--reason", "fixed"],
    ],
)
def test_close_input_failures_save_invocation_reports(open_case, arguments):
    root, _, _ = open_case
    before = feedback_state.load_active_state(root)
    result = runner.invoke(
        app, ["feedback", "close", *arguments], catch_exceptions=False
    )
    assert result.exit_code == 1, result.output
    assert "feedback/invocation" in str(terminal_primary_report(result))
    assert feedback_state.load_active_state(root).current == before.current


def test_close_preserves_other_cases_and_subthreshold_aggregates(
    open_case, monkeypatch
):
    root, session_id, issue = open_case
    payload = _payload(kind="other", path=None, text="独立した構成の問題")
    payload["category"] = "configuration"
    payload["summary"] = "人間による設定確認が必要"
    accepted, _ = store_agent_observation(
        root, _context(root, session_id=session_id), payload
    )
    other_id = feedback_state.issue_id(f"agent\0{accepted['observation_id']}")
    log = root / ".cmoc/gu/log/sub_command/exec_000000_2026-10-08_00-00.jsonl"
    log.write_text("{}\n")
    context = _context(root, session_id=session_id)
    _, raw = store_machine_observation(
        root,
        context,
        rule_id="feedback.reporter_unavailable.v1",
        category="tooling",
        subject_type="reporter_component",
        normalized_subject_id="reporter:missing",
        summary="初回の reporter 失敗",
        impact="観測が欠落する",
        human_action="reporter を確認する",
        event={
            "event_schema_version": 1,
            "event_id": "evt_subthreshold",
            "event_type": "feedback.reporter_unavailable",
            "occurred_at": rfc3339_now(),
            "subcommand_invocation_id": context["subcommand_invocation_id"],
            "component": "reporter",
            "failure_code": "missing",
        },
        log_path=log,
    )

    def fake_call(*_args, **kwargs):
        identity = (
            kwargs["purpose"]
            .removeprefix("feedback issue remediation (")
            .removesuffix(")")
        )
        status = "human_required" if identity == other_id else "inconclusive"
        return _fake_result(root, _remediation_output(identity, status))

    monkeypatch.setattr(report_module, "run_codex_exec", fake_call)
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    before = feedback_state.validate_feedback_state(root)
    assert set(before.issues) == {issue["issue_id"], other_id}
    assert len(before.machine_aggregates) == 1
    assert not raw.exists()
    monkeypatch.setattr(
        report_module,
        "run_codex_exec",
        lambda *_a, **_k: pytest.fail("close must not call an agent"),
    )
    result = _close(issue)
    assert result.exit_code == 0, result.output
    after = feedback_state.validate_feedback_state(root)
    assert after.current["result"] == "attention"
    assert after.issues == {other_id: before.issues[other_id]}
    assert after.machine_aggregates == before.machine_aggregates
    text = terminal_primary_report(result).read_text()
    assert before.issues[other_id]["case_id"] in text
    assert 'latest_state_summary: "attention"' in text


def test_close_rejects_writer_lock_and_pending_feedback_run(open_case, monkeypatch):
    root, _, issue = open_case
    before = feedback_state.load_active_state(root)
    with feedback_state.feedback_writer_lock(root):
        result = _close(issue)
    assert result.exit_code == 1, result.output
    assert feedback_state.load_active_state(root).current == before.current

    def failed_call(*_a, **_k):
        raise OSError("injected agent failure")

    monkeypatch.setattr(report_module, "run_codex_exec", failed_call)
    report = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert report.exit_code == 1, report.output
    assert feedback_state.load_report_cut(root) is not None
    result = _close(issue)
    assert result.exit_code == 1, result.output
    assert close_state.load_close_work(root) is None
    assert feedback_state.load_active_state(root).current == before.current


def test_close_completion_log_failure_reports_published_state(open_case, monkeypatch):
    root, _, issue = open_case
    original = SubcommandLogger.event

    def fail_completion(self, event, **fields):
        if event == "feedback_close_completed":
            raise OSError("injected completion log failure")
        return original(self, event, **fields)

    monkeypatch.setattr(SubcommandLogger, "event", fail_completion)
    result = _close(issue)
    assert result.exit_code == 1, result.output
    state = feedback_state.validate_feedback_state(root)
    assert state.issues == {}
    assert close_state.load_close_work(root) is None
    text = terminal_primary_report(result).read_text()
    assert 'publication_status: "completed"' in text
    assert 'cleanup: "completed"' in text
    assert "current_pointer_update_status" not in text
    assert state.current["generation_id"] in text
    monkeypatch.setattr(SubcommandLogger, "event", original)
    repeated = _close(issue)
    assert repeated.exit_code == 0, repeated.output
    assert "already_closed" in repeated.output


def test_incomplete_is_reconfirmed_from_active_without_raw_and_keeps_case(
    open_case, monkeypatch
):
    root, _, issue = open_case
    _install_codex_outputs(
        monkeypatch, _remediation_output(issue["issue_id"], "human_required")
    )
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    state = feedback_state.validate_feedback_state(root)
    assert state.current["result"] == "attention"
    assert state.issues[issue["issue_id"]]["case_id"] == issue["case_id"]
    assert state.history[-1]["events"][0]["before"] == issue
    assert _close(issue).exit_code == 1
    _install_codex_outputs(
        monkeypatch, _remediation_output(issue["issue_id"], "already_resolved")
    )
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    assert feedback_state.load_active_state(root).issues == {}
    assert _close(issue).exit_code == 1


def test_machine_recurrence_gets_new_case_and_old_close_cannot_target_it(
    tmp_path, monkeypatch
):
    root = make_repo(tmp_path)
    _active_session(root, monkeypatch)
    log = root / ".cmoc/gu/log/sub_command/exec_000000_2026-10-08_00-00.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text("{}\n")

    def observe(start):
        canonical = None
        for index in range(start, start + 2):
            context = _context(root, session_id=f"sess_{index:06d}_2026-10-08_00-00")
            event = {
                "event_schema_version": 1,
                "event_id": f"evt_{index}",
                "event_type": "feedback.reporter_unavailable",
                "occurred_at": rfc3339_now(),
                "subcommand_invocation_id": context["subcommand_invocation_id"],
                "component": "reporter",
                "failure_code": "missing",
            }
            _, raw = store_machine_observation(
                root,
                context,
                rule_id="feedback.reporter_unavailable.v1",
                category="tooling",
                subject_type="reporter_component",
                normalized_subject_id="reporter:missing",
                summary="反復する失敗",
                impact="観測が欠落する",
                human_action="reporter を確認する",
                event=event,
                log_path=log,
            )
            canonical = feedback_state.machine_canonical_key(read_json_object(raw))
        return feedback_state.issue_id(canonical)

    identity = observe(0)
    _install_codex_outputs(monkeypatch, _remediation_output(identity, "inconclusive"))
    assert (
        runner.invoke(app, ["feedback", "report"], catch_exceptions=False).exit_code
        == 0
    )
    first = feedback_state.load_active_state(root).issues[identity]
    assert _close(first).exit_code == 0
    assert observe(2) == identity
    _install_codex_outputs(monkeypatch, _remediation_output(identity, "inconclusive"))
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    second = feedback_state.load_active_state(root).issues[identity]
    assert second["case_id"] != first["case_id"]
    assert second["occurrence_count"] == 2
    repeated = _close(first, "新しい理由")
    assert repeated.exit_code == 0, repeated.output
    assert "already_closed" in repeated.output
    assert feedback_state.load_active_state(root).issues[identity] == second


def test_confirmed_history_corruption_blocks_close(open_case):
    root, _, issue = open_case
    state = feedback_state.load_active_state(root)
    path = root / state.generation_manifest["history"][0]["path"]
    history = json.loads(path.read_text())
    history["events"][0]["case_id"] = "fbc_zzzzzz_2026-10-08_00-00"
    path.write_bytes(canonical_json_bytes(history))
    result = _close(issue)
    assert result.exit_code == 1
    assert close_state.load_close_work(root) is None
