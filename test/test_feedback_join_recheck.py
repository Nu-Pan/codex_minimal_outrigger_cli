"""join 後の判定失効、入力保持、次回再確認と終了処理の復旧を検証する。"""

import json

import pytest
from _cli_support import runner, terminal_primary_report
from _git_support import SESSION_ID, current_branch, run_git
from _report_support import report_metadata
from test_feedback import _fake_result, _remediation_output, _store_agent_issue

from cmoc_runtime import load_state_for_branch
from commons import runtime_feedback_state as feedback_state
from commons import runtime_merge_conflict
from commons.runtime_feedback_store import feedback_completion_counts, feedback_root
from main import app
from sub_commands.feedback import decision, recovery, remediation, report


def _invoke():
    result = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    return report_metadata(terminal_primary_report(result).read_text())


def _repair(root, identity, calls):
    def call(parameter, **_kwargs):
        calls.append("repair")
        (parameter.agent_call_cwd / "README.md").write_text("run repair\n")
        output = _remediation_output(identity, "fixed")
        output["result"]["changed_paths"] = ["README.md"]
        return _fake_result(root, output)

    return call


def _change_session_after_seal(root, monkeypatch, *, conflict):
    seal = remediation._seal

    def change(*args):
        seal(*args)
        path = root / ("README.md" if conflict else "dependency.conf")
        path.write_text("session change\n")
        run_git(root, "add", path.name)
        run_git(root, "commit", "-m", "session change after issue verification")

    def resolve(parameter, **_kwargs):
        assert "sealed_feedback_result" not in parameter.prompt
        assert "封印済み結果を維持する統合" not in parameter.prompt
        (parameter.agent_call_cwd / "README.md").write_text("integrated repair\n")
        result = _fake_result(root, {})
        result.output_text = "merge_resolution: resolved\ncontent verified"
        return result

    monkeypatch.setattr(remediation, "_seal", change)
    monkeypatch.setattr(runtime_merge_conflict, "run_codex_exec", resolve)


@pytest.mark.parametrize(
    "conflict", [False, True], ids=["automatic-merge", "agent-merge"]
)
@pytest.mark.parametrize(
    "prior_active", [False, True], ids=["raw-input", "active-input"]
)
def test_changed_join_keeps_inputs_and_rechecks_on_next_report(
    feedback_publication_session, monkeypatch, conflict, prior_active
):
    root = feedback_publication_session
    _, raw, identity = _store_agent_issue(root, SESSION_ID)
    if prior_active:
        monkeypatch.setattr(
            report,
            "run_codex_exec",
            lambda *_args, **_kwargs: _fake_result(
                root, _remediation_output(identity, "human_required")
            ),
        )
        assert _invoke()["result"] == "attention"
    before = feedback_state.load_active_state(root)
    pointer = feedback_state.current_pointer_path(root)
    pointer_bytes = pointer.read_bytes() if pointer.exists() else None
    calls = []
    with monkeypatch.context() as changed:
        changed.setattr(report, "run_codex_exec", _repair(root, identity, calls))
        _change_session_after_seal(root, changed, conflict=conflict)
        metadata = _invoke()

    assert metadata["result"] == "recheck_pending"
    assert metadata["publication_established"] is False
    assert metadata["recheck_pending_issues"] == [identity]
    assert metadata["state_after"] == "ready"
    assert metadata["cleanup"] == "completed"
    assert feedback_state.load_report_cut(root) is None
    after = feedback_state.validate_feedback_state(root)
    assert after.current == before.current
    assert after.issues == before.issues
    assert (pointer.read_bytes() if pointer.exists() else None) == pointer_bytes
    assert raw.exists() is not prior_active
    assert feedback_completion_counts(root)[0] == (0 if prior_active else 1)
    assert (root / "README.md").read_text() == (
        "integrated repair\n" if conflict else "run repair\n"
    )
    [receipt_path] = (feedback_root(root) / "work").glob("*/join_result.json")
    receipt = json.loads(receipt_path.read_text())
    assert receipt["publication"] is False
    assert receipt["recheck_pending_issues"] == [identity]
    manifest = json.loads((root / receipt["manifest"]["path"]).read_text())
    checkpoint = root / manifest["processing"]["remediation_checkpoints"][-1]["path"]
    checkpoint_bytes = checkpoint.read_bytes()
    assert (
        json.loads(checkpoint_bytes)["structured_output"]["result"]["status"] == "fixed"
    )
    assert not (feedback_root(root) / "finalization.json").exists()
    assert not load_state_for_branch(root, current_branch(root))[2].run.branch

    def recheck(parameter, **_kwargs):
        calls.append("recheck")
        assert json.loads(parameter.prompt)["issue_id"] == identity
        return _fake_result(root, _remediation_output(identity, "already_resolved"))

    monkeypatch.setattr(report, "run_codex_exec", recheck)
    assert _invoke()["result"] == "ok"
    assert calls == ["repair", "recheck"]
    assert not raw.exists()
    assert feedback_state.validate_feedback_state(root).issues == {}
    assert checkpoint.read_bytes() == checkpoint_bytes


@pytest.mark.parametrize("fault", ["journal", "receipt", "run_cleanup"])
def test_recheck_finalization_resumes_without_repair_or_republication(
    feedback_publication_session, monkeypatch, fault
):
    root = feedback_publication_session
    _, raw, identity = _store_agent_issue(root, SESSION_ID)
    calls = []
    with monkeypatch.context() as failing:
        failing.setattr(report, "run_codex_exec", _repair(root, identity, calls))
        _change_session_after_seal(root, failing, conflict=True)
        if fault == "run_cleanup":
            cleanup = recovery.cleanup_joined_run

            def fail_cleanup(*args, **kwargs):
                cleanup(*args, **kwargs)
                raise OSError("cleanup result interrupted")

            failing.setattr(recovery, "cleanup_joined_run", fail_cleanup)
        else:
            write = recovery.write_immutable_json

            def fail_write(path, value):
                if path.name == "finalization.json" and fault == "journal":
                    raise OSError("journal write interrupted")
                result = write(path, value)
                if path.name == "join_result.json" and fault == "receipt":
                    raise OSError("receipt return interrupted")
                return result

            failing.setattr(recovery, "write_immutable_json", fail_write)
        failed = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
        assert failed.exit_code == 1, failed.output
    joined_head = run_git(root, "rev-parse", "HEAD").stdout
    monkeypatch.setattr(
        report,
        "run_codex_exec",
        lambda *_args, **_kwargs: pytest.fail("finalization must not call remediation"),
    )
    monkeypatch.setattr(
        decision,
        "worktree_inputs",
        lambda *_args: pytest.fail("recheck was already selected before finalization"),
    )
    recovered = _invoke()
    assert recovered["result"] == "recheck_pending"
    assert recovered["publication_established"] is False
    assert recovered["state_after"] == "ready"
    assert calls == ["repair"]
    assert run_git(root, "rev-parse", "HEAD").stdout == joined_head
    assert raw.exists()
    assert feedback_state.validate_feedback_state(root).current is None
    assert feedback_state.load_report_cut(root) is None
    assert not (feedback_root(root) / "finalization.json").exists()


@pytest.mark.parametrize("prior_active", [False, True])
def test_changed_basis_after_publication_failure_discards_only_staged_artifacts(
    feedback_publication_session, monkeypatch, prior_active
):
    root = feedback_publication_session
    _, raw, identity = _store_agent_issue(root, SESSION_ID)
    if prior_active:
        monkeypatch.setattr(
            report,
            "run_codex_exec",
            lambda *_args, **_kwargs: _fake_result(
                root, _remediation_output(identity, "human_required")
            ),
        )
        assert _invoke()["result"] == "attention"
    before = feedback_state.load_active_state(root)
    calls = []
    with monkeypatch.context() as failing:
        failing.setattr(report, "run_codex_exec", _repair(root, identity, calls))

        def fail_publication(*_args, **_kwargs):
            raise OSError("publication interrupted")

        failing.setattr(
            report,
            "publish_current_pointer",
            fail_publication,
        )
        failed = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
        assert failed.exit_code == 1, failed.output
    manifest, path = feedback_state.load_report_cut(root)
    publication = manifest["publication"]
    staged = [
        *publication["generation_artifacts"],
        *publication["history_artifacts"],
        publication["report"],
    ]
    assert all((root / item["path"]).exists() for item in staged)
    (root / "dependency.conf").write_text("changed after failed publication\n")
    run_git(root, "add", "dependency.conf")
    run_git(root, "commit", "-m", "change before publication recovery")
    monkeypatch.setattr(
        report,
        "run_codex_exec",
        lambda *_args, **_kwargs: pytest.fail("recovery must not call remediation"),
    )
    # 未公開 generation の回収途中で停止しても、欠落済み artifact を許して再開する。
    unlink = feedback_state._unlink_artifact_reference
    with monkeypatch.context() as failing:

        def fail_unlink(*args, **kwargs):
            unlink(*args, **kwargs)
            raise OSError("staged cleanup interrupted")

        failing.setattr(feedback_state, "_unlink_artifact_reference", fail_unlink)
        failed = runner.invoke(app, ["feedback", "report"], catch_exceptions=False)
        assert failed.exit_code == 1, failed.output
    assert _invoke()["result"] == "recheck_pending"
    assert raw.exists() is not prior_active
    after = feedback_state.validate_feedback_state(root)
    assert after.current == before.current
    assert after.issues == before.issues
    assert feedback_state.load_report_cut(root) is None
    assert path.exists()
    assert all(not (root / item["path"]).exists() for item in staged)
    assert calls == ["repair"]
