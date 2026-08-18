"""oracle file を扱う agent call 向け instruction 文面の構築定義。"""

from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_oracle_policy() -> tuple[PlaceholderMap, SDHeader]:
    """oracle file の作成・変更・レビューに必要な規定を構築する。"""
    return (
        {},
        SDHeader(
            "oracle policy",
            SDPolicy(
                when_use_this="oracle file の作成・変更・レビューをする時、以下の規定に従うこと",
                require=(
                    "oracle and realization basic の要件に従うこと",
                    "プロンプト > oracle file > installed skill の優先順位で指示に従う事",
                    "oracle file から実装差を許容する・しないの境界が読み取れる事",
                    "oracle file から、仕様の背後にある人間意図としての goal, non-goal が読み取れる事",
                    "合わせて読む必要がある oracle file が存在する場合、それへの参照 (ファイルパスと行数) を示すこと",
                    "プロンプトで作業対象として明示されていない部分は、既存の意味を可能な限り維持すること",
                    "複数個所で登場する同じ概念に専用の用語を与える時、その命名はリポジトリ全体で統一すること",
                    "「用語だけから推測される意味」と「oracle file から実際に読み取れる用語の意味」とが一致するように用語を命名すること",
                    "実装差を許容する余地を最大限尊重した仕様断片にすること",
                    "仕様断片上定義されている事項と、未定義の事項とを区別すること",
                ),
                prohibit=(
                    "realization file を根拠に oracle file の意味を変更してはいけない",
                    "realization file から正本仕様断片を逆算してはいけない",
                    "一般的なベストプラクティスだけを根拠に正本仕様断片を修正してはいけない",
                    "仕様の隙間を埋めることだけを目的として正本仕様断片を修正してはいけない",
                    "仕様断片間の矛盾はあってはいけない"
                    "同じ意味の記述を複数箇所へ重複させてはいけない",
                    "正本仕様断片の隙間の未定義事項を正本仕様として断定してはいけない",
                    "誤字・脱字・文法誤りを残してはいけない",
                ),
                allow=(
                    "oracle file の問題 (矛盾・実現不能な仕様) を調べる場合に限り、実装上の制約を修正プランの判断材料にしてよい",
                ),
                supplemental=(
                    "oracle file は仕様 **断片** であり、それを判断する人間の認知負荷の観点から、可能な限り疎であることが求められる",
                ),
            ),
        ),
    )


def build_oracle_investigation_policy() -> tuple[PlaceholderMap, SDHeader]:
    """oracle file の読み取り専用調査に必要な規定を構築する。"""
    return (
        {},
        SDHeader(
            "oracle investigation policy（oracle file の読み取り専用調査時）",
            SDPolicy(
                when_use_this="",
                require=("oracle file で定義されている事項と未定義の事項を区別する",),
                prohibit=("未定義の事項を正本仕様として断定してはいけない",),
            ),
        ),
    )
