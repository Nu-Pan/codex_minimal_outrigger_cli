"""重要事項確認の回復・補正・取消と、本命の終了結果との分離を検証する。"""

import json
import os
import signal
import threading
from functools import partial
from pathlib import Path

import oracle.other.path_model as path_model_module
import pytest
import typer
from _cli_support import terminal_primary_report
from _codex_support import (
    codex_override_config,
    script_codex_calls,
    setup_codex_home,
)
from _command_support import write_python_executable
from _report_support import assert_report_layout, report_metadata, report_section

import commons.runtime_cli as runtime_cli
import commons.runtime_codex_exec as exec_module
import commons.runtime_codex_profile as profile_module
import commons.runtime_codex_recovery as recovery
import commons.runtime_primary_report_review as review_module
from commons.runtime_errors import CmocError, CodexProcessStopError
from commons.runtime_git import WorktreeSnapshot
from commons.runtime_logging import SubcommandLogger
from commons.runtime_primary_report_review import (
    PrimaryReportReviewState,
    add_primary_report_review,
)
from commons.runtime_report_markdown import ReportSummary, render_report_document
from commons.runtime_results import TerminalResult
from config.cmoc_config import CmocConfig

_SUCCESS = (
    '{"type":"thread.started","thread_id":"review-session"}\n'
    '{"type":"turn.completed"}\n'
)
_NONE = {"status": "no_findings", "findings": []}
_FINDING = {
    "summary": "目標未達の作業があります。",
    "evidence": [{"location": "詳細結果", "quote": "目標未達で停止しました。"}],
}


def mechanical_report():
    return render_report_document(
        "cmoc doctor report",
        {"command": "cmoc doctor", "execution_id": "source", "work_root": "/repo"},
        ReportSummary("完了"),
        "目標未達で停止しました。\n末尾まで確認する必要のある本文。",
        execution_record="## 実行記録\n\n本命の最終出力全文。",
    )


@pytest.fixture
def review_runtime(
    tmp_path,
    monkeypatch,
    primary_report_review_runner,
    nonpersistent_codex_ids,
):
    """確認の制御・保存を、解決済み root と変更のない作業成果物で検証する。"""
    root = tmp_path / "repo"
    root.mkdir()
    setup_codex_home(tmp_path, monkeypatch)

    # 実 Git の root・linked worktree 解決は test_codex_runtime_paths.py に残し、
    # ここでは完全な builder・prompt と実 exec 制御を同じ対象 root で通す。
    def resolve_roots(cwd):
        assert cwd == root
        return root, root

    monkeypatch.setattr(path_model_module, "_resolve_git_worktree_roots", resolve_roots)

    # Fake は .cmoc 内の応答・診断だけを保存する。実成果物の変動検出と復元は
    # test_codex_runtime_retry.py の restores_artifacts_changed_by_correction に残す。
    def unchanged_artifacts(work_root):
        assert work_root == root
        return WorktreeSnapshot(work_root, ())

    monkeypatch.setattr(exec_module, "capture_worktree_snapshot", unchanged_artifacts)
    monkeypatch.setattr(
        review_module,
        "run_codex_exec",
        partial(
            primary_report_review_runner,
            config=CmocConfig(),
            quota_poll_interval_sec=0,
            transient_poll_interval_sec=0,
        ),
    )
    return root, SubcommandLogger(root, "doctor")


@pytest.mark.parametrize(
    "result",
    [
        _NONE,
        {"status": "findings", "findings": [_FINDING]},
        {
            "status": "incomplete",
            "reason": "context の制限で全文を扱えませんでした。",
            "reviewed_scope": "詳細結果まで確認。実行情報は未確認。",
            "findings": [_FINDING],
        },
    ],
)
def test_review_accepts_schema_results_and_preserves_frozen_full_input(
    review_runtime, monkeypatch, result
):
    root, logger = review_runtime
    source = mechanical_report()
    calls = script_codex_calls(
        monkeypatch, [(0, _SUCCESS, json.dumps({"result": result}, ensure_ascii=False))]
    )
    rendered = add_primary_report_review(
        root, source, logger, PrimaryReportReviewState()
    )
    assert len(calls) == 1  # 正式な incomplete 自体は補正・再試行の理由にしない。
    frozen = next((root / ".cmoc/gu/log/codex").glob("*/*review*.md"))
    assert frozen.read_text() == source
    assert str(frozen) in calls[0]["prompt"]
    assert calls[0]["cwd"] == root
    assert "resume" not in calls[0]["argv"]
    assert "--output-schema" in calls[0]["argv"]
    overrides = codex_override_config(calls[0]["argv"])
    for server in ("cmoc_feedback", "cmoc_document_search", "cmoc_editor_input"):
        assert overrides["mcp_servers"][server]["enabled"] is False
        assert overrides["mcp_servers"][server]["command"]
        assert overrides["mcp_servers"][server]["enabled_tools"] == []
    assert_report_layout(rendered)
    assert rendered.index("## 次の操作") < rendered.index("## 重要事項の確認結果")
    assert rendered.index("## 重要事項の確認結果") < rendered.index("## 元の指示")
    assert report_metadata(rendered) == report_metadata(source)
    for name in (
        "実行結果",
        "要注意事項",
        "次の操作",
        "元の指示",
        "詳細結果",
        "実行記録",
    ):
        assert report_section(rendered, name) == report_section(source, name)
    section = report_section(rendered, "重要事項の確認結果")
    if result["status"] == "no_findings":
        assert "全文を確認した範囲では該当なし" in section
    else:
        assert _FINDING["summary"] in section
        assert _FINDING["evidence"][0]["quote"] in section
        assert _FINDING["evidence"][0]["location"] in section
    assert ("エージェントによる重要事項の確認は完了していません。" in section) == (
        result["status"] == "incomplete"
    )
    if result["status"] == "incomplete":
        assert result["reason"] in section and result["reviewed_scope"] in section
    record = report_section(rendered, "重要事項確認の実行記録")
    assert "対象外" in record and str(frozen) in record
    call = logger.codex_call_records()[0]
    assert call["call_log_path"] in record and call["output_path"] in record
    assert result["status"] in record


@pytest.mark.parametrize("recovers", [True, False])
def test_review_uses_common_correction_limit_and_retains_rejected_output(
    review_runtime, monkeypatch, recovers
):
    root, logger = review_runtime
    replies = [(0, _SUCCESS, '{"result":{"status":"findings","findings":[]}}')] * 3
    if recovers:
        replies[-1] = (0, _SUCCESS, json.dumps({"result": _NONE}))
    calls = script_codex_calls(monkeypatch, replies)
    rendered = add_primary_report_review(
        root, mechanical_report(), logger, PrimaryReportReviewState()
    )
    assert len(calls) == 3
    for call in calls[1:]:
        index = call["argv"].index("resume")
        assert call["argv"][index + 1] == "review-session"
        assert "完全な置換出力" in call["prompt"]
    logs = logger.codex_call_records()
    assert all(Path(call["output_path"]).exists() for call in logs)
    assert len({call["output_path"] for call in logs}) == 3
    assert "検証不合格" in rendered
    section = report_section(rendered, "重要事項の確認結果")
    assert ("該当なし" in section) is recovers
    if not recovers:
        assert "エージェントによる重要事項の確認は完了していません。" in section
        assert "maximum output corrections reached: 2" in section
        assert any(
            e["event"] == "codex.structured_output_validation_exhausted"
            for e in logger.event_records()
        )


@pytest.mark.parametrize("reason", ["Quota exceeded", "Selected model is at capacity"])
def test_review_waits_probes_and_resumes_with_common_recovery(
    review_runtime, monkeypatch, reason
):
    root, logger = review_runtime
    calls = script_codex_calls(
        monkeypatch,
        [
            (
                1,
                _SUCCESS.splitlines()[0]
                + "\n"
                + json.dumps({"type": "turn.failed", "error": {"message": reason}}),
                None,
            ),
            (0, _SUCCESS, "available"),
            (0, _SUCCESS, json.dumps({"result": _NONE})),
        ],
    )
    rendered = add_primary_report_review(
        root, mechanical_report(), logger, PrimaryReportReviewState()
    )
    assert len(calls) == 3
    assert "resume" not in calls[1]["argv"]
    index = calls[2]["argv"].index("resume")
    assert calls[2]["argv"][index + 1] == "review-session"
    assert calls[2]["prompt"] == calls[0]["prompt"]
    assert "全文を確認した範囲では該当なし" in rendered
    assert "probe" in report_section(rendered, "重要事項確認の実行記録") or any(
        "probe" in e.get("purpose", "") for e in logger.codex_call_records()
    )


@pytest.mark.parametrize(
    "phase", ["initial", "correction", "waiting", "probe", "acceptance"]
)
def test_review_cancellation_prevents_all_subsequent_calls(
    review_runtime, monkeypatch, phase
):
    root, logger = review_runtime
    replies = [(0, _SUCCESS, json.dumps({"result": _NONE}))]
    if phase == "correction":
        replies.insert(0, (0, _SUCCESS, "invalid JSON"))
    if phase in {"waiting", "probe"}:
        replies.insert(
            0, (1, '{"type":"turn.failed","error":{"message":"Quota exceeded"}}', None)
        )
    if phase == "probe":
        replies.insert(1, (0, _SUCCESS, "available"))

    def on_call(number, call):
        if (phase in {"initial", "acceptance"} and number == 1) or (
            phase in {"correction", "probe"} and number == 2
        ):
            if phase == "acceptance":
                recovery.current_recovery_cancellation().set()
            else:
                os.kill(os.getpid(), signal.SIGINT)

    if phase == "waiting":

        def wait(**kwargs):
            os.kill(os.getpid(), signal.SIGINT)

        monkeypatch.setattr(exec_module, "wait_for_recovery", wait)
    calls = script_codex_calls(monkeypatch, replies, on_call=on_call)
    state = PrimaryReportReviewState()
    rendered = add_primary_report_review(root, mechanical_report(), logger, state)
    assert state.cancelled
    assert len(calls) == (2 if phase in {"correction", "probe"} else 1)
    assert "エージェントによる重要事項の確認は完了していません。" in rendered
    assert "該当なし" not in report_section(rendered, "重要事項の確認結果")
    later_source = mechanical_report().replace("目標未達", "別の本文")
    later = add_primary_report_review(root, later_source, logger, state)
    assert len(calls) == (2 if phase in {"correction", "probe"} else 1)
    assert "別の本文" in later and "開始していません" in later
    assert len(list((root / ".cmoc/gu/log/codex").glob("*/*review*.md"))) == 1


def test_review_starts_after_main_interruption_and_accepts_new_signal(
    review_runtime, monkeypatch
):
    root, logger = review_runtime
    restore = recovery.install_recovery_interruption()
    try:
        prior = recovery.current_recovery_cancellation()
        prior.set()
        with recovery.defer_recovery_interruption(check_pending=False, propagate=False):
            calls = script_codex_calls(
                monkeypatch,
                [(0, _SUCCESS, json.dumps({"result": _NONE}))],
                on_call=lambda *_args: os.kill(os.getpid(), signal.SIGINT),
            )
            state = PrimaryReportReviewState()
            rendered = add_primary_report_review(
                root, mechanical_report(), logger, state
            )
            assert len(calls) == 1 and state.cancelled
            assert "取り消されました" in rendered
        assert recovery.current_recovery_cancellation() is prior and prior.is_set()
    finally:
        restore()


@pytest.mark.parametrize("ending", ["natural_completion", "user_interruption", "error"])
@pytest.mark.parametrize("failure", ["call", "cancel", "stop", "log"])
@pytest.mark.parametrize("result_field", ["result", "completion_reason"])
def test_review_failure_preserves_main_outcome_except_required_finalization(
    cli_terminal_directory, monkeypatch, capsys, ending, failure, result_field
):
    root = cli_terminal_directory
    # この fixture は root 解決を省く。builder の対象だけ実際のパラメータに置換する。
    monkeypatch.setattr(
        review_module,
        "build_primary_report_review_parameter",
        lambda **kwargs: object(),
    )

    def failed_review(*args, **kwargs):
        if failure == "cancel":
            raise KeyboardInterrupt
        if failure == "stop":
            raise CodexProcessStopError("stop failed", [], "process still running")
        if failure == "log":
            raise OSError("record save failed")
        raise CmocError("review failed", [], "call failed")

    monkeypatch.setattr(review_module, "run_codex_exec", failed_review)

    def work():
        result = TerminalResult(**{result_field: "attention"})
        if ending == "error":
            raise CmocError(
                "main failed", [], "original failure", terminal_result=result
            )
        if ending == "user_interruption":
            runtime_cli.mark_current_subcommand_interrupted()
        return result

    if ending == "error" or failure in {"stop", "log"}:
        with pytest.raises(typer.Exit) as exited:
            runtime_cli.run_cli_subcommand(
                work, command_name="doctor", doctor_preprocess=False
            )
        assert exited.value.exit_code == 1
    else:
        runtime_cli.run_cli_subcommand(
            work, command_name="doctor", doctor_preprocess=False
        )
    output = capsys.readouterr()
    events = [
        json.loads(line)
        for line in next((root / ".cmoc/gu/log/sub_command").glob("*.jsonl"))
        .read_text()
        .splitlines()
    ]
    finished = events[-1]
    assert finished["event"] == "command_finished"
    if failure in {"stop", "log"}:
        assert finished["classification"] == "error" and finished["returncode"] == 1
        assert "primary_report_path" not in finished
    else:
        assert finished["classification"] == ending
        assert finished["returncode"] == (1 if ending == "error" else 0)
        assert finished[result_field] == "attention"
        text = terminal_primary_report(output.out + output.err).read_text()
        assert "エージェントによる重要事項の確認は完了していません。" in text


def test_missing_codex_home_marks_review_unstarted_without_call_files(
    review_runtime, tmp_path, monkeypatch
):
    root, logger = review_runtime
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "missing"))
    script_codex_calls(monkeypatch, [])
    rendered = add_primary_report_review(
        root, mechanical_report(), logger, PrimaryReportReviewState()
    )
    assert "エージェントによる重要事項の確認は完了していません。" in rendered
    assert "Codex call: 未開始" in rendered
    assert not list((root / ".cmoc/gu/log/codex").glob("*/*_call.json"))


def test_review_process_start_failure_is_incomplete(review_runtime, monkeypatch):
    root, logger = review_runtime

    def denied(*args, **kwargs):
        raise PermissionError("executable permission denied")

    # Git 解決は Popen の置換より前に終え、子 process の開始不能だけを注入する。
    parameter_builder = review_module.build_primary_report_review_parameter
    parameter = parameter_builder(
        mechanical_report_path=root / "input.md", agent_call_cwd=root
    )
    context = profile_module.AgentCallPathContext(root)
    monkeypatch.setattr(profile_module.subprocess, "Popen", denied)
    monkeypatch.setattr(
        review_module,
        "build_primary_report_review_parameter",
        lambda **kwargs: parameter,
    )
    monkeypatch.setattr(exec_module, "AgentCallPathContext", lambda *_args: context)
    rendered = add_primary_report_review(
        root, mechanical_report(), logger, PrimaryReportReviewState()
    )
    assert "エージェントによる重要事項の確認は完了していません。" in rendered
    assert "permission denied" in rendered


def test_cancelled_review_stops_fake_process_and_keeps_collected_diagnostics(
    review_runtime, tmp_path, monkeypatch
):
    root, logger = review_runtime
    fake_bin = tmp_path / "fake-bin"
    fake_bin.mkdir()
    ready = tmp_path / "ready.pid"
    write_python_executable(
        fake_bin / "codex",
        [
            "import os, pathlib, sys, time",
            "sys.stdin.read()",
            "output = pathlib.Path(sys.argv[sys.argv.index('--output-last-message') + 1])",
            "output.write_text('unaccepted partial output')",
            "print('partial stdout', flush=True)",
            "print('partial stderr', file=sys.stderr, flush=True)",
            f"pathlib.Path({str(ready)!r}).write_text(str(os.getpid()))",
            "time.sleep(30)",
        ],
    )
    monkeypatch.setenv("PATH", str(fake_bin) + os.pathsep + os.environ["PATH"])
    stopped = threading.Event()

    def cancel_when_ready():
        while not stopped.wait(0.01):
            if ready.is_file() and ready.read_text():
                os.kill(os.getpid(), signal.SIGINT)
                return

    monitor = threading.Thread(target=cancel_when_ready)
    monitor.start()
    state = PrimaryReportReviewState()
    try:
        rendered = add_primary_report_review(root, mechanical_report(), logger, state)
    finally:
        stopped.set()
        monitor.join(timeout=5)
    assert state.cancelled and not monitor.is_alive()
    with pytest.raises(ProcessLookupError):
        os.kill(int(ready.read_text()), 0)
    (call,) = logger.codex_call_records()
    assert Path(call["stdout_log_path"]).read_text() == "partial stdout\n"
    assert Path(call["stderr_log_path"]).read_text() == "partial stderr\n"
    assert "unaccepted partial output" in report_section(
        rendered, "重要事項確認の実行記録"
    )
    result = report_section(rendered, "重要事項の確認結果")
    assert "エージェントによる重要事項の確認は完了していません。" in result
    assert "unaccepted partial output" not in result
