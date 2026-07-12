# cmoc
from oracle.other.path_model import resolve_repo_root, resolve_work_root
from oracle.other.struct_doc import StructDoc
from oracle.acp_builder.basic import FileAccessMode
from oracle.prompt_builder.basic import PlaceholderMap


def build_file_access_rule(mode: FileAccessMode) -> tuple[PlaceholderMap, StructDoc]:
    """
    AI エージェントによるファイル読み書き規則のプロンプトを構築する

    規則は、原則として、リポジトリ全体 repo-write をベースとした deny list 形式で記述する。

    mode:
        読み書きモードプリセット
    """
    # リポジトリ外 deny ルール
    # NOTE
    #   work-root 外の書き込み禁止は、言わなくてもわかりそう。
    #   だが、ルール文章としての整合性を優先して明示する。
    # NOTE
    #   ログ関係だけは例外的に `<run-root>` で作業していようと cmoc が `<repo-root>/.cmoc/gu/ar/log` に書きに行く。
    #   その関係で、agent が `<run-root>` での作業中に `<repo-root>/.cmoc/gu/ar/log` を読みに行きたくなる事がある。
    #   更に log から `<repo-root>/.cmoc` ツリー内を読みに行きたくなるはずである (report とか)。
    #   よって、`<repo-root>/.cmoc/g*/ar` だけは例外的にアクセスを許可する。
    repo_root = resolve_repo_root()
    work_root = resolve_work_root()
    if repo_root == work_root:
        out_repo_deny_rule = [
            "`<repo-root>` ツリー外は読み書き禁止",
        ]
    else:
        out_repo_deny_rule = [
            "`<work-root>` ツリー外は読み書き禁止だが、例外的に `<repo-root>/.cmoc/g*/ar` ツリー内は読み込み可能",
        ]
    # 基礎 deny ルール
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
    # NOTE
    #   memo は agent 不可視のユーザーワークスペースとするので読み書き禁止で固定
    base_deny_rule = [
        *out_repo_deny_rule,
        "`<work-root>/.git` ツリー内は書き込み禁止",
        "`<work-root>/.agents` ツリー内は書き込み禁止",
        "`<work-root>/.codex` ツリー内は書き込み禁止",
        "`<work-root>/.cmoc/g*/ar` ツリー内は書き込み禁止",
        "`AGENTS.md` は書き込み禁止",
        "`INDEX.md` は書き込み禁止",
        "`<work-root>/memo` は読み書き禁止",
    ]
    # モード別ルール設定
    # NOTE
    #   許可系ルールを書こうとすると対象範囲・優先順位の明示に文字数が必要になって大変。
    #   そもそも「書いてない＝リポジトリ全体規則が適用される」なので、暗に分かるはず。
    #   ということで、ルール文には「例外的に〇〇は許可」は書かず、補足コメントだけを書く。
    # NOTE
    #   Codex CLI が使用するサンドボックスは permission profile を `:read-only` に設定しても __pycache_ とかは通してしまう。
    #   つまり、本当に純粋な read-only ではなく、しかもその例外リストは具体的に何なのかはよくわからない。
    #   よって、意味的に read-only なモードでも Codex CLI permission profile は `:workspace` で固定とする。
    #   代わりに cmoc が注入するプロンプトと cmoc による事後チェックでカバーする。
    match mode:
        case FileAccessMode.READONLY:
            # NOTE
            #   リポジトリ全体の **cmoc 上の論理的な意味での** 読み取り専用
            #   主要な編集対象である oracle file, realization file を読み取り専用にする
            #   ルール上言及されていない隙間は `__pycache__` のような一時ファイルを想定しており、そこは読み書き自由とする
            #   調査系タスク、cmoc が書き込みを代行するケースで使われる想定
            deny_rule = [
                *base_deny_rule,
                "oracle file は書き込み禁止",
                "realization file は書き込み禁止",
            ]
        case FileAccessMode.PURE_ORACLE_READ:
            # NOTE
            #   READONLY + realization file アクセス禁止
            #   realization file に釣られずに oracle file から判断してほしい系のタスクで使われる想定
            deny_rule = [
                *base_deny_rule,
                "oracle file は書き込み禁止",
                "realization file は読み書き禁止",
            ]
        case FileAccessMode.REPO_WRITE:
            # NOTE
            #   リポジトリ書き込み可能
            #   `cmoc tui` で微妙なタスクを渡された時に使われる想定
            deny_rule = [
                *base_deny_rule,
                # oracle file は書き込み許可
                # realization file は書き込み許可
            ]
        case FileAccessMode.PURE_ORACLE_WRITE:
            # NOTE
            #   REPO_WRITE + realization file アクセス禁止
            #   realization file に釣られずに oracle file の修正作業をしてほしい時に使われる想定
            deny_rule = [
                *base_deny_rule,
                # oracle file は書き込み許可
                "realization file は読み書き禁止",
            ]
        case FileAccessMode.REALIZATION_WRITE:
            # NOTE
            #   REPO_WRITE + oracle file 書き込み禁止
            #   realization file を oracle file に追従させる作業で使われる想定
            deny_rule = [
                *base_deny_rule,
                "oracle file は書き込み禁止",
                # realization file は書き込み許可
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
            "repo-root": repo_root,
            "work-root": work_root,
        },
        StructDoc(
            f"file read write rule - {mode.value}",
            "\n".join(f"- {r}" for r in deny_rule),
        ),
    )
