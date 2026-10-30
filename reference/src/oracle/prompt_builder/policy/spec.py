"""oracle file を扱う agent call 向け instruction 文面の構築定義。"""

from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_spec_policy() -> tuple[PlaceholderMap, SDHeader]:
    """spec が満たすべき規定を構築する

    NOTE
        cmoc basic instruction と重複しないように注意
    """
    return (
        {},
        SDHeader(
            "spec policy",
            SDPolicy(
                what_is_this="spec が満たすべき規定を以下に示す",
                require=(
                    # NOTE 実装差≒未定義を最大化して、spec の肥大化を抑制したい
                    "spec から、実装差を許容する・しないの境界が読み取れる事",
                    "実装差を許容する余地を最大限尊重する事",
                    # NOTE 参照を書かせて、関係情報の取りこぼしを予防したい
                    "併せて読む必要がある decisition, reference, spec への参照を書く事",
                    # NOTE 用語を統一してキーワード検索の有効性を担保したい
                    "ある概念が複数個所で繰り返し登場する場合、リポジトリ全体で統一的な専用の用語を与える事",
                ),
                prohibit=(
                    # NOTE spec の肥大化を抑制したい
                    "仕様の隙間を埋めることだけを目的として spec を修正してはいけない",
                    "同じ意味の記述を複数箇所へ重複させてはいけない",
                ),
            ),
        ),
    )
