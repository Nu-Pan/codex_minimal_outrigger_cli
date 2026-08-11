"""oracle file への適合性を判断する agent 向け文面の構築定義。"""

# cmoc
from oracle.other.standard import Requirement, Standard, standard_to_struct_doc
from oracle.other.struct_doc import StructDoc
from oracle.prompt_builder.basic import PlaceholderMap


def build_apply_review_standard() -> tuple[PlaceholderMap, StructDoc]:
    """realization の追従要否と所見を判断する規範を構築する。"""
    standards = [
        Standard(
            title="明確な不適合または致命的な実装問題を修正対象にする",
            requirements=[
                Requirement(
                    "必須",
                    "oracle file の具体的な要求と realization file の具体的な挙動が明確に不整合な場合は修正対象とする",
                ),
                Requirement(
                    "必須",
                    "realization file だけから実行不能または明白な致命的バグと説明できる場合は修正対象とする",
                ),
                Requirement(
                    "必須",
                    "修正対象は根拠となる oracle file と realization file、または致命的な実装箇所を具体的に示す",
                ),
                Requirement(
                    "必須",
                    "修正後の realization file も関連する oracle file の明示要求を満たす",
                ),
            ],
        ),
        Standard(
            title="仕様の隙間や改善案だけを修正対象にしない",
            requirements=[
                Requirement(
                    "禁止",
                    "oracle file に記述がないことだけを理由に realization file を修正対象にしてはいけない",
                ),
                Requirement(
                    "禁止",
                    "複数の妥当解、好み、推測、または一般的なベストプラクティスだけを根拠に修正対象を作ってはいけない",
                ),
                Requirement(
                    "禁止",
                    "realization file の既存挙動を正本仕様として oracle file へ逆流させてはいけない",
                ),
                Requirement(
                    "禁止",
                    "調査開始時点ですでに解消されている問題を所見として扱ってはいけない",
                ),
            ],
        ),
    ]
    return (
        {},
        StructDoc(
            "apply review standard",
            StructDoc(
                "適用条件",
                "- oracle file に対する realization file の追従要否、所見、または修正内容を判断する場合に適用する",
            ),
            *[standard_to_struct_doc(standard) for standard in standards],
        ),
    )
