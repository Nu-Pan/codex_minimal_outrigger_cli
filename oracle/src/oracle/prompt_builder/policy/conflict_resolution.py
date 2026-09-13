"""session join の conflict 解消用 instruction 文面の構築定義。"""

from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_conflict_resolution_policy() -> tuple[PlaceholderMap, SDHeader]:
    """merge conflict 解消結果が満たすべき規定を構築する。

    NOTE
        意味仕様は `{{cmoc-root}}/oracle/doc/app_spec/sub_command/session_join.md` の
        「oracle file 規定と conflict 解消の優先順位」を参照。
    """
    return (
        {},
        SDHeader(
            "conflict resolution policy",
            SDPolicy(
                what_is_this="merge conflict を解決した結果が満たすべき規定を以下に示す",
                require=(
                    "conflict の両側と関連する oracle file を確認し、両 branch の両立する意図と挙動を解消結果に保持する",
                    "両側の意味を両立できず人間意図の選択が必要な場合は、推測で一方を破棄せず未解消事項として報告する",
                ),
                prohibit=(
                    "適用される規定に違反する解消結果を conflict 解消完了として扱ってはいけない",
                ),
                allow=(
                    "解消に付随する編集の要否・範囲は自ら判断してよい",
                ),
            ),
        ),
    )
