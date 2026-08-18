"""realization file を扱う agent call 向け instruction 文面の構築定義。"""

from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_realization_policy(
    path_context: AgentCallPathContext,
) -> tuple[PlaceholderMap, SDHeader]:
    """realization file の作成・変更・レビューに必要な規定を構築する。"""
    return (
        path_context.root_placeholder_definitions(),
        SDHeader(
            "realization policy",
            SDPolicy(
                when_use_this="realization file の作成・変更・リファクタ・レビューをする時、以下の規定に従うこと",
                require=(
                    "oracle file を **人間意図を具体化した正本仕様断片** として扱う",
                    "関連する oracle file を先に確認し、その明示要求と矛盾しない realization file にする",
                    "oracle fiel 側に実装が存在する場合、可能な限りをそれをそのまま使用する",
                    "今現在の仕様を満たすために必要な realization file だけに保つ (YAGNI)",
                    "新しい実装を追加する時、意味的に近い既存実装を同時に整理する",
                    "責務が重複する実装・テストは、可能な限り直交させてシンプルに保つこと",
                    "参照可能な文章上で指示されている手順に基づいて、作業後の状態を検証・テストする",
                    "検証・テストを何らかの理由で実施できない場合は、検証済みと扱わず不足を報告する",
                ),
                prohibit=(
                    "realization file を根拠に oracle file に変更を加えてはいけない",
                    "oracle file の正本仕様断片を realization file へ複製してはいけない",
                    "不要になった実装・テスト (e.g. 旧仕様の分岐、未使用の識別子、置換済みコード) を残してはいけない",
                    "将来必要になる可能性だけを根拠に realization file を複雑化させてはいけない",
                    "シンプル化によって、正本仕様断片上必要とされる要素 (e.g. 意味、可読性、失敗時挙動、検証) を損なってはいけない",
                    "`{{work-root}}` 固有の指示を根拠とせずに `{{work-root}}.agents/skills` だけを根拠に作業方法を断定してはいけない",
                ),
                allow=(
                    "重要な人間意図へ絞りつつ、明示仕様の隙間は、現行の oracle file と、file access が許す場合の既存実装・既存 test から自然に導ける範囲で実装者が補ってよい",
                    "どうしても oracle file をそのまま使用出来ない場合のみ、同等の機能を realization file に最小限の範囲内で実装しても良い",
                ),
            ),
        ),
    )
