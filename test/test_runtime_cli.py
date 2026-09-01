"""CLI の error、log、preflight、completion 境界を検証する。

根拠:
- {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
- {{work-root}}/oracle/doc/app_spec/error_handling.md
- {{work-root}}/oracle/doc/app_spec/cli_auto_completion.md
- {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
- {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
- {{work-root}}/oracle/doc/app_spec/timestamp.md
- {{work-root}}/oracle/doc/app_spec/windows_toast_notification.md
- {{work-root}}/oracle/src/oracle/other/path_model.py

CLI lifecycle の error、log、preflight、completion は同じ runner、work root、
subcommand event を共有する一つの外部契約として一箇所で検証する。
この file は 16,000 文字を超えるが、error report、console log、preflight、completion
が共通の runner と終了処理を観測するため、これ以上分割すると同じ外部契約の文脈が
分散する。
"""

import json
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
import typer
from _cli_support import run_doctor, runner
from _codex_support import codex_parameter, setup_codex_home, stub_codex_overrides
from _git_support import make_repo, run_git

import commons.runtime_cli as runtime_cli
import commons.runtime_codex_tui as runtime_codex_tui
import commons.runtime_feedback as runtime_feedback
import commons.runtime_logging as runtime_logging
import commons.runtime_windows_toast as runtime_windows_toast
import main as main_module
from cmoc_runtime import (
    CmocError,
    SubcommandLogger,
    TerminalResult,
    format_duration,
    render_error,
)
from config.cmoc_config import CmocConfig
from main import app


@pytest.fixture(autouse=True)
def _clear_completion_probe_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """通常の in-process CLI test を外部の completion probe 環境から分離する。"""
    # {{work-root}}/oracle/doc/app_spec/cli_auto_completion.md
    monkeypatch.delenv("_CMOC_COMPLETE", raising=False)


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (0.19, " 0.1 Sec"),
        (59.99, "59.9 Sec"),
        (60, " 1 Min  0.0 Sec"),
        (10 * 3600, "10 Hr  0 Min  0.0 Sec"),
        (24 * 3600, " 1 Day  0 Hr  0 Min  0.0 Sec"),
        (30 * 24 * 3600, " 1 Mo  0 Day  0 Hr  0 Min  0.0 Sec"),
        (
            (99 * 30 + 29) * 24 * 3600 + 23 * 3600 + 59 * 60 + 59.99,
            "99 Mo 29 Day 23 Hr 59 Min 59.9 Sec",
        ),
    ],
)
def test_format_duration_uses_compact_space_padded_time_parts(
    seconds: float, expected: str
) -> None:
    """duration を上位 0 単位なしの固定幅 field で表示する。"""
    assert format_duration(seconds) == expected


def test_format_duration_rejects_unrepresentable_values() -> None:
    """負値と 2 桁の最大構成を超える duration を拒否する。"""
    with pytest.raises(ValueError, match="two-digit month"):
        format_duration(100 * 30 * 24 * 3600)
    with pytest.raises(ValueError, match="non-negative"):
        format_duration(-0.1)


def test_subcommand_logger_keeps_one_file_per_command_on_timestamp_collision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """同一 timestamp でもサブコマンドごとに固有のログファイルを保持する。"""
    timestamps = iter(
        [
            "2026-06-27_10-00_00_000001000",
            "2026-06-27_10-00_00_000001000",
            "2026-06-27_10-00_00_000002000",
        ]
    )
    monkeypatch.setattr(runtime_logging, "timestamp", lambda: next(timestamps))

    first = SubcommandLogger(tmp_path, "first")
    second = SubcommandLogger(tmp_path, "second")
    first.event("marker")
    second.event("marker")

    assert first.path.name == "2026-06-27_10-00_00_000001000.jsonl"
    assert second.path.name == "2026-06-27_10-00_00_000002000.jsonl"
    assert [line for line in first.path.read_text().splitlines() if line]
    assert [line for line in second.path.read_text().splitlines() if line]


def test_subcommand_logger_handles_parallel_worker_events_and_quota_wait(
    tmp_path: Path,
) -> None:
    """共有 logger へ並列 worker が記録しても event と待機時間を失わない。"""
    logger = SubcommandLogger(tmp_path, "indexing")
    worker_count = 8
    barrier = threading.Barrier(worker_count)

    def record_worker_event(index: int) -> None:
        """共有 logger への並列書き込みを再現する。"""
        barrier.wait()
        logger.add_quota_wait(0.25)
        logger.event("worker", index=index)

    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        list(executor.map(record_worker_event, range(worker_count)))

    events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    assert len(events) == worker_count
    assert all(event["event"] == "worker" for event in events)
    assert sorted(event["index"] for event in events) == list(range(worker_count))
    assert logger.quota_wait_sec == pytest.approx(worker_count * 0.25)


def test_noninteractive_success_emits_one_terminal_result_after_progress(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """stdout を成功 terminal result だけにし、詳細 step はログへ閉じる。"""
    # {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(
        runtime_cli,
        "start_feedback_invocation",
        lambda *_args: (None, None),
    )
    report_path = root / "report.md"
    report_path.write_text("# report\n")

    def succeed() -> TerminalResult:
        """トップレベルと内部 step を含む成功結果を返す。"""
        runtime_cli.start_subcommand_step(1, "top level", "top level")
        runtime_cli.start_subcommand_step("1/1, 1/1", "nested", "nested")
        return TerminalResult(
            primary_report=report_path,
            primary_report_role="probe report",
            result="attention",
            next_actions=("report を確認してください。",),
        )

    runtime_cli.run_cli_subcommand(
        succeed,
        command_name="probe",
        command_argv=["cmoc", "probe"],
        doctor_preprocess=False,
    )

    captured = capsys.readouterr()
    stdout_lines = captured.out.splitlines()
    assert stdout_lines[0] == "# 完了: cmoc probe"
    assert stdout_lines[1] == (
        f"- primary report (probe report): `{report_path.resolve()}`"
    )
    assert stdout_lines[2] == "- result: `attention`"
    assert stdout_lines[3] == "- 次の操作: report を確認してください。"
    assert captured.out.count("# 完了: cmoc probe") == 1
    assert captured.out.count(str(report_path.resolve())) == 1
    assert "cmoc probe を開始" in captured.err
    assert "cmoc probe: top level" in captured.err
    assert "nested" not in captured.err

    [log_path] = (root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert events[-1]["event"] == "command_finished"
    assert events[-1]["classification"] == "natural_completion"
    assert events[-1]["terminal_result"]["result"] == "attention"
    assert any(event.get("step") == "nested" for event in events)


def test_internal_failure_traceback_is_logged_but_not_printed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """想定外障害の stack は診断ログだけに保存する。"""
    # {{work-root}}/oracle/doc/app_spec/error_handling.md
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(
        runtime_cli,
        "start_feedback_invocation",
        lambda *_args: (None, None),
    )

    def fail() -> None:
        raise ValueError("unexpected failure")

    with pytest.raises(typer.Exit):
        runtime_cli.run_cli_subcommand(
            fail,
            command_name="probe",
            command_argv=["cmoc", "probe"],
            doctor_preprocess=False,
        )

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "# 失敗: cmoc probe" in captured.err
    assert "unexpected failure" in captured.err
    assert "Traceback" not in captured.err
    [log_path] = (root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    failure = events[-1]["failure"]
    assert failure["classification"] == "internal_failure"
    assert "Traceback" in failure["traceback"]
    assert "ValueError: unexpected failure" in failure["traceback"]


def test_error_terminal_result_does_not_repeat_primary_report_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """error detail 内の primary report path は console で重複させない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(
        runtime_cli,
        "start_feedback_invocation",
        lambda *_args: (None, None),
    )
    report_path = root / "error-report.md"
    report_path.write_text("# error report\n")

    def fail() -> None:
        raise CmocError(
            "known conflict",
            ["report を確認してください。"],
            f"report: {report_path}\nconflict remains",
            terminal_result=TerminalResult(
                primary_report=report_path,
                primary_report_role="error report",
            ),
        )

    with pytest.raises(typer.Exit):
        runtime_cli.run_cli_subcommand(
            fail,
            command_name="probe",
            command_argv=["cmoc", "probe"],
            doctor_preprocess=False,
        )

    captured = capsys.readouterr()
    assert captured.out == ""
    stderr_lines = captured.err.splitlines()
    heading_index = stderr_lines.index("# 失敗: cmoc probe")
    assert stderr_lines[heading_index + 1] == (
        f"- primary report (error report): `{report_path.resolve()}`"
    )
    assert captured.err.count(str(report_path.resolve())) == 1
    assert "conflict remains" in captured.err

    [log_path] = (root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert str(report_path) in events[-1]["failure"]["detail"]


def test_detector_does_not_swallow_keyboard_interrupt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """detector 中の Ctrl+C を本命サブコマンドの中断として扱う。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)

    def interrupt_detector(_event: dict[str, object], _log_path: Path) -> None:
        """detector 中のユーザー中断を再現する。"""
        raise KeyboardInterrupt()

    monkeypatch.setattr(runtime_feedback, "detect_feedback_event", interrupt_detector)

    def invoke_stable_event() -> None:
        """detector を呼び出す stable event を記録する。"""
        logger = runtime_logging.current_subcommand_logger()
        assert logger is not None
        logger.event(
            "feedback.reporter_unavailable",
            event_schema_version=1,
            event_id="evt_keyboard_interrupt",
            event_type="feedback.reporter_unavailable",
            occurred_at="2026-08-09T00:00:00Z",
            subcommand_invocation_id=logger.invocation_id,
            component="collector",
            failure_code="protocol_error",
        )

    with pytest.raises(KeyboardInterrupt):
        runtime_cli.run_cli_subcommand(
            invoke_stable_event,
            command_name="probe",
            command_argv=["cmoc", "probe"],
            doctor_preprocess=False,
        )

    [log_path] = (root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert not any(event["event"] == "feedback.detector_failed" for event in events)


def test_cli_wrapper_doctor_preprocess_failure_writes_subcommand_log(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """doctor preprocess の失敗を終了コードとサブコマンドログに記録する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)

    def fail_doctor(_root: Path) -> None:
        """doctor preprocess の失敗を再現する fake。

        根拠: {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
        """
        raise CmocError("doctor failed", ["fix doctor"], "doctor detail")

    monkeypatch.setattr(runtime_cli, "run_doctor_preprocess", fail_doctor)

    with pytest.raises(typer.Exit) as exc_info:
        runtime_cli.run_cli_subcommand(
            lambda: 0,
            command_name="probe",
            command_argv=["cmoc", "probe"],
        )

    assert exc_info.value.exit_code == 1
    [log_path] = (root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert events[0]["event"] == "command_invoked"
    assert any(event["event"] == "step_started" for event in events)
    assert events[-1]["event"] == "command_finished"
    assert events[-1]["returncode"] == 1
    assert "probe" in json.dumps(events[0], ensure_ascii=False)
    assert "doctor failed" in json.dumps(events[-1], ensure_ascii=False)
    assert events[-1]["failure"]["classification"] == "handled_failure"
    assert "traceback" not in events[-1]["failure"]


def test_cli_nonzero_impl_result_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """callback の非0 returnも共通error reportと終了コードへ変換する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)

    with pytest.raises(typer.Exit) as exc_info:
        runtime_cli.run_cli_subcommand(
            lambda: 7,
            command_name="probe",
            command_argv=["cmoc", "probe"],
            doctor_preprocess=False,
        )

    captured = capsys.readouterr()
    assert exc_info.value.exit_code == 7
    assert captured.out == ""
    assert "# 失敗: cmoc probe" in captured.err
    assert "returncode: 7" in captured.err
    assert "Traceback" not in captured.err
    assert "- 終了コード: `7`" in captured.err


def test_cli_error_report_survives_failed_error_log_flush(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """終了ログの失敗が元の error report を隠さないことを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    original_event = runtime_cli.SubcommandLogger.event

    def fail_finish_event(
        logger: SubcommandLogger, kind: str, **payload: object
    ) -> None:
        """command_finished のログ書き込み失敗を再現する。"""
        if kind == "command_finished":
            raise OSError("log flush failed")
        original_event(logger, kind, **payload)

    def fail_impl() -> None:
        """callback の失敗を再現する。"""
        raise ValueError("callback failed")

    monkeypatch.setattr(runtime_cli.SubcommandLogger, "event", fail_finish_event)

    with pytest.raises(typer.Exit) as exc_info:
        runtime_cli.run_cli_subcommand(
            fail_impl,
            command_name="probe",
            command_argv=["cmoc", "probe"],
            doctor_preprocess=False,
        )

    captured = capsys.readouterr()
    assert exc_info.value.exit_code == 1
    assert captured.out == ""
    assert "# 失敗: cmoc probe" in captured.err
    assert "callback failed" in captured.err
    assert "Traceback" not in captured.err


def test_cli_wrapper_does_not_convert_keyboard_interrupt_to_error_report(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Codex CLI へ委ねる Ctrl+C を cmoc の error report に変換しない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)

    def interrupt() -> None:
        """子 process から伝播した Ctrl+C を再現する。"""
        raise KeyboardInterrupt()

    with pytest.raises(KeyboardInterrupt):
        runtime_cli.run_cli_subcommand(
            interrupt,
            command_name="probe",
            command_argv=["cmoc", "probe"],
            doctor_preprocess=False,
        )

    captured = capsys.readouterr()
    assert "# 失敗" not in captured.out
    assert "# 失敗" not in captured.err
    [log_path] = (root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert events[-1]["event"] == "command_finished"
    assert events[-1]["returncode"] == 130


def test_cli_tui_keyboard_interrupt_does_not_emit_terminal_result_notification(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """TUI の Ctrl+C は Codex CLI に委ね、終了 toast を追加しない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    notifications: list[str] = []
    monkeypatch.setattr(
        runtime_cli,
        "notify_terminal_result",
        lambda _command, _repository, state: notifications.append(state),
    )

    def interrupt() -> None:
        """TUI process から伝播した Ctrl+C を再現する。"""
        runtime_cli.mark_current_tui_process_started()
        raise KeyboardInterrupt()

    with pytest.raises(KeyboardInterrupt):
        runtime_cli.run_cli_subcommand(
            interrupt,
            command_name="tui",
            command_argv=["cmoc", "tui"],
            doctor_preprocess=False,
            tui_process=True,
        )

    assert notifications == []


def test_cli_tui_startup_keyboard_interrupt_emits_failure_notification(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """TUI process 起動前の Ctrl+C は失敗結果として通知する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    notifications: list[str] = []
    monkeypatch.setattr(
        runtime_cli,
        "notify_terminal_result",
        lambda _command, _repository, state: notifications.append(state),
    )

    def interrupt_before_launch() -> None:
        """TUI 起動前の準備処理から伝播した Ctrl+C を再現する。"""
        raise KeyboardInterrupt()

    with pytest.raises(KeyboardInterrupt):
        runtime_cli.run_cli_subcommand(
            interrupt_before_launch,
            command_name="tui",
            command_argv=["cmoc", "tui"],
            doctor_preprocess=False,
            tui_process=True,
        )

    assert notifications == ["failed"]
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "# 失敗: cmoc tui" in captured.err
    assert "Traceback" not in captured.err


def test_cli_tui_subprocess_startup_interrupt_emits_failure_notification(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Codex subprocess の起動前中断を TUI 終了後の中断と混同しない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    notifications: list[str] = []
    monkeypatch.setattr(
        runtime_cli,
        "notify_terminal_result",
        lambda _command, _repository, state: notifications.append(state),
    )

    def interrupt_before_process_start(*_args: object, **_kwargs: object) -> object:
        """Popen 前の Codex 起動失敗を再現する。"""
        raise KeyboardInterrupt()

    monkeypatch.setattr(
        runtime_codex_tui,
        "run_codex_subprocess",
        interrupt_before_process_start,
    )

    def invoke_tui() -> None:
        """共通 runner から実際の TUI runtime 起動境界を通る。"""
        runtime_codex_tui.run_codex_tui(
            codex_parameter(agent_call_cwd=root),
            root=root,
            config=CmocConfig(),
        )

    with pytest.raises(KeyboardInterrupt):
        runtime_cli.run_cli_subcommand(
            invoke_tui,
            command_name="tui",
            command_argv=["cmoc", "tui"],
            doctor_preprocess=False,
            tui_process=True,
        )

    assert notifications == ["failed"]


@pytest.mark.parametrize(
    ("tui_process", "expected_state"),
    [(False, "completed"), (True, None)],
)
def test_cli_terminal_notification_boundary_on_success(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tui_process: bool,
    expected_state: str | None,
) -> None:
    """非対話成功だけを終了 log と cleanup の後に terminal 通知する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    calls: list[tuple[str, Path, str]] = []

    def record_notification(command: str, repository: Path, state: str) -> None:
        """通知時点の logger と終了 event を検証する。"""
        assert runtime_cli.current_subcommand_logger() is None
        [log_path] = (root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").glob(
            "*.jsonl"
        )
        events = [json.loads(line) for line in log_path.read_text().splitlines()]
        assert events[-1]["event"] == "command_finished"
        calls.append((command, repository, state))

    monkeypatch.setattr(runtime_cli, "notify_terminal_result", record_notification)

    runtime_cli.run_cli_subcommand(
        lambda: None,
        command_name="probe",
        command_argv=["cmoc", "probe"],
        doctor_preprocess=False,
        tui_process=tui_process,
    )

    captured = capsys.readouterr()
    expected = [] if expected_state is None else [("probe", root, expected_state)]
    assert calls == expected
    if tui_process:
        assert captured.out == ""
        assert "# 完了: cmoc probe" not in captured.err
    else:
        assert "# 完了: cmoc probe" in captured.out


@pytest.mark.parametrize("tui_process", [False, True])
def test_cli_terminal_notification_reports_error_for_all_command_kinds(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    tui_process: bool,
) -> None:
    """非対話と TUI の確定済み失敗をどちらも 1 回だけ通知する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    calls: list[tuple[str, Path, str]] = []
    monkeypatch.setattr(
        runtime_cli,
        "notify_terminal_result",
        lambda command, repository, state: calls.append((command, repository, state)),
    )

    with pytest.raises(typer.Exit) as exc_info:
        runtime_cli.run_cli_subcommand(
            lambda: 7,
            command_name="probe",
            command_argv=["cmoc", "probe"],
            doctor_preprocess=False,
            tui_process=tui_process,
        )

    assert exc_info.value.exit_code == 7
    assert calls == [("probe", root, "failed")]


def test_cli_terminal_notification_distinguishes_user_interruption(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """正常に確定したユーザー中断を自然完了やエラーとして通知しない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    calls: list[str] = []
    monkeypatch.setattr(
        runtime_cli,
        "notify_terminal_result",
        lambda _command, _repository, state: calls.append(state),
    )

    def interrupt_normally() -> None:
        """中断可能サブコマンドの正常な完了処理を再現する。"""
        runtime_cli.mark_current_subcommand_interrupted()

    runtime_cli.run_cli_subcommand(
        interrupt_normally,
        command_name="probe",
        command_argv=["cmoc", "probe"],
        doctor_preprocess=False,
    )

    assert calls == ["interrupted"]


def test_interruptible_cli_handles_common_preprocess_interrupt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """interruptible command の common preprocess 中断を正常完了として扱う。"""
    # {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    calls: list[str] = []
    monkeypatch.setattr(
        runtime_cli,
        "notify_terminal_result",
        lambda _command, _repository, state: calls.append(state),
    )

    def interrupt_doctor(_root: Path) -> None:
        """common doctor preprocess 中のユーザー中断を再現する。"""
        raise KeyboardInterrupt()

    monkeypatch.setattr(runtime_cli, "run_doctor_preprocess", interrupt_doctor)

    runtime_cli.run_cli_subcommand(
        lambda: pytest.fail("implementation must not start after interruption"),
        command_name="interruptible probe",
        command_argv=["cmoc", "interruptible-probe"],
        interruptible=True,
    )

    assert calls == ["interrupted"]
    [log_path] = (root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert events[-1]["event"] == "command_finished"
    assert events[-1]["returncode"] == 0
    assert events[-1]["classification"] == "user_interruption"
    assert events[-1]["terminal_result"]["classification"] == "user_interruption"


def test_cli_notification_failure_does_not_change_terminal_result(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """通知 callback 自体の失敗を成功したサブコマンドへ逆流させない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)

    def fail_notification(*_args: object) -> None:
        """通知境界からの想定外例外を再現する。"""
        raise RuntimeError("toast failed")

    monkeypatch.setattr(runtime_cli, "notify_terminal_result", fail_notification)

    runtime_cli.run_cli_subcommand(
        lambda: None,
        command_name="probe",
        command_argv=["cmoc", "probe"],
        doctor_preprocess=False,
    )


def test_render_error_uses_concise_handled_failure_format() -> None:
    """logger 初期化前の handled failure も簡潔に整形する。"""
    try:
        raise CmocError("summary", ["next"], "detail")
    except CmocError as exc:
        rendered = render_error(exc)

    assert rendered.splitlines() == [
        "# 失敗: cmoc",
        "- 理由: summary",
        "- 次の操作: next",
        "- 詳細: detail",
    ]
    assert "Traceback" not in rendered


def test_render_error_fills_empty_next_actions() -> None:
    """next actions 未指定でも回復行動の既定文を出す。"""
    try:
        raise CmocError("summary", [], "detail")
    except CmocError as exc:
        rendered = render_error(exc)

    assert rendered.count("- 次の操作:") == 1
    assert "入力、実行場所、設定、作業ツリー状態を確認" in rendered


def test_render_error_does_not_expose_internal_traceback() -> None:
    """logger 初期化前でも internal failure の stack を console へ出さない。"""
    try:
        raise ValueError("reported error")
    except ValueError as reported:
        try:
            raise RuntimeError("unrelated active error")
        except RuntimeError:
            rendered = render_error(reported)

    assert "reported error" in rendered
    assert "RuntimeError: unrelated active error" not in rendered
    assert "Traceback" not in rendered


def test_cli_handled_failure_is_written_to_stderr(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """想定済み CLI error は簡潔な terminal result を stderr に返す。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    run_git(root, "switch", "--detach", "HEAD")

    result = runner.invoke(app, ["session", "fork"])

    assert result.exit_code != 0
    assert result.stdout == ""
    assert "# 失敗: cmoc session fork" in result.stderr
    assert "detached HEAD 上では実行できません。" in result.stderr
    assert "Traceback" not in result.stderr


def test_cli_parse_error_report_is_written_to_stderr() -> None:
    """Click の引数解析 error も cmoc 形式で stderr に出す。"""
    result = runner.invoke(app, ["--bad-option"])

    assert result.exit_code != 0
    assert result.stdout == ""
    assert "# 失敗: cmoc" in result.stderr
    assert "CLI 引数解析に失敗しました。" in result.stderr
    assert "No such option: --bad-option" in result.stderr
    assert "Traceback" not in result.stderr
    assert "- 終了コード: `2`" in result.stderr


def test_unknown_subcommand_option_is_rejected_by_cli_parser() -> None:
    """未知の option はサブコマンド実行前の CLI 解析で拒否する。"""
    argv = ["realization", "apply", "fork", "--scope", "bad"]
    result = runner.invoke(app, argv)

    assert result.exit_code != 0
    assert result.stdout == ""
    assert "# 失敗: cmoc" in result.stderr
    assert "CLI 引数解析に失敗しました。" in result.stderr
    assert "No such option: --scope" in result.stderr


def test_cli_requires_current_directory_to_be_work_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """work root 以外からの CLI 実行では副作用を出す前に拒否する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root / "oracle")

    result = runner.invoke(app, ["doctor"])

    assert result.exit_code != 0
    assert result.stdout == ""
    assert "# 失敗: cmoc doctor" in result.stderr
    assert "cmoc は work root で実行してください。" in result.stderr
    assert f"cwd: {(root / 'oracle').resolve()}" in result.stderr
    assert f"work_root: {root.resolve()}" in result.stderr
    assert not (root / ".gitignore").exists()


def test_cli_completion_probe_skips_cmoc_preflight_and_side_effects(
    tmp_path: Path,
) -> None:
    """shell completion probe は cmoc preflight と初期化副作用を起こさない。"""
    root = make_repo(tmp_path)
    isolated_home = tmp_path / "home"
    isolated_home.mkdir()
    main_path = Path(main_module.__file__).resolve()
    result = subprocess.run(
        [sys.executable, str(main_path), "doctor"],
        cwd=root,
        env={
            "PYTHONPATH": str(main_path.parent),
            "_CMOC_COMPLETE": "complete_bash",
            "COMP_WORDS": "cmoc doctor",
            "COMP_CWORD": "1",
            "HOME": str(isolated_home),
        },
        text=True,
        capture_output=True,
        check=False,
    )

    completion_output = result.stdout + result.stderr
    # {{work-root}}/oracle/doc/app_spec/cli_auto_completion.md
    assert result.returncode == 0
    assert "# 失敗" not in completion_output
    assert "サブコマンドログ" not in completion_output
    assert "開始 doctor" not in completion_output
    assert "完了 doctor" not in completion_output
    assert not (root / ".gitignore").exists()
    assert not (root / ".cmoc").exists()


@pytest.mark.parametrize("marker", ["", "complete_bash"])
def test_cli_completion_marker_skips_normal_command(
    monkeypatch: pytest.MonkeyPatch, marker: str
) -> None:
    """補完 marker の値によらず通常の command callback を実行しない。"""
    calls: list[str] = []
    transport_checks: list[str] = []
    monkeypatch.setenv("_CMOC_COMPLETE", marker)
    monkeypatch.setenv("COMP_WORDS", "cmoc doctor")
    monkeypatch.setenv("COMP_CWORD", "1")
    monkeypatch.setattr(main_module, "cmoc_doctor_impl", lambda: calls.append("doctor"))
    monkeypatch.setattr(
        runtime_windows_toast,
        "_powershell_executable",
        lambda: transport_checks.append("checked") or None,
    )

    result = runner.invoke(app, ["doctor"], catch_exceptions=False)

    assert result.exit_code == 0
    assert calls == []
    assert transport_checks == []
    if not marker:
        assert result.output == ""


def test_pre_log_check_failure_writes_subcommand_log(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """pre-log check の失敗時にもサブコマンドログを生成する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    log_dir = root / ".cmoc" / "gu" / "ar" / "log" / "sub_command"
    log_paths_before = set(log_dir.glob("*.jsonl"))
    (root / "README.md").write_text("dirty\n")

    result = runner.invoke(app, ["indexing"])

    assert result.exit_code == 1
    new_logs = set(log_dir.glob("*.jsonl")) - log_paths_before
    assert len(new_logs) == 1
    assert result.stdout == ""
    assert "- 診断用サブコマンドログ:" in result.stderr
    assert "- 終了コード: `1`" in result.stderr
    events = [
        json.loads(line) for line in next(iter(new_logs)).read_text().splitlines()
    ]
    assert events[0]["event"] == "command_invoked"
    assert any(event["event"] == "step_started" for event in events)
    assert events[-1]["event"] == "command_finished"
    assert events[-1]["returncode"] == 1
    assert "indexing" in json.dumps(events[0], ensure_ascii=False)


def test_cli_wrapper_doctor_preprocess_uses_current_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """doctor preprocess は runtime state 保存先ではなく current work root を修復する。"""
    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-test", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    doctor_roots: list[Path] = []
    pre_log_roots: list[Path] = []

    monkeypatch.setattr(runtime_cli, "run_doctor_preprocess", doctor_roots.append)

    runtime_cli.run_cli_subcommand(
        lambda: 0,
        pre_log_check=pre_log_roots.append,
        command_name="probe",
        command_argv=["cmoc", "probe"],
    )

    assert doctor_roots == [linked.resolve()]
    assert pre_log_roots == [root.resolve()]
    # {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
    log_dir = root / ".cmoc" / "gu" / "ar" / "log" / "sub_command"
    assert len(list(log_dir.glob("*.jsonl"))) == 1
    assert not (linked / ".cmoc" / "gu" / "ar" / "log" / "sub_command").exists()
