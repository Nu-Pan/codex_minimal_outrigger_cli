"""出力補正、CLI failure、中断と作業差分の保持を検証する。"""

import json
import subprocess
from pathlib import Path
from unittest.mock import Mock

import oracle.other.path_model as path_model_module
import pytest
from _acp_builder_support import oracle_schema_path
from _codex_support import (
    codex_override_config,
    script_codex_calls,
    setup_codex_home,
    stub_codex_overrides,
)
from _git_support import init_repo, run_git
from oracle.other.cmoc_config import DocumentSearchConfig

import cmoc_runtime
import commons.runtime_codex_exec as runtime_codex_exec
from basic.acp import AgentCallParameter, FileAccessMode
from cmoc_runtime import CmocError, SubcommandLogger
from commons.runtime_codex import run_codex_exec
from commons.runtime_git import WorktreeSnapshot
from commons.runtime_results import StructuredOutputValidationIssue
from config.cmoc_config import CmocConfig


@pytest.fixture
def failure_control_root(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    nonpersistent_codex_ids: None,
) -> Path:
    """応答・回復制御の検査では Git 探索と永続採番を準備しない。"""
    root = tmp_path / "repo"
    root.mkdir()
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    # cwd・linked worktree の解決は test_codex_runtime_paths.py、
    # probe の実結合は quota_retry に残す。
    # 成果物の差分取得・復元を検査するケースは実 Git の cli_repository を使う。
    monkeypatch.setattr(
        path_model_module, "_resolve_git_worktree_roots", lambda _cwd: (root, root)
    )
    return root


@pytest.fixture
def output_only_root(
    failure_control_root: Path, monkeypatch: pytest.MonkeyPatch
) -> Path:
    """成果物を操作しない出力検証では、snapshot を空の状態として扱う。"""
    # 実 Git の差分取得・補正時の復元は corrects_declared_postcondition と
    # restores_artifacts_changed_by_correction に残す。
    monkeypatch.setattr(
        runtime_codex_exec,
        "capture_worktree_snapshot",
        lambda work_root: WorktreeSnapshot(work_root, ()),
    )
    return failure_control_root


def test_run_codex_exec_corrects_schema_output_in_same_session(
    output_only_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """schema 不合格を同じ session で補正し、Codex call ごとの log を保存する。"""
    # 実 process の stdin・stdout・stderr は test_codex_runtime_exec.py に残す。
    # 補正では実際に渡す argv・本文と保存済み log を照合し、子起動と回数 file を省く。
    root = output_only_root
    roots = Mock(return_value=(root, root))
    monkeypatch.setattr(path_model_module, "_resolve_git_worktree_roots", roots)
    stdout = (
        '{"type": "thread.started", "thread_id": "session-1"}\n'
        '{"type": "turn.completed"}\n'
    )
    calls = script_codex_calls(
        monkeypatch,
        [(0, stdout, '{"bad": true}'), (0, stdout, '{"ok": true}')],
        stderr="private stderr\n",
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
    roots.assert_called_once_with(root)
    assert len(calls) == 2
    call_paths = sorted((root / ".cmoc" / "gu" / "log" / "codex").glob("*/*_call.json"))
    call_logs = [json.loads(path.read_text()) for path in call_paths]
    assert len(call_logs) == 2
    assert [log["argv"] for log in call_logs] == [call["argv"] for call in calls]
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
        assert server["cwd"] == str(root)
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
    assert prompts == [call["prompt"] for call in calls]
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
    assert all(Path(log["stdout_log_path"]).read_text() == stdout for log in call_logs)
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
    captured = capsys.readouterr()
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

    _text, output, issues = runtime_codex_exec._validate_structured_output(
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
    cli_repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    nonpersistent_codex_ids: None,
) -> None:
    """初回 call の実差分で決定論的事後条件を検証し、出力だけを補正する。"""
    root = cli_repository
    (root / "README.md").write_text("# repo\n")
    # 非 ignore file の実差分で照合できるため、staging や履歴は準備しない。
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
    output_only_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """session ID を取得できない出力契約違反を新しい session で代替しない。"""
    root = output_only_root
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
    cli_repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    nonpersistent_codex_ids: None,
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
    # 事後条件なしの開始前読み取りを拒否し、補正前の状態取得と復元は実行する。
    capture_snapshot = runtime_codex_exec.capture_worktree_snapshot

    def capture_after_initial_call(work_root):
        assert calls, "no postcondition needs a pre-call artifact snapshot"
        return capture_snapshot(work_root)

    monkeypatch.setattr(
        runtime_codex_exec, "capture_worktree_snapshot", capture_after_initial_call
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
    failure_control_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """KeyboardInterrupt を failed call event として記録し、例外を伝播する。"""
    root = failure_control_root

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
    output_only_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """parse failure を同じ session で補正し、元の出力と診断を保持する。"""
    root = output_only_root
    # 検証済み本文の再読み取りを検出し、補正・保存の既存ケースで I/O 回帰も守る。
    output_reads: list[Path] = []
    original_open = Path.open

    def record_output_read(path, mode="r", *args, **kwargs):
        if path.name.endswith("_output.json") and "r" in mode:
            output_reads.append(path)
        return original_open(path, mode, *args, **kwargs)

    monkeypatch.setattr(Path, "open", record_output_read)
    # parse と補正・ログ保存を検証し、process の受け渡しは schema 補正の結合に残す。
    stdout = (
        '{"type":"thread.started","thread_id":"session-1"}\n{"type":"turn.completed"}\n'
    )
    calls = script_codex_calls(
        monkeypatch,
        [(0, stdout, "NaN"), (0, stdout, " 1 \n")],
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
    assert result.output_text == " 1 \n"
    assert output_reads.count(result.output_path) == 1
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
        " 1 \n",
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
    failure_control_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    schema_bytes: bytes,
) -> None:
    """不正な Structured Output schema は Codex 呼び出し前に失敗させる。"""
    root = failure_control_root
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


def test_run_codex_exec_rechecks_schema_source_and_each_output(
    output_only_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """検証器を再利用しても、別 call の不正出力と source の更新・破損を検出する。"""
    root = output_only_root
    schema = tmp_path / "schema.json"
    schema_text = oracle_schema_path("feedback", "normalize_issue.json").read_text(
        encoding="utf-8"
    )
    schema.write_text(schema_text, encoding="utf-8")
    valid = {"result": {"decision": "new", "existing_issue_id": None}}
    invalid = {"result": {"decision": "existing", "existing_issue_id": None}}
    updated = {**valid, "new_field": None}
    calls = script_codex_calls(
        monkeypatch,
        [
            (0, '{"type":"turn.completed"}\n', json.dumps(output))
            for output in (valid, invalid, updated)
        ],
    )
    parameter = AgentCallParameter(
        "build_feedback_normalize_issue_parameter",
        FileAccessMode.READONLY,
        "prompt",
        schema,
        root,
        enable_feedback_reporting=False,
    )
    config = CmocConfig()

    assert run_codex_exec(parameter, root=root, config=config).output_json == valid
    with pytest.raises(CmocError, match="Structured Output 検証"):
        run_codex_exec(parameter, root=root, config=config)

    definition = json.loads(schema_text)
    definition["properties"]["new_field"] = {"type": "null"}
    definition["required"].append("new_field")
    schema.write_text(json.dumps(definition), encoding="utf-8")
    assert run_codex_exec(parameter, root=root, config=config).output_json == updated

    schema.write_text("{", encoding="utf-8")
    with pytest.raises(CmocError, match="Structured Output schema"):
        run_codex_exec(parameter, root=root, config=config)
    assert len(calls) == 3


@pytest.mark.parametrize("failure_returncode", [0, 1])
def test_run_codex_exec_logs_capacity_recovery_calls(
    failure_control_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure_returncode: int,
) -> None:
    """終了 code ごとに、capacity の待機・probe・再実行を記録する。"""
    root = failure_control_root
    # 診断形式の組合せは recovery の test_failure_diagnostic_classification に集約する。
    # ここでは分類から回復・log 保存までを通し、終了 code の記録も検査する。
    prompts = []

    def fake_run(argv, **kwargs):
        prompts.append(kwargs["stdin"].read())
        if len(prompts) == 1:
            return subprocess.CompletedProcess(
                argv,
                failure_returncode,
                '{"type":"error","message":"Selected model is at capacity"}\n',
                "",
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


@pytest.mark.parametrize("structured_output", [False, True])
def test_run_codex_exec_fails_on_unknown_jsonl_error_with_zero_returncode(
    failure_control_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    structured_output: bool,
) -> None:
    """未知の JSONL error は終了コード 0 でも即時失敗させ、再試行しない。"""
    root = failure_control_root
    # 診断形式の組合せは recovery の test_failure_diagnostic_classification に集約する。
    # schema の有無によらず、分類から即時失敗・診断の非公開化までを検査する。
    calls = script_codex_calls(
        monkeypatch,
        [
            (
                0,
                '{"type":"turn.failed","error":{"message":"unexpected failure"}}\n',
                '{"ok": true}',
            )
        ],
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
    failure_control_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """capacity 回復待ち を挟んでも Codex が作った agent diff を保持する。"""
    root = failure_control_root
    blocked = root / "src" / "blocked.py"

    def retain_artifact(index, _call):
        if index == 1:
            blocked.parent.mkdir()
            blocked.write_text("blocked\n")
        else:
            assert blocked.read_text() == "blocked\n"

    # 実ファイルと回復制御は保ち、process 受け渡しは既存の結合テストへ委ねる。
    stdout = '{"type":"turn.completed"}\n'
    calls = script_codex_calls(
        monkeypatch,
        [
            (
                1,
                '{"type":"error","message":"Selected model is at capacity"}\n',
                None,
            ),
            (0, stdout, '{"ok":true}\n'),
            (0, stdout, '{"ok":true}\n'),
        ],
        on_call=retain_artifact,
    )

    result = run_codex_exec(
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

    assert len(calls) == 3
    assert calls[0]["prompt"] == calls[2]["prompt"] == "prompt"
    assert calls[1]["prompt"] != "prompt"
    assert result.output_json == {"ok": True}
    assert blocked.read_text() == "blocked\n"


def test_run_codex_exec_ignores_error_markers_outside_stdout_jsonl(
    failure_control_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """stdout JSONL 外の error marker を retry 判定に使わず、直接失敗させる。"""
    root = failure_control_root
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
    output_only_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """補正を 2 回で終え、正式出力の受理失敗を元の call と対応付ける。"""
    root = output_only_root
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
