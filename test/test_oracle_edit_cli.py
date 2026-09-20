"""`cmoc oracle edit` の main-worktree exec 制御を検証する。

根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md
{{work-root}}/oracle/src/oracle/acp_builder/oracle/edit/launch_exec.py

成功時と各失敗時で同じ editor、Git 差分、session state、および通知境界を比較する。
分割すると同じ invocation の前提と不変条件が重複するため、一つの制御テストに保つ。
"""

import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from _cli_support import run_doctor, runner, terminal_primary_report
from _codex_support import FakeCodexResult, codex_override_config, setup_codex_home
from _git_support import current_branch, make_repo, run_git

import commons.runtime_cli as runtime_cli_module
import commons.runtime_codex_preflight as codex_preflight_module
import sub_commands.oracle.edit as oracle_edit_module
from basic.acp import AgentCallParameter, FileAccessMode
from cmoc_runtime import CmocError
from commons.runtime_codex_profile import build_codex_override_args
from commons.runtime_config import config_path
from commons.runtime_state import (
    RunPart,
    SessionPart,
    SessionState,
    state_path,
    write_state,
)
from main import app


@pytest.fixture(autouse=True)
def reset_indexing_preflight() -> Iterator[None]:
    """各 test の前後で indexing preflight の process-local state を初期化する。"""
    codex_preflight_module.disable_indexing_preflight()
    yield
    codex_preflight_module.disable_indexing_preflight()


def _activate_session(
    root: Path,
    *,
    session_state: str = "active",
    run: RunPart | None = None,
) -> tuple[str, Path]:
    """隔離 repository に oracle edit 用の session state を作成する。"""
    home_branch = current_branch(root)
    fork_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    session_id = "oracle-edit-test"
    session_branch = f"cmoc/session/{session_id}"
    run_git(root, "checkout", "-b", session_branch)
    path = state_path(root, session_id)
    write_state(
        path,
        SessionState(
            SessionPart(session_state, home_branch, fork_commit, None),
            run or RunPart(),
        ),
    )
    return session_branch, path


def _prepared_repo(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Path:
    """doctor 済みの隔離 repository を準備する。"""
    setup_codex_home(tmp_path, monkeypatch)
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    run_doctor(root)
    return root


def _assert_exec_parameter(
    parameter: AgentCallParameter,
    root: Path,
) -> None:
    """2 回の exec に共通する起動契約を検証する。"""
    assert parameter.file_access_mode == FileAccessMode.PURE_ORACLE_WRITE
    assert parameter.structured_output_schema_path is None
    assert parameter.run_indexing_preflight is False
    assert parameter.agent_call_cwd == root.resolve()


@pytest.mark.parametrize(
    "failure_stage",
    [None, "first", "second"],
    ids=["success", "first-failure", "second-failure"],
)
@pytest.mark.parametrize("first_changes", [True, False], ids=["edit", "no-change"])
def test_oracle_edit_runs_two_exec_calls_and_preserves_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure_stage: str | None,
    first_changes: bool,
) -> None:
    """既存差分を保ち、初回成功時は変更の有無によらず同じ入力で再実行する。"""
    root = _prepared_repo(tmp_path, monkeypatch)
    active_run = RunPart(
        "running",
        "realization_apply",
        "cmoc/run/oracle-edit-test/active-run",
        "abc",
    )
    _session_branch, session_state_path = _activate_session(root, run=active_run)
    state_before = json.loads(session_state_path.read_text())
    readme_path = root / "README.md"
    readme_path.write_text("# staged change\n")
    run_git(root, "add", "README.md")
    readme_path.write_text("# unstaged change\n")
    staged_diff_before = run_git(root, "diff", "--cached", "--", "README.md").stdout
    unstaged_diff_before = run_git(root, "diff", "--", "README.md").stdout
    time_stamp = "2026-07-20_00-00-00_000000000"
    editor_work_path = root / ".cmoc" / "gu" / "editor_input" / f"{time_stamp}_orig.md"
    input_copy_path = (
        root / ".cmoc" / "gu" / "log" / "editor_input" / f"{time_stamp}_orig.md"
    )
    editor_work_path.parent.mkdir(parents=True, exist_ok=True)
    input_copy_path.parent.mkdir(parents=True, exist_ok=True)
    editor_calls: list[tuple[Path, Path, str]] = []
    built_main_parameters: list[AgentCallParameter] = []
    events: list[str] = []
    notifications: list[tuple[str, Path, str]] = []

    real_run_doctor_preprocess = runtime_cli_module.run_doctor_preprocess

    def record_run_doctor_preprocess(
        target_root: Path,
        *,
        sync_refactor_entries: bool = True,
    ) -> None:
        """対象 invocation の doctor preprocess を記録して本来の処理へ委譲する。"""
        assert target_root == root
        events.append("doctor")
        real_run_doctor_preprocess(
            target_root,
            sync_refactor_entries=sync_refactor_entries,
        )

    def fake_reserve_prompt_editor_input(
        target_root: Path,
    ) -> tuple[Path, Path]:
        """決定論的な editor path を返す。"""
        assert target_root == root
        editor_work_path.touch()
        return editor_work_path, input_copy_path

    real_build_main_parameter = (
        oracle_edit_module.build_oracle_edit_main_launch_exec_parameter
    )

    def record_build_main_parameter(
        user_instruction: str,
    ) -> AgentCallParameter:
        """skeleton 用と実行用の本命 builder 呼び出しを記録する。"""
        events.append(
            "build-main-skeleton"
            if user_instruction == oracle_edit_module.ORIGINAL_PROMPT_PLACEHOLDER
            else "build-main"
        )
        parameter = real_build_main_parameter(user_instruction)
        built_main_parameters.append(parameter)
        return parameter

    def fake_edit_prompt_editor_input(
        target_root: Path,
        work_path: Path,
        complete_prompt_skeleton: str,
    ) -> None:
        """エディタへ渡す path と完全 prompt skeleton を記録する。"""
        events.append("editor")
        assert target_root == root
        editor_calls.append((work_path, input_copy_path, complete_prompt_skeleton))

    def fake_collect_prompt_editor_input(
        target_root: Path,
        work_path: Path,
        saved_copy_path: Path,
    ) -> str:
        """一回の最終読み取りから抽出した入力を返す。"""
        events.append("collect")
        assert target_root == root
        assert work_path == editor_work_path
        saved_copy_path.write_text("oracle spec を更新する", encoding="utf-8")
        return "oracle spec を更新する"

    real_finalize_prompt_editor_input = oracle_edit_module.finalize_prompt_editor_input

    def record_finalize_prompt_editor_input(
        target_root: Path,
        work_path: Path,
    ) -> None:
        """agent call 前の editor work file cleanup を記録する。"""
        events.append("finalize")
        real_finalize_prompt_editor_input(target_root, work_path)

    monkeypatch.setattr(
        oracle_edit_module,
        "reserve_prompt_editor_input",
        fake_reserve_prompt_editor_input,
    )
    monkeypatch.setattr(
        runtime_cli_module,
        "run_doctor_preprocess",
        record_run_doctor_preprocess,
    )
    monkeypatch.setattr(
        oracle_edit_module,
        "build_oracle_edit_main_launch_exec_parameter",
        record_build_main_parameter,
    )
    monkeypatch.setattr(
        oracle_edit_module,
        "edit_prompt_editor_input",
        fake_edit_prompt_editor_input,
    )
    monkeypatch.setattr(
        oracle_edit_module,
        "collect_prompt_editor_input",
        fake_collect_prompt_editor_input,
    )
    monkeypatch.setattr(
        oracle_edit_module,
        "finalize_prompt_editor_input",
        record_finalize_prompt_editor_input,
    )
    calls: list[tuple[AgentCallParameter, dict[str, object]]] = []

    def fake_indexing_preflight(
        update_root: Path,
        _codex_exec: object,
    ) -> None:
        """oracle edit 前の indexing preflight 呼び出しを記録する。"""
        assert update_root == root
        events.append("indexing")

    real_load_config = oracle_edit_module.load_config
    config_file = config_path(root)
    configured = json.loads(config_file.read_text())
    call_kind = "build_oracle_edit_main_launch_exec_parameter"
    configured["codex"]["agent_calls"][call_kind] = {
        "model_provider": "custom",
        "model": "custom-model",
        "reasoning_effort": "high",
    }
    configured["codex"]["model_providers"]["custom"] = {
        "settings": {"name": "custom", "http_headers": {"X-Test": "original"}}
    }
    config_file.write_text(json.dumps(configured))

    def record_load_config(target_root: Path):
        events.append("config")
        return real_load_config(target_root)

    monkeypatch.setattr(oracle_edit_module, "load_config", record_load_config)
    override_args: list[list[str]] = []

    real_require_launch_preconditions = (
        oracle_edit_module._require_oracle_edit_launch_preconditions
    )

    def record_launch_preconditions(repository: Path, current_root: Path) -> None:
        """oracle edit の起動前提検査を記録して本来の検査へ委譲する。"""
        events.append("check")
        real_require_launch_preconditions(repository, current_root)

    def fake_runtime_exec(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> FakeCodexResult:
        """各 exec の差分と、失敗後も差分を残す挙動を再現する。"""
        calls.append((parameter, kwargs))
        assert parameter is built_main_parameters[1]
        override_args.append(build_codex_override_args(parameter, kwargs["config"]))
        if len(calls) == 1:
            events.append("first")
            if first_changes:
                (root / "oracle" / "spec.md").write_text("# first edit\n")

            # 自己編集に相当する定義・設定の変更後も再構築・再読込を許さない。
            def reject_rebuild(_instruction):
                pytest.fail("editor input was rebuilt after the first call")

            monkeypatch.setattr(
                oracle_edit_module,
                "build_oracle_edit_main_launch_exec_parameter",
                reject_rebuild,
            )
            configured["codex"]["agent_calls"][call_kind]["model"] = "changed-model"
            configured["codex"]["model_providers"]["custom"]["settings"][
                "http_headers"
            ]["X-Test"] = "changed"
            config_file.write_text(json.dumps(configured))
            if failure_stage == "first":
                raise CmocError("first failed", [], "returncode: 7")
        else:
            events.append("second")
            expected_before_second = "# first edit\n" if first_changes else spec_before
            assert (root / "oracle" / "spec.md").read_text() == expected_before_second
            (root / "oracle" / "spec.md").write_text("# second edit\n")
            if failure_stage == "second":
                raise CmocError("second failed", [], "returncode: 8")
        return FakeCodexResult()

    monkeypatch.setattr(
        oracle_edit_module,
        "run_indexing_preflight",
        fake_indexing_preflight,
    )
    monkeypatch.setattr(
        oracle_edit_module,
        "_require_oracle_edit_launch_preconditions",
        record_launch_preconditions,
    )
    monkeypatch.setattr(
        codex_preflight_module,
        "runtime_run_codex_exec",
        fake_runtime_exec,
    )
    monkeypatch.setattr(
        runtime_cli_module,
        "notify_terminal_result",
        lambda command, repository, state: notifications.append(
            (command, repository, state)
        ),
    )

    spec_before = (root / "oracle" / "spec.md").read_text()
    result = runner.invoke(app, ["oracle", "edit"], catch_exceptions=False)

    assert result.exit_code == (0 if failure_stage is None else 1)
    assert len(built_main_parameters) == 2
    assert editor_calls[0][:2] == (editor_work_path, input_copy_path)
    complete_prompt_skeleton = editor_calls[0][2]
    assert (
        complete_prompt_skeleton.count(oracle_edit_module.ORIGINAL_PROMPT_PLACEHOLDER)
        == 1
    )
    assert "# file R/W policy (pure_oracle_write)" in complete_prompt_skeleton
    skeleton_objective = complete_prompt_skeleton.split(
        '<cmoc_block id="objective">', 1
    )[1].split("</cmoc_block>", 1)[0]
    assert "# task" in skeleton_objective
    assert "目標状態" in skeleton_objective
    assert "# completion criteria" in skeleton_objective
    assert "# scope" in skeleton_objective
    assert "# 変更操作の制約" in complete_prompt_skeleton
    assert "`git add`、`git commit`、`git stash`、branch 切替" in (
        complete_prompt_skeleton
    )
    assert "変更を未コミットのまま残す" in complete_prompt_skeleton
    expected_events = [
        "doctor",
        "build-main-skeleton",
        "editor",
        "collect",
        "build-main",
        "config",
        "finalize",
        "indexing",
        "check",
        "first",
    ]
    if failure_stage != "first":
        expected_events.append("second")
    assert events == expected_events
    assert len(calls) == (1 if failure_stage == "first" else 2)

    main_parameter, main_kwargs = calls[0]
    assert main_parameter is built_main_parameters[1]
    _assert_exec_parameter(main_parameter, root)
    assert "cwd" not in main_kwargs
    assert "before_agent_call" not in main_kwargs
    assert main_kwargs["root"] == root
    assert main_kwargs["purpose"] == "oracle edit first"
    complete_prompt = main_parameter.prompt
    assert "oracle spec を更新する" in complete_prompt
    assert oracle_edit_module.ORIGINAL_PROMPT_PLACEHOLDER not in complete_prompt
    assert "# oracle policy" in complete_prompt
    assert "# routing policy" in complete_prompt
    main_objective = complete_prompt.split('<cmoc_block id="objective">', 1)[1].split(
        "</cmoc_block>", 1
    )[0]
    assert "# task" in main_objective
    assert "# completion criteria" in main_objective
    assert "# 変更操作の制約" in complete_prompt

    assert "custom-model" in override_args[0]
    assert 'model_provider="custom"' in override_args[0]
    assert 'model_reasoning_effort="high"' in override_args[0]
    assert codex_override_config(override_args[0])["model_providers"]["custom"][
        "http_headers"
    ] == {"X-Test": "original"}
    if failure_stage != "first":
        second_parameter, second_kwargs = calls[1]
        assert second_parameter is main_parameter
        assert second_kwargs["root"] == root
        assert second_kwargs["config"] is main_kwargs["config"]
        assert second_kwargs["purpose"] == "oracle edit second"
        assert override_args[1] == override_args[0]

    assert input_copy_path.read_text(encoding="utf-8") == "oracle spec を更新する"
    assert not editor_work_path.exists()
    assert not list(input_copy_path.parent.glob("*_cmpl.md"))
    expected_spec = "# second edit\n"
    if failure_stage == "first":
        expected_spec = "# first edit\n" if first_changes else spec_before
    assert (root / "oracle" / "spec.md").read_text() == expected_spec
    assert json.loads(session_state_path.read_text()) == state_before
    assert readme_path.read_text() == "# unstaged change\n"
    assert (
        run_git(root, "diff", "--cached", "--", "README.md").stdout
        == staged_diff_before
    )
    assert run_git(root, "diff", "--", "README.md").stdout == unstaged_diff_before
    if failure_stage != "first" or first_changes:
        assert run_git(root, "status", "--short", "oracle/spec.md").stdout.strip()
    assert not (root / ".cmoc" / "gu" / "report" / "oracle" / "edit" / "fork").exists()
    terminal_output = result.stdout + result.stderr
    if failure_stage is None:
        assert "# 完了: cmoc oracle edit" in result.stdout
        assert notifications == [("oracle edit", root, "completed")]
    else:
        assert "# 失敗: cmoc oracle edit" in result.stderr
        assert notifications == [("oracle edit", root, "failed")]
    assert (
        terminal_output.count("# 完了: cmoc oracle edit")
        + terminal_output.count("# 失敗: cmoc oracle edit")
        == 1
    )
    assert "- result:" not in terminal_output
    assert "- completion_reason:" not in terminal_output
    report_path = terminal_primary_report(result)
    assert terminal_output.count(str(report_path)) == 1
    report = report_path.read_text(encoding="utf-8")
    expected_classification = "natural_completion" if failure_stage is None else "error"
    expected_first_status = "failed" if failure_stage == "first" else "succeeded"
    expected_second_status = {
        None: "succeeded",
        "first": "not_started",
        "second": "failed",
    }[failure_stage]
    assert f'terminal_classification: "{expected_classification}"' in report
    assert f"exit_code: {result.exit_code}" in report
    assert f'first_agent_call_status: "{expected_first_status}"' in report
    assert f'second_agent_call_status: "{expected_second_status}"' in report
    assert "# cmoc oracle edit report" in report
    assert "診断用サブコマンドログ" in report


def test_oracle_edit_builder_failure_does_not_reserve_editor_work_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """skeleton 構築に失敗した場合は editor work file を残さない。"""
    root = _prepared_repo(tmp_path, monkeypatch)

    def fail_build_main_parameter(_user_instruction: str) -> AgentCallParameter:
        """skeleton の構築失敗を再現する。"""
        raise CmocError("builder failed", [], "test failure")

    monkeypatch.setattr(
        oracle_edit_module,
        "build_oracle_edit_main_launch_exec_parameter",
        fail_build_main_parameter,
    )

    result = runner.invoke(app, ["oracle", "edit"], catch_exceptions=False)

    assert result.exit_code == 1
    assert not list((root / ".cmoc" / "gu" / "editor_input").glob("*_orig.md"))


@pytest.mark.parametrize("failure_stage", ["config", "indexing", "preconditions"])
def test_oracle_edit_preparation_failure_leaves_both_calls_not_started(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure_stage: str
) -> None:
    """共用入力確定後の準備失敗では、どちらの編集も開始済みにしない。"""
    root = _prepared_repo(tmp_path, monkeypatch)
    _activate_session(root)
    monkeypatch.setattr(
        oracle_edit_module, "edit_prompt_editor_input", lambda *_args: None
    )
    monkeypatch.setattr(
        oracle_edit_module, "collect_prompt_editor_input", lambda *_args: "edit oracle"
    )
    events = []

    def record_stage(stage):
        events.append(stage)
        if stage == failure_stage:
            raise CmocError(f"{stage} failed", [], "test failure")

    real_load_config = oracle_edit_module.load_config

    def load_config(repository):
        record_stage("config")
        return real_load_config(repository)

    monkeypatch.setattr(oracle_edit_module, "load_config", load_config)
    monkeypatch.setattr(
        oracle_edit_module,
        "run_indexing_preflight",
        lambda *_args: record_stage("indexing"),
    )
    monkeypatch.setattr(
        oracle_edit_module,
        "_require_oracle_edit_launch_preconditions",
        lambda *_args: record_stage("preconditions"),
    )
    monkeypatch.setattr(
        oracle_edit_module,
        "run_codex_exec",
        lambda *_args, **_kwargs: pytest.fail("edit started after preparation failure"),
    )

    result = runner.invoke(app, ["oracle", "edit"], catch_exceptions=False)

    assert result.exit_code == 1
    stages = ["config", "indexing", "preconditions"]
    assert events == stages[: stages.index(failure_stage) + 1]
    report = terminal_primary_report(result).read_text()
    for pass_name in ("first", "second"):
        assert f'{pass_name}_agent_call_status: "not_started"' in report


@pytest.mark.parametrize(
    ("case", "message"),
    [
        ("linked", "main worktree"),
        ("non_session", "session branch"),
        ("inactive", "active な session"),
    ],
)
def test_oracle_edit_launch_preconditions(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    case: str,
    message: str,
) -> None:
    """oracle edit の各起動前提違反を利用者向け例外として検証する。"""
    root = _prepared_repo(tmp_path, monkeypatch)
    current_root = root
    if case != "non_session":
        _activate_session(
            root,
            session_state="joined" if case == "inactive" else "active",
        )
    if case == "linked":
        current_root = root / ".cmoc" / "gu" / "worktree" / "linked"
        run_git(
            root,
            "worktree",
            "add",
            "-b",
            "linked-oracle-edit-test",
            str(current_root),
            "HEAD",
        )
    with pytest.raises(CmocError, match=message):
        oracle_edit_module._require_oracle_edit_launch_preconditions(
            root,
            current_root,
        )


def test_oracle_edit_prompt_preserves_user_log_reference(tmp_path, monkeypatch):
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    instruction = (
        "診断用サブコマンドログ /example/sender.jsonl を参考に oracle を編集する"
    )
    empty = oracle_edit_module.build_oracle_edit_main_launch_exec_parameter("").prompt
    prompt = oracle_edit_module.build_oracle_edit_main_launch_exec_parameter(
        instruction
    ).prompt
    assert instruction in prompt
    for prior_context in ("過去の agent の会話", "最終回答", "実行ログ"):
        assert prior_context not in empty
