"""oracle review の所見成立条件を伝える agent 向け文面の構築定義。"""

from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_oracle_review_policy() -> tuple[PlaceholderMap, SDHeader]:
    """oracle review の全段階で共有する所見判定規定を構築する。"""
    return (
        {},
        SDHeader(
            "oracle findings review policy",
            SDPolicy(
                what_is_this="oracle file に対する所見が満たすべき規定を以下に示す",
                require=(
                    "正本仕様断片同士に解釈の余地がない明確な矛盾がある場合は fatal 所見とする",
                    "仕様に従うと実装者の裁量では解消不能な問題が必ず発生する場合は fatal 所見とする",
                    "所見の根拠として oracle file, realization file の記述・挙動を示す",
                    "fatal 所見は、妥当な実装方針が残っていないことを具体的な記述から説明する",
                    "文意または検索性を損なう誤字、脱字、明確な文法誤り、用語不統一、または表記揺れは minor 所見とする",
                    "minor 所見は正本仕様の意味を変更しない表記上の修正として説明できなければならない",
                    "oracle file だけから成立する所見について、作業の種類によらず一貫した成立条件を使用する",
                ),
                prohibit=(
                    "興味の対象ではない事 (e.g. 根拠が oracle file にない、仕様の隙間がある、複数の妥当解がある、好みでしかない、推測に基づく、一般的なベストプラクティスだけを根拠とする) を根拠に所見を作ってはいけない",
                    "oracle file の外 (e.g. realization file、リポジトリ外部の事情、未確認の可能性を追加しなければ成立しない事項) を根拠に所見を作ってはいけない",
                ),
            ),
        ),
    )
