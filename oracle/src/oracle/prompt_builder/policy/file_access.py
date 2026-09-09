"""FileAccessMode に応じたファイルアクセス制限規定文面の構築定義。"""

# cmoc
from oracle.acp_builder.basic import FileAccessMode
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_file_access_policy(
    mode: FileAccessMode,
    path_context: AgentCallPathContext,
) -> tuple[PlaceholderMap, SDHeader] | None:
    """エージェントに伝えるファイルアクセス制限規定の文面を構築する。

    Returns:
        共通 file access policy の placeholder 定義と文面。
        `None` は、有効な mode に共通 file access policy が存在しないことだけを表す。

    NOTE
        意味仕様は `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の
        「ファイルアクセス制限」を参照。
        sandbox の設定は non-goal である。
    """
    if mode is FileAccessMode.NO_POLICY:
        # 有効な mode だが、共通 file access policy は存在しない。
        return None

    # agent の直接アクセスに対する共通の禁止事項。
    base_denials = [
        "`{{work-root}}` ツリー外は書き込み禁止",
        "`{{work-root}}/.git` ツリー内は書き込み禁止",
        "Git metadata は配置先によらず変更禁止",
        "`{{work-root}}/.agents` ツリー内は書き込み禁止",
        "`{{work-root}}/.codex` ツリー内は書き込み禁止",
        "`{{work-root}}/.cmoc` ツリー内は書き込み禁止",
        "`AGENTS.md` は書き込み禁止",
        "`INDEX.md` は書き込み禁止",
        # NOTE
        #   memo は agent 不可視のユーザーワークスペースとするので読み書き禁止で固定
        "`{{work-root}}/memo` は読み書き禁止",
    ]
    # mode 別の禁止事項
    match mode:
        case FileAccessMode.READONLY:
            # NOTE
            #   リポジトリ全体の **cmoc 上の論理的な意味での** 読み取り専用
            #   主要な編集対象である oracle file, realization file を読み取り専用にする
            #   規定上言及されていない一時ファイル用の path 例外は生成しない
            #   調査系タスク、cmoc が書き込みを代行するケースで使われる想定
            denials = [
                *base_denials,
                "oracle file は書き込み禁止",
                "realization file は書き込み禁止",
            ]
        case FileAccessMode.PURE_ORACLE_READ:
            # NOTE
            #   READONLY + realization file アクセス禁止
            #   realization file に釣られずに oracle file から判断してほしい系のタスクで使われる想定
            denials = [
                *base_denials,
                "oracle file は書き込み禁止",
                "realization file は読み書き禁止",
            ]
        case FileAccessMode.REPO_WRITE:
            # NOTE
            #   リポジトリ書き込み可能
            #   `cmoc tui` で微妙なタスクを渡された時に使われる想定
            denials = [
                *base_denials,
                # oracle file は書き込み許可
                # realization file は書き込み許可
            ]
        case FileAccessMode.PURE_ORACLE_WRITE:
            # NOTE
            #   REPO_WRITE + realization file アクセス禁止
            #   realization file に釣られずに oracle file の修正作業をしてほしい時に使われる想定
            denials = [
                *base_denials,
                # oracle file は書き込み許可
                "realization file は読み書き禁止",
            ]
        case FileAccessMode.REALIZATION_WRITE:
            # NOTE
            #   REPO_WRITE + oracle file 書き込み禁止
            #   realization file を oracle file に追従させる作業で使われる想定
            denials = [
                *base_denials,
                "oracle file は書き込み禁止",
                # realization file は書き込み許可
            ]
        case _:
            raise ValueError(f"Invalid mode (mode={mode})")
    return (
        path_context.root_placeholder_definitions(),
        SDHeader(
            f"file R/W policy ({mode.value})",
            SDPolicy(
                what_is_this="エージェントの直接ファイルアクセスに適用する規定と、書き込み主体による例外を以下に示す",
                require=(),
                prohibit=tuple(denials),
                allow=(),
                exception=(
                    "MCP 経由の外部ツールによるファイル書き込みは、この policy の書き込み制限の対象外とする",
                    "Structured Output を受け取った外部ツールによるファイル書き込みは、この policy の書き込み制限の対象外とする",
                ),
                supplemental=(
                    "この policy は deny list であり、許容されるファイルアクセスには言及していない",
                ),
            ),
        ),
    )
