"""join の競合解消に共通する agent 向け指示文の構築定義。"""

from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_conflict_resolution_policy() -> tuple[PlaceholderMap, SDHeader]:
    """両側の意図を統合し、検証して報告するための規定を構築する。

    NOTE
        意味仕様は `{{cmoc-root}}/oracle/doc/app_spec/merge_conflict_resolution.md` の
        「統合の判断基準」「agent と cmoc の責務」「受理と報告」を参照。
    """
    return (
        {},
        SDHeader(
            "conflict resolution policy",
            SDPolicy(
                what_is_this="両 branch の変更を整合したマージ結果にするための作業規定を以下に示す",
                require=(
                    "conflict の両側と関連する oracle file を確認し、両 branch の両立する意図と挙動を解消結果に保持する",
                    "適用されるファイルアクセス境界内で、競合箇所の選択、関連ファイルの組み直し、rename・削除、テストの調整など、統合に必要な編集を自律的に行う",
                    "初期の競合一覧にない関連ファイルも、統合に必要なら付随編集の対象として判断する",
                    "対象リポジトリの手順に従って必要な検証を実行し、結果と完了判断の根拠を報告する。実行できなかった検証を検証済みとして扱わない",
                    "関連する oracle と変更意図からも決められない相反する要求の採否など、新しい人間意図の選択が必要な場合は未解消として報告する",
                ),
                prohibit=(
                    "複数の妥当な実装方法があることや、両側を組み直す必要があることだけを理由に、人間へ判断を戻してはいけない",
                    "片側との内容一致や初期の競合 path 集合への限定を目的として、両立する意図や必要な付随編集を捨ててはいけない",
                    "実装都合から oracle の意味を逆算・変更したり、相反する人間意図の採否を推測で決めたりしてはいけない",
                    "適用される規定に違反する解消結果を conflict 解消完了として扱ってはいけない",
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
