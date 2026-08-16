"""oracle file への適合性を判断する agent 向け文面の構築定義。"""

from oracle.other.struct_doc import StructDoc
from oracle.prompt_builder.basic import PlaceholderMap


def build_apply_review_policy() -> tuple[PlaceholderMap, StructDoc]:
    """realization の追従要否と所見を判断する規定を構築する。"""
    return (
        {},
        StructDoc(
            "apply review policy（oracle file に対する realization file の追従要否・所見・修正の判断時）",
            StructDoc(
                "oracle authority policy（oracle・realization file を扱う時）",
                StructDoc(
                    "oracle file を正本仕様断片として扱う",
                    """
                    **必須**

                    - oracle file を人間が所有する正本仕様断片として扱う
                    """,
                ),
                StructDoc(
                    "realization file から oracle file へ意味を逆流させない",
                    """
                    **禁止**

                    - realization file の都合または挙動を根拠に oracle file の意味を変更してはいけない
                    """,
                ),
            ),
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
                "明確な不適合または致命的な実装問題を修正対象にする",
                """
                **必須**

                - oracle file の具体的な要求と realization file の具体的な挙動が明確に不整合な場合は修正対象とする
                - realization file だけから実行不能または明白な致命的バグと説明できる場合は修正対象とする
                - 修正後の realization file も関連する oracle file の明示要求を満たす
                """,
            ),
            StructDoc(
                "調査開始時点で解消済みの問題を所見にしない",
                """
                **禁止**

                - 調査開始時点ですでに解消されている問題を所見として扱ってはいけない
                """,
            ),
        ),
    )
