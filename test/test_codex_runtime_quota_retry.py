"""quota probe の構築、実行、共有と再開を検証する。"""

import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Event, Lock
from typing import TextIO, cast
from unittest.mock import Mock

import oracle.other.path_model as path_model_module
import pytest
from _codex_support import (
    codex_arg_value,
    codex_override_config,
    script_codex_calls,
    setup_codex_home,
    stub_codex_overrides,
)
from oracle.request_builder.common.quota_probe import (
    build_quota_availability_probe_request as build_canonical_quota_probe_parameter,
)

import commons.runtime_codex_exec as runtime_codex_exec
from basic.acp import AgentCallParameter, FileAccessMode
from cmoc_runtime import SubcommandLogger
from commons.runtime_codex import run_codex_exec
from commons.runtime_errors import CmocError
from config.cmoc_config import CmocConfig


@pytest.fixture
def quota_prompt_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """prompt・parameter の検査では root 探索結果だけを置換する。"""
    root = tmp_path / "repo"
    root.mkdir()
    # 実 Git の root 導出は test_basic_runtime.py と test_codex_runtime_paths.py に残し、
    # prompt の結合検査では context と正本 probe builder を実物で使う。
    monkeypatch.setattr(
        path_model_module, "_resolve_git_worktree_roots", lambda _cwd: (root, root)
    )
    return root


@pytest.fixture
def quota_control_root(
    quota_prompt_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    nonpersistent_codex_ids: None,
) -> Path:
    """回復制御に必要な HOME・設定・probe を用意し、永続採番を省く。"""
    root = quota_prompt_root
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)

    # 完全 prompt の生成と受け渡しは canonical_complete_prompt と
    # polls_and_resumes に残し、制御の検査では期待値・実行用の再生成を省く。
    def probe_parameter(base: AgentCallParameter) -> AgentCallParameter:
        return AgentCallParameter(
            agent_call_kind="build_quota_availability_probe_request",
            file_access_mode=FileAccessMode.READONLY,
            prompt="quota probe",
            structured_output_schema_path=None,
            agent_call_cwd=base.agent_call_cwd,
            enable_document_search_mcp=False,
        )

    monkeypatch.setattr(
        runtime_codex_exec, "_quota_availability_probe_parameter", probe_parameter
    )
    # logger・current_execution_id・agent・Codex call の採番は共通 fixture を使う。
    # 永続性・process 間の採番は test_runtime_ids.py と test_codex_runtime_paths.py で検証する。
    return root


def quota_probe_prompt(agent_call_cwd: Path) -> str:
    """runtime が使用する quota probe の prompt を返す。"""
    return runtime_codex_exec._quota_availability_probe_parameter(
        AgentCallParameter(
            agent_call_kind="realization_edit",
            file_access_mode=FileAccessMode.READONLY,
            prompt="base",
            structured_output_schema_path=None,
            agent_call_cwd=agent_call_cwd,
        )
    ).prompt


def test_session_id_is_read_from_persisted_stdout_jsonl_log(tmp_path: Path) -> None:
    """保存済み stdout JSONL から session ID を復元し、欠落時は None にする。"""
    log_path = tmp_path / "failed_call.jsonl"
    log_path.write_text('{"type":"thread.started","thread_id":"sess-from-log"}\n')

    assert (
        runtime_codex_exec._extract_session_id_from_stdout_log(log_path)
        == "sess-from-log"
    )
    assert (
        runtime_codex_exec._extract_session_id_from_stdout_log(
            tmp_path / "missing.jsonl"
        )
        is None
    )


def test_run_codex_exec_polls_and_resumes_after_quota(
    tmp_path: Path,
    quota_prompt_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    nonpersistent_codex_ids: None,
) -> None:
    """相対 HOME と cwd の受け渡し、probe・元 session の resume を検証する。"""
    root = quota_prompt_root
    codex_home = setup_codex_home(tmp_path, monkeypatch)
    # 実 process の stdin・出力捕捉は test_codex_runtime_exec.py、相対 HOME の
    # cwd 基準の解決は test_codex_runtime_paths.py に残し、3 回の子起動を省く。
    # 初回・probe・resume には、呼び出し時に渡された cwd と env を照合する。
    relative_codex_home = "../codex_home"
    monkeypatch.setenv("CODEX_HOME", relative_codex_home)
    timestamps = iter(
        [
            "2099-01-01_00-00-30_000",
            "2099-01-01_00-00-20_000",
            "2099-01-01_00-00-10_000",
        ]
    )
    monkeypatch.setattr(runtime_codex_exec, "timestamp", lambda: next(timestamps))
    probe_prompt = quota_probe_prompt(root)
    call_records = script_codex_calls(
        monkeypatch,
        [
            (
                1,
                '{"type": "thread.started", "thread_id": "sess-1"}\n'
                '{"type": "error", "message": "Quota exceeded"}\n',
                None,
            ),
            (0, '{"type": "turn.completed"}\n', '{"probe": true}'),
            (0, '{"type": "turn.completed"}\n', '{"ok": true}'),
        ],
    )
    parameter = AgentCallParameter(
        "realization_edit",
        FileAccessMode.PURE_ORACLE_READ,
        "prompt",
        None,
        root,
    )
    logger = SubcommandLogger(root, "test")
    config = CmocConfig()
    base_call_config = config.codex.agent_calls[parameter.agent_call_kind]
    probe_call_config = config.codex.agent_calls[
        "build_quota_availability_probe_request"
    ]

    result = run_codex_exec(
        parameter,
        root=root,
        quota_poll_interval_sec=0,
        config=config,
        subcommand_logger=logger,
    )

    assert len(call_records) == 3
    argv_calls = [record["argv"][1:] for record in call_records]
    assert all(args.count("--no-daemon") == 1 for args in argv_calls)
    assert argv_calls[0][-1] == "-"
    for record in call_records:
        assert Path(record["cwd"]) == root
        assert codex_arg_value(record["argv"], "--cd") == str(root)
        assert record["env"]["CODEX_HOME"] == relative_codex_home
        assert (
            Path(record["cwd"]) / record["env"]["CODEX_HOME"]
        ).resolve() == codex_home
    assert call_records[1]["prompt"] == probe_prompt
    assert argv_calls[1][:3] == [
        "--ask-for-approval",
        "on-request",
        "--model",
    ]
    assert argv_calls[1][argv_calls[1].index("exec") + 1] == "--skip-git-repo-check"
    assert codex_arg_value(argv_calls[1], "--model") == probe_call_config.model
    assert codex_arg_value(argv_calls[1], "--sandbox") == "workspace-write"
    assert "--approve-for-me" not in argv_calls[1]
    probe_config = codex_override_config(argv_calls[1])
    assert "approval_policy" not in probe_config
    assert probe_config["approvals_reviewer"] == "auto_review"
    assert probe_config["model_reasoning_effort"] == probe_call_config.reasoning_effort
    assert "--profile" not in argv_calls[1]
    assert "--json" in argv_calls[1]
    assert "--output-last-message" in argv_calls[1]
    assert argv_calls[1][-1] == "-"
    assert "resume" in argv_calls[2]
    assert "sess-1" in argv_calls[2]
    assert result.output_json == {"ok": True}
    call_entries = [
        (path, json.loads(path.read_text()))
        for path in sorted(
            (root / ".cmoc" / "gu" / "log" / "codex").glob("*/*_call.json")
        )
    ]
    call_logs = [log for _path, log in call_entries]
    assert [log["purpose"] for log in call_logs] == [
        "codex exec",
        "quota availability probe",
        "codex exec",
    ]
    probe_logs = [
        log for log in call_logs if log["purpose"] == "quota availability probe"
    ]
    probe_call_path = next(
        path
        for path, log in call_entries
        if log["purpose"] == "quota availability probe"
    )
    assert len(probe_logs) == 1
    assert probe_logs[0]["argv"][1:] == argv_calls[1]
    assert "profile_name" not in probe_logs[0]
    assert "profile_path" not in probe_logs[0]
    assert probe_logs[0]["model_provider"] == probe_call_config.model_provider
    assert probe_logs[0]["model"] == probe_call_config.model
    assert probe_logs[0]["reasoning_effort"] == probe_call_config.reasoning_effort
    assert probe_logs[0]["file_access_mode"] == "readonly"
    assert Path(probe_logs[0]["stdout_log_path"]).read_text().strip() == (
        '{"type": "turn.completed"}'
    )
    assert Path(probe_logs[0]["prompt_log_path"]).read_text() == probe_prompt
    assert Path(probe_logs[0]["stderr_log_path"]).read_text() == ""
    assert Path(probe_logs[0]["output_path"]).read_text() == '{"probe": true}'
    main_entries = [
        (path, log) for path, log in call_entries if log["purpose"] == "codex exec"
    ]
    main_logs = [log for _path, log in main_entries]
    assert len(main_logs) == 2
    assert [log["argv"][1:] for log in main_logs] == [argv_calls[0], argv_calls[2]]
    for log in main_logs:
        assert log["model_provider"] == base_call_config.model_provider
        assert log["model"] == base_call_config.model
        assert log["reasoning_effort"] == base_call_config.reasoning_effort
        assert log["file_access_mode"] == "pure_oracle_read"
    initial_log = next(log for log in main_logs if "resume" not in log["argv"])
    resume_log = next(log for log in main_logs if "resume" in log["argv"])
    resume_entry = next((path, log) for path, log in main_entries if log is resume_log)
    assert initial_log["argv"][1:] == argv_calls[0]
    assert resume_log["argv"][1:] == argv_calls[2]
    assert codex_arg_value(probe_logs[0]["argv"], "--model") == probe_call_config.model
    assert codex_arg_value(initial_log["argv"], "--model") == base_call_config.model
    assert codex_arg_value(initial_log["argv"], "--sandbox") == "workspace-write"
    assert codex_arg_value(resume_log["argv"], "--sandbox") == "workspace-write"
    assert "--profile" not in initial_log["argv"]
    assert "profile_name" not in initial_log
    assert "profile_path" not in initial_log
    assert len({log["stdout_log_path"] for log in main_logs}) == 2
    assert [Path(log["prompt_log_path"]).read_text() for log in main_logs] == [
        "prompt",
        "prompt",
    ]
    assert len({log["prompt_log_path"] for log in main_logs}) == 2
    assert Path(initial_log["stdout_log_path"]).read_text().strip() == (
        '{"type": "thread.started", "thread_id": "sess-1"}\n'
        '{"type": "error", "message": "Quota exceeded"}'
    )
    assert not Path(initial_log["output_path"]).with_suffix(".jsonl").exists()
    assert Path(resume_log["stdout_log_path"]).read_text().strip() == (
        '{"type": "turn.completed"}'
    )
    assert result.call_log_path == resume_entry[0]
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert [event["purpose"] for event in codex_events] == [
        "codex exec",
        "quota availability probe",
        "codex exec",
    ]
    assert [event["status"] for event in codex_events] == [
        "quota_waiting",
        "succeeded",
        "succeeded",
    ]
    assert codex_events[0]["returncode"] == 1
    assert codex_events[0]["stdout_log_path"] == main_logs[0]["stdout_log_path"]
    assert codex_events[0]["prompt_log_path"] == main_logs[0]["prompt_log_path"]
    assert codex_events[0]["output_path"] == main_logs[0]["output_path"]
    assert codex_events[1]["returncode"] == 0
    assert codex_events[1]["stdout_log_path"] == probe_logs[0]["stdout_log_path"]
    assert codex_events[1]["prompt_log_path"] == probe_logs[0]["prompt_log_path"]
    assert codex_events[1]["output_path"] == probe_logs[0]["output_path"]
    captured = capsys.readouterr()
    assert captured.out == ""
    assert str(probe_call_path) not in captured.err
    assert "Codex CLI の quota 回復待ち: 待機を継続" in captured.err
    assert "Codex CLI の quota 回復待ち: 復旧を確認。処理を再開" in captured.err


def test_run_codex_exec_logs_keyboard_interrupt_from_quota_probe(
    quota_control_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """代表 probe の KeyboardInterrupt をログへ記録して伝播する。"""
    root = quota_control_root
    probe_prompt = quota_probe_prompt(root)
    calls: list[str] = []

    def fake_run(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        """初回 quota 失敗後の代表 probe を KeyboardInterrupt にする。"""
        prompt = cast(TextIO, kwargs["stdin"]).read()
        calls.append(prompt)
        if prompt == "prompt":
            return subprocess.CompletedProcess(
                argv,
                1,
                '{"type":"thread.started","thread_id":"sess-1"}\n'
                '{"type":"error","message":"Quota exceeded"}\n',
                "",
            )
        raise KeyboardInterrupt

    monkeypatch.setattr(runtime_codex_exec, "run_codex_subprocess", fake_run)
    logger = SubcommandLogger(root, "test")

    with pytest.raises(KeyboardInterrupt):
        run_codex_exec(
            AgentCallParameter(
                "build_feedback_issue_normalization_request",
                FileAccessMode.READONLY,
                "prompt",
                None,
                root,
            ),
            root=root,
            quota_poll_interval_sec=0,
            config=CmocConfig(),
            subcommand_logger=logger,
        )

    assert calls == ["prompt", probe_prompt]
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "Codex CLI の quota 回復待ち: 待機を継続" in captured.err
    assert "quota availability probe" not in captured.err
    assert "KeyboardInterrupt" not in captured.err
    events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in events if event["event"] == "codex_call"]
    assert [event["purpose"] for event in codex_events] == [
        "codex exec",
        "quota availability probe",
    ]
    assert codex_events[0]["status"] == "quota_waiting"
    assert codex_events[1]["status"] == "failed"
    assert codex_events[1]["error"] == "KeyboardInterrupt()"


def test_quota_probe_uses_canonical_complete_prompt(
    quota_prompt_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """quota probe が正本 builder の完全 prompt と固有 call kind を使用する。"""
    root = quota_prompt_root
    base = AgentCallParameter(
        agent_call_kind="realization_edit",
        file_access_mode=FileAccessMode.REPO_WRITE,
        prompt="base",
        structured_output_schema_path=None,
        agent_call_cwd=root,
    )
    # {{work-root}}/spec/app_spec/codex_common_rule.md
    # 正本の生成結果を一度だけ作り、runtime が cwd を渡してそのまま返すことを確かめる。
    builder = Mock(return_value=build_canonical_quota_probe_parameter(root))
    monkeypatch.setattr(
        "oracle.request_builder.common.quota_probe.build_quota_availability_probe_request",
        builder,
    )
    probe = runtime_codex_exec._quota_availability_probe_parameter(base)

    builder.assert_called_once_with(root)
    assert probe is builder.return_value
    assert probe.agent_call_kind == "build_quota_availability_probe_request"
    assert probe.file_access_mode == FileAccessMode.READONLY
    assert probe.prompt
    assert "# feedback observation reporting" in probe.prompt
    assert probe.prompt.count("# feedback observation reporting") == 1
    assert "# routing policy" not in probe.prompt
    objective = probe.prompt.split('<cmoc_block id="objective">', 1)[1].split(
        "</cmoc_block>", 1
    )[0]
    assert "# task" in objective
    assert "Codex CLI の利用可能性を確認するため、短い応答を 1 回返す" in (objective)
    assert "# non-goals" in objective
    assert "追加の調査や作業を行わない" in objective
    assert "# scope" not in objective
    assert "# completion criteria" not in objective
    assert probe.structured_output_schema_path is None
    assert probe.enable_document_search_mcp is False
    assert probe.agent_call_cwd == base.agent_call_cwd


def test_run_codex_exec_reruns_after_quota_without_session_id(
    quota_control_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """session ID がない quota 復帰で同じ prompt を再実行する。"""
    root = quota_control_root
    probe_prompt = quota_probe_prompt(root)
    # argv・cwd とログ保存の結合は polls_and_resumes の代表ケースに残す。
    calls = script_codex_calls(
        monkeypatch,
        [
            (1, '{"type":"error","message":"Quota exceeded"}\n', None),
            (0, '{"type":"turn.completed"}\n', '{"probe": true}'),
            (0, '{"type":"turn.completed"}\n', '{"ok": true}'),
        ],
    )
    parameter = AgentCallParameter(
        "build_feedback_issue_normalization_request",
        FileAccessMode.READONLY,
        "prompt",
        None,
        root,
    )

    result = run_codex_exec(
        parameter,
        root=root,
        quota_poll_interval_sec=0,
        config=CmocConfig(),
    )

    assert [record["prompt"] for record in calls] == [
        "prompt",
        probe_prompt,
        "prompt",
    ]
    assert all("resume" not in record["argv"] for record in calls)
    assert result.output_json == {"ok": True}


@pytest.mark.parametrize("probe_returncode", [0, 2])
def test_quota_probe_non_quota_failure_fails_immediately(
    quota_control_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    probe_returncode: int,
) -> None:
    """代表 probe の quota 以外の失敗を伝播し、作業中の成果物を保持する。"""
    root = quota_control_root
    probe_prompt = quota_probe_prompt(root)
    artifact = root / "src" / "probe.py"

    def during_probe(index, _call):
        if index == 2:
            artifact.parent.mkdir()
            artifact.write_text("blocked\n")

    calls = script_codex_calls(
        monkeypatch,
        [
            (
                1,
                '{"type":"thread.started","thread_id":"sess-1"}\n'
                '{"type":"error","message":"Quota exceeded"}\n',
                None,
            ),
            (
                probe_returncode,
                '{"type":"error","message":"override is broken"}\n',
                None,
            ),
        ],
        on_call=during_probe,
    )
    parameter = AgentCallParameter(
        "build_feedback_issue_normalization_request",
        FileAccessMode.READONLY,
        "prompt",
        None,
        root,
    )
    logger = SubcommandLogger(root, "test")

    with pytest.raises(CmocError, match="回復確認 probe"):
        run_codex_exec(
            parameter,
            root=root,
            quota_poll_interval_sec=0,
            config=CmocConfig(),
            subcommand_logger=logger,
        )

    assert [record["prompt"] for record in calls] == [
        "prompt",
        probe_prompt,
    ]
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert [event["status"] for event in codex_events] == ["quota_waiting", "failed"]
    assert codex_events[1]["purpose"] == "quota availability probe"
    assert codex_events[1]["returncode"] == probe_returncode
    assert "override is broken" in codex_events[1]["error"]
    assert artifact.read_text() == "blocked\n"


def test_quota_probe_rejects_invalid_jsonl_with_zero_returncode_and_valid_output(
    quota_control_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """probe も valid output だけでは不正 stdout を成功扱いしない。"""
    root = quota_control_root
    probe_prompt = quota_probe_prompt(root)
    calls = script_codex_calls(
        monkeypatch,
        [
            (1, '{"type":"error","message":"Quota exceeded"}\n', None),
            (0, "not-json\n", '{"probe": true}'),
        ],
    )
    logger = SubcommandLogger(root, "test")

    with pytest.raises(CmocError) as exc_info:
        run_codex_exec(
            AgentCallParameter(
                "build_feedback_issue_normalization_request",
                FileAccessMode.READONLY,
                "prompt",
                None,
                root,
            ),
            root=root,
            quota_poll_interval_sec=0,
            config=CmocConfig(),
            subcommand_logger=logger,
        )

    assert "回復確認 probe" in str(exc_info.value)
    assert "malformed JSONL event (invalid JSON): not-json" not in exc_info.value.detail
    assert [record["prompt"] for record in calls] == ["prompt", probe_prompt]
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert [event["status"] for event in codex_events] == ["quota_waiting", "failed"]
    assert codex_events[1]["returncode"] == 0
    assert "malformed JSONL event (invalid JSON): not-json" in codex_events[1]["error"]


@pytest.mark.parametrize("probe_fails", [False, True], ids=["success", "failure"])
def test_parallel_quota_calls_share_probe_result(
    quota_control_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    probe_fails: bool,
) -> None:
    """代表 probe の成功・失敗を共有し、成功時だけ全 call を再開する。"""
    root = quota_control_root
    probe_prompt = quota_probe_prompt(root)
    calls: list[tuple[str, list[str]]] = []
    calls_lock = Lock()
    joined = Event()
    logger = SubcommandLogger(root, "test")
    log_event = logger.event

    def observe_recovery(kind: str, **fields: object) -> None:
        """待機側が代表と同じ回復 group に参加したことを通知する。"""
        log_event(kind, **fields)
        if kind == "codex_recovery" and fields.get("status") == "joined":
            joined.set()

    monkeypatch.setattr(logger, "event", observe_recovery)

    def fake_run(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        """CLI 入出力だけを代替し、並行する回復・再開処理は実行する。"""
        prompt = cast(TextIO, kwargs["stdin"]).read()
        assert prompt in {"prompt", probe_prompt}
        kind = (
            "resume"
            if "resume" in argv
            else "probe" if prompt == probe_prompt else "initial"
        )
        with calls_lock:
            calls.append((kind, argv))
        if kind == "initial":
            return subprocess.CompletedProcess(
                argv,
                1,
                '{"type":"thread.started","thread_id":"sess-parallel"}\n'
                '{"type":"error","message":"Quota exceeded"}\n',
                "",
            )
        if kind == "probe":
            # 固定 sleep ではなく、実際の参加を待ってから代表の結果を返す。
            assert joined.wait(timeout=5), "quota waiter did not join the probe"
            if probe_fails:
                return subprocess.CompletedProcess(
                    argv,
                    1,
                    '{"type":"error","message":"invalid configuration"}\n',
                    "",
                )
        output = Path(argv[argv.index("--output-last-message") + 1])
        output.write_text(
            json.dumps({"probe": True} if kind == "probe" else {"ok": True})
        )
        return subprocess.CompletedProcess(argv, 0, '{"type":"turn.completed"}\n', "")

    monkeypatch.setattr(runtime_codex_exec, "run_codex_subprocess", fake_run)
    parameter = AgentCallParameter(
        "build_feedback_issue_normalization_request",
        FileAccessMode.READONLY,
        "prompt",
        None,
        root,
    )

    def call_codex() -> object:
        """同じ条件の call を並行して quota 回復処理へ渡す。"""
        return run_codex_exec(
            parameter,
            root=root,
            quota_poll_interval_sec=0,
            config=CmocConfig(),
            subcommand_logger=logger,
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(call_codex) for _index in range(2)]
        errors = [future.exception(timeout=5) for future in futures]

    kinds = [kind for kind, _argv in calls]
    assert kinds.count("initial") == 2
    assert kinds.count("probe") == 1
    assert kinds.count("resume") == (0 if probe_fails else 2)
    recovery_events = [
        event for event in logger.event_records() if event["event"] == "codex_recovery"
    ]
    assert sum(event["status"] == "started" for event in recovery_events) == 1
    assert sum(event["status"] == "joined" for event in recovery_events) == 1
    assert len({event["recovery_id"] for event in recovery_events}) == 1
    if probe_fails:
        assert all(isinstance(error, CmocError) for error in errors)
    else:
        assert errors == [None, None]
        assert [future.result().output_json for future in futures] == [{"ok": True}] * 2
        assert all(
            codex_arg_value(argv, "resume") == "sess-parallel"
            for kind, argv in calls
            if kind == "resume"
        )


def test_session_id_returns_none_for_invalid_stdout_encoding(tmp_path: Path) -> None:
    """不正な UTF-8 の保存ログでは resume せず再実行する。"""
    log_path = tmp_path / "invalid_encoding.jsonl"
    log_path.write_bytes(b"\xff\n")

    assert runtime_codex_exec._extract_session_id_from_stdout_log(log_path) is None


def test_recovery_group_is_released_when_progress_output_fails(
    monkeypatch,
):
    """通知失敗が次の同条件 call の代表選択を妨げない。"""
    import commons.runtime_codex_recovery as recovery

    # CLI・prompt・ログとの結合は polls_and_resumes と parallel_quota_calls に残す。
    # 同じ key で失敗後に成功させ、古い group の例外を再送するだけの実装を検出する。
    key = (object(),)
    probe = Mock(return_value="succeeded")

    def wait():
        return recovery.wait_for_recovery(
            key=key,
            reason="quota",
            probe=probe,
            quota_interval=0,
            transient_interval=0,
            logger=None,
            agent_call_id="agent",
            stopped_codex_call_id="call",
            call_log_path="call.json",
        )

    def fail_print(*args, **kwargs):
        raise BrokenPipeError("closed output")

    with monkeypatch.context() as output_failure:
        output_failure.setattr(recovery, "print", fail_print, raising=False)
        with pytest.raises(BrokenPipeError, match="closed output"):
            wait()

    probe.assert_not_called()
    wait()
    probe.assert_called_once()
