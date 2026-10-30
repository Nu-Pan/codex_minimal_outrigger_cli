"""編集 run の自動 join と明示 join に共通する競合解消 call の構築定義。"""

from pathlib import Path

from oracle.other.path_model import AgentCallPathContext, resolve_real_path
from oracle.other.struct_doc import (
    SDCodeBlock,
    SDHeader,
    SDTagBlock,
    render_sd_node_as_markdown,
)
from oracle.prompt_builder.merge_conflict_resolution import (
    build_merge_conflict_resolution_prompt,
)
from oracle.request_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
)


def build_run_join_conflict_resolution_request(
    run_head_commit: str,
    session_head_commit: str,
    run_worktree: Path,
    *,
    feedback_report_cut_path: Path | None = None,
) -> AgentCallParameter:
    """run 上で session の変更を統合し、必要なら封印済み結果を検証する。

    Args:
        run_head_commit: 差分検査と必要な取消の後、session 統合直前の run HEAD。
        session_head_commit: 今回の準備で基準とする session HEAD。
        run_worktree: session を統合する merge が進行中の run worktree。
        feedback_report_cut_path: 自然完了した feedback の封印済み report cut への参照。
            publication を行わない join と他 workload では渡さない。

    NOTE
        意味仕様は `{{cmoc-root}}/spec/app_spec/sub_command/editing_run.md` の
        「競合解消」と、`{{cmoc-root}}/spec/app_spec/sub_command/feedback_report.md` の
        「封印後のマージ調整」「join 後の検証と記録」を参照。
        decision・reference は変更せず、spec・realization の統合に
        SPEC_AND_REALIZATION_WRITE を使う。
    """
    # merge target の run を起点に、呼び出し全体のアクセス境界をそろえる。
    path_context = AgentCallPathContext(agent_call_cwd=run_worktree)
    static_prompt: tuple[SDHeader | SDTagBlock, ...] = (
        SDHeader(
            "今回の統合",
            """
            - source は session の確定済み変更、target はその変更を受け入れる merge の開始直前の run HEAD を表す
            - cwd と `{{work-root}}` は、session を統合中の run worktree を指す。ここで内容の統合と必要な検証を完了すること
            - 元の成果の commit を書き換えず、進行中の merge 結果を編集すること
            """,
        ),
    )
    dynamic_prompt: tuple[SDHeader | SDTagBlock, ...] = ()
    if feedback_report_cut_path is not None:
        report_cut_path = resolve_real_path(feedback_report_cut_path, path_context)
        static_prompt += (
            SDHeader(
                "採用結果と判定根拠の読み方",
                """
                - 入力の report cut は、維持すべき採用結果と、その根拠を記録した checkpoint への参照を示す
                - `fixed` は修正と必要な検証が完了した結果、`already_resolved` は処理時点ですでに問題が存在しなかった結果を表す
                - `not_actionable` は具体的な根拠のある報告対象の問題に該当しなかった結果を表す
                - `human_required` は問題が現在も存在し、decision・reference の変更、人間意図の確定、外部状態の変更など、spec file・realization file の編集だけでは満たせない具体的な対応を必要とする結果を表す
                - `inconclusive` は許可された情報では判定できない、または再確認・再修正が同じ状態を往復して収束できないことが確認された結果を表す
                - 判定根拠には対象ファイルだけでなく、依存設定、検査の条件と結果なども含む。ファイル内容の変化だけで旧判定の誤りや問題の解消を断定しないこと
                """,
            ),
            SDHeader(
                "封印済み結果を維持する統合",
                """
                - 封印済み結果の参照 <cmoc_ref target="sealed_feedback_result"/> にある report cut と、そこから参照される採用結果・checkpoint・判定根拠を読み取り専用で確認すること。report cut の run HEAD は封印時の成果を指し、現在の merge 結果とは区別すること
                - 封印済みの採用結果を維持するために必要なマージ調整だけを行うこと。内容を封印時と同一に保つこと自体は目的にしないこと
                - 調整の影響を受ける判定を全結果分類から特定し、作業を終える前に必要な検証を行うこと
                - 最終回答で、調整の対象・判断理由、影響を受けた判定、採用結果を維持できる根拠、および検証の対象と結果を報告すること
                - 結果分類そのものの変更が必要な場合、または必要な検証で採用結果の維持を確認できない場合は、未解消として具体的な理由を報告すること
                - 封印済み artifact、採用結果とその結果分類、または run branch の issue commit を書き換えないこと。issue 処理のやり直しや対象外 issue の探索を行わないこと
                - artifact の hash 一致だけを、マージ調整後の内容や採用結果が妥当である根拠にしないこと
                """,
            ),
        )
        dynamic_prompt = (
            SDTagBlock(
                "sealed_feedback_result",
                SDHeader(
                    "封印済み結果の参照",
                    SDCodeBlock("text", str(report_cut_path)),
                ),
            ),
        )

    # 共通の目的・commit 参照入力・policy を、run 固有の編集境界に合わせる。
    prompt = build_merge_conflict_resolution_prompt(
        source_commit=session_head_commit,
        target_commit=run_head_commit,
        file_access_mode=FileAccessMode.SPEC_AND_REALIZATION_WRITE,
        path_context=path_context,
        aux_static_prompt=static_prompt,
        aux_dynamic_prompt=dynamic_prompt,
    )
    return AgentCallParameter(
        agent_call_kind="realization_edit",
        file_access_mode=FileAccessMode.SPEC_AND_REALIZATION_WRITE,
        prompt=render_sd_node_as_markdown(*prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        enable_document_search_mcp=True,
    )
