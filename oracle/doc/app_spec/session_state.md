# `{{cmoc-session-state-file}}`

## 概要

- cmoc workflow 上の session と、明示的な join を必要とする編集 run の lifecycle を一意に定める JSON file である。
- 保存先は `{{repo-root}}/.cmoc/gu/ar/session/{{session-id}}.json` とする。

## スキーマ設計の基本原則

- 永続化する情報は必要最小限に留める。
- その場で確実に解決できる情報は state に持たせない。
- 1 session に未 join の編集 run は高々 1 つとする。

## スキーマ定義

```json
{
  "session": {
    "state": "active | joined | abandoned | error",
    "session_home_branch": "...",
    "session_fork_commit": "...",
    "last_joined_apply_fork_commit": "... | null"
  },
  "run": {
    "state": "ready | running | joinable | error",
    "kind": "realization_apply | realization_refactor | null",
    "branch": "... | null",
    "fork_commit": "... | null"
  }
}
```

## session field

### `session.state`

- 現在の session の状態である。
- session 新規作成直後の初期値は `active` とする。
- `cmoc session` 系サブコマンドによって遷移する。

### `session.session_home_branch`

- session の fork 元 branch であり join 先でもある。
- `cmoc session fork` が、その時点で checkout している `{{local-branch}}` 名で初期化する。

### `session.session_fork_commit`

- session の `{{cmoc-session-fork-commit}}` である。

### `session.last_joined_apply_fork_commit`

- その session で最後に merge へ成功した realization apply run の `{{cmoc-run-fork-commit}}` である。
- session 新規作成直後の初期値は `null` とする。
- active run の kind が `realization_apply` である `cmoc run join` が merge に成功した場合だけ更新する。

## run field

### `run.state`

- `ready` は未 join の編集 run がない状態である。
- `running` は workload の処理が実行中である状態である。
- `joinable` は正常終了、または整合した処理単位でのユーザー中断後で、`cmoc run join` または `cmoc run abandon` を待つ状態である。
- `error` は続行不能な失敗後で、確定済み成果物に対する `cmoc run join` または run 全体に対する `cmoc run abandon` を待つ状態である。
- session 新規作成直後の初期値は `ready` とする。

### `run.kind`

- active な realization 編集 run の workload を表す。
- `run.state` が `ready` の場合は `null` とする。
- join と abandon はこの値から workload を解決する。
- `cmoc oracle edit` は run ではなく、この field の値にならない。

### `run.branch`

- active run の `{{cmoc-run-branch}}` 名である。
- `run.state` が `ready` の場合は `null` とする。

### `run.fork_commit`

- active run の `{{cmoc-run-fork-commit}}` である。
- apply の差分終点と run join の差分検査にも使用する。
- `run.state` が `ready` の場合は `null` とする。

## 状態遷移

- workload 固有の fork が新しい編集 run を開始すると、`ready` から `running` へ遷移する。
- workload が正常終了すると `joinable` へ遷移する。
- 中断可能な workload が整合した処理単位でユーザー中断を完了すると `joinable` へ遷移する。
- workload が続行不能な失敗で停止すると `error` へ遷移する。
- `cmoc run join` または `cmoc run abandon` が正常終了すると `ready` へ遷移し、`kind`, `branch`, `fork_commit` を `null` に初期化する。
