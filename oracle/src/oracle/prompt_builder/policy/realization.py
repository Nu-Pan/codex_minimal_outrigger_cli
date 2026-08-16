"""realization file を扱う agent call 向け instruction 文面の構築定義。"""

from oracle.other.struct_doc import StructDoc
from oracle.prompt_builder.basic import PlaceholderMap


def build_realization_policy() -> tuple[PlaceholderMap, StructDoc]:
    """realization file の作成・変更・レビューに必要な規定を構築する。"""
    return (
        {},
        StructDoc(
            "realization policy（realization file の作成・変更・リファクタ・レビュー時）",
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
                "realization file を現行の oracle file に適合させる",
                """
                **必須**

                - 関連する oracle file を先に確認し、その明示要求と矛盾しない realization file にする
                - 正本と同じ情報が必要な場合は、参照、生成、または変換により正本を一箇所に保つ

                **禁止**

                - oracle src の定義または prompt 文面を realization file へ正本のように複製してはいけない
                """,
            ),
            StructDoc(
                "現行仕様に必要な実装だけを保つ",
                """
                **必須**

                - 現行仕様を満たすために必要な implementation、test、設定、および ancillary だけを保つ
                - 新しい実装は実在する責務境界または重複に対応させ、既存の近い責務を同時に整理する

                **禁止**

                - 同じ責務の実装、旧仕様の分岐、未使用の識別子、または置換済みの test を残してはいけない
                - 将来使う可能性だけを根拠に抽象化、公開 interface、設定、永続状態、依存関係、または補助 file を追加してはいけない
                - 簡潔化のために意味、可読性、失敗時挙動、または必要な検証を損なってはいけない
                """,
            ),
            StructDoc(
                "対象 repository 固有の手順で変更を検証する",
                """
                **必須**

                - 対象 repository で追跡されている関連手順を配置場所にかかわらず特定し、変更に必要な検証を行う
                - 必要な手順または実行環境が利用できない場合は、検証済みと扱わず不足を報告する

                **禁止**

                - work-root 固有手順の配置先を `.agents/skills` に限定してはいけない
                """,
            ),
        ),
    )
