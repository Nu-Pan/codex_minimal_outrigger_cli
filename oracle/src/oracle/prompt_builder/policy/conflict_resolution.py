"""session join の conflict 解消用 instruction 文面の構築定義。"""

from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_conflict_resolution_policy() -> tuple[PlaceholderMap, SDHeader]:
    """oracle / realization の意味を保つ conflict 解消規定を構築する。"""
    return (
        {},
        SDHeader(
            "conflict resolution policy（`cmoc session join` の conflict marker 解消時だけ）",
            SDPolicy(
                when_use_this="",
                require=(
                    "oracle authority policy（oracle・realization file を扱う時）では、oracle file を人間が所有する正本仕様断片として扱う",
                    "conflict 対象の両側と関連する oracle file を読み、両立する意図と挙動を失わない解消結果にする",
                    "両側の意味を両立できず人間意図の選択が必要な場合は、推測で一方を破棄せず未解消事項として報告する",
                ),
                prohibit=(
                    "oracle authority policy（oracle・realization file を扱う時）では、realization file の都合または挙動を根拠に oracle file の意味を変更してはいけない",
                    "conflict marker の解消に不要な仕様変更、実装改善、整形、または別 file の変更を行ってはいけない",
                ),
                allow=(),
            ),
        ),
    )
