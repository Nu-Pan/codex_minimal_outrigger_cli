"""oracle findings policy の構築定義。"""

from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_oracle_findings_policy() -> tuple[PlaceholderMap, SDHeader]:
    """oracle file に対する所見が満たすべき規定を構築する。

    NOTE
        意味仕様は `oracle/doc/app_spec/sub_command/oracle_review.md:95` の
        「所見」の定義を参照。
        review の各ステップで用いる規定を共通化するために、わざわざ独立した関数として定義している。
    """
    return (
        {},
        SDHeader(
            "oracle findings policy",
            SDPolicy(
                what_is_this="oracle file に対する所見が満たすべき規定を以下に示す",
                require=(
                    "所見は oracle file, realization file の記述・挙動を根拠として持つ",
                    "正本仕様断片同士の解釈の余地がない明確な矛盾は fatal 所見とする",
                    "実装者裁量の範囲内で解決出来ない問題は fatal 所見とする",
                    "正本仕様の意味を変更しない表記上の問題を minor 所見とする",
                    "初歩的な言葉の問題 (e.g. 誤字、脱字、明確な文法誤り、用語不統一、表記揺れ） は minor 所見とする",
                    "所見に対して適用する基準は常に一貫していること",
                ),
                prohibit=(
                    "規定上必須とされていない事を所見の根拠にしてはいけない",
                    "調査開始時点ですでに解消されている問題を新しい所見として重複させてはいけない",
                ),
            ),
        ),
    )
