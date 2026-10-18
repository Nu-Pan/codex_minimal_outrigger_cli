# `cmoc feedback report`

`cmoc feedback report` は、同一 invocation 内で feedback remediation run を作成する。安全な realization file の修正を issue 単位で commit した後、session branch へ自動 join する。自然完了では検証を経て最新状態を publication し、正常なユーザー中断では確定済み commit の取り込みだけを行う。通常の確認対象には、その時点の active の案件を提示する。

関連する仕様の正本を次に示す。

- raw observation：`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「feedback observation の収集」
- 結果分類：`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「用語と結果分類」
- repository-local state：`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「feedback の repository-local state」

## CLI 契約

- 位置引数を受け取らない。
- サブコマンド固有 option を受け取らない。
- 正常経路では、利用者に別の fork、join、または remediation 操作を要求しない。
- session branch 上の既存の git 未コミット差分を、自動 stash、commit、revert、または破棄してはならない。ただし、doctor preprocess がその仕様に従って作成する commit は許容する。

## 事前条件と run の開始または再開

共通の開始処理は、次の順序で行う。

1. doctor preprocess を実行する。同期に先立つ join 復旧情報の確認には、`{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「editing run の join での同期時点」を適用する。
2. `{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「active session context」の条件を確認する。
3. session worktree と staging area が clean であることを確認する。
4. repository-level feedback writer 排他を取得する。
5. current pointer、pending recovery、および既存 feedback state の schema、path、hash、branch reference の整合性を検証する。

未完了の close がある場合は、新しい run を作らず、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_close.md` の「保存失敗と recovery」に従う再実行を案内してエラー終了する。close の固定入力を report で書き換えない。

その後は、既存 run の状態に応じて分岐する。自動 join 済み feedback run の publication または publication 後 cleanup を再開できる場合は、本書の「join 後の publication failure」に従って recovery を完了する。この経路では、新しい run を開始しない。

recovery 対象がない場合は、session state の `run.state` が `ready` であることを確認し、次の順序で新しい run を開始する。

1. `{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「共通開始処理」に従い、`run.kind=feedback_report` の編集 run を開始する。`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「feedback run」に従って feedback run ID を発行し、その編集 run と対応付ける。
2. collector の最初の high-watermark を確定し、最初の intake wave を固定する。

recovery 対象ではない active run が残っている場合、または事前条件に違反した場合は、新しい run を作らない。既存の worktree、staging area、raw observation、および current pointer を変更しない。

run の branch、commit、および worktree の定義は、`{{cmoc-root}}/oracle/doc/branch_model.md` の「cmoc の branch model」を正本とする。run の一般 lifecycle と隔離境界は、`{{cmoc-root}}/oracle/doc/app_spec/run_isolation.md` の「run 作業隔離規則」を正本とする。

## feedback remediation run

run branch 上の想定内差分を次に示す。

- issue remediation agent が変更した realization file
- cmoc が同期した tracked refactor state
- workload 固有仕様が issue 処理単位で必要とするその他の tracked な機械生成物

repository-local feedback state、subcommand log、および Codex call log は `{{repo-root}}/.cmoc/gu` 側に保存し、run branch の commit に含めない。issue commit と正式な feedback checkpoint は、commit ID と hash で相互に結び付ける。

自然完了・正常中断時の自動 join、異常時の `cmoc run join` と `cmoc run abandon`、想定内差分、および recovery の共通境界は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「編集 run の共通仕様」を正本とする。

## issue 処理 call の observation 報告

normalization と issue remediation では、調査対象の再報告が追加 evidence として同じ issue の再確認を誘発する経路を止めるため、feedback reporter の提供を無効にする。対象は、本書の「agent observation と normalization」「issue remediation agent call」で委譲する `build_feedback_*_issue_parameter` 系とし、現在は `build_feedback_normalize_issue_parameter` と `build_feedback_remediate_issue_parameter` の 2 種類である。判定根拠の変化に伴う再確認 call も対象に含む。

対象 call では、同じ issue の再報告と、作業中に見つかった別の問題の追加報告をともに行えなくてよい。MCP の非提供と報告規定の非注入、および同じ論理 call の補正・retry・再開での維持は、`{{cmoc-root}}/oracle/doc/app_spec/codex_common_rule.md` の「feedback reporter と collector context」に従う。これは feedback report invocation 全体の無効化ではなく、別の call kind である回復確認 probe、join の競合解消、および他の workload の報告契約を変更しない。primary report の重要事項確認用 call の提供判断も、同節が参照する共通仕様に従う。

入力 observation の同一性判断と、入力 issue の確認・修正・検証および `human_required` を含む結果は、既存の Structured Output で返す。追加報告ができないことを結果分類の理由にしてはならない。別 issue の追加報告用 field、代替 tool、または log からの自動 issue 化など、非提供を補う収集経路は設けない。

他の作業から受理された observation の取り込みと、実際の判定根拠の変化に伴う再確認は、本書の「intake wave loop」に従って継続する。

## intake の validation と normalization

### validation

各 raw observation の schema、path、および canonical hash は、対応する intake wave または wave 終了時の追加入力記録と一致しなければならない。同じ observation ID で hash が異なる場合は corruption とする。

1 件でも validation を通過できない input がある場合は、publication を行わない。invalid input を処理済みとして削除せず、path と理由を invocation report と subcommand log に示す。

### machine observation

machine observation は、detector rule が定める canonical key、recurrence window、および distinct dimension だけで集約する。自由文や AI 判断を identity または threshold 判定に使用してはならない。

threshold 未満の aggregate は、人間向け issue や remediation call の対象にしない。threshold を満たした aggregate は 1 件の issue candidate とし、同じ canonical key の active issue があれば機械的に統合する。

既存の active issue は、追加 observation や新たな threshold 到達の有無によらず再確認する。終了した案件への再統合は行わず、案件の対応は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「案件 ID と状態遷移」に従う。

### agent observation と normalization

agent observation は、観測日時と observation ID による安定した順序で処理する。比較対象には、run 開始時の active issue と、同じ run で先に形成した issue candidate を含める。history の案件は比較対象にしない。

agent が入力した deduplication hint は、候補検索にだけ使用する。issue identity の確定根拠にはしない。機械的な完全一致で同一と判断できる場合は、normalization agent を呼び出さない。

normalization agent は、入力した observation が既存 candidate と同じ issue か、新しい issue かだけを返す。normalization は issue identity を確定する責務であり、issue remediation call には数えない。

正確な prompt part、文面、workload 固有の起動パラメータ、およびその選択理由は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.py` の `build_feedback_normalize_issue_parameter` へ委譲する。Structured Output schema は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.json` の root schema（JSON Pointer `#`）へ委譲する。

cmoc が normalization agent に渡す比較用の入力は、次の 2 つとする。

- 検証済みの構造化 observation
- 機械的に絞り込んだ既存 issue candidate

入力だけでは同一性の判断に必要な情報が得られない場合、normalization agent は処理経路や原因を含む関連情報を、`{{work-root}}` 内の oracle file、realization file などから読み取り専用で参照してよい。参照先の選択には、`{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の「検索と routing」を適用する。候補外の issue は探索しない。

normalization agent は独立した原因診断や、summary、impact、現在性、actionability、remediation result、human action、relation の生成は行わない。問題の現在状態の確認と修正は、本書の「issue remediation agent call」で定める call が担う。

同一性の判断では、観測当時の evidence と現在のファイル状態を区別する。ファイルの変化や問題の解消だけを理由に、別 issue と判断してはならない。

既存 issue を選ぶ output の issue ID は、入力候補の issue ID と一致しなければならない。schema と宣言済みの決定論的事後条件に適合する output を受理できなければ、invocation error とする。

判定の記録は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「checkpoint」に従う。

normalization と remediation の agent 入出力は、引き続き issue ID を使用する。案件 ID との対応付け・採番・手動クローズは cmoc が管理し、agent の結果分類や Structured Output へ追加しない。

## 1 issue identity の処理単位

### call 回数と順序

正規化済み issue identity の初回処理と、同じ run 内で判定根拠の変化に伴って行う各再確認を、それぞれ独立した論理 issue remediation agent call とする。

- issue ID は runtime input とし、`agent_call_kind` に含めない。
- Structured Output correction、retry、および quota または一時障害の回復待ち後の再開は、同じ論理 agent call として数える。回復確認 probe は issue remediation call に数えない。
- issue remediation call は、同じ run branch の最新状態を順に参照できるよう逐次実行する。

各 wave 内の issue identity は、安定した issue ID 順で処理する。

### issue remediation agent call

issue remediation agent call は、1 issue について次の処理を同じ call 内で行う。

1. 現在状態の確認
2. realization file だけで可能な修正
3. 修正後の検証

再確認 call には、現在の入力に加えて、先行判定とその判定根拠、再確認を必要とした変化、および関連する再確認履歴を渡す。

収束不能を理由に `inconclusive` と判定した issue について、cmoc は、その診断根拠が変わらないまま同じ状態を往復する再試行を続けてはならない。

正確な prompt part、文面、workload 固有の起動パラメータ、およびその選択理由は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/remediate_issue.py` の `build_feedback_remediate_issue_parameter` へ委譲する。Structured Output schema は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/remediate_issue.json` の root schema（JSON Pointer `#`）へ委譲する。

call の境界を次に示す。

- cwd は `{{cmoc-run-worktree}}` とする。
- oracle file は読めるが変更できない。
- agent が変更する作業成果物は realization file だけとする。
- 一時作業領域の利用は、`{{cmoc-root}}/oracle/doc/app_spec/codex_common_rule.md` の「一時作業領域」に従う。
- agent に feedback state file、Git index、branch、commit、または worktree lifecycle を操作させない。
- candidate 外の issue を remediation 対象として探索させない。

issue remediation call の設定選択は、`{{cmoc-root}}/oracle/doc/app_spec/codex_model_provider.md` の「agent call ごとの直接設定」に従う。provider、model、および reasoning effort の既定値を含む正確な設定値は、`{{cmoc-root}}/oracle/src/oracle/other/cmoc_config.py` の `CmocConfigCodex.agent_calls["realization_edit"]` へ委譲する。設定値を prompt 文面へ注入してはならない。

### Structured Output と結果分類

agent は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「用語と結果分類」に従って issue remediation result を 1 つ返す。

`inconclusive` があっても、残りの issue は可能な限り処理する。

### net 差分と機械的受理条件

cmoc は、論理 agent call の開始時点から正式な終了時点までの realization file の net 差分を算出する。Structured Output correction 中の差分不変性は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「補正 turn の実行条件」を正本とする。

正式な output には、schema に加えて次の決定論的事後条件をすべて要求する。

- output の issue ID が入力 issue identity と一致する。
- schema の `changed_paths` に重複がなく、そこから得る path 集合が実際の realization file の変更 path 集合と一致する。
- path は、正規化済みの `{{work-root}}` 相対 path とする。変更の種類ごとの表現は次のとおりとする。
    - 追加と変更：終了時点の path
    - 削除：開始時点の path
    - rename：rename 前後の path
- `fixed` は 1 件以上の実際の realization 差分と、成功した修正後 verification を持つ。
- `already_resolved`、`not_actionable`、および `inconclusive` は実際の差分を持たない。
- `human_required` が差分を持つ場合、その差分は独立して安全であり、必要な verification が成功している。

処理単位の commit 受理条件として、`changed_paths` の照合とは別に、run worktree の全 net 差分を検査する。oracle file、禁止 path、または workload の想定外 path に変更があれば、その処理単位を確定してはならない。

差分検証の共通規則は、`{{cmoc-root}}/oracle/doc/app_spec/codex_common_rule.md` の「agent call の差分検証」を正本とする。

agent が返した `fixed` の自己申告だけを、意味的な正しさの証明として扱ってはならない。正式な結果とするには、次の両方を満たす必要がある。

- agent が必要な検証を実行し、結果を報告している。
- cmoc が、schema、決定論的事後条件、差分、および検証記録を照合できる。

### issue 単位の commit と rollback

受理済み結果ごとに、cmoc は次の処理を 1 つの整合した issue 単位として行う。

1. agent の realization 差分と verification result を検査する。
2. 必要な refactor state と tracked processing state を機械的に同期する。
3. 想定内差分と変更禁止対象を再検査し、run branch の 1 commit として確定する。
4. commit ID と正式な result を feedback checkpoint に durable 保存する。

実際の tracked 差分が空の場合は、空 commit を作らない。`already_resolved`、`not_actionable`、`inconclusive`、および差分のない `human_required` は、commit なしの正式な checkpoint としてよい。

`human_required` であっても、安全で独立して検証済みの部分修正は、同じ issue commit に残してよい。変更を安全に部分確定できない場合は、処理単位全体を agent call 開始時点へ rollback する。

commit が成功する前に `fixed` として publication、active state からの除外、または observation cleanup を行ってはならない。commit または rollback 後は、次の issue call を開始する前に run worktree と staging area が整合した clean 状態でなければならない。

refactor state または巡内の unresolved target 集合を feedback issue state として流用してはならない。refactor の継続反復や終了条件も feedback report には適用せず、本書の「intake wave loop」「ユーザー中断」に従う。

## intake wave loop

intake wave と high-watermark の state 契約は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「intake wave と high-watermark」、report cut の封印条件は同文書の「report cut」を正本とする。

最初の wave の候補には、raw observation が cleanup 済みのものを含め、全 active issue を使う。`inconclusive` の再確認を過去の raw observation や Markdown report の再読込へ依存させない。

各 wave の終了時は、次の順序で停止判定を行う。

1. wave に含まれる全 issue identity を終端結果まで処理する。
2. wave の remediation agent call について、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「call の終了」に従い、作成済み reporter context の受付停止と受付済み submission の保存完了を確定する。
3. collector が durable に受理済みの observation に対する high-watermark を atomic に確定する。
4. 前回境界より後、今回の high-watermark 以前にある observation を validation、normalization、および deduplication する。
5. 後続の修正、機械的同期、および追加 evidence による判定根拠の変化を、全結果分類について確認する。
6. 新しい未処理 issue identity または再確認が必要な判定があれば、次の immutable な intake wave を作成する。
7. `{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「処理モデル」が定める自然完了条件を満たした場合だけ、wave loop を自然完了する。

次の入力だけを理由に、新しい remediation call または wave を増やしてはならない。

- 既知 issue の完全な重複 observation
- 判定根拠に影響しない occurrence 集計の更新
- 判定根拠が変わっていない処理済み issue への理由のない再試行

新しい wave を要しない追加入力も、消費する場合はその入力・集計・採用結果への対応を report cut に固定する。入力の消費と cleanup は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「入力の消費と cleanup」に従う。

quiet period、directory の列挙タイミング、または一定時間 observation がなかったことを停止条件にしてはならない。

新しい異なる issue が継続的に発生する限り自然完了しない。issue 数、wave 数、または実行時間による任意の上限を設けない。ユーザー中断と続行不能な失敗だけを別の停止経路とする。

## 自動 join と join 後の確定

本節は自然完了の経路に適用する。wave loop が自然完了した場合は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「report cut」に従って report cut を封印し、`run.state=joinable` とする。その後、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「正常終了時の自動 join」に従う共通 join を行う。正常なユーザー中断では、本書の「publication を行わない feedback join」を適用する。

自動 join 前に、`fixed` としての publication または observation cleanup を行ってはならない。

### 封印後のマージ調整

競合解消には、`{{cmoc-root}}/oracle/doc/app_spec/merge_conflict_resolution.md` の「join の競合解消」を適用する。競合の発生そのものを publication failure にしてはならない。

競合解消 agent は、封印済みの採用結果を維持するために、session を統合中の run worktree の merge 結果を調整してよい。内容が封印時と異なっても、両側の変更意図と採用結果を維持できる調整を認める。影響を受ける判定を全結果分類から特定し、run 側の merge commit 前に必要な検証を行う。issue 処理をやり直すための新しい wave や、別の remediation・レビュー call は開始しない。

cmoc は、merge 対象 commit の参照に加えて、封印済み report cut の path を agent へ渡す。agent は、そこから採用結果、対応する checkpoint、および判定根拠を読み取り専用で参照し、調整と検証の結果を報告する。封印済み artifact や issue commit は書き換えず、受理した調整を cmoc が run の後続履歴に残す。封印時 run HEAD と準備完了 run HEAD の対応は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「report cut」「publication completion record」に従う。正確な入力と指示文は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/run/join/conflict_resolution.py` の `build_run_join_conflict_resolution_parameter` へ委譲する。

結果分類そのものの変更が必要な場合、または必要な検証で封印済み結果の維持を確認できない場合は、調整を確定せず、session への取り込みと publication を停止する。この停止を新しい issue result、`human_required`、または `incomplete` へ変換しない。run 側の統合・同期 commit がすでに作成されていても、session への取り込み前なら、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「join の失敗と復旧」に従って準備変更を取り消す。

cmoc は、共通 join の同期まで完了した run tree に対して、保存した検証記録が適用でき、採用する全結果の判定根拠を維持できることを確認してから session へ取り込む。必要な検証は run 側の準備で完了し、最終 session tree との対応の確認を取り込み後に行う。

本節の調整は、本書の「net 差分と機械的受理条件」「issue 単位の commit と rollback」が定める元の issue 処理の受理条件を変更しない。issue の `changed_paths` と issue commit は元の処理単位の記録として保持し、マージ調整に伴う付随編集の記録と区別する。

### join 後の検証と記録

session への取り込み成立後、publication に先立ち、issue commit と準備完了 run HEAD の到達可能性、マージ調整を含む変更 path、必要な機械生成物、および採用する全結果の判定根拠を検証する。最終取り込み結果である session commit と tree を特定し、その tree が準備完了時の run tree と一致すること、run 側で保存した検証記録をその tree に適用できることを確認する。publication 前の現在の session 状態についても、保存済み記録から全採用結果の有効性を確認する。検証済みの修正の効果と採用結果の有効性、および publication の整合性を確認できなければ、join 後検査失敗とする。

この検証段階では新しい Codex call、修正、または refactor state 同期を開始しない。停止後の現在の session 状態に対する publication の再開条件は、本書の「join 後の publication failure」に従い、最終取り込み結果と区別する。終了時の primary report の重要事項確認は、本書の「invocation report」で別に扱う。

封印済み artifact の hash 整合性は、その artifact が変わっていないことの検査である。最終取り込み結果が封印時 run HEAD と同一の内容であることや、採用結果の意味的な妥当性の証明として扱ってはならない。調整と検証の記録は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「publication completion record」に従って最終取り込み結果と結び付ける。

初回の正常な finalization では、publication と workload 固有 cleanup が完了するまで `run.state=joinable` と隔離資源を維持する。その後の結果保存、`ready` 初期化、および隔離資源 cleanup は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「merge と post-join」に従う。未解消競合、差分不整合、結果分類変更の必要、または join 後検査失敗では `run.state=error` とし、publication と observation cleanup を行わない。run branch、run worktree、issue commit、raw observation、直前の current pointer、封印済み artifact、および診断情報を保持する。取り込み確定後の停止は本書の「join 後の publication failure」に従う。

## publication

wave loop の自然完了によって封印した全 issue の採用結果が有効であり、自動 join と join 後検査が成功した場合だけ publication を行う。`inconclusive` も、その判定不能の根拠が有効であることを確認する。state の確定と cleanup の順序は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「最新状態の atomic publication」に従う。

report の `result` と invocation の成否の区別は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「最新状態の要約」に従う。

### 正常 publication

採用結果に `inconclusive` がなければ、正常 report として `ok` または `attention` を publication する。

issue commit ID、変更 path、agent verification、および cmoc の機械検査結果は、history から参照できる run report、invocation report、または subcommand log に残してよい。自動修正済み issue の詳細を現在の案件一覧へ掲載してはならない。

### `incomplete`

採用する有効な結果に `inconclusive` が 1 件以上ある場合も、残りの issue の処理と必要な再確認を経て wave loop を自然完了し、安全な issue commit を自動 join する。自動 join と join 後検査が成功した後に、`incomplete` 診断 report と、採用結果を反映した active・history・入力消費記録を publication する。`incomplete` を理由に直前の正常 publication へ current を戻したり、更新を凍結したりしない。

validation 失敗、agent call failure、Structured Output 受理失敗、差分検査失敗、commit 失敗、state corruption、merge 失敗、または durable report 保存失敗を `incomplete` として扱ってはならない。

### join 後の publication failure

自然完了経路で session への取り込みが成立した後に、post-join、検証、publication、結果保存、state 更新、または cleanup に失敗した場合は、`run.state=error` とする。取り込み直後で join 結果の保存前に停止した場合も、共通 join の復旧情報から成立を確認できればこの経路とする。取り込み済みの session commit と publication point を巻き戻さず、未 cleanup の raw observation、current pointer、および recovery に必要な run artifact と診断を保持する。共通 join の確定済み処理を重複適用せず、未完了の後処理を特定して再開する。重要事項確認の未完了には、本書の「invocation report」が参照する共通規約の例外を適用する。

publication point 前後の state と入力の扱いは、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「最新状態の atomic publication」に従う。確定後の cleanup 失敗では、新しい current が成立したことを invocation report に明示し、処理済み入力を pending として再取り込みしない。

次回の `cmoc feedback report` は、共通 join の復旧情報・Git と immutable artifact から同じ run の取り込み成立、publication の成立有無、および未完了処理を一意に特定できる場合に限り、次の条件で idempotent に再開する。run 側の準備完了だけを取り込み成立とみなさず、取り込み済みなら再同期・再 merge は行わない。

| 確定状況 | 再開条件と処理 |
|---|---|
| publication point 前 | 取り込み成立時の tree と現在の session 状態を確認し、保存済みの判定根拠と準備時の検証記録から封印済み結果をそのまま採用できる場合だけ、同じ publication を再開する。同期や追加修正でこの条件を満たそうとしてはならない。 |
| publication point 後 | 確定済み generation・history・入力消費記録と固定済み cleanup 対象の整合性を検証し、残った後処理だけを再開する。確定済み判定の現在性を再評価して publication をやり直さない。 |

publication point 後に外部状態や session tree が変わっていても、最後に確定した状態を保持して後処理を完了する。変化後の判定は次の新規 report で行う。run の隔離資源を削除する条件は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「使用済み branch と worktree の cleanup」に従う。

新しい wave または Codex call は開始しない。ただし、今回の invocation report の重要事項確認だけは、本書の「invocation report」に従う例外とする。安全に再開できない場合は、`run.state=error` と資源を維持する。

再開したサブコマンドには、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「実行 ID の開始表示」に従う新しい実行 ID を付与する。feedback run の識別情報と、引き継ぐ正常 report と `incomplete` 診断 report の target は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「feedback run」「report cut」に従う。

再開した実行のサブコマンドログには、その実行 ID、report 保存先を固定した実行 ID、feedback run と report cut の識別情報、および引き継ぐ report の path と保存状況を対応付けて記録する。対応付けには、report cut に封印した実行 ID と参照を使用する。

未 publication の結果を採用するために、封印済みの結果分類の変更、新たな意味判断のための agent call、または追加修正を必要とする停止 run は、この recovery の対象外とする。run 側の準備で許されたマージ調整を、取り込み後にも継続できるとは扱わない。封印済み artifact の改変や session 上の直接修正を、暗黙の救済手段にしてはならない。

手動 close は、この run の入力・採用結果を書き換える recovery 手段にはしない。close の開始条件は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_close.md` の「事前条件」に従う。

## ユーザー中断

本コマンドは中断可能サブコマンドとする。共通動作は、`{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` の「サブコマンドのユーザー中断」を正本とする。

`Ctrl+C` は、開始準備と、issue remediation agent call 中を含む wave loop の実行中に受け付ける。中断要求後は、新しい issue 処理、wave、本命の agent call、retry、または回復待ちを開始しない。

実行中の agent、検証、および作業用子 process を停止し、書き込み得る process の停止を確認してから、未確定の issue 処理単位を整合させる。停止の猶予は有限とし、終了しなければ停止手段を切り替えて回収する。すでに必要な検証と受理条件を満たし、正式な結果と commit・checkpoint を一体として確定できる単位だけを確定し、それ以外は単位全体を直前の確定状態へ rollback する。確定のための新たな issue call や追加検証は開始しない。停止・確定・rollback に失敗した場合は正常中断にせず、資源と診断を保持する。

doctor preprocess または共通開始処理の途中では、その準備が導入した未確定更新と作成資源を取り消す。開始前からの資源や人間の未コミット差分は保持する。run 成立前に終了した場合は、未完了の段階を report し、存在しない run、`joinable` state、または join を作らずに正常中断を完了する。

成立済み run は、整合化後に `run.state=joinable` とし、同じ invocation 内で本書の「publication を行わない feedback join」を実行する。中断後の新しい call と検証は、この join に必要な競合解消と検証、および共通中断契約が定める primary report の重要事項確認に限る。新しい report cut を封印したり、issue 処理を再開したりしない。

自然完了経路では report cut の封印を開始する前に中断要求を確認し、受理済みなら中断経路へ移る。封印の開始から自動 join・join 後検査・publication・cleanup までは、不可分な finalization とする。中断経路でも、整合化後の自動 join 開始から必要な後処理・cleanup までは不可分な finalization とし、途中の停止要求は整合した境界まで保留する。

finalization 中の process interruption、取消、または操作失敗は、正常な `user_interruption` へ変換しない。自然完了経路で取り込み済みなら本書の「join 後の publication failure」、それ以外は `{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「join の失敗と復旧」に従う。

invocation report の重要事項確認は、この不可分な finalization の終了後に行う。確認の停止要求を、issue 処理の再開や publication の取消として扱わない。

### publication を行わない feedback join

正常なユーザー中断後の自動 join と、ユーザー中断・エラーで残った run の `cmoc run join` は、確定済み issue commit を成果として、共通 join の「run 側での準備 → session への取り込み → 後処理」を行う。統合・競合解消・同期による後続の変更も共通契約に従い、新しい issue 処理は始めない。自然完了時の封印済み採用結果の検証は、この経路の publication 条件として適用しない。

feedback の publication、`incomplete` 診断 report の生成、active・history の更新、および observation の消費・cleanup は行わない。raw observation、直前の current pointer、必要な checkpoint を保持し、feedback work state に join 結果と publication 未実施を記録する。取り込みと必要な結果保存を終えたら、共通 join に従って `ready` 初期化と隔離資源 cleanup を行う。

次の新しい `cmoc feedback report` は、現在の session tree、pending observation、および最新の active record を再確認する。保存した checkpoint を中断位置からの再開や publication の許可に使わない。この経路の join 後の失敗は共通の手動 join・abandon で復旧し、封印済み結果の publication recovery へ切り替えない。

自然完了経路ですでに自動 join した run は、本節の明示 join の対象にせず、「join 後の publication failure」に従う。

## 続行不能な失敗

本節は本命の issue 処理と join・publication の失敗を扱う。primary report の重要事項確認用 call の停止・失敗は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「確認の停止・失敗と保存」「確認結果と終了結果の分離」に従う。

本命処理の続行不能な失敗では、実行中の issue 処理単位を正式な結果と commit まで確定できる場合だけ commit し、それ以外は処理単位全体を rollback する。成立済み run を `run.state=error` とし、自動 join しない。run 成立前なら新しい run state を作らない。

確定済み issue commit、run branch、run worktree、raw observation、current pointer、正式な checkpoint、および再確認に必要な診断情報を保持する。失敗を新しい publication または `incomplete` 診断で確定せず、observation cleanup は行わない。すでに publication point を通過した場合は、本書の「join 後の publication failure」に従い、確定済み state を保持する。

agent call failure、tool 失敗、validation 失敗、差分検査失敗、commit 失敗、および orchestration 失敗を feedback issue または `human_required` に変換してはならない。

quota と一時障害の分類・回復待ち・再開は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「`codex exec` が失敗した場合」に従う。Structured Output の補正と受理条件は、同文書の「Structured Output」に従う。これらの処理でも続行できない場合に、本節の終了処理へ移る。

## report の保存と表示

実行 ID と、本節の各 report の共通表示契約は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「実行 ID の開始表示」「primary report」に従う。最外側の実行結果を示す invocation report を primary report とし、publication で current pointer に結び付ける immutable な report とは役割を分ける。共通掲載内容の実行記録は、以下の issue 一覧とは区別する。

自動 join の競合解消については、`{{cmoc-root}}/oracle/doc/app_spec/merge_conflict_resolution.md` の「受理と報告」が定める判断、付随編集、検証、および未解消理由を実行記録に含める。封印済み結果への影響と検証結果、publication completion record との対応、または publication を停止した理由も判別可能にする。自動修正済み issue を人間向け issue 一覧に再掲載するためには用いない。

### publication report と終了時の記録

current pointer に結び付ける report は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「最新状態の atomic publication」に従って、切替前に保存する immutable な publication artifact である。掲載する一覧は publication 対象の generation に対応させ、冒頭の要約にも report 保存時点の記録であることを明示する。要約と実行記録には保存時点までに確定した処理を載せ、保存後に行う publication、cleanup、および run state の終了処理を、実行済みの成功として先取りして記載してはならない。

冒頭の要約では、それらが保存時点では未完了であることと、必要な確認・操作を示す。保存後の結果の確認先として元の実行のサブコマンドログを案内する。保存後に確定した処理結果と最終 state は、そのログと terminal result に記録し、publication report を書き換えない。`cmoc feedback report` では、これらの最終結果を今回の invocation report にも載せ、その 1 件を primary report とする。publication report 保存までの共通掲載内容は省略しない。

publication artifact の不変性と掲載時点は、正常 report、`incomplete` 診断 report、および `cmoc feedback close` が publication する report に共通して適用する。close の primary report と保存後の記録先は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_close.md` の「primary report と終了結果」を維持する。本コマンドの再開した実行の記録と帰属は、本書の「再開時の report と実行記録」に従う。

本コマンドの publication report は primary report を兼ねないため、重要事項確認用 call とその結果欄を追加しない。重要事項の確認は、保存後の処理結果まで含めた今回の invocation report に対して行う。primary report を兼ねる close の publication report には、この省略を適用しない。

### 現在の案件一覧

通常の問題一覧は、publication した generation の active issue だけから作る。案件 ID 順に並べ、案件 ID、issue ID、最新の判定と確認時点、category、summary、impact、reason、確認できた current evidence、occurrence 集計、観測期間、および bounded representative evidence を示す。`human_required` には human action を、`inconclusive` には確認できなかった内容と具体的な理由を示す。

current evidence には、人間が report から確認できる path、subject、probe、location、fingerprint、または finding を記載する。証拠を得られなかった場合はその旨を示し、削除予定の wave または checkpoint への link だけで済ませてはならない。

generation ID、確定日時と作成元、入力の確認境界、および history の保存先・該当履歴への参照を示す。未取り込みの観測や確定後の変化まで確認済みとは表示しない。旧判定や終了案件は現在の一覧へ混在させず、経緯は history から確認できるようにする。

### 再開時の report と実行記録

publication または cleanup の再開で引き継ぐ正常 report と `incomplete` 診断 report の実行情報は、report cut で保存先を固定した実行に帰属させる。再開した実行の ID に付け替えず、掲載する個々の呼び出しや observation も実際に属する実行に対応付ける。

publication report の保存段階では、未保存なら固定済み target へ保存し、保存済みなら path と hash を検証して再利用する。保存済み report は、冒頭の要約や元の指示も含めて元の入力と掲載時点を維持し、再開した実行の入力や結果に置き換えない。

再開した実行の作業内容、終端結果、および共通掲載対象の本文を含む実行記録は、再開した実行のサブコマンドログと「invocation report」へ残す。成功・失敗にかかわらず今回の invocation report を primary report とし、今回の実行 ID、引き継いだ publication report と元の実行への参照、再開した処理、および最終 state・cleanup を示す。引き継ぐ publication report に今回の実行記録を追記してはならない。

### 正常 report

正常 report の保存先は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「report cut」に従って次に固定する。

```text
{{repo-root}}/.cmoc/gu/report/feedback/{{execution-id}}.md
```

保存した正常 report を publication artifact とする。実行情報には、少なくとも次の情報を含める。

- command、生成日時、repo root、および session branch
- feedback run ID、run branch、run fork commit、および run join commit。no-op join では run join commit を `null` とする
- report cut ID、active generation ID、最終 high-watermark、および wave 数
- remediation 対象 issue 数と `human_required` issue 数
- `result: ok | attention`

案件一覧は本書の「現在の案件一覧」に従う。正常 report では `human_required` の案件だけが残る。

### `incomplete` 診断 report

`incomplete` 診断 report の durable 保存と state 境界は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「`incomplete` 診断 report」を正本とする。保存した診断 report を publication artifact とし、invocation report と terminal result に `result: incomplete` を含める。

実行情報には、正常 report と同じ実行・run・report cut・generation・入力境界の情報、各終端結果の件数、および `result: incomplete` を含める。

冒頭の要約で、この generation に判定不能の案件が含まれ、最新状態の要約が `incomplete` であることを明示する。詳細結果には、本書の「現在の案件一覧」に従い、次の区分を分けて示す。

1. `human_required の案件`
2. `inconclusive の案件`

各項目は、診断 report 単独で reason と確認できた current evidence を読める内容にする。外部解決を人間が確認した場合の操作は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_close.md` の「CLI 契約」に従って案内する。自動 join 済み修正の監査情報は、run report または subcommand log に保持する。

### invocation report

`natural_completion`、`user_interruption`、`error` のすべてで、今回の invocation report を primary report として次へ保存する。run 成立前の中断、事前条件違反などの開始前エラー、および同じ feedback run の recovery も対象とする。

```text
{{repo-root}}/.cmoc/gu/report/feedback/invocation/{{execution-id}}.md
```

実行情報には、少なくとも次の項目を含める。

- command、生成日時、repo root、session branch、および terminal result
- run kind、run branch、run fork commit、run worktree、state before、および state after
- 自然完了またはその recovery で確定した場合は、publication の `result: ok | attention | incomplete`

詳細結果には、次の内容を含める。

- 完了した wave、high-watermark、処理済み issue、確定済み commit、および rollback
- 自動 join の準備・取り込み・後処理とその結果。共通項目は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「join の共通記録」「workload の report」に従い、封印時の成果との対応も示す
- publication の成立有無と、成立した generation・publication report への参照。自然完了では本書の「現在の案件一覧」をその generation に対応させて掲載する。recovery では元の確定時点の一覧であることを示す
- 未実行の処理、維持した state、中断またはエラーの理由、次の操作、および関連ログ

invocation report は feedback publication または active state の一部ではなく、current pointer の参照先にしない。candidate を publication 済み issue または active issue として扱ってはならない。

上記の確定結果を掲載した機械生成版について、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「重要事項確認用 call」に従う確認工程を行う。確認未完了と必要な保存・終了処理の失敗は、同文書の「確認結果と終了結果の分離」に従って区別する。recovery でも今回の invocation report を確認し、引き継いだ publication artifact の再判定・追記・上書きは行わない。重要事項の確認状態と、publication の `result: incomplete` は別の意味として表示する。

`user_interruption` では publication 未実施と保持した観測・checkpoint を明記する。自動 join に成功した場合は、成果の取り込みと最新状態の未 publication を区別し、次回 report で再確認することを示す。run 成立前なら、自動 join は未実行とする。

`error` では、今回完了できなかった処理と、最後に確定した generation・report を区別して示す。publication 前に失敗した場合は、今回の最新状態の確認・確定が成立していないことを示す。publication 後に失敗した場合は、成立済みの更新と残った処理を示す。未確定の結果を `incomplete` や解決済みへ変換しない。

## 終了コード

以下は本命処理と必要な確定・保存処理の結果を表す。重要事項確認自体の未完了には、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「確認結果と終了結果の分離」の例外を適用する。

- `ok`、`attention`、`incomplete` は、自然完了の自動 join・publication と必要な終了処理まで成功した場合に終了コード 0 とする。正常なユーザー中断も、成立済み run の自動 join と必要な終了処理を完了した場合、または run 成立前に整合して終了した場合に 0 とする。
- validation 失敗、agent call failure、Structured Output 受理失敗、差分検査失敗、commit 失敗、state corruption、merge 失敗、required recovery 失敗、および durable report・publication・cleanup の失敗は終了コード 1 とする。

終了コードは、今回の invocation が利用可能な終端結果を確定できたかを表す。直前の最新状態が残っていること、または一般的なエラー説明を出力できたことだけでは、今回の invocation が report result を確定したとはみなさない。

issue の件数、category、impact、`human_required` の有無、または fixed issue の件数だけを理由に非 0 を返してはならない。fixed issue の有無や件数を、他 workload の成功判定、retry、または recovery へ伝播させない。
