"""oracle review の所見成立条件を伝える agent 向け文面の構築定義。"""

from oracle.other.struct_doc import StructDoc
from oracle.prompt_builder.basic import PlaceholderMap


def build_oracle_review_policy() -> tuple[PlaceholderMap, StructDoc]:
    """oracle review の全段階で共有する所見判定規定を構築する。"""
    return (
        {},
        StructDoc(
            "oracle review policy（oracle file の所見の列挙・統合・検証・採否判定時）",
            """
            **必須**

            - finding basis policy（所見・修正対象の判断時）に従い、所見または修正対象には、用途固有の policy が認める具体的な oracle file または realization file の記述・挙動を示す
            - 正本仕様断片同士に解釈の余地がない明確な矛盾がある場合は fatal とする
            - 仕様に従うと実装者の裁量では解消不能な問題が必ず発生する場合は fatal とする
            - fatal は、両立する妥当な実装方針が残っていないことを具体的な記述から説明する
            - 文意または検索性を損なう誤字、脱字、明確な文法誤り、用語不統一、または表記揺れは minor とする
            - minor は正本仕様の意味を変更しない表記上の修正として説明できなければならない
            - oracle file だけから成立する所見について、列挙、統合、擁護理由列挙、反証理由列挙、および採否判定で同じ成立条件を使用する

            **禁止**

            - finding basis policy（所見・修正対象の判断時）に従い、oracle file に記述がないこと、仕様の隙間、複数の妥当解、好み、推測、または一般的なベストプラクティスだけを根拠に所見または修正対象を作ってはいけない
            - 文法的に正しく検索性も損なわない言い回しを、好みだけで minor にしてはいけない
            - realization file、外部事情、または未確認の可能性を追加しなければ成立しない事項を、oracle file だけから成立する所見にしてはいけない
            """,
        ),
    )
