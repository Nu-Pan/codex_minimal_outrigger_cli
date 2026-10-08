"""refactor fork のファイル単位の調査・改善 prompt 文面の構築定義。"""

# std
from pathlib import Path

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
)
from oracle.other.path_model import AgentCallPathContext, resolve_real_path
from oracle.other.struct_doc import SDHeader, render_sd_node_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_realization_refactor_fork_file_review_and_fix_parameter(
    target_path: Path,
    run_worktree: Path,
) -> AgentCallParameter:
    """仕様適合と検出能力を保つ、ファイル起点の改善パラメータを構築する。

    Args:
        target_path: run worktree 上のレビュー対象 path。
        run_worktree: AgentCallParameter.agent_call_cwd とする linked worktree。

    NOTE
        意味仕様は `{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md`
        の「1 処理単位」「確定前の検証」と、
        `{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization.md`
        の「realization refactor の改善判断」を参照。
    """
    path_context = AgentCallPathContext(agent_call_cwd=run_worktree)
    prompt = build_complete_prompt(
        task="""
        - oracle file または realization file である `{{target-path}}` を起点に、仕様への適合と必要な回帰検出能力を保ちながら、テストと実装のムダを調査・削減し、テスト実行時間の短縮につながる realization file の改善を行うこと
        """,
        scope="""
        - `{{target-path}}` と、関連する oracle file および realization file を調べ、変更と検証を一体として扱える小さなまとまりを選ぶこと。関連する複数 file の変更を含めてよい
        """,
        completion_criteria="""
        - 今回の関連範囲を調査し、残す変更について、この agent call 内で修正後の再調査と所定の検証を終えていること。根拠のある改善が見つからない場合は、変更なしで完了してよい
        """,
        non_goals="""
        - 一つの agent call で全 file の調査を完遂すること、改善余地の不存在を証明すること、または一定の短縮率を達成すること
        - 無関係な機能の再設計や、将来用の汎用化
        """,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        path_context=path_context,
        enable_document_search_mcp=True,
        aux_static_prompt=[
            SDHeader(
                "改善の判断基準",
                """
                - 仕様に適合する箇所にも、具体的な根拠のあるムダの削減を認める。重複テスト、過剰な準備処理、不要な待機・process 起動、責務の重複、旧仕様の実装などを調べる
                - 対象箇所と、不要・重複・過剰と判断した根拠を確認し、改善がテストの負担を減らす理由を説明できる変更にする。好みや一般論だけで変更しない
                - テストを削除・統合する場合は、維持すべき要求と検出する回帰を特定し、残る検証でその能力を保てること、または現行仕様で不要になった根拠を確かめる。必要な境界条件や失敗時挙動の検証を失わせない
                - 件数・行数の減少や test の成功だけを削除の根拠にしない。期待効果と実測値を区別し、test の除外や検出能力の低下を時間短縮の成果にしない
                - full test 1 回の時間短縮と、検査の実行回数を減らしたことによる作業全体の時間短縮を混同しない
                """,
            ),
            SDHeader(
                "変更後の検証",
                """
                - 対象 repository が定める品質検証を、残す差分全体の最後の変更後に、この agent call 内で実施する
                - full test を含む完了ゲートが要求される変更では、その全体を終える。focused test だけで済ませたり、後続の作業へ全体検証を先送りしたりしない
                - 検証の未実行・途中・失敗を成功として扱わない。中断を通知された場合は、新しい作業・検査を開始せず、実行中の作業を停止する
                - Real Codex CLI を使う test は、その実行をユーザーが明示的に指示した場合に限る。この改善作業の依頼だけを実行指示として扱わない
                """,
            ),
            SDHeader(
                "Structured Output の決定論的事後条件",
                """
                - この agent call の開始時点を基準として、出力時点に残る realization file の net 差分の path 集合を、実際の変更 path 集合とする
                - 実際の変更 path 集合は、schema が `changed_paths` に定義する path 表現に従って算出する
                - 全所見の `changed_paths` の和集合を、申告された変更 path 集合とする。同じ path を複数の所見に含めてよい
                - 申告された変更 path 集合は、実際の変更 path 集合と一致しなければならない
                - `evidences[].path` は変更 path の申告または照合に使用しない
                """,
            ),
            SDHeader(
                "作業上の注意点",
                """
                - commit 差分、変更 commit の列、変更要約は入力として与えられていない。最近の差分を推測して作業範囲を狭めてはいけない
                - 所見の調査、修正、修正後の検証を同一の agent call 内で行う
                - git add と git commit は実行禁止
                """,
            ),
        ],
        aux_placeholder_def={
            "target-path": resolve_real_path(target_path, path_context),
        },
        oracle_and_realization_basic=True,
        realization_policy=True,
        realization_findings_policy=True,
        routing_policy=True,
    )
    return AgentCallParameter(
        agent_call_kind=(
            build_realization_refactor_fork_file_review_and_fix_parameter.__name__
        ),
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        prompt=render_sd_node_as_markdown(*prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        agent_call_cwd=path_context.agent_call_cwd,
        enable_document_search_mcp=True,
    )
