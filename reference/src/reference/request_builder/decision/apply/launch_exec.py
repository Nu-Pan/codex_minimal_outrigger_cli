"""`cmoc decision apply` の各ステップ用 prompt と起動パラメータの構築定義。"""

# std
from pathlib import Path
from typing import Literal

from reference.other.path_model import AgentCallPathContext
from reference.other.struct_doc import (
    SDHeader,
    SDPolicy,
    SDTagBlock,
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
    """decision の形式検証と自動修正を依頼するリクエストを構築する。

    Args:
        agent_call_cwd: 検証・修正する worktree 内の agent call の cwd。

    Returns:
        decision の決定内容を保って形式だけを修正する非対話 call の入力。
        機械検証・修正・再検証は、この入力を受け取った agent が行う。
    """
    # decision 全体の検査が必要なので、差分や文書検索による対象の絞り込みはしない。
    path_context = AgentCallPathContext(agent_call_cwd=agent_call_cwd)
    complete_prompt = build_complete_prompt(
        task="""
        decision の形式を機械的に検証し、違反がある場合は決定内容を変えずに自動修正すること
        """,
        scope="""
        - 対象は `{{work-root}}` ツリー内の decision file すべて
        - 修正は、見出しの ID の不足・形式違反・重複と、それに伴う decision 内の参照表記の修正に限定すること
        """,
        completion_criteria="""
        - 対象全体をコマンドまたはスクリプトで機械的に検証していること
        - 修正した場合は同じ検証を再実行し、形式違反が残っていないことを確認していること
        - decision の決定内容と意味、および一意で形式が正しい既存 ID を保持していること
        - 最終応答に、検証方法・結果、修正したファイルと ID、未解消の違反があればその場所と理由を記載すること
        """,
        non_goals="""
        - 決定事項の追加・削除、内容の補完、矛盾の解消、文章の推敲
        - reference, spec, realization の調査・同期・編集
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
            典型的には、前回の `cmoc decision apply` と対応する run fork commit が渡されるはず
        diff_end_commit:
            追従対象差分の終点 commit のハッシュ値
            `step_name=="to_spec"`: 典型的には、今回の `cmoc decision apply` と対応する run fork commit が渡されるはず
            `step_name=="to_realization"`: 典型的には、直前の `to_spec` が正常終了した時点の commit が渡されるはず
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
                    - 始点: `{diff_begin_commit}`
                    - 終点: `{diff_end_commit}`
                    """,
                ),
            )
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
