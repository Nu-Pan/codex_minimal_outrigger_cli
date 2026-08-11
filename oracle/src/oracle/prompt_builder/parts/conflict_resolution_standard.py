"""session join の conflict 解消用 instruction 文面の構築定義。"""

# cmoc
from oracle.other.standard import Requirement, Standard, standard_to_struct_doc
from oracle.other.struct_doc import StructDoc
from oracle.prompt_builder.basic import PlaceholderMap


def build_conflict_resolution_standard() -> tuple[PlaceholderMap, StructDoc]:
    """oracle / realization の意味を保つ conflict 解消規範を構築する。"""
    standard = Standard(
        title="両 branch の意味を保って conflict marker だけを解消する",
        requirements=[
            Requirement(
                "必須",
                "conflict 対象の両側と関連する oracle file を読み、両立する意図と挙動を失わない解消結果にする",
            ),
            Requirement(
                "禁止",
                "conflict marker の解消に不要な仕様変更、実装改善、整形、または別 file の変更を行ってはいけない",
            ),
            Requirement(
                "禁止",
                "realization file の都合を正本として oracle file の意味を変更してはいけない",
            ),
            Requirement(
                "必須",
                "両側の意味を両立できず人間意図の選択が必要な場合は、推測で一方を破棄せず未解消事項として報告する",
            ),
        ],
    )
    return (
        {},
        StructDoc(
            "conflict resolution standard",
            StructDoc(
                "適用条件",
                "- `cmoc session join` の conflict marker を解消する場合だけ適用する",
            ),
            standard_to_struct_doc(standard),
        ),
    )
