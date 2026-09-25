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

`run.state` が `running`、`joinable`、または `error` の間は、新しい editing run を開始しない。

`joinable` または `error` の run では、原則として、その run に対する `cmoc run join` と `cmoc run abandon` だけを lifecycle 操作として許可する。ただし、自動 join 済みの `feedback_report` では、workload 固有の `cmoc feedback report` recovery だけを許可する。

## 共通事前条件

editing run を開始する workload 固有コマンドは、doctor preprocess と workload が必要とする preflight の後に、`{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「active session context と編集 run 開始・session 終了の共通事前条件」を検査する。満たさない場合はエラー終了する。

workload 固有仕様が preflight 後の staging area も clean とする場合は、その条件を追加で検査する。未コミット差分を自動 stash、commit、revert、または破棄して事前条件を満たしてはならない。

## 共通開始処理

workload は、write 権限を持つ本命 agent call の開始前に、次の準備を完了しなければならない。

1. run isolation 仕様に従って、`{{cmoc-run-fork-commit}}`、`{{cmoc-run-branch}}`、および `{{cmoc-run-worktree}}` を確定する。
2. session state の `run.state` を `running` にし、`kind`、`branch`、`fork_commit` を保存する。

準備後、workload の編集作業を `{{cmoc-run-worktree}}` 上で行う。

## 編集責務と想定内差分

- agent が編集してよい file と cmoc が機械的に更新してよい file は、workload 固有仕様で定義する。
- agent が変更した file と workload 固有の tracked state 更新は、workload 固有仕様が定める整合した処理単位で `{{cmoc-run-branch}}` に commit する。
- run worktree に未確定差分を残したまま、次の処理単位、join、publication、または cleanup へ進んではならない。
- ユーザー中断を正常系として扱う workload は、実行中の処理単位を commit まで完了するか rollback してから `run.state` を `joinable` にする。
- 続行不能な失敗では、未確定の処理単位を commit または rollback により整合させ、`run.state` を `error` にする。
- editing run と feedback data の境界は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「既存 workload との境界」と `{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「スキーマ設計の基本原則」を正本とする。

各 workload と join の call に提供する文書検索は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「文書検索 MCP」に従う。検索の管理物は、`{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の「identity と保存先」に従って成果差分から分離し、cleanup 時は同節の回収責務を適用する。

## 明示的な join を待つ workload

`realization_apply` と `realization_refactor` が正常終了した場合は、`run.state` を `joinable` にする。利用者は後続の `cmoc run join` または `cmoc run abandon` で run を終了する。

## self-joining feedback run

`feedback_report` は、workload 固有仕様が定める intake wave loop と issue commit を完了した後に `run.state` を `joinable` にし、同じ invocation 内で自動 join を開始する。

自動 join は、後述する `cmoc run join` と同じ事前検証、差分検査、merge、および post-join を使用する。公開 CLI を再帰的に起動する必要はない。

merge または no-op join 後の tree 検査、publication、および workload 固有 cleanup が完了するまで、`run.state` を `ready` へ初期化せず、run branch と worktree を保持する。失敗時は `run.state=error` とし、join 済み run の recovery は workload 固有仕様に従う。

## join と abandon の共通事前条件

`cmoc run join` と `cmoc run abandon` は、次の条件を共通して検査する。

- 現在の branch が `{{cmoc-session-branch}}` または active な `{{cmoc-run-branch}}` のいずれかである。
- 対応する `session.state` は、`{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「`session.state`」が定める `active` である。

## `cmoc run join`

### active workload の解決

- join 対象の workload と branch は session state の `run.kind` と `run.branch` から解決する。
- 位置引数や workload を指定する option は受け取らず、想定外差分への対応用 option `--force-resolve` を受け取る。

### 事前条件

次の場合はエラー終了する。

- `run.state` が `joinable` または `error` ではない。
- `run.kind`、`run.branch`、`run.fork_commit` のいずれかを state から特定できない。
- session worktree または run worktree に git 未コミット差分がある。

### 差分検査

- `{{cmoc-run-fork-commit}}` から run branch HEAD までの変更 path を検査する。
- run branch では、active workload の想定内差分だけを許可する。
- run 開始後の session branch の commit 済み変更は、file 種別で制限せず統合対象とする。realization file の変更があることだけを理由に join を拒否しない。
- 通常モードでは run branch の想定外差分を report して join を中止する。
- `--force-resolve` は run branch 上の想定外差分だけを revert して続行する。session branch 上のユーザー成果物を revert してはいけない。通常の競合解消にこの option を要求しない。

この検査は元の workload の成果物に対する検査であり、merge 開始後の競合解消に伴う付随編集へ元の変更 path 集合を強制するものではない。`feedback_report` の issue 単位差分検査は workload 固有仕様でも行う。join の差分検査は、その検査を省略または緩和するものではない。

### merge と post-join

1. doctor preprocess を呼び出し、事前条件と差分を検査する。
2. run branch HEAD が session branch から到達可能で取り込む commit がなければ no-op join とする。それ以外は、merge 前の両 HEAD を確定し、`{{cmoc-session-branch}}` 上で `git merge --no-ff {{cmoc-run-branch}}` を実行する。競合時は本書の「競合解消」に従い、成立した merge commit を `{{cmoc-run-join-commit}}` とする。no-op join のために競合解消 agent を呼び出さない。
3. active workload が定める join 後 hook を実行する。
4. join 後の session tree に対して refactor state を同期する。同期で生じた tracked 差分は cmoc が commit する。
5. join 結果と hook の結果を保存する。
6. 明示的な join では、`run.state` を `ready` にし、active run 情報を初期化する。`feedback_report` の自動 join では、この更新を workload 固有の publication と cleanup が確定するまで遅延する。

apply の比較始点の更新条件は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_apply.md` の「join 後 hook」を正本とする。

refactor state の同期規則は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の「entry 集合の同期」を正本とする。

### 競合解消

判断基準、agent と cmoc の責務、受理、および報告は、`{{cmoc-root}}/oracle/doc/app_spec/merge_conflict_resolution.md` の「join の競合解消」に従う。

競合解消 agent は、merge target である session worktree で作業する。oracle を判断根拠として読み、realization file を統合に必要な範囲で編集する。oracle file は変更しない。run worktree の issue commit や成果物を書き換えず、進行中の merge 結果へ調整を加える。

call 固有の正確な prompt 文面、builder の引数、prompt part の選択、起動パラメータ、および選択理由は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/run/join/conflict_resolution.py` の `build_run_join_conflict_resolution_parameter` へ委譲する。feedback の自動 join でもこの call を用い、封印後の入力・調整範囲は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「自動 join と join 後の確定」に従う。

競合解消または merge commit 確定前の検証・管理処理に失敗した場合は、cmoc が merge を中止し、merge と競合解消が導入した作業ファイルの差分を除去する。付随する追加・変更・rename・削除と tracked な生成物も含め、session worktree と staging area を merge 開始前の clean な状態へ戻す。そのうえで `run.state=error` とし、run branch と run worktree を保持する。report とログ、および repository-local feedback state はこの作業差分の rollback 対象にせず、それぞれの保持契約に従う。report には未解消理由と復旧結果を残し、復旧自体に失敗した場合も cleanup せず、残存差分と必要な次の操作を示す。

この rollback は、取り込み確定後の hook、report、publication、または cleanup の失敗には適用しない。確定した取り込み結果と未完了処理を report し、資源の削除には本書の cleanup 条件を適用する。自動 join 済み feedback run の recovery は workload 固有契約に従う。

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

self-joining 経路の join がすでに成功した `feedback_report` は、`cmoc run abandon` の対象にしない。run branch を削除しても、session tree 上の変更は破棄できないためである。封印済み report cut の publication または cleanup が未完了であれば、`cmoc feedback report` recovery を要求する。

## report と terminal result

### 共通内容

fork、self-joining workload、join、および abandon の report は Markdown と YAML Front Matter で構成する。report から、run kind、branch、worktree、fork commit、実行前後の state、warning、および cleanup 結果を判別可能にする。同じ commit を workload 固有の別名でも重複掲載してはいけない。

### fork と self-joining workload の report

fork report の YAML Front Matter は、少なくとも次の項目を含む。

- workload：`run_kind`
- branch：`session_branch`、`run_branch`
- fork commit：`session_fork_commit`、`run_fork_commit`
- worktree：`run_worktree`
- 実行前後の state：`state_before`、`state_after`

確定できない項目は `null` とし、存在しない branch、commit、worktree、または state を作ってはならない。fork report には変更 path と完了理由も含める。保存先と workload 固有項目は、workload 固有仕様で定める。

self-joining workload の primary report は、上記の run identity と state に加えて、自動 join、workload 固有の確定処理、および cleanup の結果を含む。保存先と追加項目は、workload 固有仕様で定める。

join と self-joining workload の report には、`{{cmoc-root}}/oracle/doc/app_spec/merge_conflict_resolution.md` の「受理と報告」が定める競合解消の判断・付随編集・検証・未解消理由を含める。競合解消を行わなかった場合は、その旨を示す。

### join と abandon の report

join と abandon は、`natural_completion` と `error` のすべての終了経路で report を保存する。共通事前条件に違反して開始できなかった場合も対象とする。両 report の YAML Front Matter は、少なくとも次の項目を含む。

- 実行情報：command、生成日時、repo root、terminal result の共通分類、終了コード
- workload：`run_kind`
- branch：`session_branch`、`run_branch`
- fork commit と worktree：`run_fork_commit`、`run_worktree`
- 実行前後の state：`state_before`、`state_after`

join report の YAML Front Matter には `{{cmoc-run-join-commit}}` も含め、no-op join の場合は `null` とする。その他の確定できない項目も `null` とする。

| report | 保存先と役割 | 本文で要約する内容 |
|---|---|---|
| join report | `{{repo-root}}/.cmoc/gu/report/run/join/{{time-stamp}}.md` に保存し、`cmoc run join` の primary report とする。 | 差分検査、想定外差分の扱い、merge と merge commit または no-op join、post-join hook、refactor state 同期、state 遷移、cleanup、エラー、および関連ログ。 |
| abandon report | `{{repo-root}}/.cmoc/gu/report/run/abandon/{{time-stamp}}.md` に保存し、`cmoc run abandon` の primary report とする。 | 停止した process、破棄対象、state 遷移、cleanup、残存資源、エラー、および関連ログ。 |

join または abandon を開始できなかった場合は、確定できた active workload と state、事前条件違反、および未実行の処理を report する。実行していない merge、hook、破棄、または cleanup の結果を作ってはならない。

### terminal result

terminal result の出力先、共通 field、および表示順序は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「コンソール・ファイル、ログ出力規則」を正本とする。各 lifecycle 操作では、次の内容を示す。

- fork の terminal result では、次に実行可能な lifecycle 操作として `cmoc run join` と `cmoc run abandon` を示す。
- join の terminal result では、`{{cmoc-run-join-commit}}`、post-join hook、refactor state 同期、および cleanup の結果をサブコマンド固有結果として判別可能にする。
- apply の比較始点を保持した join を、report や terminal result で「比較始点を更新した」と表示してはならない。
- abandon の terminal result では、破棄対象と cleanup の結果をサブコマンド固有結果として判別可能にする。
