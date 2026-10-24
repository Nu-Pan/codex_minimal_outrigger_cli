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
        意味仕様は `{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の
        「ファイルアクセス制限」を参照。
        sandbox の設定は non-goal である。
    """
    # mode 別の禁止事項
    match mode:
        case FileAccessMode.READONLY:
            # NOTE
            #   リポジトリ全体の **cmoc 上の論理的な意味での** 読み取り専用
            #   `cmoc_basic_instruction` で定義されている各編集対象を読み取り専用にする
            #   一時作業領域は共通規定に従って利用できる
            #   調査系タスク、cmoc が書き込みを代行するケースで使われる想定
            mode_prohibit = [
                "decision, reference, spec, realization は書き込み禁止",
            ]
        case FileAccessMode.REPO_WRITE:
            # NOTE
            #   リポジトリ書き込み可能
            #   `cmoc tui` みたいな、何の仮定も置けないタスクで使われる想定
            mode_prohibit = [
                "decision, reference は書き込み禁止"
                # decision, reference, spec, realization (つまり全部) が読み書き許可
            ]
        case FileAccessMode.DECISION_PLAN:
            # NOTE
            #   `cmoc decision plan` 専用
            mode_prohibit = [
                "decision, reference, spec は書き込み禁止",
                "realization は読み書き禁止",
            ]
        case FileAccessMode.SPEC_WRITE:
            # NOTE
            #   spec に対する編集操作用
            #   `cmoc decision apply` (to spec) で使う想定
            mode_prohibit = [
                "decision, reference は書き込み禁止",
                # spec は読み書き許可
                "realization は読み書き禁止",
            ]
        case FileAccessMode.REALIZATION_WRITE:
            # NOTE
            #   realization に対する編集操作用
            #   `cmoc decision apply` (to realization) で使う想定
            mode_prohibit = [
                "decision, reference, spec は書き込み禁止",
                # realization は読み書き許可
            ]
        case FileAccessMode.NO_POLICY:
            # NOTE
            #   NO_POLICY は有効な mode であり、
            #   共通 file access policy が空であることが正しい。
            return None
        case _:
            raise ValueError(f"Invalid mode (mode={mode})")
    # 規定全体を構築して返す
    return (
        path_context.root_placeholder_definitions(),
        SDHeader(
            f"file access policy ({mode.value})",
            SDPolicy(
                what_is_this="エージェントによる直接ファイルアクセスが満たすべき規定を以下に示す",
                require=(),
                prohibit=(
                    # NOTE
                    #   Codex の repo-write サンドボックスのアクセス制限をここで明言
                    "`{{work-root}}` ツリー外は書き込み禁止",
                    "`{{work-root}}/.git` ツリー内は書き込み禁止",
                    "Git metadata は配置先によらず変更禁止",
                    "`{{work-root}}/.agents` ツリー内は書き込み禁止",
                    "`{{work-root}}/.codex` ツリー内は書き込み禁止",
                    "`{{work-root}}/.cmoc` ツリー内は書き込み禁止",
                    "`AGENTS.md` は書き込み禁止",
                    # NOTE
                    #   memo は agent 不可視のユーザーワークスペースとするので読み書き禁止で固定
                    "`{{work-root}}/memo` は読み書き禁止",
                    "一時作業領域を禁止・制限事項の迂回に使ってはいけない",
                    *mode_prohibit,
                ),
                allow=(),
                exception=(
                    "`/tmp`, `%TMPDIR` ツリー内は読み書きして良い（一時作業領域として使って良い）",
                    "MCP 経由の外部ツールによるファイル書き込みは、この policy の書き込み制限の対象外とする",
                    "Structured Output を受け取った外部ツールによるファイル書き込みは、この policy の書き込み制限の対象外とする",
                ),
                supplemental=(
                    "この policy は deny list で記述しており、禁止されていない読み書きは暗黙に許容される",
                ),
            ),
        ),
    )
