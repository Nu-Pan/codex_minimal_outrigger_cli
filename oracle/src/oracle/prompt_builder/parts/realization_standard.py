"""realization file を扱う agent call に注入する規範の正本。"""

# cmoc
from oracle.other.path_model import AgentCallPathContext
from oracle.other.standard import Requirement, Standard, standard_to_struct_doc
from oracle.other.struct_doc import StructDoc
from oracle.prompt_builder.basic import PlaceholderMap


def build_realization_standard(
    path_context: AgentCallPathContext,
) -> tuple[PlaceholderMap, StructDoc]:
    """realization file の作成・変更・レビューに必要な規範を構築する。"""
    # 規範本文が参照する work-root を call-scoped context から取得する。
    root_definitions = path_context.root_placeholder_definitions()
    standards = [
        Standard(
            title="realization file を現行の oracle file に適合させる",
            backgrounds=[
                "realization file は oracle file に記述された人間意図を具体化する",
                "正本仕様にない実装詳細は実装者の小さな裁量で補われる",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "関連する oracle file を先に確認し、その明示要求と矛盾しない realization file にする",
                ),
                Requirement(
                    "禁止",
                    "realization file の都合に合わせて oracle file の意味を変更してはいけない",
                ),
                Requirement(
                    "禁止",
                    "oracle src の定義または prompt 文面を realization file へ正本のように複製してはいけない",
                ),
                Requirement(
                    "必須",
                    "正本と同じ情報が必要な場合は、参照、生成、または変換により正本を一箇所に保つ",
                ),
            ],
        ),
        Standard(
            title="現行仕様に必要な実装だけを保つ",
            backgrounds=[
                "重複、旧実装、不要な公開面は AI が読む文脈と保守対象を増やす",
                "将来の可能性だけに基づく抽象化は現行仕様の実装を複雑にする",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "現行仕様を満たすために必要な implementation、test、設定、および ancillary だけを保つ",
                ),
                Requirement(
                    "禁止",
                    "同じ責務の実装、旧仕様の分岐、未使用の識別子、または置換済みの test を残してはいけない",
                ),
                Requirement(
                    "禁止",
                    "将来使う可能性だけを根拠に抽象化、公開 interface、設定、永続状態、依存関係、または補助 file を追加してはいけない",
                ),
                Requirement(
                    "必須",
                    "新しい実装は実在する責務境界または重複に対応させ、既存の近い責務を同時に整理する",
                ),
                Requirement(
                    "禁止",
                    "簡潔化のために意味、可読性、失敗時挙動、または必要な検証を損なってはいけない",
                ),
            ],
        ),
        Standard(
            title="対象 repository 固有の手順で変更を検証する",
            backgrounds=[
                "言語、framework、tool 固有の開発手順は対象 repository が所有する",
                "cmoc は任意の対象 repository の開発手順を内蔵しない",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "対象 repository で追跡されている関連手順を配置場所にかかわらず特定し、変更に必要な検証を行う",
                ),
                Requirement(
                    "禁止",
                    "work-root 固有手順の配置先を `.agents/skills` に限定してはいけない",
                ),
                Requirement(
                    "必須",
                    "必要な手順または実行環境が利用できない場合は、検証済みと扱わず不足を報告する",
                ),
            ],
        ),
    ]
    return (
        {"work-root": root_definitions["work-root"]},
        StructDoc(
            "realization standard",
            StructDoc(
                "適用条件",
                "- realization file を作成、変更、リファクタ、またはレビューする場合に適用する",
            ),
            *[standard_to_struct_doc(standard) for standard in standards],
        ),
    )
