# `cmoc session abandon`

## 概要

- `cmoc session abandon` は、現在の `<cmoc-session-branch>` を `<cmoc-session-home-branch>` に merge せず破棄する。
- session を完了させる `cmoc session join` とは異なり、session の成果物を本流へ取り込まない。
- `cmoc session join` 済みの結果を取り消す rollback コマンドではない。
- cmoc 管理下の session を破棄する正規の手段であり、ユーザーが手作業で `<cmoc-session-branch>` を削除する代わりに使う。

## 引数

- 引数なし

## 事前条件

`cmoc session abandon` は `<cmoc-session-branch>` 上でのみ実行できる。

以下の場合はエラー終了する。

- 現在のブランチが `<cmoc-session-branch>` ではない
- 対応する `<cmoc-session-state-file>` が存在しない
- 対応する `<cmoc-session-state-file>` の `session.state` が `active` ではない
- 対応する `<cmoc-session-state-file>` の `apply.state` が `ready` ではない
    - active, completed, error などの apply run が残っている場合は、先に `cmoc apply abandon` で apply run を破棄する
- `<cmoc-session-home-branch>` が存在しない
- `<cmoc-session-branch>` 側の worktree に git 未コミット差分が存在する

## 破棄対象

`cmoc session abandon` は以下を破棄してよい。

- `<cmoc-session-branch>`
- `<cmoc-session-branch>` 上にだけ存在する commit
- `<cmoc-session-branch>` 上で行われた oracle 改訂
- `<cmoc-session-branch>` 上で行われた実装修正

`cmoc session abandon` は以下を破棄してはいけない。

- `<cmoc-session-home-branch>`
- `<cmoc-session-home-branch>` 上の commit
- `<cmoc-session-state-file>` 自体
- 既に保存済みの report
- active apply run
    - active apply run が残っている場合は `cmoc session abandon` では処理せず、先に `cmoc apply abandon` を要求する

## 実行手順

1. 現在の `<cmoc-session-branch>` から `<session-id>` を特定する。
2. `<cmoc-session-state-file>` を読み込む。
3. `session.state` が `active` であることを確認する。
4. `apply.state` が `ready` であることを確認する。
5. metadata から `<cmoc-session-home-branch>` を取得する。
6. `<cmoc-session-home-branch>` が local branch として存在することを確認する。
7. `<cmoc-session-branch>` 側の worktree に git 未コミット差分が存在しないことを確認する。
8. `<repo-root>/.cmoc` が git の追跡対象外であることを保証する。
9. `git switch <cmoc-session-home-branch>` を実行する。
10. `<cmoc-session-state-file>` の `session.state` を `abandoned` に更新する。
11. `session.joined_at` は `null` のままとする。
12. `<cmoc-session-branch>` を強制削除する。
    - `<cmoc-session-branch>` が `<cmoc-session-home-branch>` に merge 済みであることは要求しない。
13. 結果を標準出力に表示する。

## 状態遷移

`cmoc session abandon` が正常終了した場合、`session.state` は `abandoned` になる。

`abandoned` になった session は active session ではない。

したがって、同じ `<cmoc-session-home-branch>` から新しい `cmoc session fork` を実行してよい。

## active apply run が残っている場合

`cmoc session abandon` は active apply run を暗黙に破棄しない。

`apply.state` が `ready` ではない場合はエラー終了し、ユーザーに先に以下を実行するよう案内する。

```bash
cmoc apply abandon
```
