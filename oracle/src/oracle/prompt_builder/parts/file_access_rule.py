# cmoc
from oracle.other.path_model import resolve_work_root
from oracle.other.struct_doc import StructDoc
from oracle.acp_builder.basic import FileAccessMode
from oracle.prompt_builder.basic import PlaceholderMap


def build_file_access_rule(mode: FileAccessMode) -> tuple[PlaceholderMap, StructDoc]:
    """
    AI エージェントによるファイル読み書き規則のプロンプトを構築する

    規則は、リポジトリ全体 read-only, repo-write をベースとした deny list 形式で記述する。

    mode:
        読み書きモードプリセット
    """
    # 全モード共通の deny ルール
    # NOTE
    #   work-root 外アクセス禁止は、言わなくてもわかりそう。
    #   ルール文章としての整合性を優先して明示する。
    # NOTE
    #   memo は agent 不可視のユーザーワークスペースとするので読み書き禁止で固定
    base_deny_rule = [
        "`<work-root>` ツリー外は読み書き禁止",
        "`<work-root>/memo` は読み書き禁止",
    ]
    # REPO_WRITE 系共通の deny ルール
    # NOTE
    #   `.git`, `.agents`, `.codex` Codex CLI の実装で書き込み禁止とされている。
    #   ルール文章の整合性として明示する。
    # NOTE
    #   `AGENTS.md` の Codex CLI による書き換えは、実質的には自己の書き換え。
    #   挙動を予測不能で非常に危険なので禁止する。
    # NOTE
    #   安いモデルを使って `INDEX.md` を更新する仕組みがすでにあって、それは READONLY で実行される。
    #   高性能モデルが作業中に `INDEX.md` を触っちゃうのはトークンの無駄なのでやらせたくない。
    #   よって、`REPO_WRITE` 系ルールでは `INDEX.md` は書き込み禁止。
    repo_write_deny_rule = [
        "`<work-root>/.git` ツリー内は書き込み禁止",
        "`<work-root>/.agents` ツリー内は書き込み禁止",
        "`<work-root>/.codex` ツリー内は書き込み禁止",
        "`AGENTS.md` は書き込み禁止",
        "`INDEX.md` は書き込み禁止",
    ]
    # モード別ルール設定
    # NOTE
    #   許可系ルールを書こうとすると対象範囲・優先順位の明示に文字数が必要になって大変。
    #   そもそも「書いてない＝リポジトリ全体規則が適用される」なので、暗に分かるはず。
    #   ということで、ルール文には「例外的に〇〇は許可」は書かず、補足コメントだけを書く。
    match mode:
        case FileAccessMode.READONLY:
            # NOTE
            #   リポジトリ全体の完全な読み取り専用
            #   Codex CLI permission は `:read-only` を想定
            deny_rule = [
                *base_deny_rule,
                "`<work-root>` ツリー内は書き込み禁止",
                # `INDEX.md` 書き込み禁止だけど、そもそもツリー内書き込み禁止なので明示不要
            ]
        case FileAccessMode.PURE_ORACLE_READ:
            # NOTE
            #   READONLY + realization file アクセス禁止
            #   Codex CLI permission は `:read-only` を想定
            #   realization file に釣られずに oracle file から判断してほしい系のタスクで使われる想定
            deny_rule = [
                *base_deny_rule,
                "`<work-root>` ツリー内は書き込み禁止",
                "realization file は読み書き禁止",
                # `INDEX.md` 書き込み禁止だけど、そもそもツリー内書き込み禁止なので明示不要
            ]
        case FileAccessMode.REPO_WRITE:
            # NOTE
            #   リポジトリ書き込み可能
            #   Codex CLI permission は `:workspace` を想定
            #   `cmoc tui` で微妙なタスクを渡された時に使われる想定
            deny_rule = [
                *base_deny_rule,
                *repo_write_deny_rule,
                # oracle file は書き込み許可
                # realization file は書き込み許可
            ]
        case FileAccessMode.PURE_ORACLE_WRITE:
            # NOTE
            #   REPO_WRITE + realization file アクセス禁止
            #   Codex CLI permission は `:workspace` を想定
            #   realization file に釣られずに oracle file の修正作業をしてほしい時に使われる想定
            deny_rule = [
                *base_deny_rule,
                *repo_write_deny_rule,
                # oracle file は書き込み許可
                "realization file は読み書き禁止",
            ]
        case FileAccessMode.REALIZATION_WRITE:
            # NOTE
            #   REPO_WRITE + oracle file 書き込み禁止
            #   Codex CLI permission は `:workspace` を想定
            #   realization file を oracle file に追従させる作業で使われる想定
            deny_rule = [
                *base_deny_rule,
                *repo_write_deny_rule,
                "oracle file は書き込み禁止",
                # realization file は書き込み許可
            ]
        case FileAccessMode.INDEX_WRITE:
            #
            deny_rule = [
                *base_deny_rule,
                "`<work-root>/.git` ツリー内は書き込み禁止",
                "`<work-root>/.agents` ツリー内は書き込み禁止",
                "`<work-root>/.codex` ツリー内は書き込み禁止",
                "`AGENTS.md` は書き込み禁止",
                # `INDEX.md` は書き込み許可
                "oracle file は書き込み禁止",
                "realization file は読み書き禁止",
            ]
        case FileAccessMode.NO_RULE:
            # `build_complete_prompt` によるアクセス規則文面が生成されない
            # 特殊文面を個別に構築する用の特別モードで、よほどのことがない限り使ってはいけない
            return ({}, StructDoc("", ""))
        case _:
            raise ValueError(f"Invalid mode (mode={mode})")
    # 正常終了
    return (
        {
            "work-root": resolve_work_root(),
        },
        StructDoc(
            f"file read write rule - {mode.value}",
            "\n".join(f"- {r}" for r in deny_rule),
        ),
    )
