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
        意味仕様は `oracle/doc/app_spec/codex_exec_rule.md` の
        「ファイルアクセス制限」を参照。
        いろいろあって、細かいアクセス制御はプロンプトによる指示とした。
        sandbox の設定は non-goal である。
    """
    if mode is FileAccessMode.NO_POLICY:
        # 有効な mode だが、共通 file access policy は存在しない。
        return None

    # リポジトリ外への禁止事項
    # NOTE
    #   work-root 外の書き込み禁止は、言わなくてもわかりそう。
    #   だが、規定文面としての整合性を優先して明示する。
    # NOTE
    #   ログ関係だけは例外的に `{{run-root}}` で作業していようと cmoc が `{{repo-root}}/.cmoc/gu/ar/log` に書きに行く。
    #   その関係で、agent が `{{run-root}}` での作業中に `{{repo-root}}/.cmoc/gu/ar/log` を読みに行きたくなる事がある。
    #   更に log から `{{repo-root}}/.cmoc` ツリー内を読みに行きたくなるはずである (report とか)。
    #   work-root が異なる場合は、repo-root の `ar` を読み取り禁止の集合から外し、
    #   書き込みだけを別の項目で禁止する。
    repo_root = path_context.repo_root
    work_root = path_context.work_root
    if repo_root == work_root:
        out_repo_denials = [
            "`{{repo-root}}` ツリー外は読み書き禁止",
        ]
    else:
        out_repo_denials = [
            "`{{work-root}}` ツリー外かつ `{{repo-root}}/.cmoc/g*/ar` ツリー外は読み書き禁止",
            "`{{repo-root}}/.cmoc/g*/ar` ツリー内は書き込み禁止",
        ]
    # 共通の禁止事項
    # NOTE
    #   `.git`, `.agents`, `.codex` Codex CLI の実装で書き込み禁止とされている。
    #   規定文面の整合性として明示する。
    # NOTE
    #   `AGENTS.md` の Codex CLI による書き換えは、実質的には自己の書き換え。
    #   挙動を予測不能で非常に危険なので禁止する。
    # NOTE
    #   安いモデルを使って `INDEX.md` を更新する仕組みがすでにあって、それは READONLY で実行される。
    #   高性能モデルが作業中に `INDEX.md` を触っちゃうのはトークンの無駄なのでやらせたくない。
    #   よって、`REPO_WRITE` 系 mode では `INDEX.md` は書き込み禁止。
    # NOTE
    #   memo は agent 不可視のユーザーワークスペースとするので読み書き禁止で固定
    base_denials = [
        *out_repo_denials,
        "`{{work-root}}/.git` ツリー内は書き込み禁止",
        "`{{work-root}}/.agents` ツリー内は書き込み禁止",
        "`{{work-root}}/.codex` ツリー内は書き込み禁止",
        "`{{work-root}}/.cmoc/g*/ar` ツリー内は書き込み禁止",
        "`AGENTS.md` は書き込み禁止",
        "`INDEX.md` は書き込み禁止",
        "`{{work-root}}/memo` は読み書き禁止",
    ]
    # mode 別の禁止事項
    # NOTE
    #   許可項目を書こうとすると対象範囲・優先順位の明示に文字数が必要になって大変。
    #   そもそも「書いてない＝リポジトリ全体の制約が適用される」ので、暗に分かるはず。
    #   ということで、禁止されていない操作は許可される deny-list とし、
    #   規定文面には禁止事項だけを書く。
    # NOTE
    #   Codex CLI sandbox への対応は `oracle/doc/app_spec/codex_exec_rule.md` を正本とする。
    #   この関数が生成する詳細な規定はプロンプトとしてのみ使用し、permission profile や
    #   path 単位の sandbox 設定へ変換してはならない。
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
                what_is_this="エージェントによるアクセスが満たすべき規定を以下に示す",
                require=(),
                prohibit=tuple(denials),
                allow=("以上のルールで禁止されていない読み書きは暗黙に許可される。",),
            ),
        ),
    )
