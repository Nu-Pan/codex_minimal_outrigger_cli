"""oracle file への適合性を判断する agent 向け文面の構築定義。"""

from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_realization_findings_policy() -> tuple[PlaceholderMap, SDHeader]:
    """realization file に対する所見が満たすべき規定。

    NOTE
        意味仕様は `oracle/doc/app_spec/oracle_and_realization.md:83` の
        「oracle file に対する realization file の適合性」を参照。
    """
    return (
        {},
        SDHeader(
            "realization findings policy",
            SDPolicy(
                what_is_this="realization file に対する所見が満たすべき規定を以下に示す",
                require=(
                    "所見は oracle file, realization file の記述・挙動を根拠として持つ",
                    "oracle file の具体的な要求と realization file の具体的な挙動が明確に不整合する場合は修正対象とする",
                    "realization file 上に明確に存在する致命的な問題は修正対象とする",
                    "所見に対して適用する基準は常に一貫していること",
                ),
                prohibit=(
                    "oracle file 自体の問題 (e.g 仕様の定義の不足) は所見の対象としてはいけない",
                    "規定上必須とされていない事を所見の根拠にしてはいけない",
                    "調査開始時点ですでに解消されている問題を新しい所見として重複させてはいけない",
                ),
            ),
        ),
    )
