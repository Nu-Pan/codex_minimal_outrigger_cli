## `<cmoc-session-state-file>`

## 概要

- cmoc ワ―フロー上発生する fork, join の挙動を一意に定めるための情報をファイル永続化するための json ファイル
- 保存先は `<repo-root>/.cmoc/sessions/<session-id>.json`

## スキーマ定義

※ファイル永続化しなくてもその場その場で解決可能な情報は持たせない方針

```json
{
  "session": {
    "state": "active | joined | abandoned | error",
    "session_home_branch": "...",
    "session_start_commit": "...",
    "last_joined_apply_oracle_snapshot_commit": "...",

  },
  "apply": {
    "state": "ready | running | completed | error",
    "apply_branch": "cmoc/apply/.../...",
    "oracle_snapshot_commit": "..."
  }
}
```

## フィールドの説明

### `session.state`

- 現在のセッションのステート
- セッション新規作成直後の初期値は `active`
- `cmoc session` 系サブコマンドによって遷移する

### `session.session_home_branch`

- そのセッションの fork 元ブランチ名であり join 先でもある
- セッション新規作成直後の初期値は null
- `cmoc apply join` によって適切な値に更新される

### `session_start_commit`

- そのセッションの fork 元コミット

### `session.last_joined_apply_oracle_snapshot_commit`

- そのセッション上で最後に join した apply の `<oracle-snapshot-commit>`
- セッション新規作成直後の初期値は null
- `cmoc apply join` によって適切な値に更新される

### `apply.state`

- その apply 処理のステート
- セッション新規作成直後の初期値は `ready`

### `apply.apply_branch`

- その apply 処理で修正内容を積み上げる先となるブランチ名
- `apply.state` が `ready` に遷移した時に null で初期化される

### `apply.oracle_snapshot_commit`

- その apply で oracles ファイルの参照に使用するコミットのハッシュ
- `apply.state` が `ready` に遷移した時に null で初期化される
