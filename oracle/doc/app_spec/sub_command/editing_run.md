# 編集 run の共通仕様

## 対象

編集 run を開始する workload と終了方法を次に示す。

| workload 固有コマンド | `run.kind` | 正常時の終了方法 |
|---|---|---|
| `cmoc realization apply` | `realization_apply` | 追従作業の確定後、同一 invocation 内で自動 join |
| `cmoc realization refactor` | `realization_refactor` | 正常なユーザー中断の整合化後、同一 invocation 内で自動 join |
| `cmoc feedback report` | `feedback_report` | 同一 invocation 内の自動 join |

feedback report の自然完了と正常なユーザー中断は、いずれも自動 join の対象とする。publication の違いは、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「自動 join と join 後の確定」「ユーザー中断」に従う。

`cmoc run join` と `cmoc run abandon` は、異常時の取り込み再試行、確定済み部分成果の取り込み、または隔離資源の破棄のために残す。封印済み report cut を持つ自動 join 済み feedback run の復旧は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「join 後の publication failure」に従う。

汎用の `cmoc run fork` は提供しない。`cmoc session fork`、`cmoc session join`、および `cmoc session abandon` は維持し、外側の session lifecycle として扱う。

`cmoc oracle edit`、read-only の investigation、run を作らない cmoc 自身の機械的更新、および session join の conflict 解消は、この editing run lifecycle の対象ではない。

`cmoc feedback close` も編集 run を作らない。未終了の feedback run との排他は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_close.md` の「事前条件」に従う。

run の隔離資源と一般 lifecycle は、`{{cmoc-root}}/oracle/doc/app_spec/run_isolation.md` の「run 作業隔離規則」を正本とする。session と run の永続 state は、`{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の `{{cmoc-session-state-file}}` を正本とする。

## 公開コマンド名

apply と refactor の公開入口は、それぞれ `cmoc realization apply` と `cmoc realization refactor` とする。旧 `cmoc realization apply fork` と `cmoc realization refactor fork` は廃止し、alias としても受け付けない。help、自動補完、report、console、およびログの command 表記には公開コマンド名を使う。

run の分岐を表す fork、`run.fork_commit`、branch model の commit 名、および委譲先の builder・agent call 種別・設定 key は、公開 CLI の階層とは区別する。

## 同時実行の境界

1 session に active な編集 run は高々 1 つとする。active run の state field は、`{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「run field」を正本とする。

`run.state` が `running`、`joinable`、または `error` の間は、新しい editing run を開始しない。

`joinable` の run は、同じ invocation の自動 join と後処理でも active なままとする。自動・明示 join または workload 固有 recovery の開始から終了処理を終えるまでは、同じ session の別の run 開始・join・abandon・recovery、および session join・abandon を重ねて開始しない。cleanup に先立つ `ready` への遷移だけで、この実行中の処理との重複を許可しない。

停止して残った `joinable` または `error` の run では、その run に対する `cmoc run join` と `cmoc run abandon` を許可する。ただし、封印済み report cut を持つ自動 join 済み `feedback_report` では、workload 固有の `cmoc feedback report` recovery だけを許可する。

## 共通事前条件

editing run を開始する workload 固有コマンドは、doctor preprocess と workload が必要とする preflight の後に、`{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「active session context と編集 run 開始・session 終了の共通事前条件」を検査する。満たさない場合はエラー終了する。

workload 固有仕様が preflight 後の staging area も clean とする場合は、その条件を追加で検査する。未コミット差分を自動 stash、commit、revert、または破棄して事前条件を満たしてはならない。

## 共通開始処理

`{{run-id}}` は、隔離して作業する 1 つの編集 run を識別する。書式と採番は、`{{cmoc-root}}/oracle/doc/app_spec/id.md` の「ID のフォーマット」「プレフィックス」「採番と順序保証」に従う。同じ run の作業、workload が許可する再開、join、および abandon では、発行済みの run ID を保持する。

workload は、write 権限を持つ本命 agent call の開始前に、次の準備を完了しなければならない。

1. 新しい編集 run の run ID を発行する。
2. `{{cmoc-root}}/oracle/doc/app_spec/run_isolation.md` の「git branch」「git worktree」に従って、`{{cmoc-run-fork-commit}}`、`{{cmoc-run-branch}}`、および `{{cmoc-run-worktree}}` を確定し、作成した worktree の初回利用に必要な配置先の準備を完了する。
3. session state の `run.state` を `running` にし、`kind`、`branch`、`fork_commit` を保存する。

準備後、workload の編集作業を `{{cmoc-run-worktree}}` 上で行う。

## 編集責務と想定内差分

- agent が編集してよい file と cmoc が機械的に更新してよい file は、workload 固有仕様で定義する。
- agent が変更した file と workload 固有の tracked state 更新は、workload 固有仕様が定める整合した処理単位で `{{cmoc-run-branch}}` に commit する。
- run worktree に未確定差分を残したまま、次の処理単位、join、publication、または cleanup へ進んではならない。
- ユーザー中断を正常系として扱う workload は、個別仕様が定める commit または rollback を終えてから `run.state` を `joinable` にする。realization refactor の停止と確定の境界は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の「不可分な確定区間」「ユーザー中断」に従う。
- 続行不能な失敗では、未確定の処理単位を commit または rollback により整合させ、`run.state` を `error` にする。
- editing run と feedback data の境界は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「既存 workload との境界」と `{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「スキーマ設計の基本原則」を正本とする。

各 workload と join の call に提供する文書検索は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「文書検索 MCP」に従う。検索の管理物は、`{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の「identity と保存先」に従って成果差分から分離し、cleanup 時は同節の回収責務を適用する。

## 正常終了時の自動 join

run を作る workload は、個別仕様に従って本命処理の成果を確定した後、`run.state=joinable` にして、同じ invocation 内で自動 join する。正常系として定義されたユーザー中断では、子 process の停止と未確定処理単位の整合化を終えてから、この境界へ進む。本命処理の続行不能な失敗では自動 join しない。

自動 join は、後述する `cmoc run join` と同じ事前条件、差分検査、merge、競合解消、post-join、および cleanup 条件を適用する。通常モードの差分検査を用い、`--force-resolve` を暗黙に有効化しない。公開 CLI を再帰的に起動する必要はない。

`joinable` は確定済み成果を取り込める状態であり、invocation の正常終了ではない。自動 join と必要な後処理、結果保存、`ready` への初期化、および資源の cleanup の結果を確定してから、最外側の invocation を終了する。各処理の順序と失敗時の扱いは、本書の「merge と post-join」「join の失敗と復旧」「使用済み branch と worktree の cleanup」に従う。

realization refactor では、全対象の調査完了や改善の収束を join の条件にしない。確定済み成果物と refactor state を取り込み、次の新しい refactor run へ調査要求を引き継ぐ。実行途中の同じ run を再開する操作は設けない。

feedback の自然完了では、`incomplete` を含む publication と workload 固有 cleanup まで必要とする。その境界は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「publication」に従う。ユーザー中断では同文書の「publication を行わない feedback join」に従う。

run 成立前に終了した場合は、作成途中の資源を個別仕様に従って整合させ、存在しない run、`joinable` state、または join を作らない。中断後に許す処理と自動 join 自体の取消・失敗の区別は、`{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` の「共通動作」に従う。

## join と abandon の共通事前条件

自動 join、`cmoc run join`、および `cmoc run abandon` は、次の条件を共通して検査する。

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

自動 join でも、開始時点でこれらを再検査する。session 側の未コミット差分を自動 stash、commit、revert、または破棄して取り込みを強行してはならない。doctor preprocess が自身の仕様に従って作成する commit は、この禁止によって変更しない。

workload または join の停止失敗後は、書き込み得る process の停止と未確定処理単位の整合化を確認してから join する。realization refactor 固有の停止確認は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の「その他のエラー」に従う。

### 差分検査

- `{{cmoc-run-fork-commit}}` から run branch HEAD までの変更 path を検査する。
- run branch では、active workload の想定内差分だけを許可する。
- run 開始後の session branch の commit 済み変更は、file 種別で制限せず統合対象とする。realization file の変更があることだけを理由に join を拒否しない。
- 通常モードでは run branch の想定外差分を report して join を中止する。
- `--force-resolve` は run branch 上の想定外差分だけを revert して続行する。session branch 上のユーザー成果物を revert してはいけない。通常の競合解消にこの option を要求しない。

この検査は元の workload の成果物に対する検査であり、merge 開始後の競合解消に伴う付随編集へ元の変更 path 集合を強制するものではない。`feedback_report` の issue 単位差分検査は workload 固有仕様でも行う。join の差分検査は、その検査を省略または緩和するものではない。

### merge と post-join

1. doctor preprocess を呼び出し、事前条件と差分を検査し、対象 run と join 開始時点の state を確定する。自動 join でも、同期時点は `{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「editing run の join での同期時点」に従う。
2. run branch HEAD が session branch から到達可能で取り込む commit がなければ no-op join とする。それ以外は、merge 前の両 HEAD を確定し、`{{cmoc-session-branch}}` 上で `git merge --no-ff {{cmoc-run-branch}}` を実行する。競合時は本書の「競合解消」に従い、成立した merge commit を `{{cmoc-run-join-commit}}` とする。no-op join のために競合解消 agent を呼び出さない。
3. active workload が定める join 後 hook を実行する。
4. join 後の session tree に対して refactor state を同期する。同期で生じた tracked 差分は cmoc が commit する。
5. workload 固有の取り込み後処理を完了する。feedback の自然完了では join 後検査・publication・入力と work artifact の cleanup、中断後または明示 join では publication 未実施の記録を行う。
6. join、hook、refactor state 同期、および workload 固有処理の結果と、run identity を含む report を保存する。その後 `run.state=ready` とし、active run 情報を初期化する。
7. 本書の「使用済み branch と worktree の cleanup」に従い隔離資源を回収する。state 更新と cleanup の実際の結果を同じ invocation の primary report の機械生成版に反映する。その後、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「重要事項確認用 call」に従って確認結果と確認自身の記録を加え、primary report を保存してから terminal result を確定する。report に後続処理の成功を先取りして記載しない。

自然完了した feedback の publication artifact は immutable のまま保ち、最外側の実行結果は `{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「invocation report」に保存する。

apply の比較始点の更新条件は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_apply.md` の「join 後 hook」を正本とする。

refactor state の同期規則は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の「entry 集合の同期」を正本とする。

### 競合解消

判断基準、agent と cmoc の責務、受理、および報告は、`{{cmoc-root}}/oracle/doc/app_spec/merge_conflict_resolution.md` の「join の競合解消」に従う。

競合解消 agent は、merge target である session worktree で作業する。oracle を判断根拠として読み、realization file を統合に必要な範囲で編集する。oracle file は変更しない。run worktree の issue commit や成果物を書き換えず、進行中の merge 結果へ調整を加える。

call 固有の正確な prompt 文面、builder の引数、prompt part の選択、起動パラメータ、および選択理由は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/run/join/conflict_resolution.py` の `build_run_join_conflict_resolution_parameter` へ委譲する。すべての自動 join と明示 join で同じ call を使用する。feedback の封印後の入力・調整範囲は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「自動 join と join 後の確定」に従う。

### join の失敗と復旧

本節の失敗・取消による state と終了結果の扱いに対し、primary report の重要事項確認の未完了には、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「確認結果と終了結果の分離」の例外を適用する。

join の事前検査で停止した場合は、取り込みを開始せず、既存の差分と run を保持する。その invocation の対象となる停止済み run を特定できる場合は `run.state=error` とする。対象がない場合は存在しない run や state を作らず、別の実行中 invocation を妨げる state 変更も行わない。失敗・取消を本命処理の正常終了や正常なユーザー中断へ変換しない。

競合解消または merge commit 確定前の検証・管理処理が失敗・取消となった場合は、書き込み得る子 process の停止を確認してから、cmoc が merge を中止し、merge と競合解消が導入した作業ファイルの差分を除去する。付随する追加・変更・rename・削除と tracked な生成物も含め、session worktree と staging area を merge 開始前の clean な状態へ戻す。そのうえで `run.state=error` とし、run branch と run worktree を保持する。report とログ、および repository-local feedback state はこの作業差分の rollback 対象にせず、それぞれの保持契約に従う。report には未解消理由と、停止確認・復旧の結果を残す。停止を確認できない場合は rollback せず `error` とし、停止または復旧に失敗した場合も cleanup せず、残存資源・差分、および必要な次の操作を示す。

この rollback は、取り込み確定後の hook、refactor state 同期、report、publication、state 更新、または cleanup の失敗・取消には適用しない。確定した取り込み結果を巻き戻さず、`run.state=error` として、未完了処理、残存資源、確定済み成果、および診断を保持する。`ready` への初期化後に必須の後処理が失敗・取消となった場合も、保存した run identity に対応する active run 情報を戻し、削除済みの資源と残存資源を区別する。状態保存自体に失敗した場合は、成功と表示せず、確認できた state と復旧に必要な記録を残す。

手動復旧では、事前条件を満たせば `cmoc run join` で取り込みを再試行できる。取り込み済み commit を再 merge せず no-op join とし、確定した処理の結果を尊重して未完了の post-join を処理する。`cmoc run abandon` は残る隔離資源を破棄できるが、session branch に取り込み済みの commit は取り消さない。部分 cleanup 等により join に必要な資源が欠ける場合は、join を実行可能と案内せず、残存資源と可能な abandon・修復を示す。

封印済み report cut を持つ自動 join 済み feedback run は、この手動 join・abandon による復旧の対象外とし、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「join 後の publication failure」に従う。

### feedback run の取り込み後処理

自然完了時の自動 join は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「自動 join と join 後の確定」「publication」に従う。ユーザー中断後の自動 join と、停止 run の明示 join は、同文書の「publication を行わない feedback join」に従う。

### 使用済み branch と worktree の cleanup

次の条件をすべて確認できた場合だけ、`{{cmoc-run-branch}}` と `{{cmoc-run-worktree}}` を削除してよい。

- `run.state` が `ready` である。
- run branch HEAD が `{{cmoc-session-branch}}` から到達可能である。
- run の結果と report が保存済みである。

確認に失敗した場合は削除せず、warning として report する。cleanup の保留と、削除操作自体の失敗を区別し、後者は「join の失敗と復旧」に従う。`ready` であることだけで、資源削除まで完了したとは表示しない。

## `cmoc run abandon`

### active workload の解決と引数

- abandon 対象の workload と branch は session state から解決する。
- worktree は branch に含まれる session ID と run ID から、`{{cmoc-root}}/oracle/doc/branch_model.md` の「`{{cmoc-run-worktree}}`」に従って決定する。
- 引数は受け取らない。

### 事前条件

次の場合はエラー終了する。

- `run.state` が `ready` である。
- active run の kind、branch、または branch に対応する worktree を特定できない。
- `{{cmoc-session-branch}}` 側の worktree に git 未コミット差分がある。

### 破棄と cleanup

- run worktree、その未コミット差分、run branch、および session state 上の active run 情報を破棄してよい。
- session branch、その commit、session home branch、保存済み report、session state file 自体を破棄してはいけない。
- `run.state` が `running` の場合は対応する process を停止し、停止を確認してから cleanup する。停止失敗後の run も、`error` であることを理由に停止確認を省略しない。realization refactor 固有の停止確認は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の「その他のエラー」に従う。
- 現在の worktree が削除対象である場合は、削除対象外の worktree から cleanup する。
- run worktree と run branch は未 merge でも強制削除してよい。
- cleanup 後に `run.state` を `ready` にして active run 情報を初期化する。
- abandon は Codex CLI を呼び出さない機械的な cleanup とする。
- 対象資源がすでに存在しない場合は warning として続行してよい。session state を `ready` に戻せない場合はエラー終了する。

active workload が `feedback_report` の場合は、abandon する commit に依存する `fixed` result を publication 可能な state から除外する。raw observation と直前の current pointer を保持し、破棄済み修正を適用済みとして扱ってはならない。

封印済み report cut を持つ自動 join 済み `feedback_report` は、`cmoc run abandon` の対象にしない。publication または cleanup が未完了であれば、`cmoc feedback report` recovery を要求する。publication を行わない中断経路の失敗では、共通の「join の失敗と復旧」に従う。

## report と terminal result

実行 ID と primary report の共通表示契約は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「実行 ID の開始表示」「primary report」に従う。

### 共通内容

workload、明示 join、および abandon の report から、run kind、branch、worktree、fork commit、実行前後の state、warning、および cleanup 結果を判別可能にする。同じ commit を workload 固有の別名でも重複掲載してはいけない。

### workload の report

workload の report の実行情報には、少なくとも次の項目を含める。

- workload：`run_kind`
- branch：`session_branch`、`run_branch`
- fork commit：`session_fork_commit`、`run_fork_commit`
- worktree：`run_worktree`
- 実行前後の state：`state_before`、`state_after`

確定できない項目は `null` とし、存在しない branch、commit、worktree、または state を作ってはならない。変更 path と完了理由も含める。保存先と workload 固有項目は、workload 固有仕様で定める。

最外側の invocation の primary report は、上記に加えて、自動 join の事前検査・差分検査・merge または no-op join、`{{cmoc-run-join-commit}}`、post-join hook、refactor state 同期、workload 固有の確定処理、state 初期化、および cleanup の実際の結果を含む。no-op join の join commit は `null` とする。未実行と失敗を区別し、失敗段階、取り込み成立の有無、残存資源、必要な復旧、および次の操作を示す。

重要事項の確認入力は、これらを掲載した機械生成版とする。「merge と post-join」の state 初期化前の保存 report を最終版とみなしたり、内部 join で確認用 call を追加したりしない。失敗経路では、その時点で確定できた結果と未完了処理を含める。

自動 join は親の実行 ID と command を引き継ぐ内部処理とし、独立した primary report、terminal result、完了時のエディタ表示、または完了通知を追加しない。正常終了後の追加の手動 join は案内しない。

feedback の publication または cleanup の再開では、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「再開時の report と実行記録」に従って、引き継ぐ report と再開した実行の記録を対応付ける。

明示 join と自動 join を含む workload の report には、`{{cmoc-root}}/oracle/doc/app_spec/merge_conflict_resolution.md` の「受理と報告」が定める競合解消の判断・付随編集・検証・未解消理由を含める。競合解消を行わなかった場合は、その旨を示す。

### join と abandon の report

明示 join と abandon は、`natural_completion` と `error` のすべての終了経路で report を保存する。共通事前条件に違反して開始できなかった場合も対象とする。両 report の実行情報には、少なくとも次の項目を含める。

- 実行情報：command、生成日時、repo root、terminal result の共通分類、終了コード
- workload：`run_kind`
- branch：`session_branch`、`run_branch`
- fork commit と worktree：`run_fork_commit`、`run_worktree`
- 実行前後の state：`state_before`、`state_after`

join report の実行情報には `{{cmoc-run-join-commit}}` も含め、no-op join の場合は `null` とする。その他の確定できない項目も `null` とする。

| report | 保存先と役割 | 詳細結果に含める内容 |
|---|---|---|
| join report | `{{repo-root}}/.cmoc/gu/report/run/join/{{execution-id}}.md` に保存し、`cmoc run join` の primary report とする。 | 差分検査、想定外差分の扱い、merge と merge commit または no-op join、post-join hook、refactor state 同期、state 遷移、cleanup、エラー、および関連ログ。 |
| abandon report | `{{repo-root}}/.cmoc/gu/report/run/abandon/{{execution-id}}.md` に保存し、`cmoc run abandon` の primary report とする。 | 停止した process、破棄対象、state 遷移、cleanup、残存資源、エラー、および関連ログ。 |

join または abandon を開始できなかった場合は、確定できた active workload と state、事前条件違反、および未実行の処理を report する。実行していない merge、hook、破棄、または cleanup の結果を作ってはならない。

### terminal result

terminal result の出力先、共通 field、および表示順序は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「コンソール・ファイル、ログ出力規則」を正本とする。各 lifecycle 操作では、次の内容を示す。

- workload の terminal result では、自動 join を含む終了結果を示す。異常時は成立済み run の state と残存資源・差分に応じ、手動 join・abandon または workload 固有 recovery の実行可否を示す。run 成立前に終了した場合は、その段階を示し、存在しない run の操作を案内しない。
- 明示 join と自動 join を含む workload の terminal result では、`{{cmoc-run-join-commit}}`、post-join hook、refactor state 同期、および cleanup の結果をサブコマンド固有結果として判別可能にする。
- apply の比較始点を保持した join を、report や terminal result で「比較始点を更新した」と表示してはならない。
- abandon の terminal result では、破棄対象と cleanup の結果をサブコマンド固有結果として判別可能にする。
