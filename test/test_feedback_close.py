"""案件の publication、手動 close、確定点前後の recovery を検証する。"""

import json

import pytest
from _cli_support import runner, seed_search_config, terminal_primary_report
from _git_support import RUN_BRANCH, SESSION_ID, current_branch, make_repo, run_git
from test_feedback import (
    _active_session,
    _context,
    _fake_result,
    _install_codex_outputs,
    _payload,
    _remediation_output,
    _store_agent_issue,
)

import commons.runtime_cli as runtime_cli
import commons.runtime_feedback_close_state as close_state
import commons.runtime_feedback_state as feedback_state
import sub_commands.feedback.close as close_module
import sub_commands.feedback.decision as decision
import sub_commands.feedback.report as report_module
from commons.runtime_errors import CmocError
from commons.runtime_feedback_history import history_artifact
from commons.runtime_feedback_intake import (
    capture_high_watermark,
    forget_observation_receipts,
)
from commons.runtime_feedback_store import (
    canonical_json_bytes,
    feedback_completion_counts,
    observation_publication_lock,
    read_json_object,
    rfc3339_now,
    sha256_bytes,
    store_agent_observation,
    store_machine_observation,
    write_immutable_bytes,
)
from commons.runtime_ids import is_common_id
from commons.runtime_logging import SubcommandLogger
from commons.runtime_state import (
    RunPart,
    SessionPart,
    SessionState,
    state_path,
    write_state,
)
from main import app

pytestmark = pytest.mark.usefixtures("feedback_without_transport")


@pytest.fixture
def reported_case(ready_content_session, monkeypatch):
    # session fork の結合は test_feedback.py の後続 wave test に残し、
    # ここでは report から close の publication・cleanup を通す。
    root, _, _ = ready_content_session
    session_id = SESSION_ID
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


@pytest.fixture
def open_case(tmp_path, monkeypatch):
    # close 固有の検査には session を作らず、report を実行するケースだけで準備する。
    # report から close への結合と入力消費は reported_case の検査に残す。
    # doctor 内部の修復・索引同期は専用 test と reported_case で検証する。
    # close が前処理の失敗を越えて更新しないことは、この file の失敗 test に残す。
    monkeypatch.setattr(close_module, "run_doctor_preprocess", lambda _root: None)
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    seed_search_config(root)
    observation_id, raw, identity = _store_agent_issue(root, None)
    observation = read_json_object(raw)
    observed_at = observation["observed_at"]
    watermark, inputs = capture_high_watermark(root, 0)
    raw_reference = {key: inputs[0][key] for key in ("path", "sha256")}
    candidate = report_module._new_candidate(
        observation, feedback_state.agent_canonical_key(observation_id)
    )
    report_module._merge_observation(root, candidate, observation)
    cut_id = feedback_state.new_report_cut_id()
    generation_id = feedback_state.new_generation_id(root)
    execution_id = "exec_zzzzzz_2026-10-08_00-00"
    source = {"kind": "report", "id": cut_id, "execution_id": execution_id}
    verdict = _remediation_output(identity, "inconclusive")["result"]
    verdict["decision_basis"] = decision.compact_basis(
        decision.decision_basis(
            decision.decision_state(decision.worktree_inputs(root), candidate),
            verdict,
            None,
        )
    )
    issue = report_module._active_issue_record(
        {
            "report_cut_id": cut_id,
            "run": {"targets": {"case_ids": {identity: "fbc_000000_2026-10-08_00-00"}}},
        },
        candidate,
        verdict,
        {},
        observed_at,
    )
    report = root / f".cmoc/gu/report/feedback/incomplete/{execution_id}.md"
    history_path, history_bytes, history_reference = history_artifact(
        root,
        {
            "schema_version": 1,
            "generation_id": generation_id,
            "source": source,
            "created_at": observed_at,
            "report": report.relative_to(root).as_posix(),
            "log": f".cmoc/gu/log/sub_command/{execution_id}.jsonl",
            "events": [
                {
                    "kind": "created",
                    "case_id": issue["case_id"],
                    "issue_id": identity,
                    "before": None,
                    "after": issue,
                    "agent_result": verdict,
                    "human_reason": None,
                }
            ],
            "observations": [
                {**inputs[0], "issue_ids": [identity], "aggregate_keys": []}
            ],
        },
    )
    generation, artifacts, reference = feedback_state.generation_artifacts(
        root,
        generation_id=generation_id,
        report_cut_id=cut_id,
        created_at=observed_at,
        session_commit=run_git(root, "rev-parse", "HEAD").stdout.strip(),
        issues={identity: issue},
        machine_aggregates={},
        source=source,
        base_current=None,
        input_boundary=watermark,
        history=[history_reference],
    )
    write_immutable_bytes(history_path, history_bytes)
    feedback_state.publish_generation_artifacts(root, generation, artifacts)
    write_immutable_bytes(report, b"# Prepared inconclusive case\n")
    # 完了済み state を配置し、staging 用の report cut は作らない。
    write_immutable_bytes(
        feedback_state.current_pointer_path(root),
        canonical_json_bytes(
            {
                "schema_version": 1,
                "generation_id": generation_id,
                "generation_manifest_path": reference["path"],
                "generation_manifest_sha256": reference["sha256"],
                "report_cut_id": cut_id,
                "report_cut_manifest_sha256": sha256_bytes(b"completed report cut"),
                "report_path": report.relative_to(root).as_posix(),
                "report_sha256": sha256_bytes(report.read_bytes()),
                "published_at": observed_at,
                "result": "incomplete",
            }
        ),
    )
    with observation_publication_lock(root):
        raw.unlink()
        forget_observation_receipts(root, [raw_reference])
    assert feedback_state.validate_feedback_state(root).issues == {identity: issue}
    monkeypatch.setattr(
        report_module,
        "run_codex_exec",
        lambda *_a, **_k: pytest.fail("close must not call an agent"),
    )
    return root, issue


def _close(case, reason="外部で解決を確認した"):
    return runner.invoke(
        app,
        ["feedback", "close", case["case_id"], "--reason", reason],
        catch_exceptions=False,
    )


def test_close_publishes_immediately_keeps_pending_and_replay_reason(
    reported_case, monkeypatch
):
    root, session_id, issue = reported_case
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
    assert "latest_state_summary: `ok`" in result.output
    assert "remaining_cases: `0`" in result.output
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
    assert "latest_state_summary: `ok`" in repeated.output
    assert "remaining_cases: `0`" in repeated.output
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
    root, issue = open_case
    # report の拒否は current 切替前後で確認し、他の保存障害では同じ検査を重ねない。
    checks_report_refusal = fault in {"pointer_before", "partial_cleanup"}
    session_id = _active_session(root, monkeypatch) if checks_report_refusal else None
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
    if checks_report_refusal:
        blocked_report = runner.invoke(
            app, ["feedback", "report"], catch_exceptions=False
        )
        assert blocked_report.exit_code == 1, blocked_report.output
        assert "未完了の feedback close" in blocked_report.output
    assert close_state.load_close_work(root) == fixed
    monkeypatch.setattr(close_state, name, original)
    if published:
        (root / "README.md").write_text("state changed after publication\n")
    resumed = _close(issue)
    assert resumed.exit_code == 0, resumed.output
    assert "latest_state_summary: `ok`" in resumed.output
    assert "remaining_cases: `0`" in resumed.output
    assert terminal_primary_report(resumed) == target
    if saved is not None:
        assert target.read_bytes() == saved
    assert close_state.load_close_work(root) is None
    final = feedback_state.validate_feedback_state(root)
    assert len(final.history) == len(old.history) + 1
    assert issue["issue_id"] not in final.issues
    assert late.exists()


def test_close_input_failures_save_invocation_reports(open_case, monkeypatch):
    root, _ = open_case
    # CLI 解析エラーは共通 wrapper の doctor を通る。修復・索引同期の
    # 検査は reported_case と test_doctor_cli.py に残す。
    monkeypatch.setattr(runtime_cli, "run_doctor_preprocess", lambda _root: None)
    before = feedback_state.load_active_state(root)
    # 各拒否後に次の入力の前提を確認する。
    for arguments in [
        [],
        ["not-a-case"],
        ["fbc_zzzzzz_2026-10-08_00-00"],
        ["fbc_zzzzzz_2026-10-08_00-00", "--reason", ""],
        ["fbc_zzzzzz_2026-10-08_00-00", "--reason", "  "],
        ["fbc_zzzzzz_2026-10-08_00-00", "--reason", "external fix"],
        ["fbc_zzzzzz_2026-10-08_00-00", "--reason"],
        ["fbc_zzzzzz_2026-10-08_00-00", "--report", "output.md"],
        ["fbc_zzzzzz_2026-10-08_00-00", "extra", "--reason", "fixed"],
    ]:
        result = runner.invoke(
            app, ["feedback", "close", *arguments], catch_exceptions=False
        )
        assert result.exit_code == 1, (arguments, result.output)
        assert "feedback/invocation" in str(terminal_primary_report(result)), arguments
        assert feedback_state.load_active_state(root) == before, arguments
        assert close_state.load_close_work(root) is None, arguments
        assert feedback_state.load_report_cut(root) is None, arguments


def test_close_doctor_failure_preserves_state_and_saves_invocation_report(
    open_case, monkeypatch
):
    root, issue = open_case
    before = feedback_state.load_active_state(root)

    def failed_preprocess(worktree):
        assert worktree == root
        raise CmocError(
            "injected doctor failure",
            ["cmoc doctor を再実行してください。"],
            str(worktree),
        )

    monkeypatch.setattr(close_module, "run_doctor_preprocess", failed_preprocess)
    result = _close(issue)
    assert result.exit_code == 1, result.output
    assert "injected doctor failure" in result.output
    assert "feedback/invocation" in str(terminal_primary_report(result))
    assert feedback_state.load_active_state(root) == before
    assert close_state.load_close_work(root) is None


def test_close_preserves_other_cases_and_subthreshold_aggregates(
    ready_content_session, monkeypatch
):
    # close の保持対象は同じ report で揃え、準備用の report/run を重ねない。
    root, _, _ = ready_content_session
    session_id = SESSION_ID
    _, issue_raw, identity = _store_agent_issue(root, session_id)
    payload = _payload(kind="other", path=None, text="独立した構成の問題")
    payload["category"] = "configuration"
    payload["summary"] = "人間による設定確認が必要"
    accepted, other_raw = store_agent_observation(
        root, _context(root, session_id=session_id), payload
    )
    other_id = feedback_state.issue_id(f"agent\0{accepted['observation_id']}")
    log = root / ".cmoc/gu/log/sub_command/exec_000000_2026-10-08_00-00.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)
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
    assert set(before.issues) == {identity, other_id}
    assert before.current["result"] == "incomplete"
    issue = before.issues[identity]
    assert issue["verification"]["status"] == "inconclusive"
    assert len(before.machine_aggregates) == 1
    assert not issue_raw.exists()
    assert not other_raw.exists()
    assert not raw.exists()
    monkeypatch.setattr(
        report_module,
        "run_codex_exec",
        lambda *_a, **_k: pytest.fail("close must not call an agent"),
    )
    result = _close(issue)
    assert result.exit_code == 0, result.output
    assert "latest_state_summary: `attention`" in result.output
    assert "remaining_cases: `1`" in result.output
    after = feedback_state.validate_feedback_state(root)
    assert after.current["result"] == "attention"
    assert after.issues == {other_id: before.issues[other_id]}
    assert after.machine_aggregates == before.machine_aggregates
    text = terminal_primary_report(result).read_text()
    assert before.issues[other_id]["case_id"] in text
    assert 'latest_state_summary: "attention"' in text


def test_close_rejects_writer_lock_and_pending_feedback_run(open_case):
    """writer 排他と各未終了 run state を、session 作成や report 実行なしで検査する。"""
    root, issue = open_case
    before = feedback_state.load_active_state(root)
    with feedback_state.feedback_writer_lock(root):
        result = _close(issue)
    assert result.exit_code == 1, result.output
    assert "feedback writer" in result.stderr
    assert close_state.load_close_work(root) is None
    assert feedback_state.load_active_state(root) == before

    # close が読む保存済み state だけを用意する。実 report cut による拒否は
    # test_feedback.py の report cut 保存直後の中断 test と一緒に検査する。
    path = state_path(root, SESSION_ID)
    commit = before.generation_manifest["session_commit"]
    state = SessionState(
        session=SessionPart(
            session_home_branch=current_branch(root), session_fork_commit=commit
        ),
        run=RunPart(
            state="running",
            kind="feedback_report",
            branch=RUN_BRANCH,
            fork_commit=commit,
        ),
    )
    for run_state in ("running", "joinable", "error"):
        state.run.state = run_state
        write_state(path, state)
        saved = path.read_bytes()

        result = _close(issue)

        assert result.exit_code == 1, (run_state, result.output)
        assert "未終了の feedback run" in result.stderr, run_state
        assert "feedback/invocation" in str(terminal_primary_report(result)), run_state
        assert close_state.load_close_work(root) is None, run_state
        assert feedback_state.load_active_state(root) == before, run_state
        assert feedback_state.load_report_cut(root) is None, run_state
        assert path.read_bytes() == saved, run_state


def test_close_completion_log_failure_reports_published_state(open_case, monkeypatch):
    root, issue = open_case
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
    root, issue = open_case
    _active_session(root, monkeypatch)
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
    ready_content_session, monkeypatch
):
    root, _, _ = ready_content_session
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
    assert "latest_state_summary: `incomplete`" in repeated.output
    assert "remaining_cases: `1`" in repeated.output
    assert feedback_state.load_active_state(root).issues[identity] == second


def test_confirmed_history_corruption_blocks_close(open_case):
    root, issue = open_case
    state = feedback_state.load_active_state(root)
    path = root / state.generation_manifest["history"][0]["path"]
    history = json.loads(path.read_text())
    history["events"][0]["case_id"] = "fbc_zzzzzz_2026-10-08_00-00"
    path.write_bytes(canonical_json_bytes(history))
    result = _close(issue)
    assert result.exit_code == 1
    assert close_state.load_close_work(root) is None


def test_close_saved_artifact_validates_fixed_and_existing_bytes(tmp_path):
    # 未保存の許容によって、固定 byte 列や現存 artifact の破損を見逃さない。
    directory = tmp_path / "artifacts"
    directory.mkdir()
    target = directory / "report.md"
    content = "saved close report\n"
    artifact = {
        "path": "artifacts/report.md",
        "sha256": sha256_bytes(content.encode()),
        "content": content,
    }
    reference = {key: artifact[key] for key in ("path", "sha256")}

    def validate(value):
        return close_state._validate_saved_bytes(
            tmp_path, value, directory, tmp_path / "operation.json"
        )

    assert validate(artifact) == reference
    target.write_text(content)
    assert validate(artifact) == reference
    with pytest.raises(CmocError, match="bytes/hash"):
        validate({**artifact, "content": "changed fixed input\n"})
    target.write_text("changed artifact\n")
    with pytest.raises(CmocError, match="SHA256"):
        validate(artifact)
