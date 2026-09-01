# 明示的な join を必要とする編集 run の共通仕様

## 対象

- 以下の workload 固有コマンドが編集 run を開始する。
    - `cmoc realization apply fork`: `realization_apply`
    - `cmoc realization refactor fork`: `realization_refactor`
- 編集 run は `cmoc run join` または `cmoc run abandon` で終了する。
- 汎用の `cmoc run fork` は提供しない。
- `cmoc session join` と `cmoc session abandon` は外側の session lifecycle であり、この仕様の対象ではない。
- `cmoc oracle edit`、read-only の investigation、cmoc 自身による機械的更新、および session join の conflict 解消は、この編集 run lifecycle の対象ではない。
- run の隔離資源と一般 lifecycle は、`{{cmoc-root}}/oracle/doc/app_spec/run_isolation.md` の「run 作業隔離規則」を正本とする。
- session と run の永続 state は、`{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の `{{cmoc-session-state-file}}` を正本とする。

## 同時実行の境界

未 join の編集 run 数は、`{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「スキーマ設計の基本原則」を正本とする。active run の state field は、同文書の「run field」を正本とする。

- `run.state` が `joinable` または `error` の間は、その run に対する `cmoc run join` と `cmoc run abandon` 以外の lifecycle 操作を受け付けない。

## fork の共通事前条件

workload 固有の fork は doctor preprocess の後に、`{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「active session context と編集 run fork・session 終了の共通事前条件」を検査する。満たさない場合はエラー終了する。

## fork の共通開始処理

1. run isolation 仕様に従って、`{{cmoc-run-fork-commit}}`、`{{cmoc-run-branch}}`、および `{{cmoc-run-worktree}}` を確定する。
2. session state の `run.state` を `running` にし、`kind`, `branch`, `fork_commit` を保存する。
3. workload の編集作業を `{{cmoc-run-worktree}}` 上で行う。

workload は、agent call の開始前に fork の共通開始処理を完了しなければならない。

## 編集責務と想定内差分

- agent が編集してよい file と cmoc が機械的に更新してよい file は、workload 固有仕様で定義する。
- agent が変更した file、cmoc が生成した `INDEX.md`、および workload 固有の state 更新は、整合した処理単位で `{{cmoc-run-branch}}` に commit する。
- workload が正常終了した場合は `run.state` を `joinable` にする。
- ユーザー中断を正常系として扱う workload は、実行中の処理単位を commit まで完了するか rollback してから `run.state` を `joinable` にする。
- 続行不能な失敗では、未確定の処理単位を commit または rollback により整合させ、`run.state` を `error` にする。
- 編集 run と feedback data の境界は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「既存 workload との境界」と `{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「スキーマ設計の基本原則」を正本とする。

## join と abandon の共通事前条件

`cmoc run join` と `cmoc run abandon` は、次の条件を共通して検査する。

- 現在の branch が `{{cmoc-session-branch}}` または active な `{{cmoc-run-branch}}` のいずれかである。
- 対応する `session.state` は、`{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の定義における `active` である。

## `cmoc run join`

### active workload の解決

- join 対象の workload と branch は session state の `run.kind` と `run.branch` から解決する。
- workload を指定する位置引数や option は受け取らない。
- 位置引数なしとし、想定外差分への対応用 option `--force-resolve` を受け取る。

### 事前条件

以下の場合はエラー終了する。

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

## report と terminal result

- fork、join、および abandon の report は Markdown と YAML Front Matter で構成する。
- join と abandon は、共通事前条件違反を含む `natural_completion` と `error` のすべての終了経路で report を保存する。
- fork report の YAML Front Matter は、少なくとも `run_kind`, `session_branch`, `session_fork_commit`, `run_branch`, `run_fork_commit`, `run_worktree`, `state_before`, `state_after` を含む。確定できない項目は `null` とし、存在しない branch、commit、worktree、または state を作ってはならない。
- join report と abandon report の YAML Front Matter は、少なくとも command、生成日時、repo root、terminal result の共通分類、終了コード、`run_kind`, `session_branch`, `run_branch`, `run_fork_commit`, `run_worktree`, `state_before`, `state_after` を含む。join report は、作成した `{{cmoc-run-join-commit}}` も含む。確定できない項目は `null` とする。
- fork, join, abandon の report から、run kind、`{{cmoc-run-branch}}`、`{{cmoc-run-worktree}}`、`{{cmoc-run-fork-commit}}`、実行前後の state、warning を判別可能にする。
- 同じ commit を workload 固有の別名でも重複掲載してはいけない。
- fork report は変更 path と完了理由を含め、保存先と workload 固有項目は workload 固有仕様で定める。
- join report は `{{repo-root}}/.cmoc/gu/ar/report/run/join/{{time-stamp}}.md` に保存し、`cmoc run join` の primary report とする。差分検査、想定外差分の扱い、merge と merge commit、post-join hook、refactor state 同期、state 遷移、cleanup、エラー、および関連ログを要約する。
- abandon report は `{{repo-root}}/.cmoc/gu/ar/report/run/abandon/{{time-stamp}}.md` に保存し、`cmoc run abandon` の primary report とする。停止した process、破棄対象、state 遷移、cleanup、残存資源、エラー、および関連ログを要約する。
- join または abandon の処理を開始できなかった場合は、確定できた active workload と state、事前条件違反、および未実行の処理を report する。実行していない merge、hook、破棄、または cleanup の結果を作ってはならない。
- fork の terminal result では、次に実行可能な lifecycle 操作として `cmoc run join` と `cmoc run abandon` を示す。
- join の terminal result では、`{{cmoc-run-join-commit}}`、post-join hook、refactor state 同期、および cleanup の結果をサブコマンド固有結果として判別可能にする。
- abandon の terminal result では、破棄対象と cleanup の結果をサブコマンド固有結果として判別可能にする。
- terminal result の出力先、共通 field、および表示順序は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` を正本とする。
