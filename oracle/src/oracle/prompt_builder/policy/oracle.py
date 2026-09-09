"""oracle file を扱う agent call 向け instruction 文面の構築定義。"""

from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_oracle_policy() -> tuple[PlaceholderMap, SDHeader]:
    """oracle file が満たすべき規定を構築する。

    NOTE
        意味仕様は `oracle/doc/app_spec/oracle_and_realization.md` の
        「oracle doc と oracle src の正本責務」から
        「正本責務に基づく優先関係」までと「oracle file を扱う判断基準」、
        `oracle/doc/app_spec/codex_exec_rule.md` の
        「call 固有の実行時指示の優先関係」を参照。
    """
    return (
        {},
        SDHeader(
            "oracle policy",
            SDPolicy(
                what_is_this="oracle file が満たすべき規定を以下に示す",
                require=(
                    "oracle and realization basic の要件に従うこと",
                    "プロンプト > oracle file > installed skill の優先順位で指示に従う事",
                    "oracle file から実装差を許容する・しないの境界が読み取れる事",
                    "oracle file から、仕様の背後にある人間意図としての goal, non-goal が読み取れる事",
                    "合わせて読む必要がある oracle file は、root path placeholder を起点とする path、安定した locator、および簡潔な内容で特定すること",
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
                    "仕様断片間の矛盾はあってはいけない",
                    "同じ意味の記述を複数箇所へ重複させてはいけない",
                    "正本仕様断片の隙間の未定義事項を正本仕様として断定してはいけない",
                    "合わせて読む必要がある oracle file への参照に行番号を含めてはいけない",
                    "誤字・脱字・文法誤りを残してはいけない",
                ),
                allow=(
                    "oracle file の問題 (矛盾・実現不能な仕様) を調べる場合に限り、実装上の制約を修正プランの判断材料にしてよい",
                ),
                supplemental=(
                    "oracle file は仕様 **断片** であり、それを判断する人間の認知負荷の観点から、可能な限り疎であることが求められる",
                ),
            ),
            SDPolicy(
                what_is_this=(
                    "oracle doc と oracle src の正本責務、委譲、および優先関係を以下に示す"
                ),
                require=(
                    "oracle doc は意味仕様を所有し、oracle src は oracle doc から明示的に委譲された正確な詳細を所有する",
                    "oracle doc から oracle src への委譲は、root path placeholder を起点とする path、安定した locator、および委譲内容の短い説明で委譲先を特定する",
                    "同じ仕様事項の正本所有者は一つだけとする",
                    "意味仕様では oracle doc を優先し、明示的に委譲された正確な詳細では委譲先の oracle src を優先する",
                    "同じ意味仕様について両者が食い違う場合は、詳細な方を採用せず、oracle file 間の不整合として扱う",
                ),
                prohibit=(
                    "oracle doc は oracle src が所有する正確な詳細を再定義してはいけない",
                    "oracle src は oracle doc が所有する意味仕様を補完、変更、または拡張してはいけない",
                    "generated prompt は、oracle doc または oracle src の正本を上書きしてはいけない",
                ),
            ),
        ),
    )
