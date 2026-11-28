"""realization file を扱う agent call 向け instruction 文面の構築定義。"""

from reference.other.path_model import AgentCallPathContext
from reference.other.struct_doc import SDHeader, SDPolicy
from reference.prompt_builder.basic import PlaceholderMap


def build_realization_policy(
    path_context: AgentCallPathContext,
) -> tuple[PlaceholderMap, SDHeader]:
    """realization file が満たすべき規定を構築する。"""
    return (
        path_context.root_placeholder_definitions(),
        SDHeader(
            "realization policy",
            SDPolicy(
                what_is_this="realization file が満たすべき規定を以下に示す",
                require=(
                    "realization が decision の要求と spec に整合していること",
                    "decision の要求が使用すべき実装まで指定している場合は、その実装を可能な限りそのまま使用すること",
                    "類似・重複する realizatinon が複数存在する時、それらが全体で見た時にシンプルに整理されていること",
                    "検証・テストに合格する状態であること",
                ),
                prohibit=(
                    "YAGNI 原則 : 現在の decision の要求と spec に照らして不要な realization を残してはいけない",
                    "YAGNI 原則 : 「将来必要になる」は realization の根拠として認められない",
                    "realization 上の致命的な問題を残してはいけない",
                ),
                allow=(
                    "decision の要求でも spec でも明示されていない仕様の欠損は、実装者の裁量において realization 上で補完して良い",
                ),
            ),
        ),
    )
