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
    # NOTE
    #   マージに関する規定はここでしか使わないので、
    #   あえて `build_complete_prompt` の引数に含めずに、
    #   ここで直書きしている。
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
                    "git 操作は状態の参照にのみ使用すること",
                    "解決済みの状態を未コミット差分として残す事",
                    "未解決が残る場合、そのことを最終回答で報告すること",
                    "未解決が残る場合も、可能な範囲内で出来る限りの作業を行い、それを作業結果として残す事",
                ),
                prohibit=(
                    "衝突解決の過程で発生した事情を、解決結果に残してはいけない",
                    "各規定に違反する解消結果を conflict 解消完了として扱ってはいけない",
                    "競合の解消を理由に、アクセス禁止規定を破ってはいけない",
                ),
                allow=(
                    "初期の競合一覧にないファイルも、必要に応じて編集して良い",
                    "解決のために必要であるならば、両ブランチの内容を保存せずに新しく書き直して良い",
                    "両 branch に相反する変更が存在し、それが解決不能な場合、未解消のままで良い",
                ),
                supplemental=(
                    "git の編集的な操作はこのセッションの外で機械的に行われる",
                ),
            ),
        )
    ]
    # 指示文、設定 key、編集範囲、MCP の有効化を両 join で共用する。
    file_access_mode = FileAccessMode.REPO_WRITE
    prompt = build_complete_prompt(
        task="""
        `{{source_commit}}` を `{{target_commit}}` にマージする際に発生した衝突を解決すること
        """,
        scope="""
        - 両 commit の共通祖先以降の変更、進行中の競合状態を基本的な根拠とすること
        - また、競合解決の過程で必要と判断した変更・ファイルは追加の根拠としてよい
        """,
        file_access_mode=file_access_mode,
        path_context=path_context,
        enable_document_search_mcp=True,
        aux_static_prompt=static_prompt,
        aux_placeholder_def={
            "source_commit": source_commit,
            "target_commit": target_commit,
        },
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
