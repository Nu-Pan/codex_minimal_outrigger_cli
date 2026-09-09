"""session join の conflict 解消用 instruction 文面の構築定義。"""

from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_conflict_resolution_policy() -> tuple[PlaceholderMap, SDHeader]:
    """merge conflict 解消結果が満たすべき規定を構築する。

    NOTE
        意味仕様は `oracle/doc/app_spec/sub_command/session_join.md` の
        「oracle file 規定と conflict 解消の優先順位」を参照。
    """
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
                ),
            ),
        ),
    )
