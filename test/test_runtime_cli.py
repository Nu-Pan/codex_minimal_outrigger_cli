"""CLI の error、log、preflight、completion 境界を検証する。

根拠:
- {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
- {{work-root}}/oracle/doc/app_spec/error_handling.md
- {{work-root}}/oracle/doc/app_spec/cli_auto_completion.md
- {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
- {{work-root}}/oracle/doc/app_spec/misc_spec.md
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
from _git_support import make_repo, run_git

import commons.runtime_cli as runtime_cli
import commons.runtime_logging as runtime_logging
import main as main_module
from cmoc_runtime import (
    CmocError,
    SubcommandLogger,
    format_duration,
    render_error,
)
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
    assert "# ERROR" in captured.out
    assert "returncode: 7" in captured.out
    assert "## Call stack" in captured.out
    assert captured.err == ""


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
    assert "# ERROR" in captured.out
    assert "callback failed" in captured.out
    assert captured.err == ""


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
    assert "# ERROR" not in captured.out
    assert "# ERROR" not in captured.err
    [log_path] = (root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert events[-1]["event"] == "command_finished"
    assert events[-1]["returncode"] == 130


def test_render_error_uses_structured_markdown() -> None:
    """CmocError は利用者が読む Markdown report として整形される。"""
    try:
        raise CmocError("summary", ["next"], "detail")
    except CmocError as exc:
        rendered = render_error(exc)

    assert "# ERROR" in rendered
    assert "## Summary\nsummary" in rendered
    assert "- next" in rendered
    next_actions = rendered.split("## Next actions\n", 1)[1].split("## Detail", 1)[0]
    assert sum(line.startswith("- ") for line in next_actions.splitlines()) >= 2
    assert "## Detail\ndetail" in rendered
    assert "## Call stack" in rendered


def test_render_error_fills_empty_next_actions() -> None:
    """next actions 未指定でも回復行動の既定文を出す。"""
    try:
        raise CmocError("summary", [], "detail")
    except CmocError as exc:
        rendered = render_error(exc)

    next_actions = rendered.split("## Next actions\n", 1)[1].split("## Detail", 1)[0]
    assert sum(line.startswith("- ") for line in next_actions.splitlines()) >= 2
    assert "入力、実行場所、設定、作業ツリー状態に問題がある場合" in next_actions
    assert "原因が実装不具合または仕様不足に見える場合" in next_actions


def test_render_error_uses_passed_exception_traceback() -> None:
    """報告対象の例外と現在の例外が異なっても対象の stack を出す。"""
    try:
        raise ValueError("reported error")
    except ValueError as reported:
        try:
            raise RuntimeError("unrelated active error")
        except RuntimeError:
            rendered = render_error(reported)

    assert "ValueError: reported error" in rendered
    assert "RuntimeError: unrelated active error" not in rendered


def test_cli_error_report_is_written_to_stdout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """想定済み CLI error は stderr ではなく stdout report として返す。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    run_git(root, "switch", "--detach", "HEAD")

    result = runner.invoke(app, ["session", "fork"])

    assert result.exit_code != 0
    assert "# ERROR" in result.stdout
    assert "detached HEAD 上では実行できません。" in result.stdout
    assert "# ERROR" not in result.stderr
    assert "detached HEAD 上では実行できません。" not in result.stderr


def test_cli_parse_error_report_is_written_to_stdout() -> None:
    """Click の引数解析 error も cmoc 形式の stdout report に変換する。"""
    result = runner.invoke(app, ["--bad-option"])

    assert result.exit_code != 0
    assert "# ERROR" in result.stdout
    assert "CLI 引数解析に失敗しました。" in result.stdout
    assert "No such option: --bad-option" in result.stdout
    assert "Traceback (most recent call last):" in result.stdout
    assert "main.py" in result.stdout
    assert "# ERROR" not in result.stderr
    assert "CLI 引数解析に失敗しました。" not in result.stderr
    assert "No such option: --bad-option" not in result.stderr


@pytest.mark.parametrize(
    ("argv", "parse_error", "allowed"),
    [
        (
            ["realization", "apply", "fork", "--scope", "bad"],
            "No such option: --scope",
            [],
        ),
        (
            ["oracle", "review", "--scope", "rolling"],
            "Invalid value for '--scope'",
            ["session", "full"],
        ),
    ],
)
def test_scope_options_are_rejected_by_cli_parser(
    argv: list[str], parse_error: str, allowed: list[str]
) -> None:
    """scope の公開値制約はサブコマンド実行前の CLI 解析で拒否する。"""
    result = runner.invoke(app, argv)

    assert result.exit_code != 0
    assert "# ERROR" in result.stdout
    assert "CLI 引数解析に失敗しました。" in result.stdout
    assert parse_error in result.stdout
    if allowed:
        assert argv[-1] in result.stdout
    for value in allowed:
        assert value in result.stdout
    assert "# ERROR" not in result.stderr


def test_cli_requires_current_directory_to_be_work_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """work root 以外からの CLI 実行では副作用を出す前に拒否する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root / "oracle")

    result = runner.invoke(app, ["doctor"])

    assert result.exit_code != 0
    assert "# ERROR" in result.stdout
    assert "cmoc は work root で実行してください。" in result.stdout
    assert "# ERROR" not in result.stderr
    assert "cmoc は work root で実行してください。" not in result.stderr
    assert f"cwd: {(root / 'oracle').resolve()}" in result.stdout
    assert f"work_root: {root.resolve()}" in result.stdout
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
    assert "# ERROR" not in completion_output
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
    monkeypatch.setenv("_CMOC_COMPLETE", marker)
    monkeypatch.setenv("COMP_WORDS", "cmoc doctor")
    monkeypatch.setenv("COMP_CWORD", "1")
    monkeypatch.setattr(main_module, "cmoc_doctor_impl", lambda: calls.append("doctor"))

    result = runner.invoke(app, ["doctor"], catch_exceptions=False)

    assert result.exit_code == 0
    assert calls == []
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
    assert "- サブコマンドログ:" in result.stdout
    assert "- 終了コード: `1`" in result.stdout
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
