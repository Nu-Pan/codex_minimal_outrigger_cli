# `cmoc session abandon`

## 概要

- `cmoc session abandon` は、現在の `{{cmoc-session-branch}}` を `{{cmoc-session-home-branch}}` に merge せず破棄する。
- session を完了させる `cmoc session join` とは異なり、session の成果物を本流へ取り込まない。
- `cmoc session join` 済みの結果を取り消す rollback コマンドではない。
- cmoc 管理下の session を破棄する正規の手段であり、ユーザーが手作業で `{{cmoc-session-branch}}` を削除する代わりに使う。

## 引数

- 引数なし

## 事前条件

`cmoc session abandon` は `{{cmoc-session-branch}}` 上でのみ実行できる。

以下の場合はエラー終了する。

- 現在のブランチが `{{cmoc-session-branch}}` ではない
- 対応する `{{cmoc-session-state-file}}` が存在しない
- 対応する `{{cmoc-session-state-file}}` の `session.state` が `active` ではない
- 対応する `{{cmoc-session-state-file}}` の `realization_run.state` が `ready` ではない
    - 未 join の realization run が残っている場合は、その種類に対応する `cmoc realization apply abandon` または `cmoc realization refactor abandon` で先に破棄する
- `{{cmoc-session-home-branch}}` が存在しない
- `{{cmoc-session-branch}}` 側の worktree に git 未コミット差分が存在する

## 破棄対象

`cmoc session abandon` は以下を破棄してよい。

- `{{cmoc-session-branch}}`
- `{{cmoc-session-branch}}` 上にだけ存在する commit
- `{{cmoc-session-branch}}` 上で行われた oracle 改訂
- `{{cmoc-session-branch}}` 上で行われた実装修正

`cmoc session abandon` は以下を破棄してはいけない。

- `{{cmoc-session-home-branch}}`
- `{{cmoc-session-home-branch}}` 上の commit
- `{{cmoc-session-state-file}}` 自体
- 既に保存済みの report
- 未 join の realization run
    - realization run が残っている場合は `cmoc session abandon` では処理せず、その種類に対応する abandon を要求する

## 実行手順

1. doctor preprocess を呼び出す
2. 事前検証
    - 事前条件を満たしている事を確認する
3. クリーンアップ
    1. `git switch {{cmoc-session-home-branch}}` を実行する。
    2. `{{cmoc-session-state-file}}` の `session.state` を `abandoned` に更新する。
    3. `session.joined_at` は `null` のままとする。
    4. `{{cmoc-session-branch}}` を強制削除する。
4. 結果を stdout に表示する。

## 状態遷移

- `cmoc session abandon` が正常終了した場合、`session.state` は `abandoned` になる。
- `abandoned` になった session は active session ではない。
- したがって、同じ `{{cmoc-session-home-branch}}` から新しい `cmoc session fork` を実行してよい。

## クリーンアップの途中で失敗した場合

- クリーンアップで行った操作をロールバックし、再実行可能な状態にする
- ユーザーに「問題の手動解決したうえで `cmoc session abandon` 再実行」を促す
