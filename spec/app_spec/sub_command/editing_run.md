# 編集 run の共通仕様

## 対象

編集 run を開始する workload と終了方法を次に示す。

| workload 固有コマンド | `run.kind` | 正常時の終了方法 |
|---|---|---|
| `cmoc realization apply` | `realization_apply` | 追従作業の確定後、同一 invocation 内で自動 join |
| `cmoc realization refactor` | `realization_refactor` | 正常なユーザー中断の整合化後、同一 invocation 内で自動 join |
| `cmoc feedback report` | `feedback_report` | 同一 invocation 内の自動 join |

feedback report の自然完了と正常なユーザー中断は、いずれも自動 join の対象とする。publication の違いは、`{{cmoc-root}}/spec/app_spec/sub_command/feedback_report.md` の「自動 join と join 後の確定」「ユーザー中断」に従う。

`cmoc run join` と `cmoc run abandon` は、異常時の取り込み再試行、確定済み部分成果の取り込み、または隔離資源の破棄のために残す。封印済み report cut を持つ自動 join 済み feedback run の復旧は、`{{cmoc-root}}/spec/app_spec/sub_command/feedback_report.md` の「join 後の publication failure」に従う。

汎用の `cmoc run fork` は提供しない。`cmoc session fork`、`cmoc session join`、および `cmoc session abandon` は維持し、外側の session lifecycle として扱う。

`cmoc oracle edit`、read-only の investigation、run を作らない cmoc 自身の機械的更新、および session join の conflict 解消は、この editing run lifecycle の対象ではない。

`cmoc feedback close` も編集 run を作らない。未終了の feedback run との排他は、`{{cmoc-root}}/spec/app_spec/sub_command/feedback_close.md` の「事前条件」に従う。

run の隔離資源と一般 lifecycle は、`{{cmoc-root}}/spec/app_spec/run_isolation.md` の「run 作業隔離規則」を正本とする。session と run の永続 state は、`{{cmoc-root}}/spec/app_spec/session_state.md` の `{{cmoc-session-state-file}}` を正本とする。

## 公開コマンド名

apply と refactor の公開入口は、それぞれ `cmoc realization apply` と `cmoc realization refactor` とする。旧 `cmoc realization apply fork` と `cmoc realization refactor fork` は廃止し、alias としても受け付けない。help、自動補完、report、console、およびログの command 表記には公開コマンド名を使う。

run の分岐を表す fork、`run.fork_commit`、branch model の commit 名、および委譲先の builder・agent call 種別・設定 key は、公開 CLI の階層とは区別する。

## 同時実行の境界

1 session に active な編集 run は高々 1 つとする。active run の state field は、`{{cmoc-root}}/spec/app_spec/session_state.md` の「run field」を正本とする。

`run.state` が `running`、`joinable`、または `error` の間は、新しい editing run を開始しない。

`joinable` の run は、同じ invocation の自動 join と後処理でも active なままとする。自動・明示 join または workload 固有 recovery の開始から終了処理を終えるまでは、同じ session の別の run 開始・join・abandon・recovery、および session join・abandon を重ねて開始しない。cleanup に先立つ `ready` への遷移だけで、この実行中の処理との重複を許可しない。`ready` 初期化後に停止した invocation の未完了処理は、本書の「join の失敗と復旧」に従って識別し、新しい run の開始や session の終了に先立って扱いを確定する。

停止して残った `joinable` または `error` の run では、その run に対する `cmoc run join` と `cmoc run abandon` を許可する。ただし、封印済み report cut を持つ自動 join 済み `feedback_report` では、workload 固有の `cmoc feedback report` recovery だけを許可する。

## 共通事前条件

editing run を開始する workload 固有コマンドは、doctor preprocess と workload が必要とする preflight の後に、`{{cmoc-root}}/spec/app_spec/session_state.md` の「active session context と編集 run 開始・session 終了の共通事前条件」を検査する。満たさない場合はエラー終了する。

workload 固有仕様が preflight 後の staging area も clean とする場合は、その条件を追加で検査する。未コミット差分を自動 stash、commit、revert、または破棄して事前条件を満たしてはならない。

## 共通開始処理

`{{run-id}}` は、隔離して作業する 1 つの編集 run を識別する。書式と採番は、`{{cmoc-root}}/spec/app_spec/id.md` の「ID のフォーマット」「プレフィックス」「採番と順序保証」に従う。同じ run の作業、workload が許可する再開、join、および abandon では、発行済みの run ID を保持する。

workload は、write 権限を持つ本命 agent call の開始前に、次の準備を完了しなければならない。

1. 新しい編集 run の run ID を発行する。
2. `{{cmoc-root}}/spec/app_spec/run_isolation.md` の「git branch」「git worktree」に従って、`{{cmoc-run-fork-commit}}`、`{{cmoc-run-branch}}`、および `{{cmoc-run-worktree}}` を確定し、作成した worktree の初回利用に必要な配置先の準備を完了する。
3. session state の `run.state` を `running` にし、`kind`、`branch`、`fork_commit` を保存する。

準備後、workload の編集作業を `{{cmoc-run-worktree}}` 上で行う。

## 編集責務と想定内差分

- agent が編集してよい file と cmoc が機械的に更新してよい file は、workload 固有仕様で定義する。
- agent が変更した file と workload 固有の tracked state 更新は、workload 固有仕様が定める整合した処理単位で `{{cmoc-run-branch}}` に commit する。
- run worktree に未確定差分を残したまま、次の処理単位、join、publication、または cleanup へ進んではならない。
- ユーザー中断を正常系として扱う workload は、個別仕様が定める commit または rollback を終えてから `run.state` を `joinable` にする。realization refactor の停止と確定の境界は、`{{cmoc-root}}/spec/app_spec/sub_command/realization_refactor.md` の「不可分な確定区間」「ユーザー中断」に従う。
- 続行不能な失敗では、未確定の処理単位を commit または rollback により整合させ、`run.state` を `error` にする。
- editing run と feedback data の境界は、`{{cmoc-root}}/spec/app_spec/feedback.md` の「既存 workload との境界」と `{{cmoc-root}}/spec/app_spec/session_state.md` の「スキーマ設計の基本原則」を正本とする。

各 workload と join の call に提供する文書検索は、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「文書検索 MCP」に従う。検索の管理物は、`{{cmoc-root}}/spec/app_spec/document_search.md` の「identity と保存先」に従って成果差分から分離し、cleanup 時は同節の回収責務を適用する。

## 正常終了時の自動 join

run を作る workload は、個別仕様に従って本命処理の成果を確定した後、`run.state=joinable` にして、同じ invocation 内で自動 join する。正常系として定義されたユーザー中断では、子 process の停止と未確定処理単位の整合化を終えてから、この境界へ進む。本命処理の続行不能な失敗では自動 join しない。

自動 join は、後述する `cmoc run join` と同じ事前条件、差分検査、merge、競合解消、post-join、および cleanup 条件を適用する。通常モードの差分検査を用い、`--force-resolve` を暗黙に有効化しない。公開 CLI を再帰的に起動する必要はない。

`joinable` は確定済み成果を取り込める状態であり、invocation の正常終了ではない。自動 join と必要な後処理、結果保存、`ready` への初期化、および資源の cleanup の結果を確定してから、最外側の invocation を終了する。各処理の順序と失敗時の扱いは、本書の「merge と post-join」「join の失敗と復旧」「使用済み branch と worktree の cleanup」に従う。

realization refactor では、全対象の調査完了や改善の収束を join の条件にしない。確定済み成果物と、次の新しい refactor run の選択順序に使う refactor state を取り込む。実行途中の同じ run を再開する操作は設けない。

feedback の自然完了では、`incomplete` を含む publication と workload 固有 cleanup まで必要とする。その境界は、`{{cmoc-root}}/spec/app_spec/sub_command/feedback_report.md` の「publication」に従う。ユーザー中断では同文書の「publication を行わない feedback join」に従う。

run 成立前に終了した場合は、作成途中の資源を個別仕様に従って整合させ、存在しない run、`joinable` state、または join を作らない。中断後に許す処理と自動 join 自体の取消・失敗の区別は、`{{cmoc-root}}/spec/app_spec/subcommand_interruption.md` の「共通動作」に従う。

## join と abandon の共通事前条件

自動 join、`cmoc run join`、および `cmoc run abandon` は、次の条件を共通して検査する。

- 現在の branch が `{{cmoc-session-branch}}` または active な `{{cmoc-run-branch}}` のいずれかである。
- 対応する `session.state` は、`{{cmoc-root}}/spec/app_spec/session_state.md` の「`session.state`」が定める `active` である。

## `cmoc run join`

### active workload の解決

- join 対象の workload と branch は session state の `run.kind` と `run.branch` から解決する。
- 位置引数や workload を指定する option は受け取らず、想定外差分への対応用 option `--force-resolve` を受け取る。

### 事前条件

取り込み前の join では、次の場合はエラー終了する。

- `run.state` が `joinable` または `error` ではない。
- `run.kind`、`run.branch`、`run.fork_commit` のいずれかを state から特定できない。
- session worktree または run worktree に git 未コミット差分がある。

自動 join でも、開始時点でこれらを再検査する。前回の join が停止している場合は、先に本書の「join の失敗と復旧」に従って対象 run と取り込み成立の有無を確認する。未取り込みなら残存処理と差分を整合させてから、clean な状態を要求する検査へ進む。取り込み済みなら、同節の後処理の復旧条件を用いる。session 側の既存の未コミット差分を自動 stash、commit、revert、または破棄して取り込みを強行してはならない。doctor preprocess が自身の仕様に従って作成する commit は、この禁止によって変更しない。

workload または join の停止失敗後は、書き込み得る process の停止と未確定処理単位の整合化を確認してから join する。realization refactor 固有の停止確認は、`{{cmoc-root}}/spec/app_spec/sub_command/realization_refactor.md` の「その他のエラー」に従う。

### 差分検査

- 検査範囲は `run.fork_commit`（`{{cmoc-run-fork-commit}}`）から、本書の「merge と post-join」が定める統合前 run HEAD までとする。active workload の想定内差分だけを許可する。
- 通常モードでは、この範囲の想定外差分を report して join を中止する。
- `--force-resolve` は、この範囲の想定外差分だけを run 上で revert して続行する。元の commit は書き換えず、取消を後続の commit として確定し、session の変更を run に統合する前に処理を終える。通常の競合解消にこの option を要求しない。
- run 開始後の session branch の commit 済み変更は、oracle・realization を含め file 種別で制限せず統合対象とする。session 由来の変更を workload の想定外差分として拒否・revert してはいけない。

この検査は元の workload の成果物に対する検査である。再試行でも保存した統合前 run HEAD を用い、session の統合、競合解消、または refactor state 同期を含む準備後の HEAD を終点にしない。取り込み済みの復旧では、この検査を再適用しない。

競合解消の付随編集は、`{{cmoc-root}}/spec/app_spec/merge_conflict_resolution.md` の「受理と報告」に従って検査し、元の workload の変更 path 集合へ限定しない。cmoc の管理更新は各管理物の規則で検証する。`feedback_report` の issue 単位差分検査など、本命作業の受理条件をこれらの処理で省略・緩和しない。

### merge と post-join

自動 join と明示 join は、全 workload で「run 側での準備 → session への取り込み → 後処理」の順とする。統合と同期の変更を run 側の履歴に残し、準備済みの tree を session へ取り込む。同期 commit を取り込み後の session branch に直接追加する処理は行わない。merge 後の到達可能履歴から同期 commit を除くことは目的にしない。

この lifecycle では次の基準を区別する。

| 名称 | 意味 |
|---|---|
| 統合前 run HEAD | join 準備による変更を加える前の、元の workload の確定済み成果。差分検査の終点と、取り込み前の rollback の基準。 |
| 基準 session HEAD | その回の準備で run へ統合する、commit 済みの session HEAD。最終取り込みの前提。 |
| 準備完了 run HEAD | session の統合、競合解消、必要な検証、および refactor state 同期を完了して確定した run HEAD。session へ取り込む成果。 |

基準と処理結果の永続化は、`{{cmoc-root}}/spec/app_spec/session_state.md` の「join の復旧情報」に従う。`run.fork_commit` はこれらの HEAD で置き換えない。

#### run 側での準備

1. 既存の復旧情報から前回の取り込み成立の有無を確認し、本書の「join の失敗と復旧」に従って停止確認と残存処理の整合化を行う。取り込み済みなら、doctor preprocess に後述の復旧時の扱いを適用し、準備を繰り返さず後処理へ進む。
2. 未取り込みの run では、元の確定済み成果を統合前 run HEAD として記録する。join 前の doctor preprocess が run に管理更新を加える場合も、その更新より先に記録し、管理更新を元の workload の成果へ混入させない。再試行では前回の統合前 run HEAD を保持する。
3. doctor preprocess と事前条件を検査し、対象 run と今回の join 開始時の state を確定する。基準 session HEAD を記録してから「差分検査」を行い、`--force-resolve` があれば取消の確定まで終える。doctor の遅延対象と復旧時の扱いは、`{{cmoc-root}}/spec/app_spec/doctor_preprocess.md` の「editing run の join での同期時点」に従う。
4. run worktree で、基準 session HEAD を run branch へ merge する。競合は本書の「競合解消」に従って解消し、必要な検証を行う。元の workload の commit は書き換えず、統合の変更を後続の履歴として扱う。元の run 成果が session から到達可能な場合も、その session tree に対して同期要否を確認できるよう run を整えるが、記録だけの merge commit は作らない。
5. session の統合と競合解消の完了後、cmoc が run tree の refactor state を同期し、tracked 差分があれば run branch に commit する。両 branch の値の統合と同期内容は、`{{cmoc-root}}/spec/app_spec/sub_command/realization_refactor.md` の「join での統合」「entry 集合の同期」に従う。準備完了の tree に必要な検証を完了し、先行する検証記録を使う場合もその tree に適用できることを確認する。run worktree と staging area を clean にし、準備完了 run HEAD と検証・同期の結果を、session への取り込みを始める前に記録する。

#### session への取り込み

記録した準備完了 run HEAD と clean な run worktree を保ち、session HEAD が基準 session HEAD と一致し、session worktree と staging area が clean である場合だけ取り込む。確認から取り込み成立までこの条件を保つ。session が途中で更新されていれば、その回は停止し、最新の session の取り込み直しは再試行で行う。進んだ session にそのまま merge して新たな競合解消を行わない。

- 準備完了 run HEAD に未取り込み commit がある場合は、`{{cmoc-session-branch}}` 上で `git merge --no-ff {{cmoc-run-branch}}` を実行し、準備完了時と同じ tree を持つ取り込み commit を確定する。これを `{{cmoc-run-join-commit}}` とする。
- 同期差分も未取り込み commit もなければ no-op join とする。基準 session HEAD と準備完了 run HEAD の対応と、no-op の成立を記録する。この記録だけを目的とする空 commit や競合解消 call は作らない。

merge commit の確定、または no-op 成立の記録を、取り込み前後の失敗境界とする。取り込み commit とその tree、または no-op の session commit を、準備完了成果と対応付ける。初回の到達可能性だけで準備を省略することと、取り込み済みの復旧とを混同しない。

#### 後処理

1. active workload が定める join 後 hook を実行する。apply の比較始点は、`{{cmoc-root}}/spec/app_spec/sub_command/realization_apply.md` の「join 後 hook」に従う。
2. workload 固有の取り込み後処理を完了する。feedback の自然完了では join 後検査・publication・入力と work artifact の cleanup、中断後または明示 join では publication 未実施の記録を行う。
3. 準備、取り込み、hook、および workload 固有処理の結果と、run identity を含む report を保存する。その後 `run.state=ready` とし、active run 情報を初期化する。
4. 本書の「使用済み branch と worktree の cleanup」に従い隔離資源を回収する。state 更新と cleanup の実際の結果を同じ invocation の primary report の機械生成版に反映する。その後、`{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「重要事項確認用 call」に従って確認結果と確認自身の記録を加え、primary report を保存してから terminal result を確定する。report に後続処理の成功を先取りして記載しない。

refactor state の同期保証は、取り込み成立時の tree に対するものとする。その後の人間編集への追従は次の通常同期で行い、この後処理や取り込み済みの復旧では再同期しない。

自然完了した feedback の publication artifact は immutable のまま保ち、最外側の実行結果は `{{cmoc-root}}/spec/app_spec/sub_command/feedback_report.md` の「invocation report」に保存する。

### 競合解消

判断基準、agent と cmoc の責務、受理、および報告は、`{{cmoc-root}}/spec/app_spec/merge_conflict_resolution.md` の「join の競合解消」に従う。

競合解消 agent は、session を source、run を target とする準備中の run worktree で作業する。oracle を判断根拠として読み、realization file を統合に必要な範囲で編集する。oracle file は変更しない。元の workload の commit や feedback の issue commit を書き換えず、進行中の merge 結果へ調整を加える。refactor state の競合解消と同期は cmoc が担当する。

call 固有の正確な prompt 文面、builder の引数、prompt part の選択、起動パラメータ、および選択理由は、`{{cmoc-root}}/reference/src/oracle/acp_builder/run/join/conflict_resolution.py` の `build_run_join_conflict_resolution_request` へ委譲する。すべての自動 join と明示 join で同じ call を使用する。feedback の封印後の入力・調整範囲は、`{{cmoc-root}}/spec/app_spec/sub_command/feedback_report.md` の「自動 join と join 後の確定」に従う。

### join の失敗と復旧

本節の失敗・取消による state と終了結果の扱いに対し、primary report の重要事項確認の未完了には、`{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「確認結果と終了結果の分離」の例外を適用する。

join の事前検査で停止した場合は、取り込みを開始せず、既存の差分と run を保持する。その invocation の対象となる停止済み run を特定できる場合は `run.state=error` とする。対象がない場合は存在しない run や state を作らず、別の実行中 invocation を妨げる state 変更も行わない。失敗・取消を本命処理の正常終了や正常なユーザー中断へ変換しない。

取り込み前の失敗・取消では、書き込み得る process の停止を確認してから、cmoc が進行中の merge を中止し、join 準備が導入した変更だけを取り消す。`--force-resolve` の取消、session の統合、競合解消の付随編集、および refactor state 同期を含め、準備中に作成済みの commit と未確定差分を区別して復旧し、run branch・worktree・staging area を統合前 run HEAD の clean な状態へ戻す。元の workload の確定済み成果と session 側の既存変更は保持する。session への取り込み操作が残した未確定差分があれば、その操作が導入したものだけを取り消し、途中で追加された session commit や人間の未コミット差分を戻さない。

取り込み前の復旧後は `run.state=error` とし、run branch と run worktree を保持する。report とログ、および repository-local feedback state はこの作業差分の rollback 対象にせず、それぞれの保持契約に従う。停止または変更の帰属を確認できない場合は rollback しない。復旧を完了できない場合も cleanup せず `error` とし、残存資源・差分と必要な次の操作を示す。

取り込み成立後は、この rollback を適用しない。確定した session commit を保持し、`run.state=error` として、未完了の hook、report、publication、state 更新、または cleanup と診断を残す。状態保存自体に失敗した場合は、成功と表示せず、確認できた state と復旧に必要な記録を残す。

復旧は、準備途中、準備完了後で未取り込み、取り込み済みで後処理未完了を、保存記録と Git から区別する。取り込み直後で結果の保存前に停止した場合も、準備完了 run HEAD と session の履歴・tree の対応から成立を確認する。到達可能性だけを過去の join 成功の証拠にせず、一意に確認できなければ rollback・再 merge・cleanup を行わない。

この確認は、`ready` 初期化後の失敗・取消・停止で active run 情報が消えている場合にも行う。復旧情報から未完了の必須処理を特定したら、保存した run identity に対応する active run 情報を復元して `error` とする。結果を保存して cleanup の保留を確定した正常終了と、処理途中の停止を区別する。後処理だけの復旧では、必要な記録を検証して削除済み資源と残存資源を区別し、削除済みの run 資源の再作成や取り込み前の事前条件の再成立を要求しない。session 状態に関する workload 固有の再開条件は維持する。

未取り込みなら、上記の復旧と事前条件を満たした後、元の成果に対して差分検査を行い、最新の session HEAD を基準に準備し直す。取り込み済みなら、初回 no-op として処理し直さず、再同期・再 merge を行わずに未完了の後処理だけを進める。元の取り込み commit または成立済み no-op の記録を保持する。apply の hook は、`{{cmoc-root}}/spec/app_spec/sub_command/realization_apply.md` の「join 後 hook」が定める今回の開始時 state による資格判定を維持する。

`cmoc run abandon` は残る隔離資源を破棄できるが、session branch に取り込み済みの commit は取り消さない。部分 cleanup 等により必要な資源が欠ける場合は、可能な後処理の再開と資源を要する取り込み再試行を区別し、実行不能な join を案内しない。

封印済み report cut を持つ自動 join 済み feedback run は、この手動 join・abandon による復旧の対象外とし、`{{cmoc-root}}/spec/app_spec/sub_command/feedback_report.md` の「join 後の publication failure」に従う。

### feedback run の取り込み後処理

自然完了時の自動 join は、`{{cmoc-root}}/spec/app_spec/sub_command/feedback_report.md` の「自動 join と join 後の確定」「publication」に従う。ユーザー中断後の自動 join と、停止 run の明示 join は、同文書の「publication を行わない feedback join」に従う。

### 使用済み branch と worktree の cleanup

次の条件をすべて確認できた場合だけ、`{{cmoc-run-branch}}` と `{{cmoc-run-worktree}}` を削除してよい。

- `run.state` が `ready` である。
- 取り込み成立を確認でき、記録された準備完了 run HEAD が `{{cmoc-session-branch}}` から到達可能である。残存する run branch・worktree はその成果を指し、新しい未確定差分を持たない。
- 必要な後処理の結果と report が保存済みであり、隔離資源を削除しても取り込みと未完了処理を判別できる復旧情報が保持される。

確認に失敗した場合は削除せず、warning として report する。cleanup の保留と、削除操作自体の失敗を区別し、後者は「join の失敗と復旧」に従う。`ready` であることだけで、資源削除まで完了したとは表示しない。

## `cmoc run abandon`

### active workload の解決と引数

- abandon 対象の workload と branch は session state から解決する。
- worktree は branch に含まれる session ID と run ID から、`{{cmoc-root}}/spec/branch_model.md` の「`{{cmoc-run-worktree}}`」に従って決定する。
- 引数は受け取らない。

### 事前条件

次の場合はエラー終了する。

- `run.state` が `ready` である。
- active run の kind、branch、または branch に対応する worktree を特定できない。
- `{{cmoc-session-branch}}` 側の worktree に git 未コミット差分がある。

### 破棄と cleanup

- run worktree、その未コミット差分、run branch、および session state 上の active run 情報を破棄してよい。
- session branch、その commit、session home branch、保存済み report、session state file 自体を破棄してはいけない。
- `run.state` が `running` の場合は対応する process を停止し、停止を確認してから cleanup する。停止失敗後の run も、`error` であることを理由に停止確認を省略しない。realization refactor 固有の停止確認は、`{{cmoc-root}}/spec/app_spec/sub_command/realization_refactor.md` の「その他のエラー」に従う。
- 現在の worktree が削除対象である場合は、削除対象外の worktree から cleanup する。
- run worktree と run branch は未 merge でも強制削除してよい。
- cleanup 後に `run.state` を `ready` にして active run 情報を初期化する。
- abandon は Codex CLI を呼び出さない機械的な cleanup とする。
- 対象資源がすでに存在しない場合は warning として続行してよい。session state を `ready` に戻せない場合はエラー終了する。

active workload が `feedback_report` の場合は、abandon する commit に依存する `fixed` result を publication 可能な state から除外する。raw observation と直前の current pointer を保持し、破棄済み修正を適用済みとして扱ってはならない。

封印済み report cut を持つ自動 join 済み `feedback_report` は、`cmoc run abandon` の対象にしない。publication または cleanup が未完了であれば、`cmoc feedback report` recovery を要求する。publication を行わない中断経路の失敗では、共通の「join の失敗と復旧」に従う。

## report と terminal result

実行 ID と primary report の共通表示契約は、`{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「実行 ID の開始表示」「primary report」に従う。

### 共通内容

workload、明示 join、および abandon の report から、run kind、branch、worktree、fork commit、実行前後の state、warning、および cleanup 結果を判別可能にする。同じ commit を workload 固有の別名でも重複掲載してはいけない。

### join の共通記録

自動 join を含む workload と明示 join の primary report は、次を判別可能にする。

- 事前条件の検査結果、統合前 run HEAD、基準 session HEAD、準備完了 run HEAD、および差分検査の範囲と結果。
- 想定外差分と `--force-resolve` の扱い、session → run の統合、競合解消、必要な検証、run 側の refactor state 同期と commit の結果。
- session への取り込み成立の有無、`{{cmoc-run-join-commit}}` または no-op、および成立時の session commit と tree。no-op の join commit は `null` とする。
- 初回の準備・取り込みと、取り込み済みの復旧の区別。復旧で merge を省略しても、元の取り込み commit を `null` や新しい no-op に置き換えない。
- post-join hook、workload 固有の確定処理、state 初期化、および cleanup の実際の結果。
- 失敗段階、process の停止確認、rollback、残存資源・差分、未完了処理、および次の操作。

元の workload の成果と準備による変更を区別する。確定できない値は `null` とし、未実行・失敗・完了・以前の完了結果の再利用を区別する。複数の役割を持つ同じ commit は一度掲載して役割を対応付ける。記録の具体的な field 名や保存形式は固定しない。

競合解消の判断・付随編集・検証・未解消理由は、`{{cmoc-root}}/spec/app_spec/merge_conflict_resolution.md` の「受理と報告」に従う。競合解消を行わなかった場合は、その旨を示す。

### workload の report

workload の report の実行情報には、少なくとも次の項目を含める。

- workload：`run_kind`
- branch：`session_branch`、`run_branch`
- fork commit：`session_fork_commit`、`run_fork_commit`
- worktree：`run_worktree`
- 実行前後の state：`state_before`、`state_after`

確定できない項目は `null` とし、存在しない branch、commit、worktree、または state を作ってはならない。変更 path と完了理由も含める。保存先と workload 固有項目は、workload 固有仕様で定める。

最外側の invocation の primary report は、上記に加えて本書の「join の共通記録」を含む。

重要事項の確認入力は、これらを掲載した機械生成版とする。「merge と post-join」の state 初期化前の保存 report を最終版とみなしたり、内部 join で確認用 call を追加したりしない。失敗経路では、その時点で確定できた結果と未完了処理を含める。

自動 join は親の実行 ID と command を引き継ぐ内部処理とし、独立した primary report、terminal result、完了時のエディタ表示、または完了通知を追加しない。正常終了後の追加の手動 join は案内しない。

feedback の publication または cleanup の再開では、`{{cmoc-root}}/spec/app_spec/sub_command/feedback_report.md` の「再開時の report と実行記録」に従って、引き継ぐ report と再開した実行の記録を対応付ける。

### join と abandon の report

明示 join と abandon は、`natural_completion` と `error` のすべての終了経路で report を保存する。共通事前条件に違反して開始できなかった場合も対象とする。両 report の実行情報には、少なくとも次の項目を含める。

- 実行情報：command、生成日時、repo root、terminal result の共通分類、終了コード
- workload：`run_kind`
- branch：`session_branch`、`run_branch`
- fork commit と worktree：`run_fork_commit`、`run_worktree`
- 実行前後の state：`state_before`、`state_after`

join report には「join の共通記録」を含める。確定できない項目は `null` とする。

| report | 保存先と役割 | 詳細結果に含める内容 |
|---|---|---|
| join report | `{{repo-root}}/.cmoc/gu/report/run/join/{{execution-id}}.md` に保存し、`cmoc run join` の primary report とする。 | join の共通記録、事前条件違反、エラー、および関連ログ。 |
| abandon report | `{{repo-root}}/.cmoc/gu/report/run/abandon/{{execution-id}}.md` に保存し、`cmoc run abandon` の primary report とする。 | 停止した process、破棄対象、state 遷移、cleanup、残存資源、エラー、および関連ログ。 |

join または abandon を開始できなかった場合は、確定できた active workload と state、事前条件違反、および未実行の処理を report する。実行していない merge、hook、破棄、または cleanup の結果を作ってはならない。

### terminal result

terminal result の出力先、共通 field、および表示順序は、`{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「コンソール・ファイル、ログ出力規則」を正本とする。各 lifecycle 操作では、次の内容を示す。

- workload の terminal result では、自動 join を含む終了結果を示す。異常時は成立済み run の state と残存資源・差分に応じ、手動 join・abandon または workload 固有 recovery の実行可否を示す。run 成立前に終了した場合は、その段階を示し、存在しない run の操作を案内しない。
- 明示 join と自動 join を含む workload の terminal result では、run 側の準備と refactor state 同期、session への取り込みと `{{cmoc-run-join-commit}}`、post-join hook、および cleanup の結果をサブコマンド固有結果として判別可能にする。取り込み済みの復旧では、今回再開した処理を示す。
- apply の比較始点を保持した join を、report や terminal result で「比較始点を更新した」と表示してはならない。
- abandon の terminal result では、破棄対象と cleanup の結果をサブコマンド固有結果として判別可能にする。
