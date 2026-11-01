"""join の競合解消に共通する agent 向け指示文の構築定義。"""

from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_conflict_resolution_policy() -> tuple[PlaceholderMap, SDHeader]:
    """両側の意図を統合し、検証して報告するための規定を構築する。

    NOTE
        意味仕様は `{{cmoc-root}}/spec/app_spec/merge_conflict_resolution.md` の
        「統合の判断基準」「agent と cmoc の責務」「受理と報告」を参照。
    """
    return (
        {},
        SDHeader(
            "conflict resolution policy",
            SDPolicy(
                what_is_this="2 つの branch をマージした結果に対する規定を以下に示す",
                require=(
                    "両 branch の両立可能な変更がマージ結果上保持されていること",
                    "可能な限り多くの衝突が解決していること",
                    "可能な限り、検証・テストに合格する状態であること",
                    "妥当な解決方法が複数ある場合、そのうち 1 つが選択されていること",
                ),
                prohibit=(
                    "衝突解決の過程で発生した事情を、解決結果に残してはいけない",
                    "各規定に違反する解消結果を conflict 解消完了として扱ってはいけない",
                ),
                allow=(
                    "初期の競合一覧にないファイルも、必要に応じて編集して良い",
                    "解決のために必要であるならば、両ブランチの内容を保存せずに新しく書き直して良い",
                    "両 branch に相反する変更が存在し、それが解決不能な場合、未解消のままで良い",
                ),
            ),
        ),
    )
