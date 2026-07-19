"""`cmoc realization refactor fork` のファイル単位レビュー・修正 prompt 正本。"""

# std
from pathlib import Path

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import resolve_real_path, resolve_repo_root
from oracle.other.struct_doc import StructDoc, render_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_realization_refactor_fork_file_review_and_fix_parameter(
    target_path: Path,
) -> AgentCallParameter:
    """差分に依存しないファイル単位の追従パラメータを構築する。"""
    # 対象 file を起点に、調査から検証までを行う完全プロンプトを構築する。
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア実装のファイル単位レビュー兼修正担当です",
        summary="""
        - oracle file または realization file である `{{target-path}}` を起点に `{{repo-root}}` ツリー内の所見を調査し、対応する realization file を修正すること
        """,
        goal="""
        - `{{target-path}}` 以外の必要な oracle file, realization file も読んでいること
        - 列挙した所見が apply review standard を満たしていること
        - 発見した所見に対応する修正をベストエフォートで実施したこと
        - 修正した file を再調査し、この agent call 内で対応可能な所見を残していないこと
        - realization file が realization standard に従っていること
        - 全ての test に通過する状態であること
        - 指定された Structured Output schema に従い、この agent call で発見した所見と対応結果を返すこと
        """,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        aux_static_prompt=[
            StructDoc(
                "作業上の注意点",
                """
                - commit 差分、変更 commit の列、変更要約は入力として与えられていない。最近の差分を推測して作業範囲を狭めてはいけない
                - 所見の調査、修正、修正後の検証を同一の agent call 内で行う
                - 修正後に解消した所見も、この agent call で発見した所見として `findings` に含める
                - 所見が見つからなかった場合は `findings` を空にし、file に差分を発生させない
                - file に加える全ての差分を、`findings` のいずれかと対応させる
                - git add と git commit は実行禁止
                """,
            ),
        ],
        aux_placeholder_def={
            "repo-root": resolve_repo_root(),
            "target-path": resolve_real_path(target_path),
        },
        oracle_standard=True,
        realization_standard=True,
        apply_review_standard=True,
    )

    # 全 oracle file と realization file に適用するため、効率モデルの最大推論を使う。
    return AgentCallParameter(
        model_class=ModelClass.EFFICIENCY,
        reasoning_effort=ReasoningEffort.MAX,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        prompt=render_as_markdown(prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        run_indexing_preflight=True,
    )
