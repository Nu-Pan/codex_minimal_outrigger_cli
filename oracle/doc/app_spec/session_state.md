# `{{cmoc-session-state-file}}`

## 概要

`{{cmoc-session-state-file}}` は、cmoc workflow 上の session と編集 run の lifecycle を一意に定める JSON file である。編集 run は、明示的な join・abandon または同一 invocation 内の自動 join で終了する。保存先は `{{repo-root}}/.cmoc/gu/session/{{session-id}}.json` とする。

保存先の session ID は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/session_fork.md` の「`{{cmoc-session-branch}}` の命名規則」で定める、同じ session の ID とする。

## スキーマ設計の基本原則

永続化する情報は必要最小限にとどめ、その場で確実に解決できる情報は state に持たせない。

- 1 session に active な編集 run は高々 1 つとする。取り込み済みでも、結果保存を終えて `ready` に初期化するまでは active に含める。初期化後の cleanup と同時実行の境界は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「同時実行の境界」「merge と post-join」に従う。
- feedback の repository-local state はこの file に保存しない。保存対象と lifecycle は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「feedback の repository-local state」を正本とする。
- session または run の状態遷移だけを理由に feedback state を変更しない。

### join の復旧情報

join の段階と基準 HEAD の意味・記録時点は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「merge と post-join」を正本とする。再試行で元の workload の成果と準備変更を混同せず、取り込み前の rollback と取り込み後の後処理を選べるよう、次の情報を run identity と結び付けて durable に保持する。

- 統合前 run HEAD、各試行の基準 session HEAD、および準備完了 run HEAD。まだ成立していない基準や成果は作らない。
- 準備変更の帰属、検証・同期の完了結果、および session への取り込み成立を判別する情報。途中の commit 作成や取り込み直後に停止しても、履歴・tree と照合できるようにする。
- 成立した取り込み commit または no-op とその session commit、確定済みの後処理、未完了処理、および残存資源への対応。

既存の管理記録を活用し、Git から確実に復元できる情報を重複保存しない。保存形式、配置、field 名、および Git との分担は固定しないが、process のメモリや削除予定の資源だけに復旧を依存させない。`ready` 初期化後と部分 cleanup 後も、未完了の後処理を判別し、必要なら同じ run の `kind`、`branch`、`fork_commit` を復元できるようにする。

これらは join の復旧情報であり、`run.state` の値を増やさない。apply の資格判定は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_apply.md` の「join 後 hook」に従う。feedback の封印済み入力と検証記録の対応は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「report cut」「publication completion record」に従い、その正本を本 file へ複製しない。

## active session context と編集 run 開始・session 終了の共通事前条件

### active session context

active session context を必要とするサブコマンドは、次の条件をすべて検証する。

- 現在の branch が `{{cmoc-session-branch}}` である。
- 対応する `{{cmoc-session-state-file}}` が存在する。
- `session.state` が `active` である。

### 編集 run 開始・session 終了

編集 run を開始する workload 固有コマンド、`cmoc session join`、および `cmoc session abandon` は、さらに次の共通事前条件を満たす。

- `run.state` が `ready` である。
- `{{cmoc-session-branch}}` 側の worktree に git 未コミット差分がない。

`ready` 初期化後の実行中または停止した invocation の扱いは、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「同時実行の境界」「join の失敗と復旧」に従い、復旧情報も確認する。

## スキーマ定義

以下は構造の模式表記であり、`|` は値の候補を表す。

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

現在の session の状態を表す。新規作成直後の初期値は `active` とし、`cmoc session` 系サブコマンドによって遷移する。

### `session.session_home_branch`

session の fork 元 branch であり、join 先でもある。`cmoc session fork` が、その時点で checkout している `{{local-branch}}` 名で初期化する。

### `session.session_fork_commit`

- session の `{{cmoc-session-fork-commit}}` である。

### `session.last_joined_apply_fork_commit`

その session の apply の追従対象差分の始点として保持する commit であり、session 新規作成直後の初期値は `null` とする。更新条件と保存する commit は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_apply.md` の「join 後 hook」を正本とする。

## run field

`run.state` が `ready` の場合は、`run.kind`、`run.branch`、および `run.fork_commit` を `null` とする。

### `run.state`

編集 run の状態を表し、session 新規作成直後の初期値は `ready` とする。

| 値 | 状態 |
|---|---|
| `ready` | active な編集 run がない。 |
| `running` | workload の処理を実行している。 |
| `joinable` | 本命処理の成果が確定し、自動 join と後処理の実行中、または停止後の join・abandon を待っている。 |
| `error` | 本命処理、join、または後処理の失敗で停止している。取り込み前後の復旧方法は共通 lifecycle に従う。 |

### `run.kind`

active な編集 run の workload を表し、join と abandon はこの値から workload を解決する。`cmoc oracle edit` は run ではないため、この field の値にならない。

各 kind の自動 join と復旧の境界は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「対象」「join の失敗と復旧」に従う。

### `run.branch`

- active run の `{{cmoc-run-branch}}` 名である。session ID と run ID を含む命名は、`{{cmoc-root}}/oracle/doc/branch_model.md` の「`{{cmoc-run-branch}}`」に従う。

### `run.fork_commit`

active run の `{{cmoc-run-fork-commit}}` であり、apply の追従対象差分の終点と run join の成果差分検査の始点に使用する。同じ run の join 準備・再試行でも不変とする。

## 状態遷移

- workload が新しい編集 run を成立させると、`ready` から `running` へ遷移する。run 成立前の中断・失敗では新しい run state を作らない。
- 本命処理の成果確定、または正常なユーザー中断の停止・整合化を終えると `joinable` へ遷移し、同じ invocation 内で自動 join する。
- 正常な自動 join では、run 側の準備、session への取り込み、post-join、および workload 固有の確定処理が終わるまで `joinable` と active run 情報を保持する。feedback の自然完了では publication と入力・work artifact の cleanup も含む。`error` からの復旧では、過去の本命処理を正常終了扱いに戻さず、join 開始時の state を `joinable` へ読み替えない。
- 結果と report を保存した後に `ready` へ遷移し、`kind`、`branch`、`fork_commit` を `null` に初期化する。その後の隔離資源 cleanup と最終記録の順序は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「merge と post-join」に従う。明示 join と workload 固有 recovery もこの境界を使用する。
- 本命処理、join、または必須の後処理が失敗した場合は `error` へ遷移する。`ready` 初期化後の後処理失敗も、同文書の「join の失敗と復旧」に従い active run 情報と残存資源を扱う。重要事項確認の未完了には、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「確認結果と終了結果の分離」の例外を適用する。
- `cmoc run abandon` は、その cleanup を完了した後に `ready` へ遷移し、active run 情報を初期化する。
