# `cmoc apply fork`

## 概要

- `cmoc apply fork` は、Codex CLI による apply ループを実行する
- この apply ループは以下の状態を目標とする
    - `{{work-root}}` の実装が `{{work-root}}/oracle` の正本仕様断片と一致している
    - `{{work-root}}` の実装が最低限度の品質を満たしている
- `cmoc apply fork` は `{{cmoc-session-branch}}` と作業用コピーを直接汚すことはしない
    - `{{cmoc-apply-branch}}` を作成し、そこにコミットを積み上げる

## 引数

- 位置引数なし
- オプション引数 `--scope={rolling|session|full}` を受け取る
    - ショートネームは `-s`
    - デフォルト値は `rolling`

## 事前条件

以下の場合はエラー終了する

- 現在のブランチが `{{cmoc-session-branch}}` ではない
- 対応する `{{cmoc-session-state-file}}` が存在しない
- 対応する `{{cmoc-session-state-file}}` の `session.state` が `active` ではない
- 対応する `{{cmoc-session-state-file}}` の `apply.state` が `ready` ではない
- git 未コミット差分が存在する

## 実行作業

1. doctor preprocess を呼び出す
2. run の隔離実行を開始する
3. 調査待ちファイルリストを初期化
4. apply ループ
    1. 調査待ちファイルリストの先頭から、調査対象ファイルを 1 件 pop
    2. agent call で「調査対象ファイルを起点にした所見調査・修正・検証」を実行
    3. agent call の結果と差分に基づいて調査待ちファイルリストを更新
    4. agent call によって発生した差分を自動的に git commit
    5. apply ループ先頭に戻る
5. `{{cmoc-session-state-file}}` の状態を更新
6. 作業結果をレポートする

## `{{cmoc-apply-branch}}` の想定内差分

- apply ループが `{{cmoc-apply-branch}}` に積み上げてよい差分は以下とする
    - ファイル単位レビュー・修正 prompt が変更を許可する realization file
    - cmoc が自動生成する任意階層の `INDEX.md`
- agent call は realization file だけを変更し、`INDEX.md` の生成は cmoc が担う

## `cmoc apply fork` の責務境界

- `cmoc apply fork` の責務は、指定された最大回数の範囲で apply ループを実行し、その結果を人間が判断できる形でレポートすることである
- `cmoc apply fork` はベストエフォートであり、正常完了しても目標達成を保証しない
    - i.e. 所見が残っていないことを保証しない
    - i.e. `cmoc apply fork` は、全ての所見を漏れなく発見することは保証しない
- ループが回数上限に達した場合も、コマンド実行としては正常系として扱う
    - 回数上限到達後にどうするかは人間が判断すべきことであり、それを奪ってはいけない

## ユーザー中断

- `cmoc apply fork` は中断可能サブコマンドとし、共通動作は `{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` を正本とする
- ユーザー中断要求を受け付けた場合、apply ループを次の一貫した境界で打ち切る
    - 完了済みの処理単位による commit は保持する
    - 実行中だった処理単位は、完了させて commit するか、そこで発生した未確定の変更を破棄する
    - `{{cmoc-apply-branch}}` と `{{cmoc-apply-worktree}}` に未確定の変更を残さない
- apply ループは未収束として正常に完了させ、`apply.state` を `completed` に遷移させる
- 中断までに確定した部分結果は `cmoc apply join` または `cmoc apply abandon` で扱えるものとし、中断した apply ループ自体は再開しない

## `{{cmoc-session-state-file}}` 状態遷移

- apply ループ開始直前
    - `apply.state` を `running` に遷移させる
    - `apply` セクションの各フィールドを、適切な値で更新する
- apply ループ完了直後
    - i.e. 全ての処理が正常に完了できた場合
    - ユーザー中断要求により未収束として正常に完了した場合を含む
    - `apply.state` を `completed` に遷移させる
    - `apply` セクションの各フィールドを、適切な値で更新する
- 途中でエラーが発生して処理を中止した場合
    - `apply.state` を `error` に遷移させる

## 「run の隔離実行を開始する」とは

- それ以降の実際の作業を `{{cmoc-apply-worktree}}` 上で隔離実行することを指す
- 詳しくは `{{cmoc-root}}/oracle/doc/app_spec/run_isolation.md` を参照すること

## 「調査待ちファイルリストを初期化」とは

- `cmoc apply fork` では調査対象のファイルを「調査待ちファイルリスト」で管理する
- `--scope rolling`: ローリングスコープ（デフォルト値）
    - 「前回の apply の `{{cmoc-apply-join-commit}}`」から「今回の apply の `{{cmoc-apply-fork-commit}}`」の間に変更があった oracle file, realization file を、調査待ちファイルリストの初期値とする
    - そのセッションの最初の apply の場合は、セッションスコープにフォールバックする
    - i.e. `cmoc apply fork` 後に変更があったファイルについて、最低 1 回は調査が行われるということ
- `--scope session`: セッションスコープ
    - `{{cmoc-session-fork-commit}}` から `{{cmoc-apply-fork-commit}}` の間で変更があった oracle file, realization file を、調査待ちファイルリストの初期値とする
    - i.e. そのセッション上で変更のあったファイルについて、最低 1 回は調査が行われるということ
- `--scope full`
    - 全ての oracle file, realization file を、調査待ちファイルリストの初期値とする
    - i.e. 全候補ファイルについて、最低 1 回は調査が行われるということ

## 「apply ループ」とは

- ファイル単位で「所見調査・修正・検証」を 1 回の agent call に依頼する
- 所見を 1 件以上検出した調査対象ファイルと、修正で差分が発生した realization file を調査待ちファイルリストへ再投入することで、回数上限に達しない範囲で所見が検出されなくなるまでファイル単位の処理を繰り返す
- 調査待ちファイルリストが空になった場合、apply ループは収束したものとして終了する
- 処理したファイル数が `CmocConfigApplyFork.num_apply_files` に達したら強制的に処理を打ち切る
- 強制的に処理を打ち切った場合、作業結果の区分「未収束」として処理を続行する（エラーとはみなさない）

## 「調査待ちファイルリストの先頭から、調査対象ファイルを 1 件 pop」とは

- 調査待ちファイルリスト上の重複する要素を削除したうえで、リスト先頭の 1 件を調査対象ファイルとして pop する
- 重複削除時は、最も先頭側の 1 件だけを残す

## 『agent call で「調査対象ファイルを起点にした所見調査・修正・検証」を実行』とは

- 調査対象ファイルとその関連ファイルを読み、所見の列挙、所見に対応する realization file の修正、修正後の検証までを同一の agent call で行う
- この処理単位では、所見調査と修正を別の agent call に分割しない
- agent call の仕様は `build_apply_fork_file_review_and_fix_parameter` を正本とする
- agent call が返す所見リストには、その agent call 内の修正で解消した所見も含める
- agent call によって所見が 1 つ以上リストアップされた場合、起点とした調査対象ファイルを調査待ちファイルリストの末尾に追加する
- agent call によって差分が発生した realization file を調査待ちファイルリストの末尾に追加する
- 所見リストが空の場合、agent call は差分を発生させてはいけない
- agent call によって発生した差分は、返された所見のいずれかに対応していなければならない

## 作業レポートの仕様

- レポートの形式は markdown + YAML Front Matter とする
- YAML Front Matter に必ず含める項目
    - `{{cmoc-session-branch}}`
    - `{{cmoc-session-fork-commit}}`
    - `{{cmoc-apply-branch}}`
    - `{{cmoc-apply-fork-commit}}`
    - `{{cmoc-apply-worktree}}`
- レポート本文に必ず含める項目
    - 作業結果
        - 収束 : 調査待ちファイルリストが空になったことによりループを終了した
        - 未収束 : 「回数上限に達した」または「ユーザー中断要求を受け付けた」ことによりループを終了した
            - どちらの終了理由であるかを明記する
        - エラー : 途中でエラーが起きてループを正常に終了できなかった
    - 所見数の推移
        - ループごとに、その agent call で何件の所見を見つけたかを書く
        - agent call 内で修正済みとなった所見も件数に含める
        - 「未収束」の場合は、まだ所見が残っている可能性を定型文で追記する
    - `{{cmoc-apply-branch}}` 上の全ての変更内容に対する要約
        - この `cmoc apply fork` で行った作業内容だけの要約に限定する
        - 変更内容の意味論に基づいたカテゴリ分けを行うこと
- レポート本体は `{{repo-root}}/.cmoc/gu/ar/report/apply/fork/{{time-stamp}}.md` として保存する
- 作成したレポートのフルパスを標準出力に流すこと (内容は流さない)

## `{{cmoc-apply-branch}}` 上の全ての変更内容に対する要約の生成方法

- `{{cmoc-apply-branch}}` 上の全ての変更内容に対する要約の生成を agent call に依頼する
- この agent call の詳細仕様は `build_apply_fork_change_summary_parameter` を正本とする
- cmoc は Structured Output を作業レポート用 Markdown にレンダリングする

## サブコマンドの終了コード

- 収束・未収束・エラーの 3 種類を区別可能であること
- ユーザー中断要求による完了は未収束に分類し、エラー終了として扱わない
