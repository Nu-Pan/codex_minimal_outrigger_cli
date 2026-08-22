"""refactor fork のファイル単位レビュー・修正 prompt 文面の構築定義。"""

# std
from pathlib import Path

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import AgentCallPathContext, resolve_real_path
from oracle.other.struct_doc import SDHeader, render_sd_node_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_realization_refactor_fork_file_review_and_fix_parameter(
    target_path: Path,
    run_worktree: Path,
) -> AgentCallParameter:
    """差分に依存しないファイル単位の追従パラメータを構築する。

    Args:
        target_path: run worktree 上のレビュー対象 path。
        run_worktree: AgentCallParameter.agent_call_cwd とする linked worktree。
    """
    # run worktree を agent_call_cwd として先に確定する
    path_context = AgentCallPathContext(agent_call_cwd=run_worktree)

    # 対象 file を起点に、調査から検証までを行う完全プロンプトを構築する。
    prompt = build_complete_prompt(
        summary="""
        - あなたはソフトウェア実装のファイル単位レビュー兼修正担当です
        - oracle file または realization file である `{{target-path}}` を起点に `{{work-root}}` ツリー内の所見を調査し、対応する realization file を修正すること
        """,
        goal="""
        - `{{target-path}}` 以外の必要な oracle file, realization file も読んでいること
        - 列挙した所見が realization findings policy を満たしていること
        - 発見した所見に対応する修正をベストエフォートで実施したこと
        - 修正した file を再調査し、この agent call 内で対応可能な所見を残していないこと
        - realization file が realization policy に従っていること
        - 対象 repository が要求する必要な検証を完了していること
        - 指定された Structured Output schema に従い、この agent call で発見した所見と対応結果を返すこと
        """,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        path_context=path_context,
        aux_static_prompt=[
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
                - 調査開始時点の既存実装ですでに解消されている問題を所見に含めてはいけない
                - 所見の調査、修正、修正後の検証を同一の agent call 内で行う
                - `resolution.status=fixed` は、この agent call 内で所見に対応する realization file を実際に変更し、修正後の検証まで行った場合だけ使用する
                - この agent call で realization file を変更して解消した所見も、この agent call で発見した所見として `findings` に含める
                - git add と git commit は実行禁止
                """,
            ),
        ],
        aux_placeholder_def={
            "target-path": resolve_real_path(target_path, path_context),
        },
        oracle_and_realization_basic=True,
        oracle_policy=True,
        realization_policy=True,
        realization_findings_policy=True,
        routing_policy=True,
    )

    # 全 oracle file と realization file に適用するため、効率モデルの最大推論を使う。
    return AgentCallParameter(
        agent_call_kind=(
            build_realization_refactor_fork_file_review_and_fix_parameter.__name__
        ),
        model_class=ModelClass.EFFICIENCY,
        reasoning_effort=ReasoningEffort.MAX,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        prompt=render_sd_node_as_markdown(*prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=True,
    )
