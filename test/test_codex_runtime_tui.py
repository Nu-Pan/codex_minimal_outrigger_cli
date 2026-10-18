"""TUI の初回 exec、保存記録、取消と公開 resume の制御を検証する。"""

import json
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing, contextmanager
from contextvars import copy_context
from dataclasses import replace
from pathlib import Path
from unittest.mock import Mock
from uuid import NAMESPACE_URL, uuid5

import oracle.other.path_model as path_model_module
import pytest
import typer
from _codex_support import (
    codex_arg_value,
    codex_override_config,
    setup_codex_home,
    stub_codex_overrides,
)
from _command_support import write_python_executable
from _handoff_support import handoff_input
from oracle.acp_builder.oracle.investigation.launch_tui import (
    build_oracle_investigation_request,
)
from oracle.acp_builder.tui.launch_tui import build_tui_request
from oracle.other.cmoc_config import CodexCallConfig

import commons.runtime_cli as runtime_cli
import commons.runtime_codex_exec as exec_module
import commons.runtime_codex_tui as tui_module
import commons.runtime_logging as logging_module
import commons.runtime_windows_toast as toast_module
from commons.runtime_codex_profile import process_group_has_running_member
from commons.runtime_codex_recovery import install_recovery_interruption
from commons.runtime_codex_session import CodexSessionLease
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
    pytest.param(build_tui_request, "tui", id="tui"),
    pytest.param(
        build_oracle_investigation_request,
        "oracle investigation",
        id="investigation",
    ),
]


@pytest.fixture
def directory(tmp_path, monkeypatch, nonpersistent_execution_ids):
    # 永続採番とログ保存の結合は test_codex_runtime_paths.py に残す。
    # TUI の制御検査では、ログ間の ID 対応を保って採番用 DB の準備を省く。
    for module in (exec_module, tui_module):
        monkeypatch.setattr(module, "new_id", logging_module.new_id)
    # この Fake は通知 callback を起動しないため、空の state の drain は省く。
    # 待機の期限・遅延起動・実 marker と cleanup の結合は test_windows_toast.py に残す。
    monkeypatch.setattr(
        toast_module, "_wait_for_tui_callback_drain", lambda _root: None
    )
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
    # 保存設定は公開 resume のケースで用意し、制御検査には設定を直接渡す。
    fake_tui(monkeypatch)
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


def fake_tui(monkeypatch, *, returncode=0, spawn_error=None, on_call=None):
    calls = []

    def run(argv, **kwargs):
        assert not {
            "stdin",
            "input",
            "stdout",
            "stderr",
            "capture_output",
            "stdout_line_callback",
        }.intersection(kwargs)
        if spawn_error is not None:
            raise spawn_error
        kwargs["process_started_callback"]()
        call = {"argv": argv, "env": kwargs["env"], "cwd": kwargs["cwd"]}
        calls.append(call)
        if on_call is not None:
            on_call(call)
        return subprocess.CompletedProcess(argv, returncode, None, None)

    monkeypatch.setattr(tui_module, "run_codex_subprocess", run)
    return calls


def fake_initial(
    monkeypatch,
    *,
    stdout=SUCCESS,
    returncode=0,
    output="initial answer",
    on_call=None,
    unique_sessions=False,
):
    calls = []

    def run(argv, **kwargs):
        kwargs["process_started_callback"]()
        prompt = kwargs["stdin"].read()
        # 並行する call の追記後も、この呼び出し自身を callback へ渡す。
        call = {"argv": argv, "prompt": prompt, "env": kwargs["env"]}
        calls.append(call)
        stream = stdout
        if unique_sessions:
            source = json.loads(kwargs["env"][EDITOR_INPUT_SOURCE_ENV])
            stream = stdout.replace(
                SESSION_ID, str(uuid5(NAMESPACE_URL, source["codex_call_id"]))
            )
        kwargs["stdout"].write(stream)
        kwargs["stdout"].flush()
        for line in stream.splitlines():
            kwargs["stdout_line_callback"](line)
        kwargs["stderr"].write("diagnostic only")
        if output is not None:
            Path(codex_arg_value(argv, "--output-last-message")).write_text(output)
        if on_call is not None:
            on_call(call)
        return subprocess.CompletedProcess(argv, returncode, None, None)

    monkeypatch.setattr(exec_module, "run_codex_subprocess", run)
    return calls


@pytest.mark.parametrize(("builder", "command"), BUILDERS)
def test_complete_prompt_and_initial_handoff_use_saved_stdin_and_actual_call(
    directory, monkeypatch, capsys, builder, command
):
    parameter = builder("long request " * 10000 + "\r\noriginal instruction")
    # 起動準備の root はログにも再利用し、別 process の context は個別に導出する。
    path_contexts = Mock(wraps=tui_module.AgentCallPathContext)
    monkeypatch.setattr(tui_module, "AgentCallPathContext", path_contexts)
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
            assert path_contexts.call_count == 1
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
        result = tui_module.run_codex_tui(
            parameter, root=directory, config=CmocConfig()
        )
        assert result.returncode == 0
        initial = [row for row in events(logger) if row["event"] == "tui_initial_exec"]
        assert [row["process_state"] for row in initial] == [
            "prepared",
            "started",
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
        assert prepared["fixed_session_id"] == SESSION_ID
        assert "codex_session_id" not in prepared
        assert "conversation_state" not in prepared
        assert prepared["prompt_log_path"] is None
        resume_call = json.loads(Path(prepared["call_log_path"]).read_text())
        # 検索設定は call 固有の context で一度だけ渡し、汎用設定を重ねない。
        for argv in (calls[0]["argv"], resume_call["argv"]):
            assert (
                sum(arg.startswith("mcp_servers.cmoc_document_search=") for arg in argv)
                == 1
            )
        assert resume_call["argv"][-2:] == ["resume", SESSION_ID]
        assert "--json" not in resume_call["argv"]
        assert "--output-last-message" not in resume_call["argv"]
        assert list(Path(prepared["call_log_path"]).parent.glob("*_prompt.md")) == [
            Path(initial[-1]["prompt_log_path"])
        ]
    assert path_contexts.call_count == 2
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
    # argv・MCP 設定の結合は complete_prompt と share_start_time_settings のケースに残す。
    # ここでは終端判定・ログ保存・移行禁止を検査し、起動設定の構築を繰り返さない。
    stub_codex_overrides(monkeypatch)
    calls = fake_initial(monkeypatch, stdout=stdout, returncode=returncode)
    transition = Mock(side_effect=AssertionError("must not resume TUI"))
    recovery = Mock(side_effect=AssertionError("must not probe or wait"))
    monkeypatch.setattr(tui_module, "_run_codex_tui_process", transition)
    monkeypatch.setattr(exec_module, "wait_for_recovery", recovery)
    with call_log(directory) as logger:
        with pytest.raises(CmocError, match="Codex CLI 呼び出しが失敗"):
            tui_module.run_codex_tui(
                build_tui_request("request"),
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
    # 起動設定は上の結合ケースに残し、保存出力と UUID の受理条件を検査する。
    stub_codex_overrides(monkeypatch)
    calls = fake_initial(monkeypatch, stdout=stdout, output=output)
    transition = Mock()
    monkeypatch.setattr(tui_module, "_run_codex_tui_process", transition)
    with pytest.raises(CmocError, match="再開に必要な記録"):
        tui_module.run_codex_tui(
            build_tui_request("request"),
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
            build_tui_request("request"),
            root=directory,
            config=CmocConfig(),
        )
    process.assert_not_called()


def test_initial_and_transition_share_start_time_settings(directory, monkeypatch):
    parameter = build_tui_request("original task")
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
    notify = Mock()
    monkeypatch.setattr(tui_module, "notify_terminal_result", notify)
    with call_log(directory) as logger:
        with pytest.raises(TuiStartupCancelled):
            tui_module.run_codex_tui(
                build_tui_request("request"),
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
    notify.assert_not_called()


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
            "child = subprocess.Popen([sys.executable, '-S', '-c', 'import time; time.sleep(100)'])",
            f"print(json.dumps({{'type': 'thread.started', 'thread_id': {SESSION_ID!r}}}), flush=True)",
            "print('partial diagnostic', file=sys.stderr, flush=True)",
            f"pathlib.Path({str(pid_file)!r}).write_text(str(os.getpid()) + ' ' + str(child.pid))",
            "time.sleep(100)",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:/usr/bin")
    parameter = replace(
        build_tui_request("request"),
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
    directory, monkeypatch, builder=build_tui_request, command="tui"
):
    calls = fake_initial(monkeypatch)
    with monkeypatch.context() as patch:
        fake_tui(patch, spawn_error=OSError("failed to spawn"))
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
    path_contexts = Mock(wraps=tui_module.AgentCallPathContext)
    monkeypatch.setattr(tui_module, "AgentCallPathContext", path_contexts)
    source_text = source.read_text()
    config = CmocConfig()
    config.codex.agent_calls[builder.__name__] = CodexCallConfig(
        "openai", "public-resume-model", "high"
    )
    write_config(directory / ".cmoc/gt/config.json", config)

    def resume(execution_id):
        path_contexts.reset_mock()
        existing = set(logs_dir(directory).glob("*.jsonl"))
        runtime_cli.run_cli_subcommand(
            lambda: tui_module.resume_codex_tui(execution_id, directory).returncode,
            command_name="resume",
            command_argv=["cmoc", "resume", execution_id],
            doctor_preprocess=False,
            tui_process=True,
        )
        # 適格性の検査・今回の準備・対話 process の導出を保ち、ログ用には増やさない。
        assert path_contexts.call_count == 3
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
    # 初回成功の根拠は今回のログに引き継がれ、再開元の保存物を再読しない。
    initial = next(
        row
        for row in map(json.loads, source_text.splitlines())
        if row.get("event") == "tui_initial_exec"
    )
    for path in Path(initial["call_log_path"]).parent.iterdir():
        path.unlink()
    source.unlink()
    resume(resumed.stem)
    assert len(calls) == 1


def test_public_resume_rejects_ineligible_source(directory, monkeypatch, tmp_path):
    # 設定・MCP と起動記録の結合は current_settings・separate_process_resources・
    # accepts_fixed_id のケースに残し、拒否条件だけが異なる検査の正常記録は一度作る。
    stub_codex_overrides(monkeypatch)
    calls, source = failed_initial_success(directory, monkeypatch)
    source_text = source.read_text()
    baseline = [json.loads(line) for line in source_text.splitlines()]
    record = next(row for row in reversed(baseline) if row["event"] == "tui_startup")
    prepared = next(row for row in baseline if row["event"] == "tui_process_prepared")
    saved_files = {
        path: path.read_bytes()
        for path in (
            source,
            Path(record["initial_output_path"]),
            Path(prepared["call_log_path"]),
        )
    }
    other_home = tmp_path / "other_home"
    other_home.mkdir()
    tui_calls = fake_tui(monkeypatch)
    # 正常な共通記録は一度検査し、各条件ではその bytes と環境を復元する。
    tui_module._validated_resume_record(source.stem, directory)

    for condition in (
        "unfinished",
        "failed",
        "cancelled",
        "unknown_exit",
        "unknown_session",
        "inconsistent_kind",
        "missing_output",
        "bad_uuid",
        "home_changed",
        "broken_json",
        "initial_exit_unknown",
        "missing_tui_call",
        "different_requested_session",
    ):
        # 削除・書き換えた通常 file、JSON の入れ子、環境変数を条件ごとに復元する。
        for path, content in saved_files.items():
            path.write_bytes(content)
        rows = [json.loads(line) for line in source_text.splitlines()]
        record = next(row for row in reversed(rows) if row["event"] == "tui_startup")
        with monkeypatch.context() as patch:
            if condition == "unfinished":
                rows.pop()
            elif condition in {"failed", "cancelled"}:
                record["initial_status"] = condition
            elif condition == "unknown_exit":
                record["tui_process_state"] = "unknown"
            elif condition == "unknown_session":
                record["fixed_session_id"] = None
            elif condition == "inconsistent_kind":
                record["tui_kind"] = "oracle_investigation"
            elif condition == "missing_output":
                Path(record["initial_output_path"]).unlink()
            elif condition == "bad_uuid":
                record["initial_session_id"] = "unknown-session"
            elif condition == "home_changed":
                patch.setenv("CODEX_HOME", str(other_home))
            elif condition == "initial_exit_unknown":
                initial = [row for row in rows if row["event"] == "tui_initial_exec"][
                    -1
                ]
                initial["process_state"] = "unknown"
            elif condition in {"missing_tui_call", "different_requested_session"}:
                prepared = next(
                    row for row in rows if row["event"] == "tui_process_prepared"
                )
                path = Path(prepared["call_log_path"])
                if condition == "missing_tui_call":
                    path.unlink()
                else:
                    call = json.loads(path.read_text())
                    call["argv"][-1] = "019efe07-4886-7423-b252-625febbe31ec"
                    path.write_text(json.dumps(call))
            source.write_text(
                "invalid JSON\n"
                if condition == "broken_json"
                else "".join(json.dumps(row) + "\n" for row in rows)
            )
            with pytest.raises(CmocError, match="再開条件を満たしません"):
                tui_module.resume_codex_tui(source.stem, directory)
        assert len(calls) == 1, condition
        assert tui_calls == [], condition


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
    result = tui_module.run_codex_tui(build_tui_request("request"), root=directory)
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
        build_tui_request("request"),
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
            while not ready.exists() or not any(
                row.get("codex_session_id") == SESSION_ID for row in events(logger)
            ):
                if future.done() or time.monotonic() >= deadline:
                    pytest.fail("fake initial exec did not reach terminal information")
                time.sleep(0.01)
            assert not future.done()
            assert not any(
                row.get("phase") == "resume_prepared" for row in events(logger)
            )
            with closing(
                CodexSessionLease(tui_module.resolve_codex_home(directory))
            ) as contender:
                with pytest.raises(CmocError, match="使用中"):
                    contender.acquire(SESSION_ID)
            release.touch()
            assert future.result(timeout=5).returncode == 0
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


# 永続採番と target の結合は test_editor_input_handoff.py に残す。
# ここでは採番 DB を準備せず、並行する実 MCP process の送信元分離を検査する。
@pytest.mark.usefixtures("nonpersistent_handoff_ids")
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

    calls = fake_initial(monkeypatch, on_call=handoff, unique_sessions=True)

    def launch(item):
        builder, command = item
        with call_log(directory, command) as logger:
            assert (
                tui_module.run_codex_tui(
                    builder("request"), root=directory, config=CmocConfig()
                ).returncode
                == 0
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
                    (build_tui_request, "tui"),
                    (
                        build_oracle_investigation_request,
                        "oracle investigation",
                    ),
                ],
            )
        )
    assert len(calls) == 2
    assert len({source["codex_call_id"] for source in observed.values()}) == 2


@pytest.mark.parametrize(("builder", "command"), BUILDERS)
@pytest.mark.parametrize("outcome", ["completed", "abnormal", "preparation", "spawn"])
def test_public_resume_accepts_fixed_id_after_initial_success(
    directory, monkeypatch, builder, command, outcome
):
    # argv 設定は complete_prompt・current_settings・notification_failure で検査する。
    # 終了状態ごとの再開適格性では、既存 helper で起動設定の再構築を省く。
    stub_codex_overrides(monkeypatch)
    write_config(directory / ".cmoc/gt/config.json", CmocConfig())
    fake_initial(monkeypatch)
    notifications = []

    def notify(name, root, state):
        notifications.append((name, root, state))

    monkeypatch.setattr(tui_module, "notify_terminal_result", notify)
    monkeypatch.setattr(runtime_cli, "notify_terminal_result", notify)
    with monkeypatch.context() as patch:
        if outcome == "preparation":
            patch.setattr(
                tui_module,
                "prepare_codex_override_args",
                Mock(side_effect=OSError("configuration unavailable")),
            )
        fake_tui(
            patch,
            returncode=17 if outcome == "abnormal" else 0,
            spawn_error=OSError("spawn failed") if outcome == "spawn" else None,
        )

        def body():
            return tui_module.run_codex_tui(
                builder("request"), root=directory, config=CmocConfig()
            ).returncode

        if outcome == "completed":
            runtime_cli.run_cli_subcommand(
                body, command_name=command, doctor_preprocess=False, tui_process=True
            )
        else:
            with pytest.raises(typer.Exit):
                runtime_cli.run_cli_subcommand(
                    body,
                    command_name=command,
                    doctor_preprocess=False,
                    tui_process=True,
                )
    [source] = list(logs_dir(directory).glob("*.jsonl"))
    rows = [json.loads(line) for line in source.read_text().splitlines()]
    record = next(row for row in reversed(rows) if row["event"] == "tui_startup")
    assert record["fixed_session_id"] == SESSION_ID
    assert "conversation_state" not in record
    expected = []
    if outcome in {"completed", "abnormal"}:
        expected.append((command, directory, "initial_completed"))
        assert record["tui_process_state"] == "exited"
        assert record["tui_returncode"] == (17 if outcome == "abnormal" else 0)
    else:
        assert record["tui_process_state"] == (
            "not_started" if outcome == "preparation" else "spawn_failed"
        )
        assert record["tui_returncode"] is None
    if outcome != "completed":
        expected.append((command, directory, "failed"))
    assert notifications == expected
    notifications.clear()
    calls = fake_tui(monkeypatch)
    with call_log(directory, "resume"):
        assert tui_module.resume_codex_tui(source.stem, directory).returncode == 0
    assert len(calls) == 1
    assert calls[0]["argv"][-2:] == ["resume", SESSION_ID]
    assert notifications == []


@pytest.mark.parametrize(
    "failure", ["prepare", "configure", "send", "cleanup", "unavailable"]
)
def test_notification_failure_preserves_tui_execution(directory, monkeypatch, failure):
    fake_initial(monkeypatch)
    calls = fake_tui(monkeypatch)
    callback = Mock(command=["notification-helper"])
    if failure == "cleanup":
        callback.close.side_effect = OSError("cleanup failed")
    if failure == "configure":
        # 実際の TOML 符号化を失敗させ、通知なしの設定へ戻れることを確かめる。
        callback.command = [None]
    if failure == "prepare":
        creator = Mock(side_effect=OSError("notification context failed"))
    else:
        creator = Mock(return_value=None if failure == "unavailable" else callback)
    monkeypatch.setattr(tui_module, "create_tui_notification_callback", creator)
    if failure == "send":
        monkeypatch.setattr(
            tui_module,
            "notify_terminal_result",
            Mock(side_effect=OSError("transport failed")),
        )
    with call_log(directory):
        assert (
            tui_module.run_codex_tui(
                build_tui_request("request"),
                root=directory,
                config=CmocConfig(),
            ).returncode
            == 0
        )
    assert len(calls) == 1
    assert (
        sum(
            arg.startswith("mcp_servers.cmoc_document_search=")
            for arg in calls[0]["argv"]
        )
        == 1
    )
    if failure in {"prepare", "configure", "unavailable"}:
        assert codex_override_config(calls[0]["argv"])["notify"] == []
    else:
        assert codex_override_config(calls[0]["argv"])["notify"] == callback.command
    if failure not in {"prepare", "unavailable"}:
        callback.close.assert_called_once()


def test_initial_and_tui_keep_separate_process_resources(directory, monkeypatch):
    contexts = []
    closed = []

    def begin(**fields):
        index = len(contexts)
        contexts.append(fields)
        call = Mock()
        call.subprocess_env.side_effect = lambda base: {
            **base,
            "CALL_CONTEXT": str(index),
        }
        call.close.side_effect = lambda: closed.append(index)
        return call

    monkeypatch.setattr(exec_module, "begin_feedback_call", begin)
    monkeypatch.setattr(tui_module, "begin_feedback_call", begin)
    initial = fake_initial(monkeypatch)

    def observe(call):
        assert closed == [0]
        assert call["env"]["CALL_CONTEXT"] == "1"
        source = json.loads(call["env"][EDITOR_INPUT_SOURCE_ENV])
        assert source["codex_call_id"] == contexts[1]["codex_call_id"]
        search = codex_override_config(call["argv"])["mcp_servers"][
            "cmoc_document_search"
        ]
        assert (
            json.loads(search["args"][-1])["log_context"]["codex_call_id"]
            == source["codex_call_id"]
        )
        assert contexts[0]["codex_call_id"] != contexts[1]["codex_call_id"]
        assert contexts[0]["agent_call_id"] != contexts[1]["agent_call_id"]
        assert contexts[1]["codex_session_id"] == SESSION_ID

    fake_tui(monkeypatch, on_call=observe)
    with call_log(directory):
        tui_module.run_codex_tui(
            build_tui_request("request"),
            root=directory,
            config=CmocConfig(),
        )
    assert initial[0]["env"]["CALL_CONTEXT"] == "0"
    assert closed == [0, 1]


def test_session_lease_covers_initial_transition_and_public_validation(
    directory, monkeypatch
):
    write_config(directory / ".cmoc/gt/config.json", CmocConfig())
    home = tui_module.resolve_codex_home(directory)

    def contested(_call):
        with closing(CodexSessionLease(home)) as contender:
            with pytest.raises(CmocError, match="使用中"):
                contender.acquire(SESSION_ID)

    fake_initial(monkeypatch, on_call=contested)
    fake_tui(monkeypatch, on_call=contested)
    runtime_cli.run_cli_subcommand(
        lambda: (
            tui_module.run_codex_tui(
                build_tui_request("request"), root=directory
            ).returncode
        ),
        command_name="tui",
        doctor_preprocess=False,
        tui_process=True,
    )
    [source] = list(logs_dir(directory).glob("*.jsonl"))
    validate = tui_module._validated_resume_record

    def validate_under_lock(*args):
        contested(None)
        return validate(*args)

    monkeypatch.setattr(tui_module, "_validated_resume_record", validate_under_lock)
    with call_log(directory, "resume"):
        assert tui_module.resume_codex_tui(source.stem, directory).returncode == 0
    with closing(CodexSessionLease(home)) as next_use:
        next_use.acquire(SESSION_ID)


def test_unknown_process_exit_keeps_session_unavailable(directory, monkeypatch):
    fake_initial(monkeypatch)

    def run(argv, **kwargs):
        kwargs["process_started_callback"]()
        raise OSError("process exit cannot be confirmed")

    monkeypatch.setattr(tui_module, "run_codex_subprocess", run)
    with call_log(directory) as logger:
        with pytest.raises(OSError, match="exit cannot be confirmed"):
            tui_module.run_codex_tui(
                build_tui_request("request"),
                root=directory,
                config=CmocConfig(),
            )
        final = [row for row in events(logger) if row.get("phase") == "tui_failed"][-1]
        assert final["tui_process_state"] == "unknown"
        assert final["tui_returncode"] is None
    with closing(
        CodexSessionLease(tui_module.resolve_codex_home(directory))
    ) as contender:
        with pytest.raises(CmocError, match="終了未確認"):
            contender.acquire(SESSION_ID)


def test_tui_process_waits_with_inherited_output_and_records_exit(
    directory, monkeypatch, tmp_path, capfd
):
    import commons.runtime_codex_profile as profile

    # 初回 process の終了待ちは test_initial_completion_waits_for_process_exit に残す。
    # 正常終了の結果・ログ・再開適格性は public_resume_accepts_fixed_id_after_initial_success
    # で検査する。端末継承と終了待ちは非ゼロ終了の実 process に集約し、異常終了も検出する。
    initial_calls = fake_initial(monkeypatch)
    ready = tmp_path / "tui-ready"
    release = tmp_path / "tui-release"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(
        bin_dir / "codex",
        [
            "import pathlib, sys, time",
            "args = sys.argv[1:]",
            f"assert args[-2:] == ['resume', {SESSION_ID!r}]",
            "print('fake interactive output', flush=True)",
            f"pathlib.Path({str(ready)!r}).touch()",
            "for _ in range(1000):",
            f"    if pathlib.Path({str(release)!r}).exists(): break",
            "    time.sleep(0.01)",
            "sys.exit(19)",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:/usr/bin")
    # MCP 自体の検査は別ケースへ残し、この Fake process では端末と終了待ちを観測する。
    monkeypatch.setattr(
        profile, "_verify_document_search_server", lambda *_args, **_kwargs: None
    )
    monkeypatch.setattr(
        tui_module, "run_codex_subprocess", profile.run_codex_subprocess
    )
    with call_log(directory) as logger, ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(
            copy_context().run,
            tui_module.run_codex_tui,
            build_tui_request("request"),
            root=directory,
            config=CmocConfig(),
        )
        try:
            deadline = time.monotonic() + 5
            while not ready.exists():
                if future.done() or time.monotonic() >= deadline:
                    pytest.fail("fake interactive process did not start")
                time.sleep(0.01)
            assert not future.done()
            assert not any(
                row["event"] == "tui_process_finished" for row in events(logger)
            )
            release.touch()
            with pytest.raises(CmocError, match="異常終了"):
                future.result(timeout=5)
            [finished] = [
                row for row in events(logger) if row["event"] == "tui_process_finished"
            ]
            assert finished["process_state"] == "exited"
            assert finished["returncode"] == 19
        finally:
            release.touch()
    assert len(initial_calls) == 1
    assert "fake interactive output" in capfd.readouterr().out
