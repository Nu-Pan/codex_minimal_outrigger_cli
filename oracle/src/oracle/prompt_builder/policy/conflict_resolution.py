"""session join の conflict 解消用 instruction 文面の構築定義。"""

from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_conflict_resolution_policy() -> tuple[PlaceholderMap, SDHeader]:
    """merge conflict 解決処理結果が満たすべき規定を構築する。"""
    return (
        {},
        SDHeader(
            "conflict resolution policy",
            SDPolicy(
                what_is_this="merge conflict を解決した結果が満たすべき規定を以下に示す",
                require=(
                    "両方のマージ元ブランチの oracle file で両立する意図と挙動を失っていない",
                    "意味を両立できる解決方法が無い場合は、一方を破棄せず未解消事項として報告する",
                ),
                prohibit=(
                    "realization file の都合または挙動を根拠に oracle file の意味を変更してはいけない",
                    "conflict marker の解消に対して不必要な変更を行ってはいけない",
                ),
            ),
        ),
    )
