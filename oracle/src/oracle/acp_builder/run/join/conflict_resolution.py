"""run join と feedback 自動 join の競合解消 call の構築定義。"""

from pathlib import Path

from oracle.acp_builder.basic import (
    AgentCallParameter,
    DocumentSearchScope,
    FileAccessMode,
)
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


def build_run_join_conflict_resolution_parameter(
    run_head_commit: str,
    session_head_commit: str,
    session_worktree: Path,
    *,
    document_search_scope: DocumentSearchScope,
    feedback_report_cut_path: Path | None = None,
) -> AgentCallParameter:
    """session 上で run の成果を統合し、必要なら封印済み結果を検証する。

    Args:
        document_search_scope: caller が確定した、その call の実効閲覧範囲。
        run_head_commit: 差分検査後、merge 前に確定した run branch の HEAD。
        session_head_commit: merge 前に確定した session branch の HEAD。
        session_worktree: run の merge が進行中の session worktree。
        feedback_report_cut_path: 自動 join 時の封印済み report cut への参照。

    NOTE
        意味仕様は `{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の
        「競合解消」と、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の
        「封印後のマージ調整」「join 後の検証と記録」を参照。
        元の workload と同様に oracle は変更せず、REALIZATION_WRITE を使う。
        進行中の tree の関連文書を検索するため、caller の scope を渡す。
    """
    # merge target を起点とし、封印済み結果がある場合だけ追加指示を組み込む。
    path_context = AgentCallPathContext(agent_call_cwd=session_worktree)
    static_prompt: tuple[SDHeader | SDTagBlock, ...] = ()
    dynamic_prompt: tuple[SDHeader | SDTagBlock, ...] = ()
    if feedback_report_cut_path is not None:
        report_cut_path = resolve_real_path(feedback_report_cut_path, path_context)
        static_prompt = (
            SDHeader(
                "採用結果と判定根拠の読み方",
                """
                - 入力の report cut は、維持すべき採用結果と、その根拠を記録した checkpoint への参照を示す
                - `fixed` は修正と必要な検証が完了した結果、`already_resolved` は処理時点ですでに問題が存在しなかった結果を表す
                - `not_actionable` は具体的な根拠のある報告対象の問題に該当しなかった結果を表す
                - `human_required` は問題が現在も存在し、oracle の変更、人間意図の確定、外部状態の変更など、realization file の編集だけでは満たせない具体的な対応を必要とする結果を表す
                - `inconclusive` は許可された情報では判定できない、または再確認・再修正が同じ状態を往復して収束できないことが確認された結果を表す
                - 判定根拠には対象ファイルだけでなく、依存設定、検査の条件と結果なども含む。ファイル内容の変化だけで旧判定の誤りや問題の解消を断定しないこと
                """,
            ),
            SDHeader(
                "封印済み結果を維持する統合",
                """
                - 封印済み結果の参照 <cmoc_ref target="sealed_feedback_result"/> にある report cut と、そこから参照される採用結果・checkpoint・判定根拠を読み取り専用で確認すること
                - 封印済みの採用結果を維持するために必要なマージ調整だけを行うこと。内容を run 側と同一に保つこと自体は目的にしないこと
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
        source_commit=run_head_commit,
        target_commit=session_head_commit,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        path_context=path_context,
        document_search_scope=document_search_scope,
        aux_static_prompt=static_prompt,
        aux_dynamic_prompt=dynamic_prompt,
    )
    return AgentCallParameter(
        agent_call_kind=build_run_join_conflict_resolution_parameter.__name__,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        prompt=render_sd_node_as_markdown(*prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        document_search_scope=document_search_scope,
    )
