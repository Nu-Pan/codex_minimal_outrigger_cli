"""`cmoc oracle investigation` の CLI 起動条件を検証する。

根拠:
- {{work-root}}/spec/app_spec/sub_command/oracle_investigation.md
- {{work-root}}/spec/app_spec/document_search.md
- {{work-root}}/spec/app_spec/prompt_editor_input.md
- {{work-root}}/reference/src/oracle/acp_builder/oracle/investigation/launch_tui.py
"""

from pathlib import Path

import oracle.other.path_model as path_model_module
import pytest
from _cli_support import runner

import commons.runtime_cli as runtime_cli_module
import sub_commands.oracle.investigation as investigation_module
from basic.acp import AgentCallParameter, FileAccessMode
from commons.runtime_logging import current_subcommand_logger
from config.cmoc_config import CmocConfig
from main import app


def test_oracle_investigation_has_no_session_precondition(
    cli_terminal_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """session 状態を用意せず、調査指示から固定 parameter で TUI を起動する。"""
    root = cli_terminal_directory

    # root の Git 導出は test_basic_runtime.py、CLI との結合は test_runtime_cli.py に残す。
    # workload の検査では空の directory を main root として渡し、Git の準備を省く。
    def resolve_test_roots(start_path: Path | None = None) -> tuple[Path, Path]:
        assert (Path.cwd() if start_path is None else start_path).resolve() == root
        return root, root

    monkeypatch.setattr(
        path_model_module, "_resolve_git_worktree_roots", resolve_test_roots
    )
    config = CmocConfig(num_parallel=3)
    instruction = "oracle の根拠を調査する"
    later_editor_content = "確定後に人間が再編集した本文"
    input_path: Path
    editor_calls: list[tuple[Path, str]] = []
    built_parameters: list[AgentCallParameter] = []
    events: list[str] = []

    # 修復・索引同期は test_doctor_cli.py、共通 CLI との結合は test_cli_tui.py に残す。
    # ここでは investigation 固有の呼び出し先・順序を検証し、履歴作成を省く。
    def record_run_doctor_preprocess(target_root: Path) -> None:
        """CLI invocation 内の doctor 呼び出し先と順序を記録する。"""
        assert target_root == root
        events.append("doctor")

    def record_editor_roots_ignored(target_root: Path) -> None:
        """共通 ignore 検査への引き渡しを記録する。"""
        assert target_root == root
        assert not (root / ".cmoc/gu/log/editor_input").exists()
        events.append("ignore")

    # 設定の保存・復元は test_runtime_config.py、CLI との実結合は
    # test_cli_tui.py の main 起動に残し、ここでは取得元と引き渡しを検査する。
    def record_load_config(target_root: Path) -> CmocConfig:
        """TUI へ渡す設定の取得元と順序を記録する。"""
        assert target_root == root
        events.append("load-config")
        return config

    real_build_parameter = investigation_module.build_oracle_investigation_request

    def record_build_parameter(
        user_instruction: str,
    ) -> AgentCallParameter:
        """skeleton 用と実行用の builder 呼び出しを記録する。"""
        assert user_instruction in (
            investigation_module.ORIGINAL_PROMPT_PLACEHOLDER,
            instruction,
        )
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
        nonlocal input_path
        input_path = work_path
        logger = current_subcommand_logger()
        assert logger is not None
        assert work_path.name == f"{logger.execution_id}_orig.md"
        events.append("editor")
        assert target_root == root
        editor_calls.append((work_path, complete_prompt_skeleton))
        work_path.write_text(instruction, encoding="utf-8")

    # 一回の読み取り・原文保存は test_prompt_editor_input.py、保存失敗時の
    # CLI 停止は test_cli_tui.py に残す。ここでは保存を繰り返さず、
    # 再編集後の file でなく確定済みの戻り値を builder に渡すことを検証する。
    def fake_collect_prompt_editor_input(
        target_root: Path,
        work_path: Path,
    ) -> str:
        """確定後の人間による再編集を模し、固定した入力を返す。"""
        events.append("collect")
        assert target_root == root
        assert work_path == input_path
        work_path.write_text(later_editor_content, encoding="utf-8")
        return instruction

    monkeypatch.setattr(
        runtime_cli_module,
        "run_doctor_preprocess",
        record_run_doctor_preprocess,
    )
    # 実 ignore の main/linked 境界は test_cli_tui.py、失敗条件は test_runtime_git_ignore.py に残す。
    # ここでは doctor 後、入力予約前の呼び出し先と順序を検証する。
    monkeypatch.setattr(
        investigation_module,
        "ensure_prompt_editor_roots_ignored",
        record_editor_roots_ignored,
    )
    monkeypatch.setattr(
        investigation_module,
        "build_oracle_investigation_request",
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
    monkeypatch.setattr(investigation_module, "load_config", record_load_config)
    calls: list[tuple[AgentCallParameter, dict[str, object]]] = []

    def fake_run_codex_tui(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> None:
        """確定後の TUI 起動を記録する。"""
        events.append("tui")
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
        "ignore",
        "build-skeleton",
        "editor",
        "collect",
        "build-parameter",
        "load-config",
        "tui",
    ]
    assert len(built_parameters) == 2
    assert len(editor_calls) == 1
    assert editor_calls[0][0] == input_path
    complete_prompt_skeleton = editor_calls[0][1]
    assert complete_prompt_skeleton == built_parameters[0].prompt
    assert "# file access policy (pure_oracle_read)" in complete_prompt_skeleton
    objective = complete_prompt_skeleton.split('<cmoc_block id="objective">', 1)[
        1
    ].split("</cmoc_block>", 1)[0]
    assert "# task" in objective
    assert "要求する事項を調査し、結果を回答する" in objective
    assert "# scope" in objective
    assert "`{{work-root}}/oracle` ツリー内の関連する oracle file を根拠" in (objective)
    assert "# completion criteria" in objective
    assert "調査結果がユーザーへ回答されている" in objective
    assert "根拠となる oracle file を回答から特定できる" in objective
    assert "# non-goals" not in objective
    assert len(calls) == 1
    parameter, kwargs = calls[0]
    assert parameter is built_parameters[1]
    assert parameter.file_access_mode == FileAccessMode.PURE_ORACLE_READ
    assert parameter.structured_output_schema_path is None
    assert parameter.agent_call_cwd == root.resolve()
    assert parameter.enable_editor_input_handoff_mcp is True
    assert parameter.enable_document_search_mcp is True
    assert kwargs["root"] == root
    assert kwargs["config"] is config
    assert kwargs["purpose"] == "oracle investigation"
    complete_prompt = parameter.prompt
    assert "# oracle investigation policy" not in complete_prompt
    assert "# oracle policy" in complete_prompt
    assert "# routing policy" in complete_prompt
    assert "# editor input handoff" in complete_prompt
    assert instruction in complete_prompt
    assert later_editor_content not in complete_prompt
    assert input_path.read_text(encoding="utf-8") == later_editor_content
    assert not list(input_path.parent.glob("*_cmpl.md"))
