"""oracle review の所見成立条件を伝える agent 向け文面の構築定義。"""

from oracle.other.struct_doc import StructDoc
from oracle.prompt_builder.basic import PlaceholderMap


def build_oracle_review_policy() -> tuple[PlaceholderMap, StructDoc]:
    """oracle review の全段階で共有する所見判定規定を構築する。"""
    return (
        {},
        StructDoc(
            "oracle review policy（oracle file の所見の列挙・統合・検証・採否判定時）",
            StructDoc(
                "finding basis policy（所見・修正対象の判断時）",
                StructDoc(
                    "所見・修正対象に具体的な根拠を求める",
                    """
                    **必須**

                    - 所見または修正対象には、用途固有の policy が認める具体的な oracle file または realization file の記述・挙動を示す

                    **禁止**

                    - oracle file に記述がないこと、仕様の隙間、複数の妥当解、好み、推測、または一般的なベストプラクティスだけを根拠に所見または修正対象を作ってはいけない
                    """,
                ),
            ),
            StructDoc(
                "実装者の裁量で解消不能な問題だけを fatal 所見にする",
                """
                **必須**

                - 正本仕様断片同士に解釈の余地がない明確な矛盾がある場合は fatal とする
                - 仕様に従うと実装者の裁量では解消不能な問題が必ず発生する場合は fatal とする
                - fatal は、両立する妥当な実装方針が残っていないことを具体的な記述から説明する
                """,
            ),
            StructDoc(
                "文意または検索性を損なう表記上の誤りだけを minor 所見にする",
                """
                **必須**

                - 文意または検索性を損なう誤字、脱字、明確な文法誤り、用語不統一、または表記揺れは minor とする
                - minor は正本仕様の意味を変更しない表記上の修正として説明できなければならない

                **禁止**

                - 文法的に正しく検索性も損なわない言い回しを、好みだけで minor にしてはいけない
                """,
            ),
            StructDoc(
                "oracle file だけから成立する問題を所見にする",
                """
                **必須**

                - 所見の列挙、統合、擁護理由列挙、反証理由列挙、および採否判定で同じ成立条件を使用する

                **禁止**

                - realization file、外部事情、または未確認の可能性を追加しなければ成立しない事項を所見にしてはいけない
                """,
            ),
        ),
    )
