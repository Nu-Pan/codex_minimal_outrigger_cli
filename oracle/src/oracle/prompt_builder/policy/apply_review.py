"""oracle file への適合性を判断する agent 向け文面の構築定義。"""

from oracle.other.struct_doc import SDHeader
from oracle.prompt_builder.basic import PlaceholderMap


def build_apply_review_policy() -> tuple[PlaceholderMap, SDHeader]:
    """realization の追従要否と所見を判断する規定を構築する。"""
    return (
        {},
        SDHeader(
            "apply review policy（oracle file に対する realization file の追従要否・所見・修正の判断時）",
            """
            **必須**

            - oracle authority policy（oracle・realization file を扱う時）では、oracle file を人間が所有する正本仕様断片として扱う
            - finding basis policy（所見・修正対象の判断時）に従い、所見または修正対象には、用途固有の policy が認める具体的な oracle file または realization file の記述・挙動を示す
            - oracle file の具体的な要求と realization file の具体的な挙動が明確に不整合な場合は修正対象とする
            - realization file だけから実行不能または明白な致命的バグと説明できる場合は修正対象とする
            - 修正後の realization file も関連する oracle file の明示要求を満たす

            **禁止**

            - oracle authority policy（oracle・realization file を扱う時）では、realization file の都合または挙動を根拠に oracle file の意味を変更してはいけない
            - finding basis policy（所見・修正対象の判断時）に従い、oracle file に記述がないこと、仕様の隙間、複数の妥当解、好み、推測、または一般的なベストプラクティスだけを根拠に所見または修正対象を作ってはいけない
            - 調査開始時点ですでに解消されている問題を所見として扱ってはいけない
            """,
        ),
    )
