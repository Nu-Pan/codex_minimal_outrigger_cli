import json
import shlex
import subprocess
import sys
import threading
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path

import pytest
from _codex_support import (
    codex_arg_value,
    codex_override_config,
    codex_parameter,
    setup_codex_home,
    stub_codex_overrides,
)
from _command_support import write_python_executable
from _git_support import make_repo, run_git
from _handoff_support import handoff_input
from oracle.other.cmoc_config import CodexCallConfig

import cmoc_runtime
import commons.runtime_codex_tui as runtime_codex_tui
from basic.acp import FileAccessMode
from cmoc_runtime import CmocError, SubcommandLogger
from commons.runtime_codex import run_codex_tui
from commons.runtime_editor_input_handoff import start_editor_input_handoff
from commons.runtime_editor_input_handoff_protocol import (
    EDITOR_INPUT_REPOSITORY_ENV,
    EDITOR_INPUT_SOURCE_ENV,
)
from commons.runtime_logging import (
    reset_current_subcommand_logger,
    set_current_subcommand_logger,
)
from config.cmoc_config import CmocConfig


def _tui_call_logs(root: Path) -> list[Path]:
    """repository に書き込まれた TUI call log を返す。"""
    directory = root / ".cmoc" / "gu" / "log" / "codex"
    return list(directory.glob("*_call.json"))


# 根拠: TUI の prompt、アクセス境界、Codex 呼び出し、ログ出力を検証する。
# {{work-root}}/oracle/doc/app_spec/sub_command/tui.md
# {{work-root}}/oracle/src/oracle/prompt_builder/policy/file_access.py
# {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
# {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
# {{work-root}}/oracle/doc/app_spec/windows_toast_notification.md
# docstring の責務記述は {{work-root}}/oracle/doc/dev_rule/coding_rule.md に従う。
def test_run_codex_tui_passes_complete_prompt_for_pure_oracle_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """PURE_ORACLE_READ の完全 prompt 本文と CLI 引数を変更せず渡す。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, os, pathlib, sys",
            "if '--version' in sys.argv[1:]:",
            "    print('codex-cli 0.153.4')",
            "    raise SystemExit(0)",
            "args = sys.argv[1:]",
            "prompt = args[-1]",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps({{",
            "    'args': args,",
            "    'cwd': os.getcwd(),",
            "    'prompt_text': prompt,",
            f"    'handoff_repository': os.environ.get({EDITOR_INPUT_REPOSITORY_ENV!r}),",
            "}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    schema_path = tmp_path / "schema.json"
    schema_path.write_text('{"type":"object"}\n')

    run_codex_tui(
        replace(
            codex_parameter(
                FileAccessMode.PURE_ORACLE_READ,
                agent_call_cwd=root,
            ),
            prompt="complete prompt\n",
            structured_output_schema_path=schema_path,
        ),
        root=root,
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    assert record["cwd"] == str(root.resolve())
    assert record["prompt_text"] == "complete prompt\n"
    assert record["handoff_repository"] is None
    assert record["args"][record["args"].index("--cd") + 1] == str(root.resolve())
    assert record["args"][record["args"].index("--sandbox") + 1] == "read-only"
    override_config = codex_override_config(record["args"])
    assert codex_arg_value(record["args"], "--ask-for-approval") == "on-request"
    assert "--approve-for-me" not in record["args"]
    assert "approval_policy" not in override_config
    assert override_config["approvals_reviewer"] == "auto_review"
    notification_command = override_config["notify"]
    assert isinstance(notification_command, list)
    assert notification_command[0] == sys.executable
    assert Path(notification_command[1]).name == "runtime_windows_toast.py"
    assert notification_command[2] == "codex-tui-callback"
    callback_state_root = Path(notification_command[3])
    assert notification_command[4:] == ["codex tui", root.name]
    assert "features" not in override_config
    assert record["args"][record["args"].index("--enable") + 1] == "hooks"
    hooks = override_config["hooks"]
    assert isinstance(hooks, dict)
    assert "Stop" not in hooks
    assert "SubagentStart" not in hooks
    assert "SubagentStop" not in hooks
    [session_group] = hooks["SessionStart"]
    [session_handler] = session_group["hooks"]
    assert session_handler["type"] == "command"
    assert session_handler["timeout"] == 10
    assert session_handler["async"] is False
    session_start_command = shlex.split(session_handler["command"])
    assert session_start_command[0] == sys.executable
    assert Path(session_start_command[1]).name == "runtime_windows_toast.py"
    assert session_start_command[2] == "codex-tui-session-start-hook"
    assert Path(session_start_command[3]) == callback_state_root
    assert not callback_state_root.exists()
    hook_state = hooks["state"]
    assert list(hook_state) == ["/<session-flags>/config.toml:session_start:0:0"]
    state = hook_state["/<session-flags>/config.toml:session_start:0:0"]
    assert state["enabled"] is True
    assert state["trusted_hash"].startswith("sha256:")
    assert len(state["trusted_hash"]) == 71
    assert override_config["tui"] == {"notifications": False}
    assert "complete prompt" not in "\n".join(notification_command)
    assert "complete prompt" not in "\n".join(session_start_command)
    assert "permissions" not in override_config
    assert "--output-schema" not in record["args"]


def test_run_codex_tui_disables_callbacks_for_unverified_codex_version(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """未検証 Codex では root filter なしの legacy callback を渡さない。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            "if '--version' in sys.argv[1:]:",
            "    print('codex-cli 0.152.0')",
            "    raise SystemExit(0)",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps(sys.argv[1:]))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_tui(
        codex_parameter(FileAccessMode.READONLY, agent_call_cwd=root),
        root=root,
        config=CmocConfig(),
    )

    override_config = codex_override_config(json.loads(recorder.read_text()))
    assert override_config["notify"] == []
    assert "hooks" not in override_config


def test_run_codex_tui_rejects_missing_call_setting_before_version_probe(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """未定義 call の TUI では Codex version probe より先に設定エラーにする。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    probe_calls: list[tuple[object, object]] = []

    def record_version_probe(*args: object, **kwargs: object) -> bool:
        """version probe が設定検証より先に走っていないことを記録する。"""
        probe_calls.append((args, kwargs))
        return False

    monkeypatch.setattr(
        runtime_codex_tui,
        "codex_cli_supports_tui_notification_hooks",
        record_version_probe,
    )
    parameter = replace(
        codex_parameter(FileAccessMode.READONLY, agent_call_cwd=root),
        agent_call_kind="missing_agent_call",
    )

    with pytest.raises(CmocError, match="Codex agent call 設定が未定義"):
        run_codex_tui(parameter, root=root, config=CmocConfig())

    assert probe_calls == []


def test_run_codex_tui_rejects_missing_provider_before_version_probe(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """未定義 provider の TUI でも Codex version probe より先に失敗する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    probe_calls: list[tuple[object, object]] = []

    def record_version_probe(*args: object, **kwargs: object) -> bool:
        """provider 検証前の version probe を記録する。"""
        probe_calls.append((args, kwargs))
        return False

    monkeypatch.setattr(
        runtime_codex_tui,
        "codex_cli_supports_tui_notification_hooks",
        record_version_probe,
    )
    config = CmocConfig()
    config.codex.agent_calls["missing_provider_call"] = CodexCallConfig(
        "missing-provider", "model", "low"
    )
    parameter = replace(
        codex_parameter(FileAccessMode.READONLY, agent_call_cwd=root),
        agent_call_kind="missing_provider_call",
    )

    with pytest.raises(CmocError, match="Codex model provider が未定義"):
        run_codex_tui(parameter, root=root, config=config)

    assert probe_calls == []


def test_run_codex_tui_skips_notification_probe_during_completion(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """シェル補完中は通知設定の Codex version probe を実行しない。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    probe_marker = tmp_path / "notification-probe-called"
    write_python_executable(
        bin_dir / "codex",
        [
            "import pathlib, sys",
            f"probe_marker = pathlib.Path({str(probe_marker)!r})",
            "if '--version' in sys.argv[1:]:",
            "    probe_marker.write_text('called')",
            "    raise SystemExit(0)",
            "raise SystemExit(0)",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    monkeypatch.setenv("_CMOC_COMPLETE", "")

    run_codex_tui(
        codex_parameter(FileAccessMode.READONLY, agent_call_cwd=root),
        root=root,
        config=CmocConfig(),
    )

    assert not probe_marker.exists()


def test_run_codex_tui_passes_repo_complete_prompt_from_linked_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree の完全 prompt 本文とアクセス上書きを維持する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    linked.parent.mkdir(parents=True)
    run_git(root, "worktree", "add", "-b", "linked-tui-runtime", str(linked), "HEAD")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, os, pathlib, sys",
            "args = sys.argv[1:]",
            "prompt = args[-1]",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps({{",
            "    'args': args,",
            "    'cwd': os.getcwd(),",
            "    'prompt_text': prompt,",
            f"    'handoff_repository': os.environ.get({EDITOR_INPUT_REPOSITORY_ENV!r}),",
            "}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_tui(
        replace(
            codex_parameter(FileAccessMode.REPO_WRITE, agent_call_cwd=linked),
            prompt="complete prompt\n",
            enable_editor_input_handoff_mcp=True,
        ),
        root=root,
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    assert record["cwd"] == str(linked.resolve())
    assert record["prompt_text"] == "complete prompt\n"
    assert record["handoff_repository"] == str(root.resolve())
    assert record["args"][record["args"].index("--cd") + 1] == str(linked.resolve())
    call_log = _tui_call_logs(root)[0]
    call_data = json.loads(call_log.read_text())
    override_config = codex_override_config(call_data["argv"])
    assert call_data["argv"][call_data["argv"].index("--sandbox") + 1] == (
        "workspace-write"
    )
    assert "permissions" not in override_config
    assert "default_permissions" not in override_config
    assert "sandbox_workspace_write" not in override_config
    assert "features" not in override_config
    assert "--profile" not in call_data["argv"]


def test_run_codex_tui_logs_successful_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """正常終了時に call log とサブコマンドイベントだけを残す。"""
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
        result = run_codex_tui(
            codex_parameter(agent_call_cwd=root), root=root, config=CmocConfig()
        )
    finally:
        reset_current_subcommand_logger(token)

    assert result.returncode == 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
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

    run_codex_tui(codex_parameter(agent_call_cwd=root), root=root, config=CmocConfig())
    run_codex_tui(codex_parameter(agent_call_cwd=root), root=root, config=CmocConfig())

    call_logs = sorted(_tui_call_logs(root))
    assert [path.name for path in call_logs] == [
        "2026-06-27_10-00_00_000001000_call.json",
        "2026-06-27_10-00_00_000002000_call.json",
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
    real_popen: Callable[..., object] = subprocess.Popen

    def fake_popen(args: list[str], *pos: object, **kwargs: object) -> object:
        """Codex の実行だけを CLI 不在に差し替え、他の subprocess は通す fake。"""
        if args[:1] == ["codex"]:
            raise FileNotFoundError("codex")
        return real_popen(args, *pos, **kwargs)

    monkeypatch.setattr(cmoc_runtime.subprocess, "Popen", fake_popen)
    logger = SubcommandLogger(root, "test")
    token = set_current_subcommand_logger(logger)
    try:
        with pytest.raises(CmocError, match="Codex CLI が見つかりません"):
            run_codex_tui(
                codex_parameter(agent_call_cwd=root),
                root=root,
                config=CmocConfig(),
            )
    finally:
        reset_current_subcommand_logger(token)

    captured = capsys.readouterr()
    call_logs = _tui_call_logs(root)
    assert len(call_logs) == 1
    assert captured.out == ""
    assert captured.err == ""

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
            run_codex_tui(
                codex_parameter(agent_call_cwd=root),
                root=root,
                config=CmocConfig(),
            )
    finally:
        reset_current_subcommand_logger(token)

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
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
            run_codex_tui(
                codex_parameter(agent_call_cwd=root),
                root=root,
                config=CmocConfig(),
            )
    finally:
        reset_current_subcommand_logger(token)

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
    call_logs = _tui_call_logs(root)
    assert len(call_logs) == 1
    call_log = json.loads(call_logs[0].read_text())
    assert call_log["argv"][:3] == [
        "codex",
        "--ask-for-approval",
        "on-request",
    ]
    assert "--profile" not in call_log["argv"]
    assert "profile_name" not in call_log
    assert "profile_path" not in call_log
    events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in events if event["event"] == "codex_call"]
    assert len(codex_events) == 1
    assert codex_events[0]["status"] == "failed"
    assert codex_events[0]["returncode"] == 7
    assert codex_events[0]["call_log_path"] == str(call_logs[0])


def test_concurrent_tui_sources_reach_mcp_with_flushed_call_mapping(
    tmp_path, monkeypatch
):
    """並行する TUI の MCP が自身の起動前ログと一致する送信元を保持する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    monkeypatch.setenv(EDITOR_INPUT_SOURCE_ENV, "stale-parent-source")
    monkeypatch.setattr(
        runtime_codex_tui,
        "codex_cli_supports_tui_notification_hooks",
        lambda *_args: False,
    )
    barrier = threading.Barrier(2)
    loggers = {
        name: SubcommandLogger(root, name) for name in ("tui", "oracle investigation")
    }
    observed = {}

    def run_process(argv, **kwargs):
        source = json.loads(kwargs["env"][EDITOR_INPUT_SOURCE_ENV])
        logger = loggers[source["subcommand"]]
        assert source["execution_id"] == logger.invocation_id
        assert source["sub_command_log_path"] == str(logger.path.resolve())
        events = [json.loads(line) for line in logger.path.read_text().splitlines()]
        event = next(
            item for item in events if item["event"] == "editor_input_handoff_source"
        )
        assert {key: event[key] for key in source} == source
        call = json.loads(Path(event["call_log_path"]).read_text())
        assert call["codex_call_id"] == source["codex_call_id"]
        assert source["codex_call_id"] != "cdc_indexing"
        assert argv[-1] == "unchanged prompt"
        assert all(
            source[key] not in argv[-1]
            for key in ("execution_id", "codex_call_id", "sub_command_log_path")
        )
        # 両起動が context を確定するまで待ち、別 process の stdio MCP へ渡す。
        barrier.wait(timeout=5)
        work = root / ".cmoc/gu/editor_input" / (source["codex_call_id"] + ".md")
        work.parent.mkdir(parents=True, exist_ok=True)
        work.write_text("initial")
        target = start_editor_input_handoff(root, work, "{{original-prompt-here}}")
        try:
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "overwrite",
                    "arguments": handoff_input(target.target_id, "request context"),
                },
            }
            requests = (json.dumps(request) + "\n") * 2
            server = codex_override_config(argv)["mcp_servers"]["cmoc_editor_input"]
            result = subprocess.run(
                [server["command"], *server["args"]],
                cwd=root,
                env={
                    "PATH": kwargs["env"]["PATH"],
                    "PYTHONDONTWRITEBYTECODE": "1",
                    **{name: kwargs["env"][name] for name in server["env_vars"]},
                    **server["env"],
                },
                input=requests,
                text=True,
                capture_output=True,
                timeout=10,
                check=True,
            )
            responses = [json.loads(line) for line in result.stdout.splitlines()]
            assert len(responses) == 2
            assert all(
                item["result"]["structuredContent"] == {"status": "accepted"}
                for item in responses
            )
            assert "request context" not in result.stdout + result.stderr
            body = work.read_text()
            for key in (
                "subcommand",
                "execution_id",
                "codex_call_id",
                "sub_command_log_path",
            ):
                assert source[key] in body
            observed[source["subcommand"]] = source
        finally:
            target.close()
        return subprocess.CompletedProcess(argv, 0)

    monkeypatch.setattr(runtime_codex_tui, "run_codex_subprocess", run_process)

    def launch(name):
        logger = loggers[name]
        token = set_current_subcommand_logger(logger)
        try:
            logger.event("codex_call", codex_call_id="cdc_indexing")
            return run_codex_tui(
                replace(
                    codex_parameter(FileAccessMode.READONLY, agent_call_cwd=root),
                    prompt="unchanged prompt",
                    enable_editor_input_handoff_mcp=True,
                ),
                root=root,
                config=CmocConfig(),
                purpose=name,
            )
        finally:
            reset_current_subcommand_logger(token)

    with ThreadPoolExecutor(max_workers=2) as pool:
        assert all(result.returncode == 0 for result in pool.map(launch, loggers))
    assert len({source["codex_call_id"] for source in observed.values()}) == 2
    for name, source in observed.items():
        completed = loggers[name].codex_call_records()[-1]
        assert completed["codex_call_id"] == source["codex_call_id"]
