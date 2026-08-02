"""oracle review の所見判定規範を構築する単一の正本。"""

# cmoc
from oracle.other.standard import Requirement, Standard, standard_to_struct_doc
from oracle.other.struct_doc import StructDoc
from oracle.prompt_builder.basic import PlaceholderMap


def build_oracle_review_standard() -> tuple[PlaceholderMap, StructDoc]:
    """oracle review の全段階で共有する所見判定規範を構築する。"""
    standards = [
        Standard(
            title="実装者の裁量で解消不能な問題だけを fatal 所見にする",
            backgrounds=[
                "明確に矛盾する正本仕様断片から一貫した実装は導けない",
                "仕様に従うと必ず発生する解消不能な問題には人間判断が必要である",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "正本仕様断片同士に解釈の余地がない明確な矛盾がある場合は fatal とする",
                ),
                Requirement(
                    "必須",
                    "仕様に従うと実装者の裁量では解消不能な問題が必ず発生する場合は fatal とする",
                ),
                Requirement(
                    "必須",
                    "fatal は、両立する妥当な実装方針が残っていないことを具体的な記述から説明する",
                ),
                Requirement(
                    "禁止",
                    "仕様の隙間、複数の妥当解、推測、好み、または一般的なベストプラクティスを fatal の根拠にしてはいけない",
                ),
            ],
        ),
        Standard(
            title="文意または検索性を損なう表記上の誤りだけを minor 所見にする",
            backgrounds=[
                "誤字や文法誤りは正本仕様の理解を損なう",
                "用語不統一と表記揺れは関連仕様の検索を不安定にする",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "文意または検索性を損なう誤字、脱字、明確な文法誤り、用語不統一、または表記揺れは minor とする",
                ),
                Requirement(
                    "必須",
                    "minor は正本仕様の意味を変更しない表記上の修正として説明できなければならない",
                ),
                Requirement(
                    "禁止",
                    "文法的に正しく検索性も損なわない言い回しを、好みだけで minor にしてはいけない",
                ),
            ],
        ),
        Standard(
            title="oracle file の具体的な記述だけから問題と言えない事項は所見にしない",
            backgrounds=[
                "oracle file は仕様全体を網羅しない正本仕様断片である",
                "所見の各段階で同じ採否境界を使用しなければ判定が不安定になる",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "各所見は oracle file の具体的な記述だけから問題であることを説明する",
                ),
                Requirement(
                    "禁止",
                    "仕様の隙間、複数の妥当解、好み、推測、または一般的なベストプラクティスだけを根拠に所見を作ってはいけない",
                ),
                Requirement(
                    "禁止",
                    "realization file、外部事情、または未確認の可能性を追加しなければ成立しない事項を所見にしてはいけない",
                ),
                Requirement(
                    "必須",
                    "所見の列挙、統合、擁護理由列挙、反証理由列挙、および採否判定でこの同じ境界を使用する",
                ),
            ],
        ),
    ]
    return (
        {},
        StructDoc(
            "oracle review standard",
            StructDoc(
                "適用条件",
                "- oracle file の所見を列挙、統合、検証、または採否判定する場合に適用する",
            ),
            *[standard_to_struct_doc(standard) for standard in standards],
        ),
    )
