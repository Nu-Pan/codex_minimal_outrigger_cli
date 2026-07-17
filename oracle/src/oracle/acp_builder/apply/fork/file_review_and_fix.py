"""`cmoc apply fork` のファイル単位レビュー・修正 prompt 正本。"""

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


def build_apply_fork_file_review_and_fix_parameter(
    target_path: Path,
) -> AgentCallParameter:
    """`cmoc apply fork` のファイル単位レビュー・修正用パラメータを構築する。"""
    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア実装のファイル単位レビュー兼修正担当です",
        summary="""
        - `{{target-path}}` を起点に `{{repo-root}}` ツリー内の所見を調査し、対応する realization file を修正すること
        """,
        goal="""
        - `{{target-path}}` 以外の必要な oracle file, realization file も読んでいること
        - 列挙した所見が apply review standard を満たしていること
        - 発見した所見に対応する修正をベストエフォートで実施したこと
        - 修正したファイルを再調査し、この agent call 内で対応可能な所見を残していないこと
        - realization file が realization standard に従っていること
        - 全てのテストに通過する状態であること
        - 指定された Structured Output schema に従い、この agent call で発見した所見と対応結果を返すこと
        """,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        aux_static_prompt=[
            StructDoc(
                "作業上の注意点",
                """
                - 所見の調査、修正、修正後の検証を同一の agent call 内で行う
                - 修正後に解消した所見も、この agent call で発見した所見として `findings` に含める
                - 所見が見つからなかった場合は `findings` を空にし、ファイルに差分を発生させない
                - ファイルに加える全ての差分を、`findings` のいずれかと対応させる
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
    # ファイル数分のコストを抑えつつ所見漏れを避けるため、効率モデルの最大推論を使う。
    return AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.MAX,
        FileAccessMode.REALIZATION_WRITE,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
        True,
    )
