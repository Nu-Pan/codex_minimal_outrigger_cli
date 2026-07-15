import json
import subprocess
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest
from _codex_support import (
    _override_permission_filesystem,
    codex_override_config,
    codex_parameter,
    setup_codex_home,
    stub_codex_overrides,
)
from _command_support import write_python_executable
from _git_support import make_repo, run_git

import cmoc_runtime
import commons.runtime_codex_tui as runtime_codex_tui
from basic.acp import FileAccessMode
from cmoc_runtime import CmocError, SubcommandLogger
from commons.runtime_codex import run_codex_tui
from commons.runtime_logging import (
    reset_current_subcommand_logger,
    set_current_subcommand_logger,
)
from config.cmoc_config import CmocConfig


def _tui_call_logs(root: Path) -> list[Path]:
    """Return the TUI call logs written for a repository."""
    directory = root / ".cmoc" / "gu" / "ar" / "log" / "codex"
    return list(directory.glob("*_tui_call.json"))


# 根拠: TUI の prompt、アクセス境界、Codex 呼び出し、ログ出力を検証する。
# {{work-root}}/oracle/doc/app_spec/sub_command/tui.md
# {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
# {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
# {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
# docstring の責務記述は {{work-root}}/oracle/doc/dev_rule/coding_rule.md に従う。
def test_run_codex_tui_checks_extra_read_path_before_starting_codex(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """許可領域外の追加読み取りパスでは Codex を起動しないことを確認する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)

    def fail_run(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        """Codex 起動が先行していないことを検出する fake subprocess。"""
        raise AssertionError("Codex subprocess must not start")

    monkeypatch.setattr(cmoc_runtime.subprocess, "run", fail_run)

    with pytest.raises(CmocError, match="許可領域外"):
        run_codex_tui(
            codex_parameter(FileAccessMode.REPO_WRITE),
            root=root,
            extra_read_paths=[root / "memo" / "prompt_cmpl.md"],
            config=CmocConfig(),
        )


def test_run_codex_tui_allows_complete_prompt_for_pure_oracle_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """PURE_ORACLE_READ で完成済み prompt を読み、CLI 引数を制約どおり渡すことを確認する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    prompt_path = root / ".cmoc" / "gu" / "ar" / "log" / "tui" / "20260101_cmpl.md"
    prompt_path.parent.mkdir(parents=True)
    prompt_path.write_text("complete prompt\n")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, os, pathlib, sys",
            "args = sys.argv[1:]",
            "prompt = args[-1]",
            "prompt_path = pathlib.Path(prompt.split(' を読んで')[0])",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps({{",
            "    'args': args,",
            "    'cwd': os.getcwd(),",
            "    'prompt_text': prompt_path.read_text(),",
            "}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    schema_path = tmp_path / "schema.json"
    schema_path.write_text('{"type":"object"}\n')

    run_codex_tui(
        replace(
            codex_parameter(FileAccessMode.PURE_ORACLE_READ),
            prompt=f"{prompt_path} を読んで、その指示に従って下さい",
            structured_output_schema_path=schema_path,
        ),
        root=root,
        extra_read_paths=[prompt_path],
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    assert record["cwd"] == str(root.resolve())
    assert record["prompt_text"] == "complete prompt\n"
    assert record["args"][record["args"].index("--cd") + 1] == str(root.resolve())
    assert "--output-schema" not in record["args"]


def test_run_codex_tui_allows_repo_complete_prompt_from_linked_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree の完成済み prompt と、そのファイルアクセス上書きを維持することを確認する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    linked.parent.mkdir(parents=True)
    run_git(root, "worktree", "add", "-b", "linked-tui-runtime", str(linked), "HEAD")
    prompt_path = root / ".cmoc" / "gu" / "ar" / "log" / "tui" / "20260101_cmpl.md"
    prompt_path.parent.mkdir(parents=True)
    prompt_path.write_text("complete prompt\n")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, os, pathlib, sys",
            "args = sys.argv[1:]",
            "prompt = args[-1]",
            "prompt_path = pathlib.Path(prompt.split(' を読んで')[0])",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps({{",
            "    'args': args,",
            "    'cwd': os.getcwd(),",
            "    'prompt_text': prompt_path.read_text(),",
            "}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_tui(
        replace(
            codex_parameter(FileAccessMode.REPO_WRITE),
            prompt=f"{prompt_path} を読んで、その指示に従って下さい",
        ),
        root=root,
        cwd=linked,
        extra_read_paths=[prompt_path],
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    assert record["cwd"] == str(linked.resolve())
    assert record["prompt_text"] == "complete prompt\n"
    assert record["args"][record["args"].index("--cd") + 1] == str(linked.resolve())
    call_log = _tui_call_logs(root)[0]
    call_data = json.loads(call_log.read_text())
    override_config = codex_override_config(call_data["argv"])
    filesystem = _override_permission_filesystem(call_data["argv"])
    assert override_config["default_permissions"] == "cmoc"
    assert filesystem[str((root / ".cmoc" / "gu" / "ar").resolve())] == "read"
    assert filesystem[str((root / ".cmoc" / "gt" / "ar").resolve())] == "read"
    assert str((root / ".cmoc" / "gu").resolve()) not in filesystem
    assert filesystem[str(linked.resolve())] == "write"
    assert "sandbox_workspace_write" not in override_config
    assert "--profile" not in call_data["argv"]


def test_run_codex_tui_logs_successful_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """正常終了時に TUI の call log、サブコマンドイベント、コンソール要約を残すことを確認する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(bin_dir / "codex", ["import sys", "sys.exit(0)"])
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    logger = SubcommandLogger(root, "test")
    token = set_current_subcommand_logger(logger)
    try:
        result = run_codex_tui(codex_parameter(), root=root, config=CmocConfig())
    finally:
        reset_current_subcommand_logger(token)

    assert result.returncode == 0
    console = capsys.readouterr().out
    assert "- Purpose: `codex tui`" in console
    assert "- Exit code: `0`" in console
    call_logs = _tui_call_logs(root)
    assert len(call_logs) == 1
    events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in events if event["event"] == "codex_call"]
    assert len(codex_events) == 1
    assert codex_events[0]["status"] == "succeeded"
    assert codex_events[0]["returncode"] == 0
    assert codex_events[0]["call_log_path"] == str(call_logs[0])


def test_run_codex_tui_keeps_call_logs_on_timestamp_collision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """同一 timestamp の TUI 呼び出しでも call log を上書きしない。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(bin_dir / "codex", ["import sys", "sys.exit(0)"])
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    timestamps = iter(
        [
            "2026-06-27_10-00_00_000001000",
            "2026-06-27_10-00_00_000001000",
            "2026-06-27_10-00_00_000002000",
        ]
    )
    monkeypatch.setattr(runtime_codex_tui, "timestamp", lambda: next(timestamps))

    run_codex_tui(codex_parameter(), root=root, config=CmocConfig())
    run_codex_tui(codex_parameter(), root=root, config=CmocConfig())

    call_logs = sorted(_tui_call_logs(root))
    assert [path.name for path in call_logs] == [
        "2026-06-27_10-00_00_000001000_tui_call.json",
        "2026-06-27_10-00_00_000002000_tui_call.json",
    ]
    assert [json.loads(path.read_text())["timestamp"] for path in call_logs] == [
        "2026-06-27_10-00_00_000001000",
        "2026-06-27_10-00_00_000002000",
    ]


def test_run_codex_tui_logs_missing_cli_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Codex CLI 不在時に未起動の失敗として各ログへ記録し、エラーを返すことを確認する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    real_run = subprocess.run

    def fake_run(args: list[str], *pos: Any, **kwargs: Any) -> Any:
        """Codex の実行だけを CLI 不在に差し替え、他の subprocess は通す fake。"""
        if args[:1] == ["codex"]:
            raise FileNotFoundError("codex")
        return real_run(args, *pos, **kwargs)

    monkeypatch.setattr(cmoc_runtime.subprocess, "run", fake_run)
    logger = SubcommandLogger(root, "test")
    token = set_current_subcommand_logger(logger)
    try:
        with pytest.raises(CmocError, match="Codex CLI が見つかりません"):
            run_codex_tui(codex_parameter(), root=root, config=CmocConfig())
    finally:
        reset_current_subcommand_logger(token)

    console = capsys.readouterr().out
    call_logs = _tui_call_logs(root)
    assert len(call_logs) == 1
    assert str(call_logs[0]) in console
    assert "not started" in console
    assert "Codex CLI が見つかりません" in console

    events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in events if event["event"] == "codex_call"]
    assert len(codex_events) == 1
    assert codex_events[0]["status"] == "failed"
    assert codex_events[0]["returncode"] is None
    assert codex_events[0]["call_log_path"] == str(call_logs[0])
    assert "Codex CLI が見つかりません" in codex_events[0]["error"]


def test_run_codex_tui_logs_keyboard_interrupt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """KeyboardInterrupt を再送出しつつ、未起動扱いの call log とイベントを残すことを確認する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)

    def interrupt(*_args: object, **_kwargs: object) -> object:
        """Codex subprocess が KeyboardInterrupt を送出する状態を作る fake。"""
        raise KeyboardInterrupt

    monkeypatch.setattr(runtime_codex_tui, "run_codex_subprocess", interrupt)
    logger = SubcommandLogger(root, "test")
    token = set_current_subcommand_logger(logger)
    try:
        with pytest.raises(KeyboardInterrupt):
            run_codex_tui(codex_parameter(), root=root, config=CmocConfig())
    finally:
        reset_current_subcommand_logger(token)

    console = capsys.readouterr().out
    assert "- Exit code: `not started`" in console
    call_logs = _tui_call_logs(root)
    assert len(call_logs) == 1
    events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in events if event["event"] == "codex_call"]
    assert len(codex_events) == 1
    assert codex_events[0]["status"] == "failed"
    assert codex_events[0]["returncode"] is None
    assert codex_events[0]["call_log_path"] == str(call_logs[0])
    assert codex_events[0]["error"] == "KeyboardInterrupt()"


def test_run_codex_tui_fails_when_codex_exits_nonzero(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Codex の非 0 終了を TUI 呼び出し失敗として報告し、call log を保存することを確認する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(bin_dir / "codex", ["import sys", "sys.exit(7)"])
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    logger = SubcommandLogger(root, "test")
    token = set_current_subcommand_logger(logger)
    try:
        with pytest.raises(CmocError, match="Codex CLI/TUI 呼び出しが失敗"):
            run_codex_tui(codex_parameter(), root=root, config=CmocConfig())
    finally:
        reset_current_subcommand_logger(token)

    console = capsys.readouterr().out
    assert "- Purpose: `codex tui`" in console
    assert "- Exit code: `7`" in console
    call_logs = _tui_call_logs(root)
    assert len(call_logs) == 1
    call_log = json.loads(call_logs[0].read_text())
    assert call_log["argv"][:3] == ["codex", "--model", "fake"]
    assert "--profile" not in call_log["argv"]
    assert "profile_name" not in call_log
    assert "profile_path" not in call_log
    events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in events if event["event"] == "codex_call"]
    assert len(codex_events) == 1
    assert codex_events[0]["status"] == "failed"
    assert codex_events[0]["returncode"] == 7
    assert codex_events[0]["call_log_path"] == str(call_logs[0])
