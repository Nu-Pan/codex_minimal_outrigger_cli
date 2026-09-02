# `{{cmoc-session-state-file}}`

## 概要

- cmoc workflow 上の session と、明示的または同一 invocation 内の自動 join で終了する編集 run の lifecycle を一意に定める JSON file である。
- 保存先は `{{repo-root}}/.cmoc/gu/ar/session/{{session-id}}.json` とする。

## スキーマ設計の基本原則

- 永続化する情報は必要最小限に留める。
- その場で確実に解決できる情報は state に持たせない。
- 1 session に未 join の編集 run は高々 1 つとする。
- feedback の repository-local state はこの file に保存しない。保存対象と lifecycle は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「feedback の repository-local state」を正本とする。
- session または run の状態遷移は、同仕様が所有する feedback state を変更しない。

## active session context と編集 run 開始・session 終了の共通事前条件

active session context を必要とするサブコマンドは、次の条件をすべて検証する。

- 現在の branch が `{{cmoc-session-branch}}` である。
- 対応する `{{cmoc-session-state-file}}` が存在する。
- `session.state` が `active` である。

編集 run を開始する workload 固有コマンド、`cmoc session join`、および `cmoc session abandon` は、さらに次の共通事前条件を満たす。

- `run.state` が `ready` である。
- `{{cmoc-session-branch}}` 側の worktree に git 未コミット差分がない。

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
    "kind": "realization_apply | realization_refactor | feedback_report | null",
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

`run.state` が `ready` の場合は、`run.kind`、`run.branch`、および `run.fork_commit` を `null` とする。

### `run.state`

- `ready` は active な編集 run がない状態である。
- `running` は workload の処理が実行中である状態である。
- `joinable` は、join、abandon、または self-joining workload の finalization を待つ状態である。
- `error` は続行不能な失敗後である。join 済みの `feedback_report` では、`cmoc feedback report` による recovery を待つ。
- session 新規作成直後の初期値は `ready` とする。

### `run.kind`

- active な編集 run の workload を表す。
- join と abandon はこの値から workload を解決する。
- `cmoc oracle edit` は run ではなく、この field の値にならない。
- `feedback_report` は同一 invocation 内で自動 join する。自動 join 前に残った run は join または abandon、自動 join 後の失敗は feedback report recovery の対象となる。

### `run.branch`

- active run の `{{cmoc-run-branch}}` 名である。

### `run.fork_commit`

- active run の `{{cmoc-run-fork-commit}}` である。
- apply の差分終点と run join の差分検査にも使用する。

## 状態遷移

- workload 固有の fork または self-joining workload が新しい編集 run を開始すると、`ready` から `running` へ遷移する。
- 明示的な join を必要とする workload が正常終了すると `joinable` へ遷移する。
- `feedback_report` は wave loop の自然完了時に `joinable` へ遷移し、自動 join、join 後検査、report の確定、および cleanup の完了時に `ready` へ遷移する。自動 join 後の失敗時は `error`、同じ run の recovery 完了時は `ready` へ遷移する。
- 中断可能な workload が整合した処理単位でユーザー中断を完了すると `joinable` へ遷移する。
- workload が続行不能な失敗で停止すると `error` へ遷移する。
- `cmoc run join` または `cmoc run abandon` が正常終了すると `ready` へ遷移し、`kind`, `branch`, `fork_commit` を `null` に初期化する。
