"""oracle file を扱う agent call 向け instruction 文面の構築定義。"""

from oracle.other.struct_doc import StructDoc
from oracle.prompt_builder.basic import PlaceholderMap


def build_oracle_policy() -> tuple[PlaceholderMap, StructDoc]:
    """oracle file の作成・変更・レビューに必要な規定を構築する。"""
    return (
        {},
        StructDoc(
            "oracle policy（oracle file の作成・変更・レビュー時）",
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
                "判断根拠と installed skill の優先関係を守る",
                """
                **必須**

                - 判断の根拠を関連する oracle file に置く
                - cmoc 固有契約または oracle file と installed skill が競合する場合は前者を優先する

                **禁止**

                - installed skill の存在を oracle file の意味または作業完了条件の前提にしてはいけない
                """,
            ),
            StructDoc(
                "一般論だけを根拠に oracle file の要求を変更しない",
                """
                **禁止**

                - 一般的なベストプラクティスだけを根拠に oracle file の要求を変更してはいけない
                """,
            ),
            StructDoc(
                "重要な人間意図へ絞り、仕様の隙間を許容する",
                """
                **必須**

                - 実装差を許容しない事項と、人間が判断した事項は、境界として明示する
                - 過剰な実装を誘発し得る境界では goal と non-goal を読み取れるようにする

                **禁止**

                - 仕様全体を網羅するためだけの分類、列挙、説明を追加してはいけない
                - 未定義部分を埋めることだけを目的に oracle file を増やしてはいけない

                **許容**

                - 明示仕様の隙間は、現行の oracle file と、file access が許す場合の既存実装・既存 test から自然に導ける範囲で実装者が補ってよい
                """,
            ),
            StructDoc(
                "実装から正本仕様を逆算しない",
                """
                **禁止**

                - realization file または実装だけから正本仕様を逆算してはいけない
                """,
            ),
            StructDoc(
                "実装上の制約は仕様の矛盾または実現不能の調査に限って使用する",
                """
                **許容**

                - 正本仕様の矛盾または実現不能を調べる場合に限り、実装上の制約を修正提案の材料にしてよい
                """,
            ),
            StructDoc(
                "正本仕様断片の整合性と検索性を保つ",
                """
                **必須**

                - 一般方針と個別仕様の優先関係を読み取れるようにする
                - 依頼の対象外である既存仕様の意味を維持する
                - oracle file を作成または変更する場合は、同じ概念の用語と表記を統一し、名前から推測される意味を定義と一致させる
                - oracle file を作成または変更する場合は、文意または検索性を損なう誤字、脱字、文法誤りを残さない

                **禁止**

                - 一方の正本仕様断片に従うと別の正本仕様断片へ必ず違反する状態を作ってはいけない
                - oracle file を作成または変更する場合は、同じ意味の記述を複数箇所へ重複させてはいけない
                """,
            ),
        ),
    )


def build_oracle_investigation_policy() -> tuple[PlaceholderMap, StructDoc]:
    """oracle file の読み取り専用調査に必要な規定を構築する。"""
    return (
        {},
        StructDoc(
            "oracle investigation policy（oracle file の読み取り専用調査時）",
            StructDoc(
                "oracle authority policy（oracle・realization file を扱う時）",
                StructDoc(
                    "oracle file を正本仕様断片として扱う",
                    """
                    **必須**

                    - oracle file を人間が所有する正本仕様断片として扱う
                    """,
                ),
            ),
            StructDoc(
                "判断根拠と installed skill の優先関係を守る",
                """
                **必須**

                - 判断の根拠を関連する oracle file に置く
                - cmoc 固有契約または oracle file と installed skill が競合する場合は前者を優先する

                **禁止**

                - installed skill の存在を oracle file の意味または作業完了条件の前提にしてはいけない
                """,
            ),
            StructDoc(
                "実装から正本仕様を逆算しない",
                """
                **禁止**

                - realization file または実装だけから正本仕様を逆算してはいけない
                """,
            ),
            StructDoc(
                "定義済みの事項と未定義の事項を区別する",
                """
                **必須**

                - oracle file で定義されている事項と未定義の事項を区別する

                **禁止**

                - 未定義の事項を正本仕様として断定してはいけない
                """,
            ),
        ),
    )
