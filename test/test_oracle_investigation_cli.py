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
    editor_path = (
        root / ".cmoc" / "gu" / "ar" / "log" / "editor_input" / f"{time_stamp}_orig.md"
    )
    complete_prompt_path = editor_path.with_name(f"{time_stamp}_cmpl.md")
    editor_path.parent.mkdir(parents=True, exist_ok=True)
    editor_calls: list[tuple[Path, str]] = []
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
    ) -> tuple[str, Path, Path]:
        """決定論的な timestamp の editor path を返す。"""
        assert target_root == root
        editor_path.touch()
        return time_stamp, editor_path, complete_prompt_path

    real_build_parameter = (
        investigation_module.build_oracle_investigation_launch_tui_parameter
    )

    def record_build_parameter(
        build_time_stamp: str,
        user_instruction: str,
    ) -> AgentCallParameter:
        """エディタより前の builder 呼び出しと戻り値を記録する。"""
        events.append("build")
        assert build_time_stamp == time_stamp
        assert user_instruction == investigation_module.ORIGINAL_PROMPT_PLACEHOLDER
        parameter = real_build_parameter(build_time_stamp, user_instruction)
        built_parameters.append(parameter)
        return parameter

    def fake_collect_prompt_editor_input(
        original_prompt_path: Path,
        complete_prompt_skeleton: str,
    ) -> str:
        """エディタ入力時点の path と完全 prompt skeleton を記録する。"""
        events.append("editor")
        assert complete_prompt_path.read_text() == complete_prompt_skeleton
        editor_calls.append((original_prompt_path, complete_prompt_skeleton))
        return "oracle の根拠を調査する"

    real_finalize_complete_prompt = investigation_module.finalize_complete_prompt

    def record_finalize_complete_prompt(
        target_path: Path,
        complete_prompt_skeleton: str,
        original_prompt: str,
    ) -> None:
        """TUI 起動前の完全 prompt 確定を記録して本来の処理へ委譲する。"""
        events.append("finalize")
        real_finalize_complete_prompt(
            target_path,
            complete_prompt_skeleton,
            original_prompt,
        )

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
        "collect_prompt_editor_input",
        fake_collect_prompt_editor_input,
    )
    monkeypatch.setattr(
        investigation_module,
        "finalize_complete_prompt",
        record_finalize_complete_prompt,
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
    assert events == ["doctor", "build", "editor", "finalize", "tui"]
    assert len(built_parameters) == 1
    assert len(editor_calls) == 1
    assert editor_calls[0][0] == editor_path
    complete_prompt_skeleton = editor_calls[0][1]
    assert (
        complete_prompt_skeleton.count(investigation_module.ORIGINAL_PROMPT_PLACEHOLDER)
        == 1
    )
    assert "# file read write rule - pure_oracle_read" in complete_prompt_skeleton
    assert "oracle file の調査担当" in complete_prompt_skeleton
    assert len(calls) == 1
    parameter, kwargs = calls[0]
    assert parameter is built_parameters[0]
    assert parameter.model_class == ModelClass.FLAGSHIP
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.file_access_mode == FileAccessMode.PURE_ORACLE_READ
    assert parameter.structured_output_schema_path is None
    assert parameter.agent_call_cwd == root.resolve()
    assert parameter.run_indexing_preflight is True
    assert kwargs["notification_command_name"] == "oracle investigation"
    assert parameter.prompt == (
        f"{complete_prompt_path} を読んで、その指示に従って下さい"
    )
    complete_prompt = complete_prompt_path.read_text(encoding="utf-8")
    assert complete_prompt == complete_prompt_skeleton.replace(
        investigation_module.ORIGINAL_PROMPT_PLACEHOLDER,
        "oracle の根拠を調査する",
        1,
    )
    assert "# oracle standard" in complete_prompt
    assert "oracle の根拠を調査する" in complete_prompt


def test_oracle_investigation_builder_exports_only_the_builder() -> None:
    """investigation の realization adapter が補助名を公開しない。"""
    expected = ["build_oracle_investigation_launch_tui_parameter"]
    assert launch_tui_module.__all__ == expected
    assert (
        sorted(name for name in vars(launch_tui_module) if not name.startswith("_"))
        == expected
    )
