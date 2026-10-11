"""出力補正、CLI failure、中断と作業差分の保持を検証する。"""

import json
import subprocess
from pathlib import Path
from unittest.mock import Mock

import pytest
from _codex_support import (
    codex_override_config,
    script_codex_calls,
    setup_codex_home,
    stub_codex_overrides,
)
from _command_support import write_python_executable
from _git_support import init_repo, run_git
from oracle.other.cmoc_config import DocumentSearchConfig

import cmoc_runtime
import commons.runtime_codex_exec as runtime_codex_exec
from basic.acp import AgentCallParameter, FileAccessMode
from cmoc_runtime import CmocError, SubcommandLogger
from commons.runtime_codex import run_codex_exec
from commons.runtime_results import StructuredOutputValidationIssue
from config.cmoc_config import CmocConfig


def test_run_codex_exec_corrects_schema_output_in_same_session(
    cli_repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capfd: pytest.CaptureFixture[str],
) -> None:
    """schema 不合格を同じ session で補正し、Codex call ごとの log を保存する。"""
    root = cli_repository
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    counter = tmp_path / "counter"
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, pathlib, sys, tomllib",
            "args = sys.argv[1:]",
            "if 'mcp' in args:",
            "    for arg in args:",
            "        if arg.startswith('mcp_servers.cmoc_document_search='):",
            "            server = tomllib.loads(arg)['mcp_servers']['cmoc_document_search']",
            "    transport = {'type': 'stdio', 'env_vars': [], **{key: server[key] for key in ('command', 'args', 'cwd', 'env')}}",
            "    print(json.dumps({'name': 'cmoc_document_search', 'transport': transport, **{key: server[key] for key in ('enabled', 'enabled_tools', 'disabled_tools', 'startup_timeout_sec', 'tool_timeout_sec')}}))",
            "    raise SystemExit(0)",
            f"counter = pathlib.Path({str(counter)!r})",
            "count = int(counter.read_text()) if counter.exists() else 0",
            "counter.write_text(str(count + 1))",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "payload = {'ok': True} if count else {'bad': True}",
            "output.write_text(json.dumps(payload))",
            "print('private stderr', file=sys.stderr)",
            "print(json.dumps({'type': 'thread.started', 'thread_id': 'session-1'}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    schema = tmp_path / "schema.json"
    schema.write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["ok"],
                "properties": {"ok": {"type": "boolean"}},
            }
        )
    )
    parameter = AgentCallParameter(
        "build_feedback_normalize_issue_parameter",
        FileAccessMode.READONLY,
        "prompt",
        schema,
        root,
        enable_document_search_mcp=True,
    )
    logger = SubcommandLogger(root, "test")

    result = run_codex_exec(
        parameter,
        root=root,
        transient_poll_interval_sec=0,
        config=CmocConfig(document_search=DocumentSearchConfig()),
        subcommand_logger=logger,
    )

    assert result.output_json == {"ok": True}
    assert counter.read_text() == "2"
    call_paths = sorted((root / ".cmoc" / "gu" / "log" / "codex").glob("*/*_call.json"))
    call_logs = [json.loads(path.read_text()) for path in call_paths]
    assert len(call_logs) == 2
    assert {log["agent_call_kind"] for log in call_logs} == {
        "build_feedback_normalize_issue_parameter"
    }
    assert len({log["agent_call_id"] for log in call_logs}) == 1
    assert len({log["codex_call_id"] for log in call_logs}) == 2
    for call in call_logs:
        server = codex_override_config(call["argv"])["mcp_servers"][
            "cmoc_document_search"
        ]
        context = json.loads(server["args"][-1])
        assert context["log_context"] == {
            "path": str(logger.path.resolve()),
            "command": logger.command,
            "execution_id": logger.execution_id,
            "codex_call_id": call["codex_call_id"],
        }
        assert context["work_root"] == str(root)
        tuning = DocumentSearchConfig()
        assert server["tool_timeout_sec"] > (
            tuning.search_request_timeout_seconds + tuning.shutdown_grace_seconds
        )
    assert [Path(log["output_path"]).read_text() for log in call_logs] == [
        '{"bad": true}',
        '{"ok": true}',
    ]
    for option in ("--cd", "--output-schema"):
        initial_option_index = call_logs[0]["argv"].index(option)
        correction_option_index = call_logs[1]["argv"].index(option)
        assert (
            call_logs[1]["argv"][correction_option_index + 1]
            == call_logs[0]["argv"][initial_option_index + 1]
        )
    prompts = [Path(log["prompt_log_path"]).read_text() for log in call_logs]
    assert prompts[0] == "prompt"
    assert prompts[1].startswith("# Structured Output の出力補正\n")
    assert "作業成果物を変更せず" in prompts[1]
    assert "完全な置換出力" in prompts[1]
    assert "違反した条件" in prompts[1]
    assert "対象 field または位置" in prompts[1]
    assert "期待値" in prompts[1]
    assert "観測値" in prompts[1]
    assert "resume" not in call_logs[0]["argv"]
    resume_index = call_logs[1]["argv"].index("resume")
    assert call_logs[1]["argv"][resume_index + 1] == "session-1"
    for key in (
        "model_provider",
        "model",
        "reasoning_effort",
        "cwd",
        "schema_path",
    ):
        assert call_logs[1][key] == call_logs[0][key]
    assert len({log["stdout_log_path"] for log in call_logs}) == 2
    assert len({log["stderr_log_path"] for log in call_logs}) == 2
    assert all(
        Path(log["stderr_log_path"]).read_text() == "private stderr\n"
        for log in call_logs
    )
    assert len({log["prompt_log_path"] for log in call_logs}) == 2
    assert result.call_log_path == call_paths[1]
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert [event["status"] for event in codex_events] == [
        "output_correction_requested",
        "succeeded",
    ]
    assert codex_events[0]["returncode"] == 0
    assert codex_events[0]["call_log_path"] == str(call_paths[0])
    assert len({event["agent_call_id"] for event in codex_events}) == 1
    assert len({event["codex_call_id"] for event in codex_events}) == 2
    captured = capfd.readouterr()
    assert captured.out == captured.err == ""


@pytest.mark.parametrize(
    ("output_bytes", "expected_error"),
    [
        pytest.param(None, "does not exist", id="missing"),
        pytest.param(b"", "is empty", id="empty"),
        pytest.param(b"{", "is not valid JSON", id="malformed"),
        pytest.param(
            b"[" * 10000 + b"0" + b"]" * 10000,
            "is not valid JSON",
            id="deeply_nested",
        ),
        pytest.param(b"NaN", "non-standard JSON constant", id="NaN"),
        pytest.param(b"Infinity", "non-standard JSON constant", id="Infinity"),
        pytest.param(
            b"-Infinity", "non-standard JSON constant", id="negative_Infinity"
        ),
        pytest.param(b"\xff", "decode", id="invalid_utf8"),
    ],
)
def test_structured_output_parse_failure_stops_before_schema_and_postcondition(
    tmp_path: Path,
    output_bytes: bytes | None,
    expected_error: str,
) -> None:
    """不正 JSON の境界値は、CLI を起動せず補正用の診断まで検証する。"""
    # parse failure の session 再開と log 保存は結合テストに残す。
    output_path = tmp_path / "output.json"
    if output_bytes is not None:
        output_path.write_bytes(output_bytes)
    schema_validator = Mock()
    postcondition = Mock()

    output, issues = runtime_codex_exec._validate_structured_output(
        output_path, schema_validator, postcondition, frozenset()
    )

    assert output is None
    [issue] = issues
    assert issue.condition == "JSON parse"
    assert issue.location
    assert issue.expected
    assert expected_error in issue.observed
    schema_validator.iter_errors.assert_not_called()
    postcondition.assert_not_called()


def test_run_codex_exec_corrects_declared_postcondition(
    cli_repository: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """初回 call の実差分で決定論的事後条件を検証し、出力だけを補正する。"""
    root = cli_repository
    (root / "README.md").write_text("# repo\n")
    # snapshot は index の追跡 file を読むため、履歴を作る必要はない。
    run_git(root, "add", "README.md")
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)

    def change_artifact(index, _call):
        if index == 1:
            (root / "README.md").write_text("first call change\n")

    # 差分取得・事後条件・補正は実行し、process の受け渡しは schema 補正の結合に残す。
    stdout = (
        '{"type":"thread.started","thread_id":"session-1"}\n{"type":"turn.completed"}\n'
    )
    calls = script_codex_calls(
        monkeypatch,
        [
            (0, stdout, '{"paths": []}'),
            (0, stdout, '{"paths": ["README.md"]}'),
        ],
        on_call=change_artifact,
    )
    schema = tmp_path / "postcondition_schema.json"
    schema.write_text(
        json.dumps(
            {
                "type": "object",
                "required": ["paths"],
                "properties": {"paths": {"type": "array", "items": {"type": "string"}}},
            }
        )
    )

    def validate_paths(
        output: object, changed_paths: frozenset[str]
    ) -> tuple[StructuredOutputValidationIssue, ...]:
        """初回 prompt が宣言した path 集合照合を再現する。"""
        assert isinstance(output, dict)
        observed = frozenset(output["paths"])
        if observed == changed_paths:
            return ()
        return (
            StructuredOutputValidationIssue(
                condition="paths が実際の変更 path 集合と一致する",
                location="paths",
                expected=repr(sorted(changed_paths)),
                observed=repr(sorted(observed)),
            ),
        )

    result = run_codex_exec(
        AgentCallParameter(
            "build_feedback_normalize_issue_parameter",
            FileAccessMode.REALIZATION_WRITE,
            "prompt",
            schema,
            root,
        ),
        root=root,
        config=CmocConfig(),
        structured_output_postcondition=validate_paths,
    )

    assert result.output_json == {"paths": ["README.md"]}
    assert len(calls) == 2
    assert (root / "README.md").read_text() == "first call change\n"


def test_run_codex_exec_does_not_replace_missing_correction_session(
    cli_repository: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """session ID を取得できない出力契約違反を新しい session で代替しない。"""
    root = cli_repository
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    # process の入出力は corrects_schema_output_in_same_session に残す。
    calls = script_codex_calls(
        monkeypatch, [(0, '{"type":"turn.completed"}\n', '{"bad": true}')]
    )
    schema = tmp_path / "missing_session_schema.json"
    schema.write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["ok"],
                "properties": {"ok": {"type": "boolean"}},
            }
        )
    )

    with pytest.raises(CmocError, match="Structured Output 検証") as error:
        run_codex_exec(
            AgentCallParameter(
                "build_feedback_normalize_issue_parameter",
                FileAccessMode.READONLY,
                "prompt",
                schema,
                root,
            ),
            root=root,
            config=CmocConfig(),
        )

    assert len(calls) == 1
    assert "session ID is unavailable" in error.value.detail


def test_run_codex_exec_restores_artifacts_changed_by_correction(
    cli_repository: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """補正 turn が変動させた成果物を初回 call 完了時へ戻して失敗する。"""
    root = cli_repository
    (root / "README.md").write_text("# repo\n")
    (root / "oracle").mkdir()
    (root / "oracle" / "spec.md").write_text("# spec\n")
    run_git(root, "add", "README.md", "oracle/spec.md")
    nested = root / "nested"
    nested.mkdir()
    init_repo(nested)
    nested_file = nested / "tracked.txt"
    nested_file.write_text("nested initial\n")
    run_git(nested, "add", "tracked.txt")
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)

    def change_artifacts(index, _call):
        if index == 1:
            (root / "README.md").write_text("first call change\n")
        else:
            (root / "README.md").write_text("correction change\n")
            nested_file.write_text("correction-only\n")
            (root / "extra.py").write_text("correction-only\n")
            (root / "oracle" / "spec.md").unlink()

    # Git 差分取得・復元は実行し、process の入出力は schema 補正の結合に残す。
    stdout = (
        '{"type":"thread.started","thread_id":"session-1"}\n{"type":"turn.completed"}\n'
    )
    calls = script_codex_calls(
        monkeypatch,
        [
            (0, stdout, '{"bad": true}'),
            (0, stdout, '{"ok": true}'),
        ],
        on_call=change_artifacts,
    )
    schema = tmp_path / "artifact_change_schema.json"
    schema.write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["ok"],
                "properties": {"ok": {"type": "boolean"}},
            }
        )
    )
    logger = SubcommandLogger(root, "test")

    with pytest.raises(CmocError, match="作業成果物を変更"):
        run_codex_exec(
            AgentCallParameter(
                "build_feedback_normalize_issue_parameter",
                FileAccessMode.REALIZATION_WRITE,
                "prompt",
                schema,
                root,
            ),
            root=root,
            config=CmocConfig(),
            subcommand_logger=logger,
        )

    assert len(calls) == 2
    assert (root / "README.md").read_text() == "first call change\n"
    assert nested_file.read_text() == "nested initial\n"
    assert not (root / "extra.py").exists()
    assert (root / "oracle" / "spec.md").read_text() == "# spec\n"
    events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in events if event["event"] == "codex_call"]
    assert [event["status"] for event in codex_events] == [
        "output_correction_requested",
        "output_correction_failed",
    ]


def test_run_codex_exec_logs_keyboard_interrupt(
    cli_repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """KeyboardInterrupt を failed call event として記録し、例外を伝播する。"""
    root = cli_repository
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)

    def interrupt(*_args: object, **_kwargs: object) -> object:
        """Codex subprocess 呼び出しを KeyboardInterrupt で中断する fake。"""
        raise KeyboardInterrupt

    monkeypatch.setattr(runtime_codex_exec, "run_codex_subprocess", interrupt)
    logger = SubcommandLogger(root, "test")

    with pytest.raises(KeyboardInterrupt):
        run_codex_exec(
            AgentCallParameter(
                "build_feedback_normalize_issue_parameter",
                FileAccessMode.READONLY,
                "prompt",
                None,
                root,
            ),
            root=root,
            config=CmocConfig(),
            subcommand_logger=logger,
        )

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
    call_logs = list((root / ".cmoc" / "gu" / "log" / "codex").glob("*/*_call.json"))
    events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in events if event["event"] == "codex_call"]
    assert len(call_logs) == 1
    assert len(codex_events) == 1
    assert codex_events[0]["status"] == "failed"
    assert codex_events[0]["returncode"] is None
    assert codex_events[0]["error"] == "KeyboardInterrupt()"


def test_run_codex_exec_corrects_structured_output_parse_failure(
    cli_repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """parse failure を同じ session で補正し、元の出力と診断を保持する。"""
    root = cli_repository
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    # parse と補正・ログ保存を検証し、process の受け渡しは schema 補正の結合に残す。
    stdout = (
        '{"type":"thread.started","thread_id":"session-1"}\n{"type":"turn.completed"}\n'
    )
    calls = script_codex_calls(
        monkeypatch,
        [(0, stdout, "NaN"), (0, stdout, "1")],
    )
    schema = tmp_path / "parse_failure_schema.json"
    schema.write_text(json.dumps({"type": "number"}))
    parameter = AgentCallParameter(
        "build_feedback_normalize_issue_parameter",
        FileAccessMode.READONLY,
        "prompt",
        schema,
        root,
    )
    logger = SubcommandLogger(root, "test")

    result = run_codex_exec(
        parameter,
        root=root,
        transient_poll_interval_sec=0,
        config=CmocConfig(),
        subcommand_logger=logger,
    )

    assert result.output_json == 1
    assert result.output_text == "1"
    assert len(calls) == 2
    call_logs = [
        json.loads(path.read_text())
        for path in sorted(result.call_log_path.parent.glob("*_call.json"))
    ]
    assert "resume" not in call_logs[0]["argv"]
    resume_index = call_logs[1]["argv"].index("resume")
    assert call_logs[1]["argv"][resume_index + 1] == "session-1"
    assert [Path(log["output_path"]).read_text() for log in call_logs] == [
        "NaN",
        "1",
    ]
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert [event["status"] for event in codex_events] == [
        "output_correction_requested",
        "succeeded",
    ]
    assert "non-standard JSON constant" in codex_events[0]["error"]


@pytest.mark.parametrize(
    "schema_bytes", [b"{", b'{"$schema": 1}', b'{"minimum": NaN}', b"\xff"]
)
def test_run_codex_exec_rejects_invalid_schema_before_codex_call(
    cli_repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    schema_bytes: bytes,
) -> None:
    """不正な Structured Output schema は Codex 呼び出し前に失敗させる。"""
    root = cli_repository
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    schema = tmp_path / "invalid_schema.json"
    schema.write_bytes(schema_bytes)
    calls = 0

    def fail_run(*_args: object, **_kwargs: object) -> object:
        """ローカル schema エラーで Codex が起動されないことを検証する。"""
        nonlocal calls
        calls += 1
        raise AssertionError("Codex must not run for an invalid schema")

    monkeypatch.setattr(runtime_codex_exec, "run_codex_subprocess", fail_run)

    with pytest.raises(CmocError, match="Structured Output schema"):
        run_codex_exec(
            AgentCallParameter(
                "build_feedback_normalize_issue_parameter",
                FileAccessMode.READONLY,
                "prompt",
                schema,
                root,
            ),
            root=root,
            config=CmocConfig(),
        )

    assert calls == 0


@pytest.mark.parametrize(
    "failure_event",
    [
        {"type": "error", "message": "Selected model is at capacity"},
        {
            "type": "turn.failed",
            "error": {"message": "Selected model is at capacity"},
        },
    ],
)
@pytest.mark.parametrize("failure_returncode", [0, 1])
def test_run_codex_exec_logs_capacity_recovery_calls(
    cli_repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure_event: dict[str, object],
    failure_returncode: int,
) -> None:
    """capacity 診断と終了 code の組合せごとに、待機・probe・再実行を記録する。"""
    root = cli_repository
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    # JSONL 分類と log は実処理し、process 受け渡しは既存の結合テストへ委ねる。
    prompts = []

    def fake_run(argv, **kwargs):
        prompts.append(kwargs["stdin"].read())
        if len(prompts) == 1:
            return subprocess.CompletedProcess(
                argv, failure_returncode, json.dumps(failure_event) + "\n", ""
            )
        output = Path(argv[argv.index("--output-last-message") + 1])
        output.write_text(json.dumps({"ok": True}), encoding="utf-8")
        return subprocess.CompletedProcess(argv, 0, '{"type":"turn.completed"}\n', "")

    monkeypatch.setattr(runtime_codex_exec, "run_codex_subprocess", fake_run)
    parameter = AgentCallParameter(
        "build_feedback_normalize_issue_parameter",
        FileAccessMode.READONLY,
        "prompt",
        None,
        root,
    )
    logger = SubcommandLogger(root, "test")

    result = run_codex_exec(
        parameter,
        root=root,
        transient_poll_interval_sec=0,
        config=CmocConfig(),
        subcommand_logger=logger,
    )

    assert result.output_json == {"ok": True}
    assert len(prompts) == 3
    assert prompts[0] == prompts[2] == parameter.prompt
    assert prompts[1] != parameter.prompt
    call_paths = sorted((root / ".cmoc" / "gu" / "log" / "codex").glob("*/*_call.json"))
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert [event["status"] for event in codex_events] == [
        "transient_waiting",
        "succeeded",
        "succeeded",
    ]
    assert codex_events[0]["returncode"] == failure_returncode
    assert codex_events[0]["call_log_path"] == str(call_paths[0])
    assert "Selected model is at capacity" in codex_events[0]["error"]


@pytest.mark.parametrize(
    "event",
    [
        {"type": "error", "message": "unexpected failure"},
        {"type": "turn.failed", "error": {"message": "unexpected failure"}},
    ],
)
@pytest.mark.parametrize("structured_output", [False, True])
def test_run_codex_exec_fails_on_unknown_jsonl_error_with_zero_returncode(
    cli_repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    event: dict[str, object],
    structured_output: bool,
) -> None:
    """未知の JSONL error は終了コード 0 でも即時失敗させ、再試行しない。"""
    root = cli_repository
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    # JSONL の読み取り・分類と log は実処理し、process 起動は結合テストに残す。
    calls = script_codex_calls(
        monkeypatch, [(0, json.dumps(event) + "\n", '{"ok": true}')]
    )
    schema: Path | None = None
    if structured_output:
        schema = tmp_path / "schema.json"
        schema.write_text("{}")
    logger = SubcommandLogger(root, "test")

    with pytest.raises(CmocError, match="Codex CLI 呼び出しが失敗しました") as error:
        run_codex_exec(
            AgentCallParameter(
                "build_feedback_normalize_issue_parameter",
                FileAccessMode.READONLY,
                "prompt",
                schema,
                root,
            ),
            root=root,
            config=CmocConfig(),
            subcommand_logger=logger,
        )

    assert "unexpected failure" not in error.value.detail
    assert len(calls) == 1
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert [event["status"] for event in codex_events] == ["failed"]
    assert codex_events[0]["returncode"] == 0
    assert "unexpected failure" in codex_events[0]["error"]


def test_run_codex_exec_keeps_agent_diff_after_capacity_recovery(
    cli_repository: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """capacity 回復待ち を挟んでも Codex が作った agent diff を保持する。"""
    # 初回 call が作る未追跡 file の保持を検証するため、初期 commit は不要。
    root = cli_repository
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    monkeypatch.setattr(cmoc_runtime.time, "sleep", lambda _seconds: None)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    counter = tmp_path / "counter"
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, pathlib, sys",
            f"counter = pathlib.Path({str(counter)!r})",
            "count = int(counter.read_text()) if counter.exists() else 0",
            "counter.write_text(str(count + 1))",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "blocked = pathlib.Path('src/blocked.py')",
            "blocked.parent.mkdir(exist_ok=True)",
            "if count == 0:",
            "    blocked.write_text('blocked\\n')",
            (
                "    print(json.dumps({'type': 'error', "
                "'message': 'Selected model is at capacity'}))"
            ),
            "    sys.exit(1)",
            "output.write_text(json.dumps({'ok': True}) + '\\n')",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_exec(
        AgentCallParameter(
            "build_feedback_normalize_issue_parameter",
            FileAccessMode.REALIZATION_WRITE,
            "prompt",
            None,
            root,
        ),
        root=root,
        transient_poll_interval_sec=0,
        config=CmocConfig(),
    )

    assert counter.read_text() == "3"
    assert (root / "src" / "blocked.py").read_text() == "blocked\n"


def test_run_codex_exec_ignores_error_markers_outside_stdout_jsonl(
    cli_repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """stdout JSONL 外の error marker を retry 判定に使わず、直接失敗させる。"""
    root = cli_repository
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    monkeypatch.setattr(cmoc_runtime.time, "sleep", lambda _seconds: None)
    parameter = AgentCallParameter(
        "build_feedback_normalize_issue_parameter",
        FileAccessMode.READONLY,
        "prompt",
        None,
        root,
    )
    cases = [
        (
            "Selected model is at capacity",
            "",
            {"transient_poll_interval_sec": 0},
        ),
        (
            "Quota exceeded",
            "Quota exceeded\n",
            {"quota_poll_interval_sec": 0},
        ),
    ]
    # stdout/stderr の分類と非公開化を実行し、process I/O は exec の結合テストに残す。
    for expected_detail, stdout_text, kwargs in cases:

        def fake_run(argv, **_kwargs):
            return subprocess.CompletedProcess(
                argv, 1, stdout_text, expected_detail + "\n"
            )

        codex_call = Mock(side_effect=fake_run)
        monkeypatch.setattr(runtime_codex_exec, "run_codex_subprocess", codex_call)
        with pytest.raises(CmocError) as error:
            run_codex_exec(parameter, root=root, config=CmocConfig(), **kwargs)
        assert error.value.summary == "Codex CLI 呼び出しが失敗しました。"
        assert expected_detail not in error.value.detail
        captured = capsys.readouterr()
        assert expected_detail not in captured.out
        assert expected_detail not in captured.err
        codex_call.assert_called_once()


def test_run_codex_exec_stops_after_output_correction_limit(
    cli_repository: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """補正を 2 回で終え、正式出力の受理失敗を元の call と対応付ける。"""
    root = cli_repository
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    sleep_calls: list[float] = []
    monkeypatch.setattr(
        runtime_codex_exec.time, "sleep", lambda seconds: sleep_calls.append(seconds)
    )
    # 補正回数の制御と診断を検証し、process の受け渡しは成功系に残す。
    calls = script_codex_calls(
        monkeypatch,
        [
            (
                0,
                '{"type":"thread.started","thread_id":"session-1"}\n'
                '{"type":"turn.completed"}\n',
                '{"bad": true}',
            )
        ]
        * 3,
    )
    schema = tmp_path / "schema.json"
    schema.write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["ok"],
                "properties": {"ok": {"type": "boolean"}},
            }
        )
    )
    logger = SubcommandLogger(root, "test")

    with pytest.raises(CmocError, match="Structured Output 検証") as error:
        run_codex_exec(
            AgentCallParameter(
                "build_feedback_normalize_issue_parameter",
                FileAccessMode.READONLY,
                "prompt",
                schema,
                root,
            ),
            root=root,
            config=CmocConfig(),
            subcommand_logger=logger,
        )

    assert len(calls) == 3
    assert "resume" not in calls[0]["argv"]
    for call in calls[1:]:
        resume_index = call["argv"].index("resume")
        assert call["argv"][resume_index + 1] == "session-1"
    assert sleep_calls == []
    assert "`additionalProperties`" in error.value.detail
    call_paths = sorted((root / ".cmoc" / "gu" / "log" / "codex").glob("*/*_call.json"))
    assert len(call_paths) == 3
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert [event["status"] for event in codex_events] == [
        "output_correction_requested",
        "output_correction_requested",
        "structured_output_validation_failed",
    ]
    assert [event["call_log_path"] for event in codex_events] == [
        str(path) for path in call_paths
    ]
    diagnostics = [
        event
        for event in log_events
        if event.get("event_type") == "codex.structured_output_validation_exhausted"
    ]
    [diagnostic] = diagnostics
    call_logs = [json.loads(path.read_text()) for path in call_paths]
    assert diagnostic["event_schema_version"] == 1
    assert diagnostic["agent_call_kind"] == "build_feedback_normalize_issue_parameter"
    assert diagnostic["agent_call_id"] == call_logs[-1]["agent_call_id"]
    assert diagnostic["codex_call_id"] == call_logs[-1]["codex_call_id"]
    assert diagnostic["last_failure_stage"] == "schema_validation"
    assert diagnostic["schema_sha256"]
