## `{{cmoc-session-state-file}}`

## 概要

- cmoc workflow 上の session と realization run の fork, join, abandon を一意に定めるための JSON file である。
- 保存先は `{{repo-root}}/.cmoc/gu/ar/session/{{session-id}}.json` とする。

## スキーマ設計の基本原則

- 永続化する情報は必要最小限に留める。
- その場で確実に解決できる情報は state に持たせない。
- 1 session に未 join の realization run は高々 1 つとする。

## スキーマ定義

```json
{
  "session": {
    "state": "active | joined | abandoned | error",
    "session_home_branch": "...",
    "session_start_commit": "...",
    "last_joined_realization_apply_oracle_snapshot_commit": "... | null"
  },
  "realization_run": {
    "state": "ready | running | paused | completed | error",
    "kind": "apply | refactor | null",
    "branch": "... | null",
    "oracle_snapshot_commit": "... | null"
  }
}
```

## フィールドの説明

### `session.state`

- 現在の session の状態である。
- session 新規作成直後の初期値は `active` とする。
- `cmoc session` 系サブコマンドによって遷移する。

### `session.session_home_branch`

- session の fork 元 branch であり join 先でもある。
- `cmoc session fork` が、その時点で checkout している `{{local-branch}}` 名で初期化する。

### `session.session_start_commit`

- session の fork 元 commit である。

### `session.last_joined_realization_apply_oracle_snapshot_commit`

- その session で最後に join した apply run の `{{realization-oracle-snapshot-commit}}` である。
- session 新規作成直後の初期値は `null` とする。
- `cmoc realization apply join` が merge に成功した場合だけ更新する。
- `cmoc realization refactor join` は更新しない。

### `realization_run.state`

- 未 join の realization run の状態である。
- session 新規作成直後の初期値は `ready` とする。
- `paused` は、ユーザー中断された refactor run だけに使用する。

### `realization_run.kind`

- active な realization run の workload を表す。
- apply run は `apply`、refactor run は `refactor` とする。
- `realization_run.state` が `ready` の場合は `null` とする。

### `realization_run.branch`

- realization の修正内容を積み上げる run branch 名である。
- `realization_run.state` が `ready` の場合は `null` とする。

### `realization_run.oracle_snapshot_commit`

- run 開始時点の `{{cmoc-session-branch}}` HEAD である。
- apply run では注入差分の終点にも使用する。
- refactor run では差分情報として agent に渡さず、join 時の想定外差分検査にだけ使用する。
- `realization_run.state` が `ready` の場合は `null` とする。

## 状態遷移

- `ready` から apply または refactor の fork を開始すると `running` になる。
- apply fork が正常終了すると `completed` になる。
- refactor state が空になると `completed` になる。
- refactor fork がユーザー中断されると `paused` になる。
- run が続行不能なエラーで停止すると `error` になる。
- 対応する join または abandon が正常終了すると `ready` になり、`kind`, `branch`, `oracle_snapshot_commit` を `null` に初期化する。
