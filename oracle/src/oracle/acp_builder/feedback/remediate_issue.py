"""feedback issue remediation 用 prompt 文面と起動パラメータの構築定義。"""

# std
from pathlib import Path

# cmoc
from oracle.acp_builder.basic import AgentCallParameter, FileAccessMode
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import SDCodeBlock, SDHeader, render_sd_node_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_feedback_remediate_issue_parameter(
    issue_json: str,
    run_worktree: Path,
) -> AgentCallParameter:
    """正規化済み issue 1 件を確認し、安全な realization 修正と検証を行う。"""
    path_context = AgentCallPathContext(agent_call_cwd=run_worktree)
    prompt = build_complete_prompt(
        task="""
        - 入力された 1 件の feedback issue が現在の run tree に存在するか確認すること
        - realization file の編集だけで安全に解決できる場合は、この agent call 内で修正し、必要な検証を完了すること
        - 確認、修正、および検証の結果を issue remediation result として返すこと
        """,
        scope="""
        - 入力 issue と、その確認・修正・検証に必要な oracle file および realization file を対象とすること
        """,
        non_goals="""
        - 入力 issue 以外の問題を、この call の remediation 対象として修正しないこと
        - oracle file、人間意図、外部状態、sandbox、または権限境界を変更しないこと
        """,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        path_context=path_context,
        aux_static_prompt=[
            SDHeader(
                "結果分類の規則",
                """
                - result は feedback の意味仕様と Structured Output schema が定める分類に従う
                - `human_required` は、realization file の編集だけでは満たせない具体的な対応を確認できた場合だけ使用する
                - 許可された情報では判定できない場合は `inconclusive` とし、`human_required` へ変換しない
                - agent call、tool、validation、または作業の失敗だけを理由に `human_required` としてはならない
                """,
            ),
            SDHeader(
                "Structured Output の決定論的事後条件",
                """
                - `result.issue_id` は入力 issue ID と完全一致させる
                - 論理 agent call の開始時点から正式な終了時点までに残る realization file の net 差分の path 集合を、実際の変更 path 集合とする
                - `result.changed_paths` に重複を含めず、実際の変更 path 集合と一致させる
                - path は正規化済みの `{{work-root}}` 相対 path とする。追加と変更は終了時点、削除は開始時点、rename は rename 前後の path で表す
                - `fixed` の verification は実際に成功した修正後の検証だけを表す
                - `already_resolved | not_actionable | inconclusive` では、実際の realization file の net 差分を残さない
                - `human_required` で差分を残す場合は、安全で独立して検証済みの部分修正だけとする
                """,
            ),
            SDHeader(
                "作業上の制約",
                """
                - 実行した command または inspection と、その成否を verification に記録する
                - `git add` と `git commit` を実行しない
                """,
            ),
        ],
        aux_dynamic_prompt=[
            SDHeader(
                "正規化済み feedback issue",
                SDCodeBlock("json", issue_json),
            ),
        ],
        oracle_and_realization_basic=True,
        realization_policy=True,
        routing_policy=True,
    )

    return AgentCallParameter(
        agent_call_kind=build_feedback_remediate_issue_parameter.__name__,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        prompt=render_sd_node_as_markdown(*prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=False,
    )
