# feedback の repository-local state

本書は、feedback の最新状態と履歴、案件の遷移、immutable な intake wave、high-watermark、checkpoint、report cut、atomic publication、および入力の消費・cleanup を定める。用語と結果分類は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「用語と結果分類」「最新状態の要約」、raw observation と detector rule は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「feedback observation の収集」を正本とする。

## state の目的

feedback state は、通常の確認・操作に使う active と、経緯を確認する history を分離する。進行中の report と close の作業記録は、最新状態でも履歴の確定済み記録でもない。

長期保持してよい情報を次に示す。

- active state へ未反映の pending observation
- active issue の compact record
- 更新前の判定、解決・手動クローズの経緯、および入力の消費を追跡できる history
- recurrence threshold 未満の machine observation の bounded aggregate
- 中断・失敗後の明示 join または abandon と、join 後の publication・cleanup の recovery に必要な run manifest、intake wave、report cut、および正式な checkpoint
- close の確定と recovery に必要な固定入力・進行記録
- publication 済み report と、最新状態を選ぶ current pointer

`fixed`、`already_resolved`、`not_actionable`、終了案件、処理済み raw observation、および完了済み checkpoint を active の問題一覧へ残してはならない。issue commit、変更 path、および検証結果の監査情報は、history から参照できる run report、invocation report、または subcommand log に保持してよい。

## 所有範囲と配置

feedback state は `{{repo-root}}` が所有する。branch、`{{work-root}}`、session、および run branch は所有単位にしない。

論理的な配置を次に示す。

```text
{{repo-root}}/.cmoc/gu/feedback/
├── observation/v1/...
├── active/current.json
├── active/generation/{{generation-id}}/
│   ├── manifest.json
│   ├── issue/...
│   └── machine_aggregate/...
├── history/...
└── work/
    ├── {{feedback-run-id}}/
    │   ├── manifest.json
    │   ├── wave/{{wave-sequence}}/...
    │   ├── checkpoint/...
    │   ├── report_cut.json
    │   └── publication_completion.json
    └── close/...

{{repo-root}}/.cmoc/gu/report/feedback/
├── {{execution-id}}.md
├── incomplete/{{execution-id}}.md
├── close/{{execution-id}}.md
└── invocation/{{execution-id}}.md
```

実行 ID は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「実行 ID の開始表示」に従う。正常 report と `incomplete` 診断 report の保存先に使う実行は、本書の「report cut」で固定する。close report は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_close.md` の「primary report と終了結果」に従う。invocation report は、それを作成する実行の ID を使う。

`observation/v1` の `v1` は、raw observation の保存 layout の version を表す。保存する reporter input schema の version とは独立している。

`{{repo-root}}/.cmoc/gu` 全体を Git 追跡対象外とする。session と run の join または abandon は、feedback state を暗黙に取り込み、巻き戻し、複製、または削除してはならない。

`invocation/{{execution-id}}.md` は中断またはエラーを要約する primary report であり、feedback state または publication artifact ではない。current pointer の参照先にしない。内容と生成条件は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「中断・エラー時の invocation report」と、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_close.md` の「primary report と終了結果」を正本とする。

まだ publication がない repository では、state root または current pointer が存在しない状態を有効な初期状態とする。既存の確定済み state の欠落を初期状態として扱ってはならない。空 directory や `.gitkeep` は作らない。

## artifact の役割

state を構成する artifact の役割を次に示す。

| artifact | 役割 |
|---|---|
| active generation | 同じ publication で確定した active issue と threshold 未満 aggregate の immutable な集合 |
| current pointer | active generation、その時点の最新一覧を載せた Markdown report、および確定済み history・入力消費記録への参照を一意に選ぶ publication point |
| history record | 更新前の判定と問題・案件の経緯を、publication の確定と対応付ける immutable な記録 |
| feedback run manifest | 1 feedback remediation run の入力、run identity、wave、join、publication、および cleanup の状態を結び付ける記録 |
| intake wave | その wave が処理する observation、active issue、正規化済み issue identity、および根拠の immutable な固定入力 |
| checkpoint | 受理済み normalization または remediation の入力、結果、検証、および commit を hash で結び付ける記録 |
| report cut | wave loop の自然完了後に封印する publication 入力。ordered wave、最終 high-watermark、base current pointer、採用する有効な結果、および merge 対象を固定する |
| publication completion record | report cut の採用結果と、マージ調整・検証を経た最終取り込み結果を結び付ける immutable な記録 |
| close の作業記録 | 対象案件・理由・base current pointer・publication target と未完了処理を結び付け、同じ close を再開するための記録 |
| `incomplete` 診断 report | `inconclusive` を含む最新状態と、判定不能の具体的な原因を記載した durable な Markdown report |

timestamp、Git commit、branch reachability、または directory の列挙順から current state を推測してはならない。

current pointer が参照する generation manifest、Markdown report、および確定済み記録は、各 path と hash を検証できなければならない。必要な対応付けと保持を確認できない state はエラーとする。最新状態の確認・操作には、検証した generation と構造化された記録を使用する。`incomplete` や close による publication にも同じ条件を適用し、Markdown report から active や入力の消費状態を逆算してはならない。

## JSON と排他制御

保存 record の詳細 schema は、本書では定めない。

state の JSON は、UTF-8、object key の辞書順、末尾改行ありの canonical form で保存する。hash は canonical byte 列の SHA256 とする。

immutable artifact は、sibling temporary file への write、file flush、atomic rename、および parent directory の flush によって durable に保存する。同じ path への同じ byte 列の再保存は idempotent とする。同じ path に異なる byte 列がある場合は corruption として停止し、自動上書きしない。

run manifest と close の作業記録の進行 state・artifact reference は、先行 state と新しい immutable artifact の hash を検証したうえで atomic に更新する。intake wave の固定入力、正式な checkpoint、封印済み report cut、および close の固定入力を in-place で変更してはならない。

`cmoc feedback report` と `cmoc feedback close` およびその recovery は、`{{repo-root}}` ごとの同じ feedback writer 排他を使用する。排他は、base current pointer と対象を検証する前から、publication と cleanup の完了、再開 state の確定、または失敗終了まで保持する。report では最初の high-watermark の固定より前に取得する。

未完了の report または close の固定入力を、別の writer が上書きしてはならない。process 終了で lock が解放されても、未完了操作の recovery 要件は消えない。新規開始・再開の分岐は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「事前条件と run の開始または再開」と、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_close.md` の「事前条件」「保存失敗と recovery」に従う。

lock の方式は実装裁量とする。所有者を安全に判定できない lock を暗黙に破棄してはならない。排他保持中も collector は新しい observation を durable 保存できなければならない。

## feedback run

`{{feedback-run-id}}` は、1 回の feedback remediation run を識別する。書式と採番は、`{{cmoc-root}}/oracle/doc/app_spec/id.md` の「ID のフォーマット」「プレフィックス」「採番と順序保証」に従う。新しい feedback run の開始時に発行し、別のサブコマンド実行からの recovery を含む同じ処理を通して保持する。

feedback run manifest は、feedback run ID と、隔離作業を担う編集 run の識別情報を対応付ける。編集 run ID の発行と保持は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「共通開始処理」に従う。新規開始と recovery の条件は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「事前条件と run の開始または再開」を正本とする。

## active generation

`{{generation-id}}` は、1 つの active generation を識別する。書式と採番は、`{{cmoc-root}}/oracle/doc/app_spec/id.md` の「ID のフォーマット」「プレフィックス」「採番と順序保証」に従う。新しい generation ごとに発行し、同じ generation の保存、検証、および publication の再開では保持する。

active generation には、次の record だけを含める。

- 未終了の案件の active issue record
- recurrence threshold 未満の machine aggregate

generation manifest は、generation ID、base current pointer、作成元の report cut または close の作業記録、作成日時、および各 record の path と hash を固定する。report による generation は join 後の session commit を含める。close は直前の判定・確認時点を引き継ぎ、新しい agent 確認や join があったとは記録しない。全 record を保存して検証した後に manifest を保存する。valid な manifest がない generation を読み取ってはならない。

current の検証に必要な情報は、旧 generation や完了済み work artifact の cleanup 後も保持する。作成元を示す監査用の参照と、現存 artifact の hash 検証を必要とする参照を区別する。

### issue identity

machine issue の canonical key は、detector rule が定める machine issue key とする。

agent observation から新しい issue を作る場合は、最初の observation ID から安定した canonical key を作る。normalization agent が既存 issue との同一性を選んだ場合は、既存の issue ID と canonical key を維持する。

issue ID は canonical key の hash から決定論的に生成する。同じ issue ID に対して異なる canonical key が見つかった場合は、collision として停止する。暗黙に salt を追加してはならない。

active state に残っていない過去の agent issue と、後日の observation の同一性は判定しない。machine issue は canonical key が同じであれば、再発時にも同じ issue identity を使用する。

### 案件 ID と状態遷移

案件 ID は、`{{cmoc-root}}/oracle/doc/app_spec/id.md` の「ID のフォーマット」「プレフィックス」「採番と順序保証」に従う。1 件の案件を 1 つの issue identity に対応付け、同じ identity の未終了案件は repository 内で高々 1 件とする。

report cut の採用結果を publication するときの遷移を次に示す。

| base の案件 | 採用結果 | publication 後 |
|---|---|---|
| なし | `human_required` または `inconclusive` | 新しい案件 ID で active に登録する。 |
| あり | `human_required` または `inconclusive` | 案件 ID を維持して判定・根拠を更新し、更新前の判定を history に残す。 |
| あり | `fixed`、`already_resolved`、または `not_actionable` | 案件を終了し、結果と経緯を history に残す。 |
| なし | `fixed`、`already_resolved`、または `not_actionable` | active の案件は作らず、issue の処理結果を history に残す。 |

新しい案件 ID と issue identity の対応は report cut の封印時に固定する。active への登録は publication point で成立し、同じ cut の保存・再開では同じ案件 ID を使う。publication 前の candidate や予約済み案件 ID を現在の案件として提示してはならない。

手動 close の対象は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_close.md` の「対象と理由」に従う。close の publication では、その案件を active から除き、人間の宣言と直前の agent 判定を区別して history に残す。他の案件と threshold 未満 aggregate はそのまま引き継ぐ。

終了した案件 ID は再使用しない。同じ machine issue identity の再発も新しい案件として登録する。history の終了記録を新しい observation に適用せず、通常の検出・normalization・threshold 判定に従う。close が対象とするのは指定された案件だけであり、同じ issue identity の後続案件へ置き換えてはならない。

### active issue record

active issue record は、次回の候補絞り込み、remediation、および人間向け表示に必要な情報だけを保持する。

- 案件 ID、issue identity、origin、category、summary、および impact
- occurrence count、affected session count、最初と最後の観測日時
- bounded な representative evidence、subject、および fingerprint
- 最新の agent result、reason、確認できた current evidence、判定根拠、および確認時点。`human_required` では human action、`inconclusive` では確認できなかった内容と具体的な理由を保持する
- 案件へ取り込んだ observation と、結果を確定した publication を追跡できる参照
- machine issue の場合だけ、recurrence window を評価できる bounded summary

evidence は、削除予定の raw observation、intake wave、または report cut だけを参照してはならない。次回 report で再確認できるよう、安定した subject と、人間が確認できる簡潔な説明を record に保存する。secret を複製してはならない。

保持件数と集計情報は schema-fixed な上限を持つ。上限超過時の選択は、wave と report cut に固定した入力に対して決定論的に行う。AI に保持対象を選ばせない。

`inconclusive` の current evidence が得られない場合は、その欠落と理由を保持する。保存のために証拠や human action を作らず、次回 report に必要な subject と判定不能の根拠を残す。

### history の保存と参照

history は、案件 ID と issue identity、判定の更新・agent の結果による終了・手動クローズの別、更新前後の判定と根拠、理由、日時、および関連 report・log への参照を保持する。案件を作らなかった処理結果には案件 ID を捏造しない。手動クローズの理由は人間の宣言として保存し、agent が外部解決を確認した証拠へ変換しない。

更新前の generation を cleanup する前に、経緯の確認に必要な内容を history に保存する。削除予定の generation や work artifact への参照だけでは代替できない。既存の history は後続 publication に引き継ぎ、同じ操作の再実行で履歴を重複追加しない。未 publication の記録は確定済み履歴として表示しない。

history は案件の経緯と close 済み案件 ID の照合に使う。通常の同一性判定、新しい observation の抑止、または active の再構築に使用しない。細かな配置・索引・record schema・保持期間は本書では固定しないが、現在状態、再適用防止、および経緯の確認に必要な記録を通常の publication cleanup で失わせてはならない。

### threshold 未満の machine aggregate

machine observation は、rule の canonical key と recurrence window で集約する。threshold 未満の場合は issue を作らず、判定に必要な count、distinct dimension、time bucket、代表 evidence、および fingerprint だけを bounded aggregate として保持する。

threshold を満たした aggregate は issue candidate へ昇格させる。同じ generation に aggregate として重複保存してはならない。window 外の occurrence を除いた結果が空なら aggregate を削除する。threshold 未満の aggregate は、人間向け report に表示しない。

## intake wave と high-watermark

### intake wave

各 intake wave は、次の入力を固定する。

- 今回の high-watermark 以前の pending observation。最初の wave は未消費の入力全体を対象とし、後続 wave は直前の境界より後の入力を追加する
- 最初の wave の場合だけ、run 開始時の current pointer、全 active issue、および threshold 未満 aggregate
- observation schema の version
- validation、normalization、deduplication、detector rule、および集約規則の version
- normalization 後の未処理 issue identity、再確認対象の issue identity、既存の案件 ID との対応、および bounded evidence
- 再確認対象の場合は、先行 checkpoint、判定根拠の変化、および関連する再確認履歴への参照

wave input は durable 保存後に変更しない。追加 evidence は後続 wave の入力として同じ issue identity へ関連付けてよい。

最初の wave では、前回 `incomplete` だった案件も active record から再確認する。消費済み raw observation が cleanup 待ちで残っていても新規入力にはしない。history や古い Markdown report の走査によって候補を復元しない。

処理対象と再試行の条件は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「call 回数と順序」と「intake wave loop」を正本とする。

### high-watermark

high-watermark の意味は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「用語と結果分類」に従う。collector の durable な受理順序に対する単調増加境界として管理し、directory の列挙順、timestamp、quiet period、observation 件数、または observation ID の通番から推測してはならない。

wave 終了時の確定順序と境界間の observation の処理は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「intake wave loop」に従う。新規受理がなければ前回と同じ high-watermark を使用してよい。

`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「処理モデル」が定める条件で wave loop を自然完了したとき、最後の境界を最終 high-watermark とする。最終 high-watermark より後に受理された observation は、次回 invocation の pending input として残す。

## checkpoint と report cut

### checkpoint

normalization と issue remediation の output は、schema と宣言済みの決定論的事後条件を満たした後だけ正式な checkpoint として保存する。

issue remediation checkpoint は、少なくとも次の情報を hash で結び付ける。

- run、wave、issue identity、既存の案件 ID、論理 agent call、builder、および schema
- 固定入力、正式な Structured Output、および終端結果
- その結果の判定根拠
- 再確認の場合は、先行 checkpoint、再確認を必要とした根拠の変化、および旧結果と新結果の関係
- realization file の net 差分、`changed_paths` の照合、および変更禁止対象の検査結果
- agent の検証結果と issue commit ID。差分がない場合は commit を作らなかったこと

不適合 output、correction の途中結果、失敗した agent call、差分検査失敗、commit 失敗、および rollback 前の差分を正式な issue result checkpoint にしてはならない。これらは invocation error の診断情報として分離する。

正式な remediation checkpoint は論理 agent call ごとに高々 1 件とする。同じ run と同じ issue identity の再確認結果は、新しい checkpoint として追加する。Structured Output correction、retry、および quota または一時障害の回復待ち後の再開は同じ論理 agent call の checkpoint に含める。

### report cut

report cut は、wave loop が自然完了した後に一度だけ封印する。intake に単一の可変 report cut を使用してはならない。

report cut は、少なくとも次の入力を固定する。

- ordered intake wave と各 wave の hash
- wave 終了時に検証・正規化した追加入力とその hash、および採用結果・集計への対応。新しい wave を要しなかった重複 observation なども、消費するなら含める
- run 開始時の current pointer、active generation、および最終 high-watermark
- 処理した issue identity ごとに採用する有効な結果、案件 ID との対応、および対応する checkpoint の path と hash
- issue commit、run branch HEAD、および merge 前の検証結果
- active generation と history の publication target、正常または `incomplete` の report target、その保存先を固定した実行 ID、および消費・cleanup 対象の入力

正常 report または `incomplete` 診断 report の保存先には、固定した時点の実行 ID を `{{execution-id}}` として使用し、最終 path とともに封印する。同じ publication を別のサブコマンド実行から再開する場合も、この target を引き継ぐ。保存先や帰属を再開した実行の ID に合わせて変更してはならない。

封印後に許す調整・検証と停止条件は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「自動 join と join 後の確定」に従う。調整によって、封印済み report cut、wave input、issue result、最終 high-watermark、または cleanup target を変更してはならない。

### publication completion record

cmoc は、封印後のマージ調整に関する agent の判断と検証結果を、merge commit の作成前に既存の Codex call log へ保存する。記録から report cut と検証対象の内容を特定できるようにし、取り込み後に停止した場合も recovery 用の根拠として保持する。

publication completion record は、merge または no-op join と post-join 後に、最終 session tree に対する検証を完了してから保存する。run manifest は、この record と report cut の path および hash を参照する。少なくとも次の対応を確認できる記録とする。

- 封印済み report cut と採用結果・checkpoint の参照。
- merge 前の両 commit、成立した merge commit または no-op join、および post-join 後の session commit。
- run branch と issue commit の到達可能性。
- マージ調整の対象、採用した判断と理由、影響を受けた判定、および merge commit 前に保存した検証記録との対応。調整しなかった場合はその旨。
- その検証記録が最終 session tree に適用でき、全採用結果が有効であることを確認した最終検証結果。

この record は、元の issue result の書き換えや新しい結果分類の保存先にはしない。artifact の不変性・hash 整合性と、調整後の内容に対する検証結果は区別して記録する。結果の有効性を確認できず停止した場合は completion を記録せず、診断情報と recovery 用資源を保持する。

保存済み record は immutable とし、recovery 時にも上書きしない。record が未保存の場合は、同じ封印済み入力と保存済み検証記録を使用し、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「join 後の publication failure」の再開条件を満たす場合だけ確定する。

## 入力の消費と cleanup

report の publication は、validated input を採用結果・active record・threshold 未満 aggregate へ確実に引き継げた範囲だけを消費済みにする。`incomplete` にも同じ条件を適用する。問題が未解決であることと、元の observation が未処理であることを区別する。

消費範囲は、report cut が参照する wave と検証済み追加入力に含まれる observation ID と hash、および案件・処理結果・aggregate への取り込み関係で固定する。high-watermark 以前にあることだけでは消費の根拠にならない。publication と結び付けた消費記録は、raw file が残っていても再取り込みを防ぎ、work artifact の cleanup 後も消費済みかどうかを判定できるようにする。

raw observation の cleanup 対象は、消費が確定し、最終 high-watermark 以前に durable 保存された、その操作の記録にある入力に限る。validation を通過できなかった入力、未取り込み・後着の入力、および別の未完了処理が参照する入力を削除してはならない。raw の削除後にも、active の再確認と history の経緯確認に必要な内容を残す。

close は新しい intake を行わず、消費範囲を広げない。close に伴う raw の cleanup を行う場合も、対象案件へ取り込み済みで、消費の確定を検証できる入力だけに限る。同じ issue identity、観測日時、または最新の high-watermark を理由に対象を広げてはならない。

cleanup は確定済みの対象と hash を検証して idempotent に行う。対象がすでに削除済みなら処理を重複適用せず、存在する内容の hash が一致しなければ corruption として停止する。案件 ID の対応、確定済み history、入力の消費記録、および再開に必要な記録を、完了済み work artifact と一緒に削除してはならない。

## `incomplete` 診断 report

診断 report の生成条件と表示は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「`incomplete`」「`incomplete` 診断 report」を正本とする。

`incomplete` 診断 report は、本書の「report cut」で固定した target へ durable に保存する。保存先は次のとおりとする。

```text
{{repo-root}}/.cmoc/gu/report/feedback/incomplete/{{execution-id}}.md
```

診断 report は、intake wave、report cut、および checkpoint を cleanup しても単独で読める内容にする。`human_required` と `inconclusive` を保持した generation とともに、本書の「最新状態の atomic publication」で current にする。report の保存だけでは publication は成立しない。

## 最新状態の atomic publication

report の開始条件は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「publication」、close の開始条件は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_close.md` の「事前条件」を正本とする。正常 report、`incomplete` 診断 report、および close による更新は、次の共通手順で確定する。

1. base current pointer、操作の固定入力、次の generation・history・report の target、および消費・cleanup 対象を durable な作業記録へ結び付ける。
2. 新しい generation の record と manifest、追加する history、および入力消費の記録を durable 保存する。これらはまだ公開しない。
3. その generation の最新一覧を載せた Markdown report を、固定済み target の最終 path へ durable 保存する。
4. 各 artifact の path と hash、および current pointer が base から変わっていないことを検証する。
5. generation、report、および引き継ぐ履歴と追加履歴・消費記録を一体として選ぶ current pointer を atomic に切り替え、durable にする。
6. 切替後にだけ、本書の「入力の消費と cleanup」に従って raw observation、切替前の generation、および完了済み work artifact を cleanup する。

current pointer の切替だけを publication point とする。active の除去・更新だけ、history の追加だけ、または入力消費だけを公開してはならない。履歴の確定範囲も pointer と検証可能に結び付け、history directory に存在するだけの staged record を確定済みとして扱わない。更新前 generation を削除しても、それ以前の確定済み history と消費記録への参照は維持する。

publication point 前の失敗では、直前の current pointer、raw observation、および recovery 用 artifact を維持する。今回の候補を最新状態にせず、入力を消費・cleanup しない。staged report、issue commit、自動 join の成功、または close の作業記録だけでは publication 済みとしない。

publication point 後の失敗では、確定済み state を巻き戻さない。最新状態の更新が成立したことと、invocation の未完了処理・エラーを別々に記録・表示する。切替の成否が不明な場合も、pointer と固定済み artifact を検証して判断し、推測で新旧いずれかを採用したり操作を再適用したりしない。invocation error を `incomplete` や解決済みの判定へ変換しない。

recovery は同じ target と固定入力を再利用し、案件の登録・終了、履歴追加、入力消費を重複適用しない。report では、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「join 後の publication failure」「再開時の report と実行記録」、close では、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_close.md` の「保存失敗と recovery」に従う。異なる base、hash 不一致、または確定状況の不明を上書きで解消しない。

処理済み入力と完了済み work artifact の cleanup を確定した後にだけ、feedback run の state と隔離資源を正常終了状態へ戻す。report の publication または cleanup の失敗中は `run.state=error` と隔離資源を維持する。close は編集 run を作らず、その未完了処理を close の作業記録で管理する。

## run lifecycle との整合

run join と abandon が feedback state に与える影響は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「編集 run の共通仕様」を正本とする。どちらも raw observation と直前の current pointer を保持し、破棄した run commit に依存する `fixed` checkpoint を publication 可能な結果として残してはならない。
