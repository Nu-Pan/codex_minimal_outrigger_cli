"""`cmoc realization apply` の追従作業用 prompt と起動パラメータの構築定義。"""

# std
from pathlib import Path
from typing import Literal

from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import (
    SDHeader,
    SDTagBlock,
    render_sd_node_as_markdown,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt

# cmoc
from oracle.request_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
)


def build_decision_apply_spec_request(
    diff_base_commit: str,
    run_fork_commit: str,
    agent_call_cwd: Path,
) -> AgentCallParameter:
    """`cmoc decision apply` の spec 同期ステップ用の agent call リクエストを構築する

    詳細は `_build_decision_apply_request_impl` を参照。
    """
    return _build_decision_apply_request_impl(
        diff_base_commit,
        run_fork_commit,
        agent_call_cwd,
        "to_spec",
    )


def build_decision_apply_realization_request(
    diff_base_commit: str,
    run_fork_commit: str,
    agent_call_cwd: Path,
) -> AgentCallParameter:
    """`cmoc decision apply` の realization 同期ステップ用の agent call リクエストを構築する

    詳細は `_build_decision_apply_request_impl` を参照。
    """
    return _build_decision_apply_request_impl(
        diff_base_commit,
        run_fork_commit,
        agent_call_cwd,
        "to_realization",
    )


def _build_decision_apply_request_impl(
    diff_base_commit: str,
    run_fork_commit: str,
    agent_call_cwd: Path,
    step_name: Literal["to_spec", "to_realization"],
) -> AgentCallParameter:
    """`cmoc decision apply` の各同期ステップ用の agent call リクエストを構築する

    Args:
        diff_base_commit:
            追従対象差分の始点 commit
            典型的には、前回の `cmoc decision apply` と対応する run fork commit が渡されるはず
        run_fork_commit:
            追従対象差分の終点 commit
            典型的には、今回の `cmoc decision apply` と対応する run fork commit が渡されるはず
        agent_call_cwd:
            エージェントに設定するカレントディレクトリパス
        step_name:
            to_spec: decision, reference --> spec の同期を行う
            to_realization: decision, reference, spec --> realization の同期を行う

    Returns:
        構築された agent call リクエスト
    """
    # 同期元・同期先の名前を解決する
    match step_name:
        case "to_spec":
            apply_from = "decision, reference"
            apply_to = "spec"
            file_access_mode = FileAccessMode.SPEC_WRITE
            spec_policy = True
            realization_policy = False
            realization_findings_policy = False
            agent_call_kind = "spec_edit"
        case "to_realization":
            apply_from = "decision, reference, spec"
            apply_to = "realization"
            file_access_mode = FileAccessMode.REALIZATION_WRITE
            spec_policy = False
            realization_policy = True
            realization_findings_policy = True
            agent_call_kind = "realization_edit"
        case _:
            raise ValueError(f"Invalid `step_name`(actual=`{step_name}`)")
    # パラメータを生成
    path_context = AgentCallPathContext(agent_call_cwd=agent_call_cwd)
    complete_prompt = build_complete_prompt(
        task=f"""
        {apply_from} の変更を {apply_to} に反映し、矛盾がない状態にすること
        """,
        scope=f"""
        - 修正対象は `{{{{work-root}}}}` ツリー内の {apply_to} すべて
        - <cmoc_ref target="decision_apply_change"/> は追従対象を特定するためのヒントであり、編集対象の制限ではない
        - 目的達成のために必要であれば、<cmoc_ref target="decision_apply_change"/> と直接関係のない {apply_to} も編集して良い
        """,
        completion_criteria=f"""
        - <cmoc_ref target="decision_apply_change"/> を根拠として {apply_from} の変更内容を読み取っていること
        - 終点の {apply_from} と作業結果の {apply_to} との間に齟齬がないこと
        - 変更への追従によって発生する周辺への影響についても整合性が取れていること
        """,
        non_goals=None,
        file_access_mode=file_access_mode,
        path_context=path_context,
        enable_document_search_mcp=True,
        aux_static_prompt=[
            SDHeader(
                "追従対象の解決方法",
                f"""
                - `{{{{work-root}}}}` ツリー内で、<cmoc_ref target="decision_apply_change"/>　が示す始点・終点 commit 間の差分を Git から取得すること
                - 始点・終点のいずれかで {apply_from} だったファイルは対象に含めること
                - 差分を取得できない場合は失敗として報告し、正常に取得できた空差分とは区別すること
                """,
            ),
        ],
        aux_dynamic_prompt=[
            SDTagBlock(
                "decision_apply_change",
                SDHeader(
                    "追従対象 git commit",
                    f"""
                    - 始点: `{diff_base_commit}`
                    - 終点: `{run_fork_commit}`
                    """,
                ),
            )
        ],
        cmoc_basic_instruction=True,
        spec_policy=spec_policy,
        realization_policy=realization_policy,
        realization_findings_policy=realization_findings_policy,
        routing_policy=True,
    )
    return AgentCallParameter(
        agent_call_kind=agent_call_kind,
        file_access_mode=file_access_mode,
        prompt=render_sd_node_as_markdown(*complete_prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        enable_document_search_mcp=True,
    )
