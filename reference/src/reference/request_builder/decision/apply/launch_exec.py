"""`cmoc decision apply` の各ステップ用 prompt と起動パラメータの構築定義。"""

# std
from pathlib import Path
from typing import Literal

from reference.mcp.decision_validation import (
    VALIDATION_MCP_SERVER,
    VALIDATION_TOOL_NAME,
)
from reference.other.path_model import AgentCallPathContext
from reference.other.struct_doc import (
    SDHeader,
    SDTagBlock,
    SDPolicy,
    render_sd_node_as_markdown,
)
from reference.prompt_builder.complete_prompt import build_complete_prompt

# cmoc
from reference.request_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
)


def build_decision_apply_decision_request(
    agent_call_cwd: Path,
) -> AgentCallParameter:
    """decision のフォーマット的な問題を修正するリクエストを構築する

    Args:
        agent_call_cwd: 検証・修正する worktree 内の agent call の cwd

    Returns:
        decision の決定内容を保って形式だけを修正する非対話 call の入力。
        機械検証は MCP tool、修正と再検証の呼び出しは agent が行う。
    """
    # decision 全体の検査が必要なので、差分や文書検索による対象の絞り込みはしない。
    path_context = AgentCallPathContext(agent_call_cwd=agent_call_cwd)
    validation_tool = f"{VALIDATION_MCP_SERVER}.{VALIDATION_TOOL_NAME}"
    complete_prompt = build_complete_prompt(
        task=f"""
        MCP tool `{validation_tool}` による検証が正常終了し、問題を報告しない状態になるよう decision を修正すること
        """,
        scope="""
        - 対象は `{{work-root}}` ツリー内の decision file すべて
        - 修正は、検証 MCP が指摘した形式違反と、それに関連する decision 内の参照に限定すること
        """,
        completion_criteria="""
        - 最後の修正後に検証 MCP を実行し、`status` が `ok` かつ `problems` が空配列であることを確認していること
        - 変更が不要な場合も検証 MCP を実行していること
        - decision の決定内容と意味、および一意で形式が正しい既存 ID を保持していること
        - 最終応答には、検証 MCP の結果と、修正したファイルと ID を記載すること
        - 決定内容や参照先を推測しなければ修正できない箇所は、そのまま残し、場所と理由を未解消として報告すること
        - 合格を確認できなかった場合は、作業が未完了であることを報告すること
        """,
        non_goals="""
        - 決定事項の追加・削除、内容の補完、矛盾の解消、文章の推敲
        - decision 以外の調査・同期・編集
        """,
        file_access_mode=FileAccessMode.DECISION_WRITE,
        path_context=path_context,
        aux_static_prompt=[
            SDHeader(
                "decision policy",
                SDPolicy(
                    what_is_this="decision が満たすべき規定を以下に示す",
                    require=(
                        # NOTE 参照システムを確実に機能させたい
                        r"decision の見出しの先頭には `\[DEC-\d{6}\]` の形式で参照用 ID を付与する事",
                        "参照用 ID は decision 全体で一意であること",
                    ),
                    allow=(
                        # NOTE 参照システムを確実に機能させたい
                        "参照用 ID に欠番は存在してよい",
                    ),
                    exception=(
                        # NOTE 参照システムを確実に機能させたい
                        "コードブロック内の見出しは、参照用 ID 付与の対象ではない",
                    ),
                ),
            )
        ],
        cmoc_basic_instruction=True,
        enable_feedback_reporting=True,
    )
    return AgentCallParameter(
        agent_call_kind=build_decision_apply_decision_request.__name__,
        file_access_mode=FileAccessMode.DECISION_WRITE,
        prompt=render_sd_node_as_markdown(*complete_prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        enable_decision_validation_mcp=True,
    )


def build_decision_apply_spec_request(
    diff_begin_commit: str,
    diff_end_commit: str,
    agent_call_cwd: Path,
) -> AgentCallParameter:
    """`cmoc decision apply` の spec 同期ステップ用の agent call リクエストを構築する

    詳細は `_build_decision_apply_request_impl` を参照。
    """
    return _build_decision_apply_request_impl(
        diff_begin_commit,
        diff_end_commit,
        agent_call_cwd,
        "to_spec",
    )


def build_decision_apply_realization_request(
    diff_begin_commit: str,
    diff_end_commit: str,
    agent_call_cwd: Path,
) -> AgentCallParameter:
    """`cmoc decision apply` の realization 同期ステップ用の agent call リクエストを構築する

    詳細は `_build_decision_apply_request_impl` を参照。
    """
    return _build_decision_apply_request_impl(
        diff_begin_commit,
        diff_end_commit,
        agent_call_cwd,
        "to_realization",
    )


def _build_decision_apply_request_impl(
    diff_begin_commit: str,
    diff_end_commit: str,
    agent_call_cwd: Path,
    step_name: Literal["to_spec", "to_realization"],
) -> AgentCallParameter:
    """`cmoc decision apply` の各同期ステップ用の agent call リクエストを構築する

    Args:
        diff_begin_commit:
            追従対象差分の始点 commit のハッシュ値
        diff_end_commit:
            追従対象差分の終点 commit のハッシュ値
        agent_call_cwd:
            エージェントに設定するカレントディレクトリパス
        step_name:
            to_spec: decision, reference --> spec の同期を行う
            to_realization: decision, reference, spec --> realization の同期を行う

    Returns:
        構築された agent call リクエスト
    """
    # 追従対象の差分を示すタグブロックを生成する
    decision_apply_change = SDTagBlock(
        "decision_apply_change",
        SDHeader(
            "追従対象 git commit",
            f"""
            - 始点: `{diff_begin_commit}`
            - 終点: `{diff_end_commit}`
            """,
        ),
    )
    # 同期元・同期先の名前を解決する
    match step_name:
        case "to_spec":
            apply_from = "decision, reference"
            apply_to = "spec"
            file_access_mode = FileAccessMode.SPEC_WRITE
            spec_policy = True
            realization_policy = False
            agent_call_kind = "spec_edit"
        case "to_realization":
            apply_from = "decision, reference, spec"
            apply_to = "realization"
            file_access_mode = FileAccessMode.REALIZATION_WRITE
            spec_policy = False
            realization_policy = True
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
        - {apply_to} すべてが修正対象である
        - 「{apply_from} の今回の変更箇所」と直接対応しない {apply_to} も、同期に必要であれば修正してよい
        - reference の差分のうち decision から委ねられていない箇所は {apply_to} に反映する対象ではない
        """,
        completion_criteria=f"""
        - {decision_apply_change.ref_tag} が示す始点と終点の commit を Git で比較し、どちらかの時点で {apply_from} に属していたファイルの差分を確認していること
        - 反映対象とした範囲内について、終点の {apply_from} と作業結果の {apply_to} との間に齟齬がないこと
        - 変更への追従によって発生する周辺への影響についても整合性が取れていること
        - 差分を取得できない場合は失敗として報告し、正常に取得できた空差分とは区別すること
        """,
        non_goals=None,
        file_access_mode=file_access_mode,
        path_context=path_context,
        enable_document_search_mcp=True,
        aux_dynamic_prompt=[
            decision_apply_change
        ],
        cmoc_basic_instruction=True,
        reference_policy=True,
        spec_policy=spec_policy,
        realization_policy=realization_policy,
        routing_policy=True,
        enable_feedback_reporting=True,
    )
    return AgentCallParameter(
        agent_call_kind=agent_call_kind,
        file_access_mode=file_access_mode,
        prompt=render_sd_node_as_markdown(*complete_prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        enable_document_search_mcp=True,
    )
