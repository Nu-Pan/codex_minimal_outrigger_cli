"""`cmoc oracle edit` の main-worktree TUI 制御を検証する。

根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md
{{work-root}}/oracle/src/oracle/acp_builder/oracle/edit/launch_tui.py
"""

import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from _cli_support import run_doctor, runner
from _codex_support import setup_codex_home
from _git_support import current_branch, make_repo, run_git

import commons.indexing as indexing_module
import commons.runtime_cli as runtime_cli_module
import commons.runtime_codex_preflight as codex_preflight_module
import sub_commands.oracle.edit as oracle_edit_module
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from cmoc_runtime import CmocError, CommandResult
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


@pytest.mark.parametrize("tui_fails", [False, True], ids=["success", "failure"])
def test_oracle_edit_runs_tui_without_using_run_lifecycle_and_preserves_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    tui_fails: bool,
) -> None:
    """既存差分を保ったまま run lifecycle なしで oracle を編集する。"""
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
    complete_prompt_path = input_copy_path.with_name(f"{time_stamp}_cmpl.md")
    editor_work_path.parent.mkdir(parents=True, exist_ok=True)
    input_copy_path.parent.mkdir(parents=True, exist_ok=True)
    editor_calls: list[tuple[Path, Path, str]] = []
    built_parameters: list[AgentCallParameter] = []
    events: list[str] = []

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
    ) -> tuple[str, Path, Path, Path]:
        """決定論的な timestamp の editor path を返す。"""
        assert target_root == root
        editor_work_path.touch()
        return time_stamp, editor_work_path, input_copy_path, complete_prompt_path

    real_build_parameter = oracle_edit_module.build_oracle_edit_launch_tui_parameter

    def record_build_parameter(
        build_time_stamp: str,
        user_instruction: str,
    ) -> AgentCallParameter:
        """エディタより前の builder 呼び出しと戻り値を記録する。"""
        events.append("build")
        assert build_time_stamp == time_stamp
        assert user_instruction == oracle_edit_module.ORIGINAL_PROMPT_PLACEHOLDER
        parameter = real_build_parameter(build_time_stamp, user_instruction)
        built_parameters.append(parameter)
        return parameter

    def fake_collect_prompt_editor_input(
        target_root: Path,
        work_path: Path,
        saved_copy_path: Path,
        complete_prompt_skeleton: str,
    ) -> str:
        """エディタ入力時点の path と完全 prompt skeleton を記録する。"""
        events.append("editor")
        assert target_root == root
        assert complete_prompt_path.read_text() == complete_prompt_skeleton
        saved_copy_path.write_text("oracle spec を更新する", encoding="utf-8")
        editor_calls.append((work_path, saved_copy_path, complete_prompt_skeleton))
        return "oracle spec を更新する"

    real_finalize_complete_prompt = oracle_edit_module.finalize_complete_prompt

    def record_finalize_complete_prompt(
        work_path: Path,
        target_path: Path,
        complete_prompt_skeleton: str,
        original_prompt: str,
    ) -> None:
        """TUI 起動前の完全 prompt 確定を記録して本来の処理へ委譲する。"""
        events.append("finalize")
        real_finalize_complete_prompt(
            work_path,
            target_path,
            complete_prompt_skeleton,
            original_prompt,
        )

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
        "build_oracle_edit_launch_tui_parameter",
        record_build_parameter,
    )
    monkeypatch.setattr(
        oracle_edit_module,
        "collect_prompt_editor_input",
        fake_collect_prompt_editor_input,
    )
    monkeypatch.setattr(
        oracle_edit_module,
        "finalize_complete_prompt",
        record_finalize_complete_prompt,
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

    def fake_runtime_tui(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> CommandResult:
        """TUI の代わりに oracle 差分を書き込み、指定時は失敗させる。"""
        events.append("tui")
        calls.append((parameter, kwargs))
        (root / "oracle" / "spec.md").write_text("# edited spec\n")
        if tui_fails:
            raise CmocError("TUI failed", [], "returncode: 7")
        return CommandResult(0, "", "")

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
        "runtime_run_codex_tui",
        fake_runtime_tui,
    )

    result = runner.invoke(app, ["oracle", "edit"], catch_exceptions=False)

    assert result.exit_code == (1 if tui_fails else 0)
    assert len(built_parameters) == 1
    assert editor_calls[0][:2] == (editor_work_path, input_copy_path)
    complete_prompt_skeleton = editor_calls[0][2]
    assert (
        complete_prompt_skeleton.count(oracle_edit_module.ORIGINAL_PROMPT_PLACEHOLDER)
        == 1
    )
    assert "# file read write rule - pure_oracle_write" in complete_prompt_skeleton
    assert "oracle file だけを編集し" in complete_prompt_skeleton
    assert events == [
        "doctor",
        "build",
        "editor",
        "finalize",
        "indexing",
        "check",
        "tui",
    ]
    assert len(calls) == 1
    parameter, kwargs = calls[0]
    assert parameter is built_parameters[0]
    assert parameter.model_class == ModelClass.FLAGSHIP
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.file_access_mode == FileAccessMode.PURE_ORACLE_WRITE
    assert parameter.structured_output_schema_path is None
    assert parameter.run_indexing_preflight is True
    assert parameter.agent_call_cwd == root.resolve()
    assert "cwd" not in kwargs
    assert kwargs["purpose"] == "oracle edit"
    assert kwargs["notification_command_name"] == "oracle edit"
    prompt_suffix = " を読んで、その指示に従って下さい"
    assert parameter.prompt.endswith(prompt_suffix)
    assert Path(parameter.prompt.removesuffix(prompt_suffix)) == complete_prompt_path
    complete_prompt = complete_prompt_path.read_text()
    assert complete_prompt == complete_prompt_skeleton.replace(
        oracle_edit_module.ORIGINAL_PROMPT_PLACEHOLDER,
        "oracle spec を更新する",
        1,
    )
    assert "oracle spec を更新する" in complete_prompt
    assert "# oracle standard" in complete_prompt
    assert "# routing rule" in complete_prompt
    assert "realization file、`INDEX.md`、`AGENTS.md` を編集していない" in (
        complete_prompt
    )
    assert input_copy_path.read_text(encoding="utf-8") == "oracle spec を更新する"
    assert not editor_work_path.exists()
    assert (root / "oracle" / "spec.md").read_text() == "# edited spec\n"
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
