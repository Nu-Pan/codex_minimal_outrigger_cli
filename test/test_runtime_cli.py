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
import os
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import pytest
import typer
from _cli_support import runner, terminal_primary_report
from _git_support import run_git

import commons.runtime_cli as runtime_cli
import commons.runtime_feedback as runtime_feedback
import commons.runtime_logging as runtime_logging
import commons.runtime_paths as runtime_paths
import commons.runtime_windows_toast as runtime_windows_toast
import main as main_module
from cmoc_runtime import (
    CmocError,
    SubcommandLogger,
    TerminalResult,
    format_duration,
    render_error,
)
from commons.runtime_errors import TuiStartupCancelled
from commons.runtime_ids import is_common_id
from main import app


@pytest.fixture(autouse=True)
def _clear_completion_probe_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """通常の in-process CLI test を外部の completion probe 環境から分離する。"""
    # {{work-root}}/oracle/doc/app_spec/cli_auto_completion.md
    monkeypatch.delenv("_CMOC_COMPLETE", raising=False)


@pytest.fixture
def _without_feedback_collector(monkeypatch: pytest.MonkeyPatch) -> None:
    """実 Git を使う CLI 境界の検査でも、観測しない collector を起動しない。"""
    # collector の TCP 受付・保存・drain は test_feedback.py に残す。
    monkeypatch.setattr(
        runtime_cli, "start_feedback_invocation", lambda *_args: (None, None)
    )


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


def test_timestamp_zero_pads_year_and_fraction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """timestamp の年とミリ秒部分を仕様どおり固定幅で生成する。"""

    class FixedDateTime:
        @classmethod
        def now(cls) -> datetime:
            return datetime(1, 2, 3, 4, 5, 6, 7)

    monkeypatch.setattr(runtime_paths, "datetime", FixedDateTime)

    assert runtime_paths.timestamp() == "0001-02-03_04-05-06_000"


def test_subcommand_logger_keeps_one_file_per_execution(
    tmp_path: Path,
) -> None:
    """実行ごとの ID と診断ログ path が一致して重複しない。"""

    first = SubcommandLogger(tmp_path, "first")
    second = SubcommandLogger(tmp_path, "second")
    first.event("marker")
    second.event("marker")

    assert is_common_id(first.execution_id, "exec")
    assert is_common_id(second.execution_id, "exec")
    assert first.execution_id < second.execution_id
    assert first.path.name == f"{first.execution_id}.jsonl"
    assert second.path.name == f"{second.execution_id}.jsonl"
    assert [line for line in first.path.read_text().splitlines() if line]
    assert [line for line in second.path.read_text().splitlines() if line]


def test_subcommand_logger_handles_parallel_worker_events_and_quota_wait(
    tmp_path: Path,
    nonpersistent_execution_ids: None,
) -> None:
    """並列記録の保存順・待機時間と、呼び出し別 snapshot の独立性を保つ。"""
    # 実採番との結合は直前の test に残し、追記の検査では SQLite を準備しない。
    logger = SubcommandLogger(tmp_path, "parallel_logging")
    worker_count = 8
    barrier = threading.Barrier(worker_count)
    assert logger.event_records() == ()
    assert logger.codex_call_records() == ()

    def record_worker_event(index: int) -> None:
        """共有 logger への並列書き込みを再現する。"""
        barrier.wait()
        logger.add_recovery_wait("quota", 0.25)
        logger.event("codex_call" if index % 2 else "worker", index=index)

    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        list(executor.map(record_worker_event, range(worker_count)))

    events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    assert len(events) == worker_count
    assert all(
        event["event"] == ("codex_call" if event["index"] % 2 else "worker")
        for event in events
    )
    assert sorted(event["index"] for event in events) == list(range(worker_count))
    assert logger.quota_wait_sec == pytest.approx(worker_count * 0.25)

    snapshot = logger.event_records()
    calls = logger.codex_call_records()
    expected_calls = tuple(event for event in events if event["event"] == "codex_call")
    assert snapshot == tuple(events)
    assert calls == expected_calls

    snapshot[0]["index"] = -1
    calls[0]["index"] = -1
    assert logger.event_records() == tuple(events)
    assert logger.codex_call_records() == expected_calls

    logger.event("codex_call", index=worker_count)
    assert len(calls) == worker_count // 2
    assert logger.codex_call_records() == (
        *expected_calls,
        logger.event_records()[-1],
    )


def test_subcommand_logger_writes_utf8_without_locale_dependency(
    tmp_path: Path,
) -> None:
    """ASCII locale でも日本語を含む JSON Lines event を保存する。"""
    # 実採番との結合は専用 test に残し、子では実ログ保存と locale の境界を検査する。
    # 標準ライブラリだけで起動し、不要な site 初期化と SQLite の準備を省く。
    source_root = Path(__file__).resolve().parents[1]
    # 子 process の cwd を test root とし、別の一時 directory を作らない。
    script = r"""
from pathlib import Path

import commons.runtime_logging as runtime_logging

runtime_logging.new_id = lambda _root, prefix: f"{prefix}_000000_2000-01-01_00-00"
logger = runtime_logging.SubcommandLogger(Path.cwd(), "probe")
logger.event("warning", message="\u65e5\u672c\u8a9e warning")
"""
    result = subprocess.run(
        [sys.executable, "-S", "-c", script],
        cwd=tmp_path,
        env={
            **os.environ,
            "LC_ALL": "C",
            "PYTHONCOERCECLOCALE": "0",
            "PYTHONUTF8": "0",
            "PYTHONPATH": os.pathsep.join(
                [str(source_root / "src"), str(source_root / "oracle" / "src")]
            ),
        },
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    [log_path] = (tmp_path / ".cmoc/gu/log/sub_command").glob("*.jsonl")
    events = [
        json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()
    ]
    assert events[0]["message"] == "日本語 warning"


def test_noninteractive_success_emits_one_terminal_result_after_progress(
    cli_terminal_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """stdout を成功 terminal result だけにし、詳細 step はログへ閉じる。"""
    # {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
    root = cli_terminal_directory
    report_path = root / "report.md"
    report_path.write_text("# report\n")

    def completion_counts(repository: Path) -> tuple[int, list[str]]:
        """検証済みの件数・warning を正しい repository の終端処理へ渡す。"""
        assert repository == root
        return 123, ["feedback warning"]

    monkeypatch.setattr(runtime_cli, "feedback_completion_counts", completion_counts)

    def succeed() -> TerminalResult:
        """トップレベルと内部 step を含む成功結果を返す。"""
        runtime_cli.start_subcommand_step(1, "top level", "top level")
        runtime_cli.start_subcommand_step(
            "1/1, 1/1", "nested", "nested log description"
        )
        return TerminalResult(
            primary_report=report_path,
            primary_report_role="probe report",
            result="attention",
            details=(
                ("target", Path("input.json")),
                ("count", 2),
                ("changed", True),
                ("unavailable", None),
                ("detail", "first\n`日本語`\ud800"),
            ),
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
    assert stdout_lines[3:9] == [
        f"- target: `{root / 'input.json'}`",
        "- count: `2`",
        "- changed: `True`",
        "- unavailable: `None`",
        "- detail: `first | '日本語'\\ud800`",
        "- 次の操作: report を確認してください。",
    ]
    assert captured.out.count("# 完了: cmoc probe") == 1
    assert captured.out.count(str(report_path.resolve())) == 1
    assert "- pending feedback observation: `123`" in captured.out
    assert captured.out.count("- warning: feedback warning") == 1
    assert "cmoc probe を開始" in captured.err
    assert "cmoc probe: top level" in captured.err
    assert "nested" not in captured.err

    [log_path] = (root / ".cmoc" / "gu" / "log" / "sub_command").glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert events[-1]["event"] == "command_finished"
    assert events[-1]["classification"] == "natural_completion"
    assert events[-1]["returncode"] == 0
    assert events[-1]["pending_feedback_observation_count"] == 123
    assert events[-1]["warnings"] == ["feedback warning"]
    assert events[-1]["terminal_result"]["pending_feedback_observation_count"] == 123
    assert events[-1]["terminal_result"]["warnings"] == ["feedback warning"]
    assert events[-1]["terminal_result"]["result"] == "attention"
    assert events[-1]["terminal_result"]["details"] == [
        {"name": "target", "value": str(root / "input.json")},
        {"name": "count", "value": 2},
        {"name": "changed", "value": True},
        {"name": "unavailable", "value": None},
        {"name": "detail", "value": "first\n`日本語`\\ud800"},
    ]
    nested_steps = [
        event["step"]
        for event in events
        if event.get("event") in {"step_started", "step_finished"}
        and event.get("step_index") == "1/1, 1/1"
    ]
    assert nested_steps == ["nested log description", "nested log description"]


def test_internal_failure_traceback_is_logged_but_not_printed(
    cli_terminal_directory: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """surrogate を含む内部障害も、stack を診断ログだけに保存して終了する。"""
    # {{work-root}}/oracle/doc/app_spec/error_handling.md
    root = cli_terminal_directory

    def fail() -> None:
        raise ValueError("unexpected failure\ud800")

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
    assert "unexpected failure\\ud800" in captured.err
    assert "Traceback" not in captured.err
    [log_path] = (root / ".cmoc" / "gu" / "log" / "sub_command").glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert events[-1]["event"] == "command_finished"
    failure = events[-1]["failure"]
    assert failure["classification"] == "internal_failure"
    assert "Traceback" in failure["traceback"]
    # UTF-8 の JSON Lines を decode した診断値には、元の surrogate を保持する。
    assert "ValueError: unexpected failure\ud800" in failure["traceback"]


def test_error_terminal_result_does_not_repeat_primary_report_path(
    cli_terminal_directory: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """error detail 内の primary report path は console で重複させない。"""
    root = cli_terminal_directory
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

    [log_path] = (root / ".cmoc" / "gu" / "log" / "sub_command").glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert str(report_path) in events[-1]["failure"]["detail"]


def test_detector_does_not_swallow_keyboard_interrupt(
    cli_terminal_directory: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """detector 中の Ctrl+C を本命サブコマンドの中断として扱う。"""
    # detector を差し替えるため、実 Git と TCP collector は準備しない。
    root = cli_terminal_directory

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
            subcommand_invocation_id=logger.execution_id,
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

    [log_path] = (root / ".cmoc" / "gu" / "log" / "sub_command").glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert not any(event["event"] == "feedback.detector_failed" for event in events)


def test_cli_wrapper_doctor_preprocess_failure_writes_subcommand_log(
    cli_terminal_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """doctor preprocess の失敗でも report を保存し、終了結果を確定する。"""
    root = cli_terminal_directory

    def fail_doctor(_root: Path) -> None:
        """doctor preprocess の失敗を再現する fake。

        根拠: {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
        """
        raise CmocError("doctor failed", ["fix doctor"], "doctor detail")

    monkeypatch.setattr(runtime_cli, "run_doctor_preprocess", fail_doctor)

    def precondition_must_not_start(_root: Path) -> None:
        pytest.fail("precondition must not start after doctor failure")

    with pytest.raises(typer.Exit) as exc_info:
        runtime_cli.run_cli_subcommand(
            lambda: pytest.fail("implementation must not start after doctor failure"),
            pre_log_check=precondition_must_not_start,
            command_name="doctor",
            command_argv=["cmoc", "doctor"],
        )

    assert exc_info.value.exit_code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    report_path = terminal_primary_report(captured.err)
    assert report_path.parent == root / ".cmoc/gu/report/doctor"
    assert captured.err.count(str(report_path)) == 1
    rendered = report_path.read_text(encoding="utf-8")
    assert 'terminal_classification: "error"' in rendered
    assert "exit_code: 1" in rendered
    assert "- 検査と修復: `error`" in rendered
    assert "doctor failed" in rendered
    assert "doctor detail" in rendered
    [log_path] = (root / ".cmoc" / "gu" / "log" / "sub_command").glob("*.jsonl")
    assert report_path.stem == log_path.stem
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert events[0]["event"] == "command_invoked"
    assert any(event["event"] == "step_started" for event in events)
    assert events[-1]["event"] == "command_finished"
    assert events[-1]["returncode"] == 1
    assert events[-1]["classification"] == "error"
    assert events[-1]["primary_report_path"] == str(report_path)
    assert events[0]["argv"] == ["cmoc", "doctor"]
    assert "doctor failed" in json.dumps(events[-1], ensure_ascii=False)
    assert events[-1]["failure"]["classification"] == "handled_failure"
    assert "traceback" not in events[-1]["failure"]


def test_cli_error_report_survives_failed_error_log_flush(
    cli_terminal_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """終了ログの失敗が元の error report を隠さないことを検証する。"""
    root = cli_terminal_directory
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
    [log_path] = (root / ".cmoc" / "gu" / "log" / "sub_command").glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert events[-1]["event"] == "command_finished"
    failure = events[-1]["failure"]
    assert failure["classification"] == "internal_failure"
    assert "Traceback" in failure["traceback"]
    assert "ValueError: callback failed" in failure["traceback"]


def test_cli_wrapper_does_not_convert_keyboard_interrupt_to_error_report(
    cli_terminal_directory: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Codex CLI へ委ねる Ctrl+C を cmoc の error report に変換しない。"""
    root = cli_terminal_directory

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
    [log_path] = (root / ".cmoc" / "gu" / "log" / "sub_command").glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert events[-1]["event"] == "command_finished"
    assert events[-1]["returncode"] == 130


def test_cli_tui_keyboard_interrupt_does_not_emit_terminal_result_notification(
    cli_terminal_directory: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """TUI の Ctrl+C は Codex CLI に委ね、終了 toast を追加しない。"""
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


def test_cli_tui_initial_cancel_reports_incomplete_work(
    cli_terminal_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """初回の取消を、部分成果による正常完了や TUI 終了と区別する。"""
    root = cli_terminal_directory
    notifications: list[str] = []
    monkeypatch.setattr(
        runtime_cli,
        "notify_terminal_result",
        lambda _command, _repository, state: notifications.append(state),
    )

    def cancel() -> None:
        raise TuiStartupCancelled()

    with pytest.raises(typer.Exit) as error:
        runtime_cli.run_cli_subcommand(
            cancel,
            command_name="tui",
            command_argv=["cmoc", "tui"],
            doctor_preprocess=False,
            tui_process=True,
        )

    assert error.value.exit_code == 130
    assert notifications == ["cancelled"]
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "初回作業は未完了" in captured.err
    assert "# 完了:" not in captured.err
    assert "primary report" not in captured.err
    [log_path] = (root / ".cmoc/gu/log/sub_command").glob("*.jsonl")
    records = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert records[-1]["event"] == "command_finished"
    assert records[-1]["result"] == "tui_startup_cancelled"
    assert records[-1]["returncode"] == 130


def test_cli_tui_success_does_not_emit_terminal_result_notification(
    cli_terminal_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """TUI 正常終了時には terminal result の表示と通知を追加しない。"""
    notifications: list[str] = []
    monkeypatch.setattr(
        runtime_cli,
        "notify_terminal_result",
        lambda _command, _repository, state: notifications.append(state),
    )

    runtime_cli.run_cli_subcommand(
        lambda: None,
        command_name="probe",
        command_argv=["cmoc", "probe"],
        doctor_preprocess=False,
        tui_process=True,
    )

    captured = capsys.readouterr()
    assert notifications == []
    assert captured.out == ""
    assert "# 完了: cmoc probe" not in captured.err


@pytest.mark.parametrize("tui_process", [False, True])
def test_cli_nonzero_impl_result_is_reported_and_notified(
    cli_terminal_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tui_process: bool,
) -> None:
    """非0 return の失敗表示・終了コードと、非対話/TUI の単発通知を検証する。"""
    root = cli_terminal_directory
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

    captured = capsys.readouterr()
    assert exc_info.value.exit_code == 7
    assert captured.out == ""
    assert "# 失敗: cmoc probe" in captured.err
    assert "returncode: 7" in captured.err
    assert "Traceback" not in captured.err
    assert "- 終了コード: `7`" in captured.err
    assert calls == [("probe", root, "failed")]


def test_cli_terminal_notification_distinguishes_user_interruption(
    cli_terminal_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """正常に確定したユーザー中断を自然完了やエラーとして通知しない。"""
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
    cli_terminal_directory: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """interruptible command の common preprocess 中断を正常完了として扱う。"""
    # {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
    root = cli_terminal_directory
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
    [log_path] = (root / ".cmoc" / "gu" / "log" / "sub_command").glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert events[-1]["event"] == "command_finished"
    assert events[-1]["returncode"] == 0
    assert events[-1]["classification"] == "user_interruption"
    assert events[-1]["terminal_result"]["classification"] == "user_interruption"


def test_cli_notification_failure_does_not_change_terminal_result(
    cli_terminal_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """終了 log と cleanup 後に成功を一度通知し、通知失敗を結果へ逆流させない。"""
    root = cli_terminal_directory
    calls: list[tuple[str, Path, str]] = []

    def fail_notification(command: str, repository: Path, state: str) -> None:
        """確定・cleanup 済みの通知境界から想定外例外を再現する。"""
        assert runtime_cli.current_subcommand_logger() is None
        [log_path] = (root / ".cmoc" / "gu" / "log" / "sub_command").glob("*.jsonl")
        events = [json.loads(line) for line in log_path.read_text().splitlines()]
        assert events[-1]["event"] == "command_finished"
        calls.append((command, repository, state))
        raise RuntimeError("toast failed")

    monkeypatch.setattr(runtime_cli, "notify_terminal_result", fail_notification)

    runtime_cli.run_cli_subcommand(
        lambda: None,
        command_name="probe",
        command_argv=["cmoc", "probe"],
        doctor_preprocess=False,
    )

    assert calls == [("probe", root, "completed")]
    captured = capsys.readouterr()
    assert "# 完了: cmoc probe" in captured.out


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
    committed_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    _without_feedback_collector: None,
) -> None:
    """想定済み CLI error は簡潔な terminal result を stderr に返す。"""
    root = committed_repository
    monkeypatch.chdir(root)
    # doctor 修復と collector の TCP lifecycle は専用 test に残し、
    # 実 Git の detached HEAD 検出から CLI の stderr・終了コードまでを通す。
    doctor_roots: list[Path] = []
    monkeypatch.setattr(runtime_cli, "run_doctor_preprocess", doctor_roots.append)
    run_git(root, "switch", "--detach", "HEAD")

    result = runner.invoke(app, ["session", "fork"])

    assert result.exit_code != 0
    assert doctor_roots == [root]
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
    cli_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    _without_feedback_collector: None,
) -> None:
    """work root 以外からの CLI 実行では副作用を出す前に拒否する。"""
    root = cli_repository
    (root / "oracle").mkdir()
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
    """補完は Git のない cwd でも command runtime を読み込まず動作する。"""
    root = tmp_path / "repo"
    root.mkdir()
    isolated_home = tmp_path / "home"
    isolated_home.mkdir()
    main_path = Path(main_module.__file__).resolve()
    # 独立 process で import の遅延を検証し、pytest の読み込み済み module に依存しない。
    script = """
import runpy
import sys

def reject_command_runtime(event, arguments):
    if event == "import" and arguments[0].split(".", 1)[0] in {
        "cmoc_runtime", "sub_commands", "acp", "oracle"
    }:
        raise AssertionError(f"completion loaded command runtime: {arguments[0]}")

sys.addaudithook(reject_command_runtime)
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
"""
    result = subprocess.run(
        [sys.executable, "-c", script, str(main_path), "doctor"],
        cwd=root,
        env={
            "PYTHONPATH": str(main_path.parent),
            "_CMOC_COMPLETE": "complete_bash",
            "COMP_WORDS": "cmoc doctor",
            "COMP_CWORD": "1",
            "HOME": str(isolated_home),
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONDEVMODE": "1",
            "PYTHONWARNINGS": "error::ResourceWarning",
        },
        text=True,
        capture_output=True,
        check=False,
    )

    completion_output = result.stdout + result.stderr
    # {{work-root}}/oracle/doc/app_spec/cli_auto_completion.md
    assert result.returncode == 0, completion_output
    assert "doctor" in result.stdout
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
    import sub_commands.doctor as doctor_module

    calls: list[str] = []
    transport_checks: list[str] = []
    monkeypatch.setenv("_CMOC_COMPLETE", marker)
    monkeypatch.setenv("COMP_WORDS", "cmoc doctor")
    monkeypatch.setenv("COMP_CWORD", "1")
    monkeypatch.setattr(
        doctor_module, "cmoc_doctor_impl", lambda: calls.append("doctor")
    )
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
    cli_terminal_directory: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """pre-log check の失敗時にもサブコマンドログを生成する。"""
    import sub_commands.session.fork as session_fork

    root = cli_terminal_directory
    log_dir = root / ".cmoc" / "gu" / "log" / "sub_command"
    doctor_roots: list[Path] = []
    # doctor 修復は専用 test で検証し、ここでは CLI dispatch と失敗時のログを通す。
    monkeypatch.setattr(runtime_cli, "run_doctor_preprocess", doctor_roots.append)

    def fail_pre_log_check(checked_root: Path) -> None:
        assert checked_root == root
        raise CmocError("pre-log check failed", ["修復して再実行してください。"], "")

    monkeypatch.setattr(
        session_fork, "ensure_cmoc_ignored_in_exclude", fail_pre_log_check
    )
    result = runner.invoke(app, ["session", "fork"])

    assert result.exit_code == 1
    assert doctor_roots == [root]
    [log_path] = log_dir.glob("*.jsonl")
    assert result.stdout == ""
    assert "- 診断用サブコマンドログ:" in result.stderr
    assert "- 終了コード: `1`" in result.stderr
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert events[0]["event"] == "command_invoked"
    assert any(event["event"] == "step_started" for event in events)
    assert events[-1]["event"] == "command_finished"
    assert events[-1]["returncode"] == 1
    assert "pre-log check failed" in result.stderr
    assert events[0]["argv"] == ["cmoc", "session", "fork"]


def test_cli_wrapper_doctor_preprocess_uses_current_worktree(
    committed_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
    _without_feedback_collector: None,
) -> None:
    """共通前処理と明示 doctor の対象 worktree・root 探索の再利用範囲を確認する。"""
    import sub_commands.doctor as doctor_command

    root = committed_repository
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-test", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    doctor_roots: list[Path] = []
    pre_log_roots: list[Path] = []
    root_queries = 0
    original_run = subprocess.run

    def record_root_query(argv, *args, **kwargs):
        nonlocal root_queries
        if argv[0] == "git" and "--show-toplevel" in argv:
            root_queries += 1
        return original_run(argv, *args, **kwargs)

    monkeypatch.setattr(subprocess, "run", record_root_query)
    monkeypatch.setattr(runtime_cli, "run_doctor_preprocess", doctor_roots.append)

    runtime_cli.run_cli_subcommand(
        lambda: 0,
        pre_log_check=pre_log_roots.append,
        command_name="probe",
        command_argv=["cmoc", "probe"],
    )

    assert doctor_roots == [linked.resolve()]
    assert pre_log_roots == [root.resolve()]
    # 開始時の work root と通知先 repo root は同じ metadata 問い合わせから導出する。
    assert root_queries == 1
    # {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
    log_dir = root / ".cmoc" / "gu" / "log" / "sub_command"
    assert len(list(log_dir.glob("*.jsonl"))) == 1
    assert not (linked / ".cmoc" / "gu" / "log" / "sub_command").exists()

    explicit_doctor_roots: list[Path] = []

    def record_explicit_doctor(work: Path, *, explicit_doctor: bool) -> None:
        assert explicit_doctor is True
        explicit_doctor_roots.append(work)
        # 修復処理へ探索結果を持ち越さず、前処理は現在の metadata を読み直す。
        before_preprocess = root_queries
        assert runtime_paths.work_root() == work
        assert root_queries == before_preprocess + 1

    monkeypatch.setattr(doctor_command, "run_doctor_preprocess", record_explicit_doctor)
    # 既存の linked metadata を共用し、次の main 起動へ root を持ち越さない。
    for work in (linked, root):
        monkeypatch.chdir(work)
        root_queries = 0
        result = runner.invoke(app, ["doctor"], catch_exceptions=False)
        assert result.exit_code == 0, result.output
        assert explicit_doctor_roots[-1] == work.resolve()
        # wrapper、本体の両 root、前処理の再確認が、それぞれ一度だけ探索する。
        assert root_queries == 3
        assert terminal_primary_report(result).parent == root / ".cmoc/gu/report/doctor"

    assert doctor_roots == [linked.resolve()]
    assert explicit_doctor_roots == [linked.resolve(), root.resolve()]
    assert len(list(log_dir.glob("*.jsonl"))) == 3
    assert not (linked / ".cmoc" / "gu" / "log" / "sub_command").exists()
