# `cmoc apply abandon`

## 概要

- `cmoc apply abandon` は、現在の session に紐づく未 join の apply run を破棄する。
- 破棄対象は `<cmoc-apply-branch>` と `<cmoc-apply-worktree>` である。
- `<cmoc-session-branch>` の commit は変更しない。
- `<cmoc-session-branch>` 上で進められた oracle 改訂作業も変更しない。
- `cmoc apply join` 済みの結果を取り消す rollback コマンドではない。
- apply 成果物を破棄する正規の手段であり、ユーザーが手作業で `<cmoc-apply-branch>` や `<cmoc-apply-worktree>` を削除する代わりに使う。

## 引数

- 引数なし

## 事前条件

以下の場合はエラー終了する。

- 現在のブランチが `<cmoc-session-branch>`, `<cmoc-apply-branch>` のいずれでもない
- 対応する `<cmoc-session-state-file>` が存在しない
- 対応する `<cmoc-session-state-file>` の `session.state` が `active` ではない
- 対応する `<cmoc-session-state-file>` の `apply.state` が `ready` である
    - `ready` は active な apply run が存在しない状態なので、破棄対象が存在しない
- 対応する `<cmoc-session-state-file>` から `<cmoc-apply-branch>` または `<cmoc-apply-worktree>` を特定できない
- `<cmoc-session-branch>` 側の worktree に git 未コミット差分が存在する

## 破棄対象

`cmoc apply abandon` は以下を破棄してよい。

- `<cmoc-apply-worktree>`
- `<cmoc-apply-worktree>` 上の未コミット差分
- `<cmoc-apply-branch>`
- `<cmoc-session-state-file>` 上の active apply run 情報

`cmoc apply abandon` は以下を破棄してはいけない。

- `<cmoc-session-branch>`
- `<cmoc-session-branch>` 上の commit
- `<cmoc-session-branch>` 上の oracle 改訂内容
- `<cmoc-session-home-branch>`
- 既に保存済みの report
- `<cmoc-session-state-file>` 自体

## 実行手順

1. 現在の branch と `<cmoc-session-state-file>` から `<session-id>` を特定する。
2. `<cmoc-session-state-file>` を読み込む。
3. `session.state` が `active` であることを確認する。
4. `apply.state` が `ready` ではないことを確認する。
5. `apply.state` が `running` である場合、実行中の apply プロセスが存在しないことを保証する (i.e. 停止する) 
6. `<cmoc-session-branch>`, `<cmoc-apply-branch>`, `<cmoc-apply-worktree>` を特定する。
7. 現在の branch が `<cmoc-apply-branch>` の場合、削除対象 worktree の外から cleanup できる状態へ移動する。
8. `<cmoc-apply-worktree>` が存在する場合、強制削除する。
    - `<cmoc-apply-worktree>` 上の未コミット差分は破棄してよい。
    - 既に存在しない場合は warning として記録し、処理を続行してよい。
9. `<cmoc-apply-branch>` が存在する場合、強制削除する。
    - `<cmoc-apply-branch>` が `<cmoc-session-branch>` に merge 済みであることは要求しない。
    - 既に存在しない場合は warning として記録し、処理を続行してよい。
10. `<cmoc-session-state-file>` の `apply.state` を `ready` に更新する。
11. active apply run を特定するための補助情報を、次回 apply の妨げにならない状態へ初期化する。
12. 結果を stdout に表示する。

## 状態遷移

- `cmoc apply abandon` が正常終了した場合、`apply.state` は `ready` になる。
- 破棄前の `apply.state` は `running`, `completed`, `error` のいずれでもよい。
- `apply.state` が `running` の状態で `cmoc apply abandon` を実行した場合
    - `cmoc apply abandon` プロセスが実行中の apply プロセスを停止させる
    - 実行中の apply プロセスが存在しないことを確認してから
- `apply.state` が `completed` の状態で `cmoc apply abandon` を実行した場合
    - その apply run の成果物は `<cmoc-session-branch>` へ merge されない。

## Codex CLI 呼び出し

- `cmoc apply abandon` は Codex CLI を呼び出さない。
- 破棄処理のために AI に修正、整理、conflict 解消、report 作成を依頼しない。
- `cmoc apply abandon` は機械的な cleanup コマンドとして実装する。

## report

`cmoc apply abandon` は少なくとも以下を stdout に表示する。

- 破棄した `<cmoc-apply-branch>`
- 破棄した `<cmoc-apply-worktree>`
- 破棄前の `apply.state`
- 破棄後の `apply.state`
- cleanup 中に発生した warning

専用の markdown report ファイルを作成する必要はない。

## cleanup 失敗時の扱い

- `<cmoc-apply-worktree>` や `<cmoc-apply-branch>` が既に存在しない場合は、warning として扱い、破棄済みとみなしてよい。
- cleanup の一部に失敗しても、`<cmoc-session-branch>` の内容は変更してはいけない。
- cleanup 後に孤立した `<cmoc-apply-branch>` や `<cmoc-apply-worktree>` が残る場合は、そのパスや branch 名を warning としてユーザーに表示する。
- `<cmoc-session-state-file>` を `ready` に戻せなかった場合はエラー終了する。

## サブコマンドの終了コード

- 正常に active apply run を破棄できた場合は 0 を返す。
- 事前条件を満たさない場合は非 0 を返す。
- `<cmoc-session-state-file>` を更新できなかった場合は非 0 を返す。
