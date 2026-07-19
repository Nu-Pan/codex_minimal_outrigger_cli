# 明示的な join を必要とする編集 run の共通仕様

## 対象

- 以下の workload 固有コマンドが編集 run を開始する。
    - `cmoc oracle edit fork`: `oracle_edit`
    - `cmoc realization apply fork`: `realization_apply`
    - `cmoc realization refactor fork`: `realization_refactor`
- 編集 run は `cmoc run join` または `cmoc run abandon` で終了する。
- 汎用の `cmoc run fork` は提供しない。
- `cmoc session join` と `cmoc session abandon` は外側の session lifecycle であり、この仕様の対象ではない。
- read-only の investigation/review、cmoc 自身による機械的更新、および session join の conflict 解消は、この編集 run lifecycle の対象ではない。

## 同時実行の境界

- 1 session が保持できる未 join の編集 run は高々 1 つとする。
- `{{cmoc-session-state-file}}` の `run` section で、active run の kind と状態を共有管理する。
- workload の異なる編集 run を同時に active にしてはいけない。
- `run.state` が `joinable` または `error` の間は、その run に対する `cmoc run join` と `cmoc run abandon` 以外の lifecycle 操作を受け付けない。

## fork の共通事前条件

workload 固有の fork は doctor preprocess の後に以下を検査し、満たさない場合はエラー終了する。

- 現在の branch が `{{cmoc-session-branch}}` である。
- 対応する `{{cmoc-session-state-file}}` が存在する。
- `session.state` が `active` である。
- `run.state` が `ready` である。
- `{{cmoc-session-branch}}` 側の worktree に git 未コミット差分がない。

## fork の共通開始処理

1. run 開始時点の `{{cmoc-session-branch}}` HEAD を `{{cmoc-run-fork-commit}}` とする。
2. workload に依存しない命名規則で `{{cmoc-run-branch}}` と `{{cmoc-run-worktree}}` を作成する。
3. session state の `run.state` を `running` にし、`kind`, `branch`, `fork_commit` を保存する。
4. workload の編集作業を `{{cmoc-run-worktree}}` 上で行う。

workload は、agent call の開始前に fork の共通開始処理を完了しなければならない。

## 編集責務と想定内差分

- agent が編集してよい file と cmoc が機械的に更新してよい file は、workload 固有仕様で定義する。
- agent が変更した file、cmoc が生成した `INDEX.md`、および workload 固有の state 更新は、整合した処理単位で `{{cmoc-run-branch}}` に commit する。
- workload が正常終了した場合は `run.state` を `joinable` にする。
- ユーザー中断を正常系として扱う workload は、実行中の処理単位を commit まで完了するか rollback してから `run.state` を `joinable` にする。
- 続行不能な失敗では、未確定の処理単位を commit または rollback により整合させ、`run.state` を `error` にする。

## `cmoc run join`

### active workload の解決

- join 対象の workload と branch は session state の `run.kind` と `run.branch` から解決する。
- workload を指定する位置引数や option は受け取らない。
- 位置引数なしとし、想定外差分への対応用 option `--force-resolve` を受け取る。

### 事前条件

以下の場合はエラー終了する。

- 現在の branch が `{{cmoc-session-branch}}` または active な `{{cmoc-run-branch}}` のいずれでもない。
- `session.state` が `active` ではない。
- `run.state` が `joinable` または `error` ではない。
- `run.kind`, `run.branch`, `run.fork_commit` のいずれかを state から特定できない。
- session worktree または run worktree に git 未コミット差分がある。

### 差分検査

- `{{cmoc-run-fork-commit}}` から run branch HEAD までの変更 path を検査する。
- run branch では、active workload の想定内差分だけを許可する。
- run 開始後の session branch では、oracle file、`memo`、および cmoc が生成する `INDEX.md` の変更を許可する。
- 通常モードでは想定外差分を report して join を中止する。
- `--force-resolve` は run branch 上の想定外差分だけを revert して続行する。session branch 上のユーザー成果物を revert してはいけない。

### merge と post-join

1. doctor preprocess を呼び出し、事前条件と差分を検査する。
2. `{{cmoc-session-branch}}` 上で `git merge --no-ff {{cmoc-run-branch}}` を実行し、その merge commit を `{{cmoc-run-join-commit}}` とする。
3. active workload が定める join 後 hook を実行する。
4. merge 後の session tree に対して refactor state を同期する。
5. join 結果と hook の結果を保存する。
6. `run.state` を `ready` にし、active run 情報を初期化する。

- `INDEX.md` の conflict は cmoc が生成し直すことで解決してよい。
- `INDEX.md` 以外が conflict した場合は merge を中止して開始前の clean な状態へ戻し、`run.state` を `error` にして conflict path を report する。conflict 解消のための agent call は行わない。
- refactor state の同期規則は `{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` を正本とする。

### 使用済み branch と worktree の cleanup

以下を全て確認できた場合だけ、`{{cmoc-run-branch}}` と `{{cmoc-run-worktree}}` を削除してよい。

- `run.state` が `ready` である。
- run branch HEAD が `{{cmoc-session-branch}}` から到達可能である。
- run の結果と report が保存済みである。

確認に失敗した場合は削除せず、warning として report する。

## `cmoc run abandon`

### active workload の解決と引数

- abandon 対象の workload と branch は session state から解決し、worktree は branch に含まれる run ID から決定する。
- 引数は受け取らない。

### 事前条件

以下の場合はエラー終了する。

- 現在の branch が `{{cmoc-session-branch}}` または active な `{{cmoc-run-branch}}` のいずれでもない。
- `session.state` が `active` ではない。
- `run.state` が `ready` である。
- active run の kind、branch、または branch に対応する worktree を特定できない。
- `{{cmoc-session-branch}}` 側の worktree に git 未コミット差分がある。

### 破棄と cleanup

- run worktree、その未コミット差分、run branch、および session state 上の active run 情報を破棄してよい。
- session branch、その commit、session home branch、保存済み report、session state file 自体を破棄してはいけない。
- `run.state` が `running` の場合は対応する process を停止し、停止を確認してから cleanup する。
- 現在の worktree が削除対象である場合は、削除対象外の worktree から cleanup する。
- run worktree と run branch は未 merge でも強制削除してよい。
- cleanup 後に `run.state` を `ready` にして active run 情報を初期化する。
- abandon は Codex CLI を呼び出さない機械的な cleanup とする。
- 対象資源が既に存在しない場合は warning として続行してよいが、session state を `ready` に戻せない場合はエラー終了する。

## report

- fork report の YAML Front Matter は、少なくとも `run_kind`, `session_branch`, `session_fork_commit`, `run_branch`, `run_fork_commit`, `run_worktree`, `state_before`, `state_after` を含む。
- fork, join, abandon の report から、run kind、`{{cmoc-run-branch}}`、`{{cmoc-run-worktree}}`、`{{cmoc-run-fork-commit}}`、実行前後の state、warning を判別可能にする。
- 同じ commit を workload 固有の別名でも重複掲載してはいけない。
- fork report は変更 path と完了理由を含め、保存先と workload 固有項目は workload 固有仕様で定める。
- join は `{{cmoc-run-join-commit}}`、post-join hook、refactor state 同期、および cleanup の結果を stdout から判別可能にする。
- abandon は破棄対象と cleanup の結果を stdout から判別可能にする。
