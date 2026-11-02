"""join の競合解消に共通する prompt と起動パラメータの構築定義。"""

from pathlib import Path

from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import (
    SDHeader,
    SDPolicy,
    SDTagBlock,
    render_sd_node_as_markdown,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt
from oracle.request_builder.basic import AgentCallParameter, FileAccessMode


def build_merge_conflict_resolution_request(
    *,
    source_commit: str,
    target_commit: str,
    merge_worktree: Path,
) -> AgentCallParameter:
    """merge conflict を解決する agent call リクエストを作成する

    Args:
        source_commit: 解決対象の merge conflict の合流元コミット
        target_commit: 解決対象の merge conflict の合流先コミット
        merge_worktree: merge conflict が発生している worktree のパス

    NOTE
        branch の決定、Git 操作、結果の受理と復旧は呼び出し元が担当する。
    """
    # process cwd に依存せず、merge の作業場所から入力とアクセス境界をそろえる。
    path_context = AgentCallPathContext(agent_call_cwd=merge_worktree)

    # 各項目を 1 行の文字列にし、行ごとに削除・コメントアウトできるようにする。
    static_prompt: list[SDHeader | SDTagBlock] = [
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
        SDHeader(
            "管理操作との境界",
            "- ファイル内容の編集と検証を行うこと",
            "- staging、commit、merge の開始・中止、branch・worktree 操作、および cmoc の管理 state の直接更新は行わないこと",
            "- refactor state（`{{work-root}}/.cmoc/gt/realization/refactor/state.json`）は直接編集しないこと",
            "- 残る管理処理は報告すること",
            "- Git index の unmerged entry を消すために staging せず、編集した内容の解消結果を報告すること",
            "- 管理物の競合や staging 待ちの unmerged entry が残ることだけを、内容の未解消として扱わないこと",
            "- 管理物の競合や staging 待ちの unmerged entry により必要な検証を実行できない場合は、その不足を報告すること",
            "- 管理物以外のアクセス禁止対象に競合がある場合は、その境界を越えて解消せず未解消として報告すること",
        ),
        SDHeader(
            "未解消の場合の扱い",
            "- 関連する decision・reference・spec と両側の変更意図からも決められない相反する要求について、新しい人間意図の選択が必要な場合は、推測で一方を採用せず未解消として報告すること",
            "- 内容の競合が残る場合、アクセス境界内で解消できない場合、または必要な検証を完了できない場合は、未解消の理由を最終回答に含めること",
            "- 未解消の場合も merge の中止や作業状態の復旧を自分で行わず、編集・検証の結果を返して終了すること",
        ),
        SDHeader(
            "最終回答で報告する事項",
            "- 編集可能な対象の内容競合を解消し、両 branch の両立する意図と挙動を保持した統合結果を必要な検証で確認できた場合は、最終回答の先頭行を `merge_resolution: resolved` とすること",
            "- 未解消事項や必要な検証の不足がある場合は、最終回答の先頭行を `merge_resolution: unresolved` とすること",
            "- 統合した両 commit と、確認した初期の競合",
            "- 採用した判断と、関連する decision・reference・spec・両側の変更意図に基づく理由",
            "- rename・削除、初期の競合一覧外の編集も含む、付随編集の対象と必要性",
            "- 実行した検証、その対象と結果、未実行または失敗の理由",
            "- 内容の解消完了または未解消の判断",
            "- 未解消の場合は、残る要求、人間意図の選択、アクセス境界、または検証不足などの具体的な理由",
        ),
        SDHeader(
            "統合対象の取得方法",
            "- cwd と `{{work-root}}` が示す repository で、指定された source・target commit の共通祖先と両側の変更を Git から取得すること",
            "- 進行中の merge の Git index と working tree から競合状態を読み取ること",
            "- rename・削除など、conflict marker のない競合も確認すること",
            "- Git 履歴・差分の参照にもファイルアクセス境界を適用すること",
            "- 取得に失敗した場合は空差分や競合なしとして扱わず、取得できなかった対象と理由を報告すること",
            "- 元の成果の commit を書き換えず、進行中の merge 結果を編集すること",
        ),
    ]
    dynamic_prompt: list[SDHeader | SDTagBlock] = [
        SDTagBlock(
            "merge_input",
            SDHeader(
                "統合対象",
                f"- source（取り込む側）: `{source_commit}`",
                f"- target（取り込み先の merge 前）: `{target_commit}`",
            ),
        ),
    ]
    # 指示文、設定 key、編集範囲、MCP の有効化を両 join で共用する。
    file_access_mode = FileAccessMode.SPEC_AND_REALIZATION_WRITE
    prompt = build_complete_prompt(
        task=(
            '- 統合対象 <cmoc_ref target="merge_input"/> の両 commit の変更意図を踏まえ、`{{work-root}}` で進行中の merge の内容競合を解消すること\n'
            "- 統合に必要な付随修正と検証を行うこと\n"
        ),
        scope="- 両 commit の共通祖先からの変更、進行中の競合状態、および関連する decision・reference・spec を判断材料とし、統合に必要な関連ファイルを調査すること",
        file_access_mode=file_access_mode,
        path_context=path_context,
        enable_document_search_mcp=True,
        aux_static_prompt=static_prompt,
        aux_dynamic_prompt=dynamic_prompt,
        cmoc_basic_instruction=True,
        spec_policy=True,
        realization_policy=True,
        routing_policy=True,
    )
    return AgentCallParameter(
        agent_call_kind=build_merge_conflict_resolution_request.__name__,
        file_access_mode=file_access_mode,
        prompt=render_sd_node_as_markdown(*prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        enable_document_search_mcp=True,
    )
