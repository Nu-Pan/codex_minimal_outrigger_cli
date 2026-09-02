# 編集 run の共通仕様

## 対象

編集 run を開始する workload と終了方法を次に示す。

| workload 固有コマンド | `run.kind` | 正常時の終了方法 |
|---|---|---|
| `cmoc realization apply fork` | `realization_apply` | 後続の `cmoc run join` または `cmoc run abandon` |
| `cmoc realization refactor fork` | `realization_refactor` | 後続の `cmoc run join` または `cmoc run abandon` |
| `cmoc feedback report` | `feedback_report` | 同一 invocation 内の自動 join |

feedback report が自動 join 前のユーザー中断または続行不能な失敗で run を残した場合は、`cmoc run join` または `cmoc run abandon` で終了する。自動 join 後の publication または cleanup の失敗は、同じ run に対する `cmoc feedback report` recovery で終了する。

汎用の `cmoc run fork` は提供しない。`cmoc session join` と `cmoc session abandon` は外側の session lifecycle であり、この仕様の対象ではない。

`cmoc oracle edit`、read-only の investigation、run を作らない cmoc 自身の機械的更新、および session join の conflict 解消は、この editing run lifecycle の対象ではない。

run の隔離資源と一般 lifecycle は、`{{cmoc-root}}/oracle/doc/app_spec/run_isolation.md` の「run 作業隔離規則」を正本とする。session と run の永続 state は、`{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の `{{cmoc-session-state-file}}` を正本とする。

## 同時実行の境界

1 session に active な編集 run は高々 1 つとする。active run の state field は、`{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「run field」を正本とする。

`run.state` が `running`、`joinable`、または `error` の間は、新しい editing run を開始しない。`joinable` または `error` の run に許可する lifecycle 操作は、原則としてその run に対する `cmoc run join` と `cmoc run abandon` だけとする。自動 join 済みの `feedback_report` では、workload 固有の `cmoc feedback report` recovery だけを許可する。

## 共通事前条件

editing run を開始する workload 固有コマンドは、doctor preprocess と workload が必要とする preflight の後に、`{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「active session context と編集 run 開始・session 終了の共通事前条件」を検査する。満たさない場合はエラー終了する。

workload 固有仕様が preflight 後の staging area も clean とする場合は、その条件を追加で検査する。未コミット差分を自動 stash、commit、revert、または破棄して事前条件を満たしてはならない。

## 共通開始処理

1. run isolation 仕様に従って、`{{cmoc-run-fork-commit}}`、`{{cmoc-run-branch}}`、および `{{cmoc-run-worktree}}` を確定する。
2. session state の `run.state` を `running` にし、`kind`、`branch`、`fork_commit` を保存する。
3. workload の編集作業を `{{cmoc-run-worktree}}` 上で行う。

workload は、write 権限を持つ本命 agent call の開始前に共通開始処理を完了しなければならない。

## 編集責務と想定内差分

- agent が編集してよい file と cmoc が機械的に更新してよい file は、workload 固有仕様で定義する。
- agent が変更した file、cmoc が生成した `INDEX.md`、および workload 固有の tracked state 更新は、workload 固有仕様が定める整合した処理単位で `{{cmoc-run-branch}}` に commit する。
- run worktree に未確定差分を残したまま、次の処理単位、join、publication、または cleanup へ進んではならない。
- ユーザー中断を正常系として扱う workload は、実行中の処理単位を commit まで完了するか rollback してから `run.state` を `joinable` にする。
- 続行不能な失敗では、未確定の処理単位を commit または rollback により整合させ、`run.state` を `error` にする。
- editing run と feedback data の境界は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「既存 workload との境界」と `{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「スキーマ設計の基本原則」を正本とする。

## 明示的な join を待つ workload

`realization_apply` と `realization_refactor` が正常終了した場合は、`run.state` を `joinable` にする。利用者は後続の `cmoc run join` または `cmoc run abandon` で run を終了する。

## self-joining feedback run

`feedback_report` は、workload 固有仕様が定める intake wave loop と issue commit を完了した後に `run.state` を `joinable` にし、同じ invocation 内で自動 join を開始する。

自動 join は、後述する `cmoc run join` と同じ事前検証、差分検査、merge、および post-join を使用する。公開 CLI を再帰的に起動する必要はない。

merge または no-op join 後の tree 検査、publication、および workload 固有 cleanup が完了するまで、`run.state` を `ready` へ初期化せず、run branch と worktree を保持する。失敗時は `run.state=error` とし、join 済み run の recovery は workload 固有仕様に従う。

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

次の場合はエラー終了する。

- `run.state` が `joinable` または `error` ではない。
- `run.kind`、`run.branch`、`run.fork_commit` のいずれかを state から特定できない。
- session worktree または run worktree に git 未コミット差分がある。

### 差分検査

- `{{cmoc-run-fork-commit}}` から run branch HEAD までの変更 path を検査する。
- run branch では、active workload の想定内差分だけを許可する。
- run 開始後の session branch では、oracle file、`memo`、および cmoc が生成する `INDEX.md` の変更を許可する。
- 通常モードでは想定外差分を report して join を中止する。
- `--force-resolve` は run branch 上の想定外差分だけを revert して続行する。session branch 上のユーザー成果物を revert してはいけない。

`feedback_report` の issue 単位差分検査は workload 固有仕様でも行う。join の差分検査は、その検査を省略または緩和するものではない。

### merge と post-join

1. doctor preprocess を呼び出し、事前条件と差分を検査する。
2. run branch HEAD が session branch から到達可能で取り込む commit がなければ no-op join とする。それ以外は、`{{cmoc-session-branch}}` 上で `git merge --no-ff {{cmoc-run-branch}}` を実行し、その merge commit を `{{cmoc-run-join-commit}}` とする。
3. active workload が定める join 後 hook を実行する。
4. join 後の session tree に対して refactor state を同期する。
5. join 結果と hook の結果を保存する。
6. 明示的な join では、`run.state` を `ready` にし、active run 情報を初期化する。`feedback_report` の自動 join では、この更新を workload 固有の publication と cleanup が確定するまで遅延する。

`INDEX.md` の conflict は cmoc が生成し直すことで解決してよい。`INDEX.md` 以外が conflict した場合は merge を中止して開始前の clean な状態へ戻し、`run.state` を `error` にして conflict path を report する。conflict 解消のための agent call は行わない。

refactor state の同期規則は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` を正本とする。

### feedback run を明示 join した場合

ユーザー中断またはエラー後の `feedback_report` を `cmoc run join` した場合は、確定済み issue commit を session branch へ取り込む。正常 feedback publication、`incomplete` 診断 report、active generation の更新、および observation cleanup は行わない。

feedback work state には join 結果と publication 未実施を記録する。次回の `cmoc feedback report` は join 後の tree と pending observation を再検証する。self-joining 経路ですでに join 済みの run は再度 join せず、workload 固有 recovery だけで再開する。

### 使用済み branch と worktree の cleanup

次の条件をすべて確認できた場合だけ、`{{cmoc-run-branch}}` と `{{cmoc-run-worktree}}` を削除してよい。

- `run.state` が `ready` である。
- run branch HEAD が `{{cmoc-session-branch}}` から到達可能である。
- run の結果と report が保存済みである。

確認に失敗した場合は削除せず、warning として report する。

## `cmoc run abandon`

### active workload の解決と引数

- abandon 対象の workload と branch は session state から解決する。
- worktree は branch に含まれる run ID から決定する。
- 引数は受け取らない。

### 事前条件

次の場合はエラー終了する。

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
- 対象資源がすでに存在しない場合は warning として続行してよい。session state を `ready` に戻せない場合はエラー終了する。

active workload が `feedback_report` の場合は、abandon する commit に依存する `fixed` result を publication 可能な state から除外する。raw observation と直前の current pointer を保持し、破棄済み修正を適用済みとして扱ってはならない。

self-joining 経路の join がすでに成功した `feedback_report` は、run branch を削除しても session tree 上の変更を破棄できないため `cmoc run abandon` の対象にしない。封印済み report cut の publication または cleanup が未完了であれば、`cmoc feedback report` recovery を要求する。

## report と terminal result

- fork、self-joining workload、join、および abandon の report は Markdown と YAML Front Matter で構成する。
- join と abandon は、共通事前条件違反を含む `natural_completion` と `error` のすべての終了経路で report を保存する。
- fork report の YAML Front Matter は、少なくとも `run_kind`、`session_branch`、`session_fork_commit`、`run_branch`、`run_fork_commit`、`run_worktree`、`state_before`、`state_after` を含む。確定できない項目は `null` とし、存在しない branch、commit、worktree、または state を作ってはならない。
- self-joining workload の primary report は、上記の run identity と state に加えて、自動 join、workload 固有の確定処理、および cleanup の結果を含む。保存先と追加項目は workload 固有仕様で定める。
- join report と abandon report の YAML Front Matter は、少なくとも command、生成日時、repo root、terminal result の共通分類、終了コード、`run_kind`、`session_branch`、`run_branch`、`run_fork_commit`、`run_worktree`、`state_before`、`state_after` を含む。join report は、`{{cmoc-run-join-commit}}` または no-op join のため `null` であることも含む。その他の確定できない項目も `null` とする。
- report から、run kind、branch、worktree、fork commit、実行前後の state、warning、および cleanup 結果を判別可能にする。
- 同じ commit を workload 固有の別名でも重複掲載してはいけない。
- fork report は変更 path と完了理由を含め、保存先と workload 固有項目は workload 固有仕様で定める。
- join report は `{{repo-root}}/.cmoc/gu/ar/report/run/join/{{time-stamp}}.md` に保存し、`cmoc run join` の primary report とする。差分検査、想定外差分の扱い、merge と merge commit または no-op join、post-join hook、refactor state 同期、state 遷移、cleanup、エラー、および関連ログを要約する。
- abandon report は `{{repo-root}}/.cmoc/gu/ar/report/run/abandon/{{time-stamp}}.md` に保存し、`cmoc run abandon` の primary report とする。停止した process、破棄対象、state 遷移、cleanup、残存資源、エラー、および関連ログを要約する。
- join または abandon を開始できなかった場合は、確定できた active workload と state、事前条件違反、および未実行の処理を report する。実行していない merge、hook、破棄、または cleanup の結果を作ってはならない。
- fork の terminal result では、次に実行可能な lifecycle 操作として `cmoc run join` と `cmoc run abandon` を示す。
- join の terminal result では、`{{cmoc-run-join-commit}}`、post-join hook、refactor state 同期、および cleanup の結果をサブコマンド固有結果として判別可能にする。
- abandon の terminal result では、破棄対象と cleanup の結果をサブコマンド固有結果として判別可能にする。
- terminal result の出力先、共通 field、および表示順序は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` を正本とする。
