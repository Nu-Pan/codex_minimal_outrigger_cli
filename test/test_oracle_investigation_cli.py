"""`cmoc oracle investigation` の CLI 起動条件を検証する。

根拠:
- {{work-root}}/oracle/doc/app_spec/sub_command/oracle_investigation.md
- {{work-root}}/oracle/doc/app_spec/indexing.md
- {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
- {{work-root}}/oracle/src/oracle/acp_builder/oracle/investigation/launch_tui.py
"""

from collections.abc import Iterator
from pathlib import Path

import pytest
from _cli_support import run_doctor, runner
from _git_support import make_repo

import acp.builder.oracle.investigation.launch_tui as launch_tui_module
import commons.runtime_cli as runtime_cli_module
import commons.runtime_codex_preflight as codex_preflight_module
import sub_commands.oracle.investigation as investigation_module
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from main import app


@pytest.fixture(autouse=True)
def reset_indexing_preflight() -> Iterator[None]:
    """各 test の前後で indexing preflight の process-local state を初期化する。"""
    codex_preflight_module.disable_indexing_preflight()
    yield
    codex_preflight_module.disable_indexing_preflight()


def test_oracle_investigation_has_no_session_precondition(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """oracle investigation が session なしの main worktree でも起動できる。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    time_stamp = "2026-08-03_00-00-00_000000000"
    editor_work_path = (
        root / ".cmoc" / "gu" / "aw" / "editor_input" / f"{time_stamp}_orig.md"
    )
    input_copy_path = (
        root / ".cmoc" / "gu" / "ar" / "log" / "editor_input" / f"{time_stamp}_orig.md"
    )
    editor_work_path.parent.mkdir(parents=True, exist_ok=True)
    input_copy_path.parent.mkdir(parents=True, exist_ok=True)
    editor_calls: list[tuple[Path, Path, str]] = []
    built_parameters: list[AgentCallParameter] = []
    events: list[str] = []
    preflight_enable_calls = 0

    real_enable_indexing_preflight = investigation_module.enable_indexing_preflight

    def record_enable_indexing_preflight() -> None:
        """本命処理より前の indexing preflight 登録を記録する。"""
        nonlocal preflight_enable_calls
        preflight_enable_calls += 1
        real_enable_indexing_preflight()

    real_run_doctor_preprocess = runtime_cli_module.run_doctor_preprocess

    def record_run_doctor_preprocess(
        target_root: Path,
        *,
        sync_refactor_entries: bool = True,
    ) -> None:
        """CLI invocation 内の doctor preprocess を記録して本来の処理へ委譲する。"""
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

    real_build_parameter = (
        investigation_module.build_oracle_investigation_launch_tui_parameter
    )

    def record_build_parameter(
        user_instruction: str,
    ) -> AgentCallParameter:
        """skeleton 用と実行用の builder 呼び出しを記録する。"""
        events.append(
            "build-skeleton"
            if user_instruction == investigation_module.ORIGINAL_PROMPT_PLACEHOLDER
            else "build-parameter"
        )
        parameter = real_build_parameter(user_instruction)
        built_parameters.append(parameter)
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
        saved_copy_path.write_text("oracle の根拠を調査する", encoding="utf-8")
        return "oracle の根拠を調査する"

    real_finalize_prompt_editor_input = (
        investigation_module.finalize_prompt_editor_input
    )

    def record_finalize_prompt_editor_input(
        work_path: Path,
    ) -> None:
        """TUI 起動前の editor work file cleanup を記録する。"""
        events.append("finalize")
        real_finalize_prompt_editor_input(work_path)

    monkeypatch.setattr(
        investigation_module,
        "reserve_prompt_editor_input",
        fake_reserve_prompt_editor_input,
    )
    monkeypatch.setattr(
        investigation_module,
        "enable_indexing_preflight",
        record_enable_indexing_preflight,
    )
    monkeypatch.setattr(
        runtime_cli_module,
        "run_doctor_preprocess",
        record_run_doctor_preprocess,
    )
    monkeypatch.setattr(
        investigation_module,
        "build_oracle_investigation_launch_tui_parameter",
        record_build_parameter,
    )
    monkeypatch.setattr(
        investigation_module,
        "edit_prompt_editor_input",
        fake_edit_prompt_editor_input,
    )
    monkeypatch.setattr(
        investigation_module,
        "collect_prompt_editor_input",
        fake_collect_prompt_editor_input,
    )
    monkeypatch.setattr(
        investigation_module,
        "finalize_prompt_editor_input",
        record_finalize_prompt_editor_input,
    )
    calls: list[tuple[AgentCallParameter, dict[str, object]]] = []

    def fake_run_codex_tui(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> None:
        """確定後の TUI 起動を記録する。"""
        events.append("tui")
        assert preflight_enable_calls == 1
        calls.append((parameter, kwargs))

    monkeypatch.setattr(
        investigation_module,
        "run_codex_tui",
        fake_run_codex_tui,
    )

    result = runner.invoke(
        app,
        ["oracle", "investigation"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert events == [
        "doctor",
        "build-skeleton",
        "editor",
        "collect",
        "build-parameter",
        "finalize",
        "tui",
    ]
    assert len(built_parameters) == 2
    assert len(editor_calls) == 1
    assert editor_calls[0][:2] == (editor_work_path, input_copy_path)
    complete_prompt_skeleton = editor_calls[0][2]
    assert (
        complete_prompt_skeleton.count(investigation_module.ORIGINAL_PROMPT_PLACEHOLDER)
        == 1
    )
    assert "# file read write rule - pure_oracle_read" in complete_prompt_skeleton
    assert "oracle file の調査担当" in complete_prompt_skeleton
    assert "関連する oracle file を根拠とする読み取り専用調査を通常の作業範囲" in (
        complete_prompt_skeleton
    )
    assert "editor handoff でも agent call の責務を維持する" in (
        complete_prompt_skeleton
    )
    assert "対象 path と理由を限定した sandbox escalation" in (complete_prompt_skeleton)
    assert "未定義の事項を正本仕様として断定していない" in (complete_prompt_skeleton)
    assert len(calls) == 1
    parameter, kwargs = calls[0]
    assert parameter is built_parameters[1]
    assert parameter.model_class == ModelClass.FLAGSHIP
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.file_access_mode == FileAccessMode.PURE_ORACLE_READ
    assert parameter.structured_output_schema_path is None
    assert parameter.agent_call_cwd == root.resolve()
    assert parameter.run_indexing_preflight is True
    assert kwargs["notification_command_name"] == "oracle investigation"
    complete_prompt = parameter.prompt
    assert "# oracle investigation standard" in complete_prompt
    assert "# oracle standard" not in complete_prompt
    assert "# routing rule" in complete_prompt
    assert "oracle の根拠を調査する" in complete_prompt
    assert investigation_module.ORIGINAL_PROMPT_PLACEHOLDER not in complete_prompt
    assert input_copy_path.read_text(encoding="utf-8") == "oracle の根拠を調査する"
    assert not editor_work_path.exists()
    assert not list(input_copy_path.parent.glob("*_cmpl.md"))


def test_oracle_investigation_builder_exports_only_the_builder() -> None:
    """investigation の realization adapter が補助名を公開しない。"""
    expected = ["build_oracle_investigation_launch_tui_parameter"]
    assert launch_tui_module.__all__ == expected
    assert (
        sorted(name for name in vars(launch_tui_module) if not name.startswith("_"))
        == expected
    )
