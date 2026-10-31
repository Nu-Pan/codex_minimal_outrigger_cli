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
                # TODO
                #   request builder 側に未解消をハンドルする仕組みを入れる必要あり
                #   マージ作業時はリポジトリ全体が編集可能ということになるはず
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
            SDHeader(
                "管理操作との境界",
                """
                - ファイル内容の編集と検証を行い、staging、commit、merge の開始・中止、branch・worktree 操作、および cmoc の管理 state の直接更新は行わないこと
                - refactor state（`{{work-root}}/.cmoc/gt/realization/refactor/state.json`）は直接編集しないこと。残る管理処理は報告すること
                - Git index の unmerged entry を消すために staging せず、編集した内容の解消結果を報告すること
                - 管理物の競合や staging 待ちの unmerged entry が残ることだけを、内容の未解消として扱わないこと。ただし、それらにより必要な検証を実行できない場合は、その不足を報告すること
                - 管理物以外のアクセス禁止対象に競合がある場合は、その境界を越えて解消せず未解消として報告すること
                """,
            ),
            SDHeader(
                "最終回答で報告する事項",
                """
                - 最終回答の先頭行を、編集可能な対象の内容競合を解消し、両 branch の両立する意図と挙動を保持した統合結果を必要な検証で確認できた場合は `merge_resolution: resolved`、未解消事項や必要な検証の不足がある場合は `merge_resolution: unresolved` とすること
                - 統合した両 commit と、確認した初期の競合
                - 採用した判断と、関連する oracle・両側の変更意図に基づく理由
                - 付随編集の対象と必要性。rename・削除、初期の競合一覧外の編集も含めること
                - 実行した検証、その対象と結果、未実行または失敗の理由
                - 内容の解消完了または未解消の判断。未解消の場合は、残る要求、人間意図の選択、アクセス境界、または検証不足などの具体的な理由
                """,
            ),
        ),
    )
