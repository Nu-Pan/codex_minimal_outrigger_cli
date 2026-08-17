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
from _codex_support import FakeCodexResult, setup_codex_home
from _git_support import current_branch, make_repo, run_git

import commons.indexing as indexing_module
import commons.runtime_cli as runtime_cli_module
import commons.runtime_codex_preflight as codex_preflight_module
import sub_commands.oracle.edit as oracle_edit_module
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from cmoc_runtime import CmocError
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
    *,
    runs_indexing: bool,
) -> None:
    """2 回の exec に共通する起動契約を検証する。"""
    assert parameter.model_class == ModelClass.FLAGSHIP
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.file_access_mode == FileAccessMode.PURE_ORACLE_WRITE
    assert parameter.structured_output_schema_path is None
    assert parameter.run_indexing_preflight is runs_indexing
    assert parameter.agent_call_cwd == root.resolve()


@pytest.mark.parametrize(
    "failure_stage",
    [None, "main", "reduction"],
    ids=["success", "main-failure", "reduction-failure"],
)
def test_oracle_edit_runs_two_exec_calls_and_preserves_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure_stage: str | None,
) -> None:
    """既存差分を保ち、本命成功時だけ仕様削減を別 exec で実行する。"""
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
    editor_work_path = (
        root / ".cmoc" / "gu" / "aw" / "editor_input" / f"{time_stamp}_orig.md"
    )
    input_copy_path = (
        root / ".cmoc" / "gu" / "ar" / "log" / "editor_input" / f"{time_stamp}_orig.md"
    )
    editor_work_path.parent.mkdir(parents=True, exist_ok=True)
    input_copy_path.parent.mkdir(parents=True, exist_ok=True)
    editor_calls: list[tuple[Path, Path, str]] = []
    built_main_parameters: list[AgentCallParameter] = []
    built_reduction_parameters: list[AgentCallParameter] = []
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

    real_build_reduction_parameter = (
        oracle_edit_module.build_oracle_edit_reduction_launch_exec_parameter
    )

    def record_build_reduction_parameter(
        user_instruction: str,
    ) -> AgentCallParameter:
        """本命成功後にだけ構築する仕様削減 parameter を記録する。"""
        events.append("build-reduction")
        assert user_instruction == "oracle spec を更新する"
        parameter = real_build_reduction_parameter(user_instruction)
        built_reduction_parameters.append(parameter)
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
        work_path: Path,
    ) -> None:
        """agent call 前の editor work file cleanup を記録する。"""
        events.append("finalize")
        real_finalize_prompt_editor_input(work_path)

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
        "build_oracle_edit_reduction_launch_exec_parameter",
        record_build_reduction_parameter,
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
        if parameter is built_main_parameters[1]:
            events.append("main")
            (root / "oracle" / "spec.md").write_text("# main edit\n")
            if failure_stage == "main":
                raise CmocError("main failed", [], "returncode: 7")
        else:
            assert parameter is built_reduction_parameters[0]
            events.append("reduction")
            (root / "oracle" / "spec.md").write_text("# reduced edit\n")
            if failure_stage == "reduction":
                raise CmocError("reduction failed", [], "returncode: 8")
        return FakeCodexResult()

    monkeypatch.setattr(
        indexing_module,
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
    assert "oracle file だけを編集し" in complete_prompt_skeleton
    expected_events = [
        "doctor",
        "build-main-skeleton",
        "editor",
        "collect",
        "build-main",
        "finalize",
        "indexing",
        "check",
        "main",
    ]
    if failure_stage != "main":
        expected_events.extend(["build-reduction", "reduction"])
    assert events == expected_events
    assert len(calls) == (1 if failure_stage == "main" else 2)

    main_parameter, main_kwargs = calls[0]
    assert main_parameter is built_main_parameters[1]
    _assert_exec_parameter(main_parameter, root, runs_indexing=True)
    assert "cwd" not in main_kwargs
    assert "before_agent_call" not in main_kwargs
    assert main_kwargs["root"] == root
    assert main_kwargs["purpose"] == "oracle edit main"
    complete_prompt = main_parameter.prompt
    assert "oracle spec を更新する" in complete_prompt
    assert oracle_edit_module.ORIGINAL_PROMPT_PLACEHOLDER not in complete_prompt
    assert "# oracle policy" in complete_prompt
    assert "# routing policy" in complete_prompt
    assert "realization file、`INDEX.md`、`AGENTS.md` を編集していない" in (
        complete_prompt
    )

    if failure_stage == "main":
        assert built_reduction_parameters == []
    else:
        assert len(built_reduction_parameters) == 1
        reduction_parameter, reduction_kwargs = calls[1]
        assert reduction_parameter is built_reduction_parameters[0]
        assert reduction_parameter is not main_parameter
        _assert_exec_parameter(reduction_parameter, root, runs_indexing=False)
        assert reduction_kwargs["root"] == root
        assert reduction_kwargs["config"] is main_kwargs["config"]
        assert reduction_kwargs["purpose"] == "oracle edit reduction"
        assert "oracle spec を更新する" in reduction_parameter.prompt
        assert "仕様削減の判断と参照の境界" in reduction_parameter.prompt
        assert "本命 agent call の prompt" in reduction_parameter.prompt
        assert "# oracle policy" in reduction_parameter.prompt
        assert "# routing policy" in reduction_parameter.prompt

    assert input_copy_path.read_text(encoding="utf-8") == "oracle spec を更新する"
    assert not editor_work_path.exists()
    assert not list(input_copy_path.parent.glob("*_cmpl.md"))
    expected_spec = "# main edit\n" if failure_stage == "main" else "# reduced edit\n"
    assert (root / "oracle" / "spec.md").read_text() == expected_spec
    assert json.loads(session_state_path.read_text()) == state_before
    assert readme_path.read_text() == "# unstaged change\n"
    assert (
        run_git(root, "diff", "--cached", "--", "README.md").stdout
        == staged_diff_before
    )
    assert run_git(root, "diff", "--", "README.md").stdout == unstaged_diff_before
    assert run_git(root, "status", "--short", "oracle/spec.md").stdout.strip()
    assert not (
        root / ".cmoc" / "gu" / "ar" / "report" / "oracle" / "edit" / "fork"
    ).exists()
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
    expected_main_status = "failed" if failure_stage == "main" else "succeeded"
    expected_reduction_status = {
        None: "succeeded",
        "main": "not_started",
        "reduction": "failed",
    }[failure_stage]
    assert f'terminal_classification: "{expected_classification}"' in report
    assert f"exit_code: {result.exit_code}" in report
    assert f'main_agent_call_status: "{expected_main_status}"' in report
    assert f'reduction_agent_call_status: "{expected_reduction_status}"' in report
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
    assert not list((root / ".cmoc" / "gu" / "aw" / "editor_input").glob("*_orig.md"))


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
