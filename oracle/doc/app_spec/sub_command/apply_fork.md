# `cmoc apply fork`

## 概要

- `cmoc apply fork` は、Codex CLI による apply ループを実行する
- この apply ループは以下の状態を目標とする
    - `<work-root>` の実装が `<work-root>/oracle` の正本仕様断片と一致している
    - `<work-root>` の実装が最低限度の品質を満たしている
- `cmoc apply fork` が正常に実行完了したからといって、目標達成が保証されるわけではない
    - あくまで、apply ループを実行し、目標達成のために努力する所までが `cmoc apply fork` の責任範囲である
    - i.e. ベストエフォート的な振る舞いで良い
- `cmoc apply fork` は `<cmoc-session-branch>` と作業用コピーを直接汚すことはしない
    - `<cmoc-apply-branch>` を作成し、そこにコミットを積み上げる

## 引数

- 位置引数なし
- オプション引数 `--scope={rolling|session|full}` を受け取る
    - ショートネームは `-s`
    - デフォルト値は `rolling`

## 事前条件

以下の場合はエラー終了する

- 現在のブランチが `<cmoc-session-branch>` ではない
- 対応する `<cmoc-session-state-file>` が存在しない
- 対応する `<cmoc-session-state-file>` の `session.state` が `active` ではない
- 対応する `<cmoc-session-state-file>` の `apply.state` が `ready` ではない
- git 未コミット差分が存在する

## 実行作業

1. `<work-root>/.cmoc` が git の追跡対象外であることを保証する
2. run の隔離実行を開始する
3. 調査待ちファイルリストを初期化
3. apply ループ
    1. 調査待ちファイルリストの先頭から、調査対象ファイルを 1 件 pop
    2. agent call で「調査対象ファイルを元にした所見のリストアップ」を実行
    3. 所見リストが空なら apply ループ先頭へ戻る
    4. agent call で「所見リストに対する修正作業」を Codex CLI に依頼する
    5. apply ループ先頭に戻る
4. `<cmoc-session-state-file>` の状態を更新
5. 作業結果をレポートする

## `cmoc apply fork` の責務境界

- `cmoc apply fork` の責務は、指定された最大回数の範囲で apply ループを実行し、その結果を人間が判断できる形でレポートすることである
- `cmoc apply fork` は、あくまでベストエフォート的に振る舞う
    - i.e. 所見が残っていないことを保証しない
    - i.e. `cmoc apply fork` は、全ての所見を漏れなく発見することは保証しない
- ループが回数上限に達した場合も、コマンド実行としては正常系として扱う
    - 回数上限到達後にどうするかは人間が判断すべきことであり、それを奪ってはいけない

## `<cmoc-session-state-file>` 状態遷移

- apply ループ開始直前
    - `apply.state` を `running` に遷移させる
    - `apply` セクションの各フィールドを、適切な値で更新する
- apply ループ完了直後
    - i.e. 全ての処理が正常に完了出来た場合
    - `apply.state` を `completed` に遷移させる
    - `apply` セクションの各フィールドを、適切な値で更新する
- 途中でエラーが発生して処理を中止した場合
    - `apply.state` を `error` に遷移させる

## 「run の隔離実行を開始する」とは

- それ以降の実際の作業を `<cmoc-review-worktree>` 上で隔離実行することを指す
- 詳しくは `<cmoc-root>/oracle/doc/app_specs/run_isolation.md` を参照すること

## 「調査待ちリストを初期化」とは

- `cmoc apply fork` では調査対象のファイルを「調査待ちファイルリスト」で管理する
- `--scope rolling`: ローリングスコープ（デフォルト値）
    - 「前回の apply の `<cmoc-apply-join-commit>`」から「今回の apply の `<cmoc-apply-fork-commit>`」の間に変更があったファイルを、調査待ちファイルリストの初期値とする
    - そのセッションの最初の apply の場合は、セッションスコープにフォールバックする
    - i.e. `cmoc apply fork` 後に変更があったファイルについて、最低 1 回は調査が行われるということ
- `--scope session`: セッションスコープ
    - `<cmoc-session-fork-commit>` から `<cmoc-apply-fork-commit>` の間で変更があったファイルを、調査待ちファイルリストの初期値とする
    - i.e. そのセッション上で変更のあったファイルについて、最低 1 回は調査が行われるということ
- `--scope full`
    - 全ての oracle file, realization file を、調査待ちファイルリストの初期値とする
    - i.e. 全候補ファイルについて、最低 1 回は調査が行われるということ

## 「apply ループ」とは

- ファイル単位で「所見調査と、それを元にした反映作業」を繰り返す
- 処理したファイル数が `CmocConfigApplyFork.num_apply_files` に達したら強制的に処理を打ち切る
- 強制的に処理を打ち切った場合、作業結果の区分「未収束」として処理を続行する（エラーとみはみなさない）

## 「調査待ちファイルリストの先頭から、調査対象ファイルを 1 件 pop」とは

- 調査待ちファイルリスト上の重複する要素を削除したうえで、リスト先頭の 1 件をと調査対象ファイルとして pop する
- 重複削除時は、最も先頭側の 1 件だけを残す

## 『agent call で「調査対象ファイルを元にした所見のリストアップ」を実行』とは

- 調査対象ファイルとその関連ファイルを読んで所見をリストアップする
- agent call の仕様は `build_apply_fork_file_finding_enumeration_parameter` を正本とする
- agent call によって所見が 1 つ以上リストアップされた場合、起点とした調査対象ファイルを調査待ちファイルリストの末尾に追加する

## 『agent call で「所見リストに対する修正作業」を Codex CLI に依頼する』とは

- 所見リストを元に、それと対応する修正作業を行う
- agent call の仕様は `build_apply_fork_finding_application_parameter` を正本とする
- agent call によって差分が発生した realization file を調査待ちファイルリストの末尾に追加する
- agent call によって発生した差分は自動的に git commit する

## 作業レポートの仕様

- レポートの形式は markdown + YAML Front Matter とする
- YAML Front Matter に必ず含める項目
    - `<cmoc-session-branch>`
    - `<cmoc-session-fork-commit>`
    - `<cmoc-apply-branch>`
    - `<cmoc-apply-fork-commit>`
    - `<cmoc-apply-worktree>`
- レポート本文に必ず含める項目
    - 作業結果
        - 収束 : 「検出された所見リストが空」によりループを終了した
        - 未収束 : 「回数上限に達した」によりループを終了した
        - エラー : 途中でエラーが起きてループを正常に終了出来なかった
    - 所見数の推移
        - ループごとに何件の所見を見つけたかを書く
        - 「未収束」の場合は、まだ所見が残っている可能性を定型文で追記する
    - `<cmoc-apply-branch>` 上の全ての変更内容に対する要約
        - この `cmoc apply fork` で行った作業内容だけの要約に限定する
        - 変更内容の意味論に基づいたカテゴリ分けを行うこと
- レポート本体は `<repo-root>/.cmoc/local/report/apply/fork/<time-stamp>.md` にファイルに保存する
- 作成したレポートのフルパスを標準出力に流すこと (内容は流さない)

## `<cmoc-apply-branch>` 上の全ての変更内容に対する要約の生成方法

- `<cmoc-apply-branch>` 上の全ての変更内容に対する要約の生成を agent call に依頼する
- この agent call の詳細仕様は `build_apply_fork_change_summary_parameter` を正本とする
- cmoc は Structured Output を作業レポート用 Markdown にレンダリングする

## サブコマンドの終了コード

- 収束・未収束・エラーの３種類を区別可能であること
