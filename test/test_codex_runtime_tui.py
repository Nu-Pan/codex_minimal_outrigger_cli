"""TUI の初回 exec、保存記録、取消と公開 resume の制御を検証する。"""

import json
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from contextvars import copy_context
from dataclasses import replace
from pathlib import Path
from unittest.mock import Mock

import oracle.other.path_model as path_model_module
import pytest
import typer
from _codex_support import codex_arg_value, codex_override_config, setup_codex_home
from _command_support import write_python_executable
from _handoff_support import handoff_input
from oracle.acp_builder.oracle.investigation.launch_tui import (
    build_oracle_investigation_launch_tui_parameter,
)
from oracle.acp_builder.tui.launch_tui import build_tui_launch_tui_parameter
from oracle.other.cmoc_config import CodexCallConfig

import commons.runtime_cli as runtime_cli
import commons.runtime_codex_exec as exec_module
import commons.runtime_codex_tui as tui_module
from commons.runtime_codex_profile import process_group_has_running_member
from commons.runtime_codex_recovery import install_recovery_interruption
from commons.runtime_config import write_config
from commons.runtime_editor_input_handoff import start_editor_input_handoff
from commons.runtime_editor_input_handoff_protocol import EDITOR_INPUT_SOURCE_ENV
from commons.runtime_errors import CmocError, TuiStartupCancelled
from commons.runtime_logging import (
    SubcommandLogger,
    reset_current_subcommand_logger,
    set_current_subcommand_logger,
)
from commons.runtime_paths import logs_dir
from commons.runtime_results import CommandResult
from config.cmoc_config import CmocConfig

SESSION_ID = "019efe07-4886-7423-b252-625febbe31eb"
SUCCESS = (
    json.dumps({"type": "thread.started", "thread_id": SESSION_ID})
    + "\n"
    + json.dumps({"type": "turn.completed"})
    + "\n"
)
BUILDERS = [
    pytest.param(build_tui_launch_tui_parameter, "tui", id="tui"),
    pytest.param(
        build_oracle_investigation_launch_tui_parameter,
        "oracle investigation",
        id="investigation",
    ),
]


@pytest.fixture
def directory(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    setup_codex_home(tmp_path, monkeypatch)
    monkeypatch.chdir(root)
    monkeypatch.delenv("_CMOC_COMPLETE", raising=False)
    monkeypatch.setattr(
        path_model_module, "_resolve_git_worktree_roots", lambda _cwd=None: (root, root)
    )
    monkeypatch.setattr(
        runtime_cli, "start_feedback_invocation", lambda *_args: (None, None)
    )
    monkeypatch.setattr(runtime_cli, "run_doctor_preprocess", lambda _root: None)
    write_config(root / ".cmoc/gt/config.json", CmocConfig())
    return root


@contextmanager
def call_log(root, command="tui"):
    logger = SubcommandLogger(root, command)
    token = set_current_subcommand_logger(logger)
    try:
        yield logger
    finally:
        reset_current_subcommand_logger(token)


def events(logger):
    return [json.loads(line) for line in logger.path.read_text().splitlines()]


def fake_initial(
    monkeypatch, *, stdout=SUCCESS, returncode=0, output="initial answer", on_call=None
):
    calls = []

    def run(argv, **kwargs):
        kwargs["process_started_callback"]()
        prompt = kwargs["stdin"].read()
        calls.append({"argv": argv, "prompt": prompt, "env": kwargs["env"]})
        kwargs["stdout"].write(stdout)
        kwargs["stderr"].write("diagnostic only")
        if output is not None:
            Path(codex_arg_value(argv, "--output-last-message")).write_text(output)
        if on_call is not None:
            on_call(calls[-1])
        return subprocess.CompletedProcess(argv, returncode, None, None)

    monkeypatch.setattr(exec_module, "run_codex_subprocess", run)
    return calls


@pytest.mark.parametrize(("builder", "command"), BUILDERS)
def test_complete_prompt_and_initial_handoff_use_saved_stdin_and_actual_call(
    directory, monkeypatch, capsys, builder, command
):
    parameter = builder("long request " * 10000 + "\r\noriginal instruction")
    stale = directory / ".cmoc/gu/log/editor_input/input_orig.md"
    stale.parent.mkdir(parents=True)
    stale.write_text("unrelated editor contents")
    read = Path.read_text

    def read_without_original(path, *args, **kwargs):
        assert path != stale, "editor input must not be read again"
        return read(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read_without_original)
    monkeypatch.setenv(EDITOR_INPUT_SOURCE_ENV, "stale-parent-source")
    with call_log(directory, command) as logger:

        def observe(call):
            source = json.loads(call["env"][EDITOR_INPUT_SOURCE_ENV])
            handoff = next(
                row
                for row in events(logger)
                if row["event"] == "editor_input_handoff_source"
            )
            assert {key: handoff[key] for key in source} == source
            initial = json.loads(Path(handoff["call_log_path"]).read_text())
            assert initial["codex_call_id"] == source["codex_call_id"]
            assert source["execution_id"] == logger.execution_id
            assert source["subcommand"] == command
            assert source["sub_command_log_path"] == str(logger.path.resolve())
            assert (
                Path(initial["prompt_log_path"]).read_bytes() == call["prompt"].encode()
            )
            search = codex_override_config(call["argv"])["mcp_servers"][
                "cmoc_document_search"
            ]
            assert (
                json.loads(search["args"][-1])["log_context"]["codex_call_id"]
                == source["codex_call_id"]
            )

        calls = fake_initial(monkeypatch, on_call=observe)
        with pytest.raises(CmocError, match="会話追跡と入力待ち確認"):
            tui_module.run_codex_tui(parameter, root=directory, config=CmocConfig())
        initial = [row for row in events(logger) if row["event"] == "tui_initial_exec"]
        assert [row["process_state"] for row in initial] == [
            "prepared",
            "started",
            "exited",
        ]
        assert initial[-1]["status"] == "succeeded"
        assert initial[-1]["returncode"] == 0
        assert initial[-1]["codex_session_id"] == SESSION_ID
        [prepared] = [
            row for row in events(logger) if row["event"] == "tui_process_prepared"
        ]
        assert prepared["agent_call_id"] != initial[-1]["agent_call_id"]
        assert prepared["codex_call_id"] != initial[-1]["codex_call_id"]
        assert prepared["execution_id"] == logger.execution_id
        assert prepared["requested_codex_session_id"] == SESSION_ID
        assert prepared["codex_session_id"] is None
        assert prepared["prompt_log_path"] is None
        resume_call = json.loads(Path(prepared["call_log_path"]).read_text())
        assert resume_call["argv"][-2:] == ["resume", SESSION_ID]
        assert "--json" not in resume_call["argv"]
        assert "--output-last-message" not in resume_call["argv"]
        assert list(Path(prepared["call_log_path"]).parent.glob("*_prompt.md")) == [
            Path(initial[-1]["prompt_log_path"])
        ]
    assert len(calls) == 1
    assert calls[0]["prompt"] == parameter.prompt
    assert calls[0]["argv"][0] == "codex"
    assert "exec" in calls[0]["argv"]
    assert calls[0]["argv"][-1] == "-"
    assert parameter.prompt not in calls[0]["argv"]
    assert "--output-schema" not in calls[0]["argv"]
    assert codex_override_config(calls[0]["argv"])["notify"] == []
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "初回応答を生成中" in captured.err
    assert "initial answer" not in captured.err
    assert "diagnostic only" not in captured.err


@pytest.mark.parametrize(
    ("stdout", "returncode"),
    [
        ("", 0),
        (json.dumps({"type": "thread.started", "thread_id": SESSION_ID}) + "\n", 0),
        (SUCCESS, 7),
        (
            SUCCESS
            + json.dumps(
                {"type": "turn.failed", "error": {"message": "Quota exceeded"}}
            )
            + "\n",
            0,
        ),
        (
            json.dumps({"type": "turn.failed", "error": {"message": "Quota exceeded"}})
            + "\n",
            1,
        ),
        (
            json.dumps(
                {
                    "type": "turn.failed",
                    "error": {"message": "Selected model is at capacity"},
                }
            )
            + "\n",
            1,
        ),
    ],
)
def test_initial_terminal_failure_never_retries_or_transitions(
    directory, monkeypatch, stdout, returncode
):
    calls = fake_initial(monkeypatch, stdout=stdout, returncode=returncode)
    transition = Mock(side_effect=AssertionError("must not resume TUI"))
    recovery = Mock(side_effect=AssertionError("must not probe or wait"))
    monkeypatch.setattr(tui_module, "_run_codex_tui_process", transition)
    monkeypatch.setattr(exec_module, "wait_for_recovery", recovery)
    with call_log(directory) as logger:
        with pytest.raises(CmocError, match="Codex CLI 呼び出しが失敗"):
            tui_module.run_codex_tui(
                build_tui_launch_tui_parameter("request"),
                root=directory,
                config=CmocConfig(),
            )
        assert [row for row in events(logger) if row["event"] == "tui_initial_exec"][
            -1
        ]["status"] == "failed"
    assert len(calls) == 1
    transition.assert_not_called()
    recovery.assert_not_called()


@pytest.mark.parametrize(
    ("stdout", "output"),
    [
        (json.dumps({"type": "turn.completed"}) + "\n", "reply"),
        (SUCCESS.replace(SESSION_ID, "not-a-uuid"), "reply"),
        (SUCCESS, None),
        (
            json.dumps({"type": "thread.started", "thread_id": SESSION_ID})
            + "\n"
            + SUCCESS,
            "reply",
        ),
    ],
)
def test_initial_success_requires_saved_output_and_unique_uuid(
    directory, monkeypatch, stdout, output
):
    calls = fake_initial(monkeypatch, stdout=stdout, output=output)
    transition = Mock()
    monkeypatch.setattr(tui_module, "_run_codex_tui_process", transition)
    with pytest.raises(CmocError, match="再開に必要な記録"):
        tui_module.run_codex_tui(
            build_tui_launch_tui_parameter("request"),
            root=directory,
            config=CmocConfig(),
        )
    assert len(calls) == 1
    transition.assert_not_called()


def test_prompt_save_failure_starts_no_process(directory, monkeypatch):
    process = Mock()
    monkeypatch.setattr(exec_module, "run_codex_subprocess", process)
    monkeypatch.setattr(
        exec_module, "write_codex_prompt_log", Mock(side_effect=OSError("disk full"))
    )
    with pytest.raises(OSError, match="disk full"):
        tui_module.run_codex_tui(
            build_tui_launch_tui_parameter("request"),
            root=directory,
            config=CmocConfig(),
        )
    process.assert_not_called()


def test_initial_and_transition_share_start_time_settings(directory, monkeypatch):
    parameter = build_tui_launch_tui_parameter("original task")
    config = CmocConfig()
    config.codex.agent_calls[parameter.agent_call_kind] = CodexCallConfig(
        "openai", "initial-model", "low"
    )

    def change_config(_call):
        config.codex.agent_calls[parameter.agent_call_kind] = CodexCallConfig(
            "openai", "changed-model", "high"
        )
        config.codex.model_providers["openai"].settings["base_url"] = (
            "https://changed.invalid"
        )
        write_config(directory / ".cmoc/gt/config.json", config)

    calls = fake_initial(monkeypatch, on_call=change_config)

    def resume(parameter, **kwargs):
        assert parameter.prompt is None
        assert parameter.tui_resume_session_id == SESSION_ID
        assert (
            kwargs["config"].codex.agent_calls[parameter.agent_call_kind].model
            == "initial-model"
        )
        assert (
            "base_url" not in kwargs["config"].codex.model_providers["openai"].settings
        )
        return CommandResult(0, "", "")

    transition = Mock(side_effect=resume)
    monkeypatch.setattr(tui_module, "_run_codex_tui_process", transition)
    result = tui_module.run_codex_tui(parameter, root=directory, config=config)
    assert result.returncode == 0
    assert codex_arg_value(calls[0]["argv"], "--model") == "initial-model"
    transition.assert_called_once()


def test_accepted_cancellation_wins_over_success(directory, monkeypatch):
    def cancel(_call):
        exec_module.current_recovery_cancellation().set()

    calls = fake_initial(monkeypatch, on_call=cancel)
    transition = Mock()
    monkeypatch.setattr(tui_module, "_run_codex_tui_process", transition)
    with call_log(directory) as logger:
        with pytest.raises(TuiStartupCancelled):
            tui_module.run_codex_tui(
                build_tui_launch_tui_parameter("request"),
                root=directory,
                config=CmocConfig(),
            )
        final = [row for row in events(logger) if row["event"] == "tui_initial_exec"][
            -1
        ]
        assert final["process_state"] == "exited"
        assert final["status"] == "cancelled"
        assert not any(row.get("phase") == "resume_prepared" for row in events(logger))
    assert len(calls) == 1
    transition.assert_not_called()


def test_cancel_stops_fake_process_and_preserves_partial_logs(
    directory, tmp_path, monkeypatch
):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    pid_file = tmp_path / "ready"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, os, pathlib, subprocess, sys, time",
            "sys.stdin.read()",
            "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(100)'])",
            f"print(json.dumps({{'type': 'thread.started', 'thread_id': {SESSION_ID!r}}}), flush=True)",
            "print('partial diagnostic', file=sys.stderr, flush=True)",
            f"pathlib.Path({str(pid_file)!r}).write_text(str(os.getpid()) + ' ' + str(child.pid))",
            "time.sleep(100)",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:/usr/bin")
    parameter = replace(
        build_tui_launch_tui_parameter("request"),
        enable_feedback_reporting=False,
        enable_document_search_mcp=False,
    )
    restore = install_recovery_interruption()
    cancellation = exec_module.current_recovery_cancellation()
    try:
        with call_log(directory) as logger, ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(
                copy_context().run,
                tui_module.run_codex_tui,
                parameter,
                root=directory,
                config=CmocConfig(),
            )
            try:
                deadline = time.monotonic() + 5
                while not pid_file.exists():
                    if time.monotonic() >= deadline:
                        pytest.fail("fake Codex did not start")
                    cancellation.wait(0.01)
                process_id, _child_id = map(int, pid_file.read_text().split())
                assert not future.done()
                cancellation.set()
                with pytest.raises(TuiStartupCancelled):
                    future.result(timeout=10)
                assert not process_group_has_running_member(process_id)
                final = [
                    row for row in events(logger) if row["event"] == "tui_initial_exec"
                ][-1]
                assert final["status"] == "cancelled"
                assert final["process_state"] == "exited"
                assert SESSION_ID in Path(final["stdout_log_path"]).read_text()
                assert (
                    "partial diagnostic" in Path(final["stderr_log_path"]).read_text()
                )
            finally:
                cancellation.set()
    finally:
        restore()


def failed_initial_success(
    directory, monkeypatch, builder=build_tui_launch_tui_parameter, command="tui"
):
    calls = fake_initial(monkeypatch)
    with pytest.raises(typer.Exit):
        runtime_cli.run_cli_subcommand(
            lambda: tui_module.run_codex_tui(
                builder("initial work"), root=directory, config=CmocConfig()
            ),
            command_name=command,
            command_argv=["cmoc", *command.split()],
            doctor_preprocess=False,
            tui_process=True,
        )
    [source] = list(logs_dir(directory).glob("*.jsonl"))
    return calls, source


@pytest.mark.parametrize(("builder", "command"), BUILDERS)
def test_public_resume_uses_current_settings_and_self_contained_logs(
    directory, monkeypatch, builder, command
):
    calls, source = failed_initial_success(directory, monkeypatch, builder, command)
    source_text = source.read_text()
    config = CmocConfig()
    config.codex.agent_calls[builder.__name__] = CodexCallConfig(
        "openai", "public-resume-model", "high"
    )
    write_config(directory / ".cmoc/gt/config.json", config)

    def resume(execution_id):
        existing = set(logs_dir(directory).glob("*.jsonl"))
        with pytest.raises(typer.Exit):
            runtime_cli.run_cli_subcommand(
                lambda: tui_module.resume_codex_tui(execution_id, directory),
                command_name="resume",
                command_argv=["cmoc", "resume", execution_id],
                doctor_preprocess=False,
                tui_process=True,
            )
        [current] = set(logs_dir(directory).glob("*.jsonl")) - existing
        rows = [json.loads(line) for line in current.read_text().splitlines()]
        prepared = next(row for row in rows if row["event"] == "tui_process_prepared")
        assert prepared["subcommand"] == "resume"
        assert prepared["execution_id"] == current.stem != execution_id
        assert prepared["initial_execution_id"] == source.stem
        call = json.loads(Path(prepared["call_log_path"]).read_text())
        assert call["model"] == "public-resume-model"
        assert call["argv"][-2:] == ["resume", SESSION_ID]
        assert call["prompt_log_path"] is None
        assert not list(Path(prepared["call_log_path"]).parent.glob("*_prompt.md"))
        return current

    resumed = resume(source.stem)
    read = Path.read_text

    def no_chain(path, *args, **kwargs):
        assert path != source, "resume must not walk earlier subcommand logs"
        return read(path, *args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(Path, "read_text", no_chain)
        resume(resumed.stem)
    assert source.read_text() == source_text
    assert len(calls) == 1


@pytest.mark.parametrize(
    "condition",
    [
        "unfinished",
        "failed",
        "cancelled",
        "unknown_exit",
        "unknown_conversation",
        "inconsistent_kind",
        "missing_output",
        "bad_uuid",
        "home_changed",
        "broken_json",
    ],
)
def test_public_resume_rejects_ineligible_source(
    directory, monkeypatch, tmp_path, condition
):
    calls, source = failed_initial_success(directory, monkeypatch)
    rows = [json.loads(line) for line in source.read_text().splitlines()]
    record = next(row for row in reversed(rows) if row["event"] == "tui_startup")
    if condition == "unfinished":
        rows.pop()
    elif condition in {"failed", "cancelled"}:
        record["initial_status"] = condition
    elif condition == "unknown_exit":
        record["tui_process_state"] = "unknown"
    elif condition == "unknown_conversation":
        record["tui_conversation_state"] = "unknown"
    elif condition == "inconsistent_kind":
        record["tui_kind"] = "oracle_investigation"
    elif condition == "missing_output":
        Path(record["initial_output_path"]).unlink()
    elif condition == "bad_uuid":
        record["initial_session_id"] = "unknown-session"
    elif condition == "home_changed":
        home = tmp_path / "other_home"
        home.mkdir()
        monkeypatch.setenv("CODEX_HOME", str(home))
    source.write_text(
        "invalid JSON\n"
        if condition == "broken_json"
        else "".join(json.dumps(row) + "\n" for row in rows)
    )
    with pytest.raises(CmocError, match="再開条件を満たしません"):
        tui_module.resume_codex_tui(source.stem, directory)
    assert len(calls) == 1


def test_public_resume_rejects_non_tui_and_invalid_id(directory):
    with call_log(directory, "oracle edit") as logger:
        logger.event("command_finished")
    for execution_id in (
        logger.execution_id,
        "../memo/anything",
        "not-an-execution-id",
    ):
        with pytest.raises(CmocError, match="再開条件を満たしません"):
            tui_module.resume_codex_tui(execution_id, directory)


def test_completion_probe_prepares_no_calls(directory, monkeypatch):
    run = Mock()
    monkeypatch.setattr(tui_module, "run_codex_exec", run)
    monkeypatch.setenv("_CMOC_COMPLETE", "")
    result = tui_module.run_codex_tui(
        build_tui_launch_tui_parameter("request"), root=directory
    )
    assert result.returncode == 0
    run.assert_not_called()


def test_initial_completion_waits_for_process_exit(directory, tmp_path, monkeypatch):
    ready = tmp_path / "ready"
    release = tmp_path / "release"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(
        bin_dir / "codex",
        [
            "import pathlib, sys, time",
            "sys.stdin.read()",
            f"print({SUCCESS!r}, end='', flush=True)",
            "args = sys.argv[1:]",
            "pathlib.Path(args[args.index('--output-last-message') + 1]).write_text('saved reply')",
            f"pathlib.Path({str(ready)!r}).touch()",
            "for _ in range(500):",
            f"    if pathlib.Path({str(release)!r}).exists(): break",
            "    time.sleep(0.01)",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:/usr/bin")
    parameter = replace(
        build_tui_launch_tui_parameter("request"),
        enable_document_search_mcp=False,
        enable_feedback_reporting=False,
    )
    with call_log(directory) as logger, ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(
            copy_context().run,
            tui_module.run_codex_tui,
            parameter,
            root=directory,
            config=CmocConfig(),
        )
        try:
            deadline = time.monotonic() + 5
            while not ready.exists():
                if future.done() or time.monotonic() >= deadline:
                    pytest.fail("fake initial exec did not reach terminal information")
                time.sleep(0.01)
            assert not future.done()
            assert not any(
                row.get("phase") == "resume_prepared" for row in events(logger)
            )
            release.touch()
            with pytest.raises(CmocError, match="会話追跡と入力待ち確認"):
                future.result(timeout=5)
            rows = events(logger)
            initial_exited = next(
                i
                for i, row in enumerate(rows)
                if row["event"] == "tui_initial_exec"
                and row["process_state"] == "exited"
            )
            resume_prepared = next(
                i for i, row in enumerate(rows) if row.get("phase") == "resume_prepared"
            )
            assert initial_exited < resume_prepared
        finally:
            release.touch()


def test_concurrent_initial_handoffs_keep_process_sources(directory, monkeypatch):
    barrier = threading.Barrier(2)
    observed = {}

    def handoff(call):
        source = json.loads(call["env"][EDITOR_INPUT_SOURCE_ENV])
        work = (
            directory / ".cmoc/gu/log/editor_input" / (source["codex_call_id"] + ".md")
        )
        work.parent.mkdir(parents=True, exist_ok=True)
        work.write_text("initial")
        target = start_editor_input_handoff(directory, work, "{{original-prompt-here}}")
        try:
            barrier.wait(timeout=5)
            server = codex_override_config(call["argv"])["mcp_servers"][
                "cmoc_editor_input"
            ]
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "overwrite",
                    "arguments": handoff_input(target.target_id, "request context"),
                },
            }
            result = subprocess.run(
                [server["command"], *server["args"]],
                cwd=directory,
                env={
                    "PATH": call["env"]["PATH"],
                    "PYTHONDONTWRITEBYTECODE": "1",
                    **{name: call["env"][name] for name in server["env_vars"]},
                    **server["env"],
                },
                input=json.dumps(request) + "\n",
                text=True,
                capture_output=True,
                timeout=10,
                check=True,
            )
            assert json.loads(result.stdout)["result"]["structuredContent"] == {
                "status": "accepted"
            }
            body = work.read_text()
            assert all(value in body for value in source.values())
            assert "送信元 Codex process" in body
            observed[source["subcommand"]] = source
        finally:
            target.close()

    calls = fake_initial(monkeypatch, on_call=handoff)

    def launch(item):
        builder, command = item
        with call_log(directory, command) as logger:
            with pytest.raises(CmocError, match="会話追跡と入力待ち確認"):
                tui_module.run_codex_tui(
                    builder("request"), root=directory, config=CmocConfig()
                )
            source = observed[command]
            initial = next(
                row for row in events(logger) if row["event"] == "tui_initial_exec"
            )
            assert initial["codex_call_id"] == source["codex_call_id"]
            assert initial["execution_id"] == source["execution_id"]

    with ThreadPoolExecutor(max_workers=2) as pool:
        list(
            pool.map(
                launch,
                [
                    (build_tui_launch_tui_parameter, "tui"),
                    (
                        build_oracle_investigation_launch_tui_parameter,
                        "oracle investigation",
                    ),
                ],
            )
        )
    assert len(calls) == 2
    assert len({source["codex_call_id"] for source in observed.values()}) == 2
