# `cmoc feedback report`

`cmoc feedback report` は、pending observation と直前の active state を report cut に固定し、現在も人間対応が必要な issue だけを新しい active state と Markdown report へ publication する。

raw observation は `{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` を正本とする。state、checkpoint、publication、および cleanup は `{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` を正本とする。

## CLI 契約

- 位置引数を受け取らない。
- サブコマンド固有 option を受け取らない。
- Git commit を作成しない。
- git working tree と staging area の clean 状態を要求しない。
- 編集 run を作らず、session state と run state を変更しない。

## 事前条件

処理は、次の順序で開始する。

1. doctor preprocess を実行する。
2. main worktree で active な `{{cmoc-session-branch}}` が checkout されていることを確認する。
3. 対応する `session.state=active` と `run.state=ready` を確認する。
4. repository-level feedback writer 排他を取得する。
5. current pointer と既存 state の schema、path、hash、および参照整合性を検証する。
6. publication 後の cleanup が残っていれば、先に再開する。
7. 再開可能な report cut があれば再利用し、なければ新しい cut を固定する。

state root または current pointer が存在しない状態は、有効な初期状態とする。既存 state に corruption がある場合は state を変更せず、新しい report を publication しない。

## report cut

新しい report cut には、次の入力を固定する。

- 今回処理する全 pending observation
- current pointer が指す active issue と threshold 未満 machine aggregate
- candidate の現在状態を確認する repository content、fingerprint、または probe result
- normalization、verification、schema、および決定論的処理規則の version

cut 固定後に追加された observation は、次回の report で処理する。report-time agent が reporter へ送った observation も、実行中の cut には加えない。

report-time agent には、cut に固定した reference だけを渡す。live repository state、raw log、過去 session、別 candidate、または feedback state を追加で読ませてはならない。

current-state probe を使用する場合は、stable probe ID、型付き入力、固定した実行対象、timeout、出力上限、および secret masking を事前定義した allowlist entry に限定する。probe は read-only とする。agent に command、引数、環境変数、または追加 probe を選ばせてはならない。

## 処理順序

report cut は、次の順序で処理する。

1. observation と既存 state を機械検証する。
2. 同じ observation ID と canonical hash を持つ完全な重複を 1 件にまとめる。
3. machine observation を canonical key と recurrence window で集約する。
4. threshold 未満の machine aggregate を、次の active generation 候補へ保持する。
5. agent observation の比較候補を、category、evidence subject、path、および fingerprint などの安定情報で絞る。
6. 同一性を機械的に確定できない agent observation だけを normalization agent へ渡す。
7. 形成した issue candidate と直前の全 active issue を verification agent で検証する。
8. 全 candidate が確定した場合だけ、新しい active generation と Markdown report を作る。
9. state 仕様に従って current pointer を切り替え、その後に処理済み input と一時 state を cleanup する。

validation、完全一致 deduplication、machine key 集約、recurrence window、threshold、および候補絞り込みを AI に代行させてはならない。

## 機械処理

### validation

raw observation の schema、path、および canonical hash は、report cut manifest と一致しなければならない。同じ observation ID で hash が異なる場合は corruption とする。

1 件でも validation を通過できない input がある場合は、正常 publication を行わない。invalid input を処理済みとして削除せず、問題の path と理由を console と subcommand log に示す。

### machine observation

machine observation は、detector rule が定める canonical key、recurrence window、および distinct dimension だけで集約する。自由文や AI 判断を identity または threshold 判定に使用してはならない。

threshold 未満の aggregate は、人間向け issue や report 項目にしない。threshold を満たした aggregate は 1 件の issue candidate とし、同じ canonical key の active issue があれば機械的に統合する。

### agent observation

agent observation は、観測日時と observation ID による安定した順序で処理する。比較対象には、cut 開始時の active issue と、同じ cut で先に形成した provisional candidate を含める。

agent が入力した deduplication hint は、候補検索にだけ使用する。issue identity の確定根拠にはしない。機械的な完全一致で同一と判断できる場合は、normalization agent を呼び出さない。

## normalization

normalization agent は、入力した observation が既存 candidate と同じ issue か、新しい issue かだけを返す。

正確な prompt と起動パラメータは、`{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.py` を正本とする。Structured Output schema は、同 directory の `normalize_issue.json` を正本とする。

normalization agent へ渡す情報を次に限定する。

- 検証済みの構造化 observation
- 機械的に絞り込んだ既存 candidate

normalization agent は、summary、impact、原因、現在性、actionability、human action、verification verdict、または relation を生成しない。候補外の issue を探索せず、repository と feedback state を変更しない。

既存 issue を選ぶ output は、入力候補の issue ID を返さなければならない。新しい issue を選ぶ output は、既存 issue ID を持たない。schema と決定論的事後条件に適合する output を受理できなければ、report 全体を失敗させる。

## verification

### 対象

verification は、次の candidate を issue identity で重複なく統合した集合に対して行う。

- threshold を満たした machine issue candidate
- normalization 後の agent issue candidate
- cut 開始時に active だった全 issue

新しい observation がない active issue も省略しない。active issue を次の generation へ持ち越すには、今回の report cut に対する新しい `unresolved` verdict を必要とする。

candidate の追加、分割、統合、および occurrence 集計は機械的に行う。verification agent に代行させてはならない。

### verdict

verification agent は、1 candidate と、その candidate に許可した report cut reference だけから次の verdict を 1 つ返す。

| verdict | 意味 |
|---|---|
| `unresolved` | report cut 時点でも問題が存在し、現在の作業外にいる人間の対応が必要である。 |
| `resolved` | 問題が report cut 時点では存在しない。 |
| `not_actionable` | 状態は存在しても、人間向け報告基準を満たさない。 |
| `inconclusive` | 許可された reference だけでは判定できない。 |

正確な prompt と起動パラメータは、`{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/verify_issue.py` を正本とする。Structured Output schema は、同 directory の `verify_issue.json` を正本とする。

verification agent は候補外の問題を探索せず、repository、config、feedback state、または問題の根拠を変更しない。

### output の受理条件

schema に加え、次の条件をすべて満たす output だけを受理する。

- candidate ID が入力と一致する。
- current evidence は、その candidate に許可した reference ID だけを使用する。
- `unresolved | resolved | not_actionable` は、1 件以上の concrete current evidence を持つ。
- 同 3 verdict は、少なくとも 1 件の repository content、current fingerprint、または probe result を根拠にする。
- 過去の observation だけを current evidence にしない。
- `unresolved` は、空でない具体的な human action を持つ。
- fingerprint だけでは存在を意味的に確認できない場合は、`unresolved` としない。
- `resolved | not_actionable | inconclusive` の human action は `null` とする。

schema または決定論的事後条件に適合する output を補正後も受理できなければ、AI call failure とする。

## publication の判定

全 candidate が `unresolved | resolved | not_actionable` のいずれかへ確定した場合だけ、正常 publication を行う。

新しい active generation には、次の record だけを含める。

- `unresolved` candidate の compact active issue record
- recurrence threshold 未満の bounded machine aggregate

正常 result は、次の 2 種類とする。

- `ok`: `unresolved` が 0 件
- `attention`: `unresolved` が 1 件以上

`inconclusive`、AI call failure、Structured Output の受理失敗、state corruption、または durable publication failure が 1 件でもあれば、新しい正常 publication を行わない。直前の current pointer を維持し、未検証 candidate や前回の active issue を新しい report として提示しない。

current pointer の切替後に cleanup だけが失敗した場合は、publication 済みの result を巻き戻さない。warning と cleanup manifest path を示し、次回 invocation で cleanup を再開する。

## ユーザー中断と再開

本コマンドは中断可能サブコマンドとする。共通動作は、`{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` を正本とする。

中断要求後は、新しい normalization、verification、correction、retry、または Codex call を開始しない。中断時は新しい active generation、Markdown report、または current pointer を publication しない。

再開に必要な report cut、reference、および正式な checkpoint だけを保持する。次回の `cmoc feedback report` は同じ cut を検証して再開する。cut 固定後の observation は次の cut へ残す。

## report の保存と表示

正常 report は Markdown と YAML Front Matter で構成し、次へ保存する。

```text
{{repo-root}}/.cmoc/gu/ar/report/feedback/{{time-stamp}}.md
```

front matter には、次の情報だけを含める。

- command、生成日時、repo root、および実行時の session branch
- report cut の ID と固定日時
- active generation ID
- verification candidate 数と unresolved issue 数
- `result: ok | attention`

issue 一覧には、`unresolved` だけを安定した issue ID 順で表示する。各 issue には、identity、category、summary、impact、human action、concrete current evidence、occurrence 集計、観測期間、および bounded representative evidence を簡潔に示す。

current evidence は、削除予定の cut 内 reference だけを指す link にしない。人間が report から確認できる path、subject、probe、location、fingerprint、または finding を materialize する。

次の情報は report に表示しない。

- `resolved`、`not_actionable`、`inconclusive`、または未検証の candidate
- threshold 未満の machine aggregate
- normalization、verification、または publication の途中結果
- 前回 report との差分

## 終了コード

- `ok`、`attention`、およびユーザー中断は終了コード 0 とする。
- validation failure、`inconclusive`、AI call failure、state corruption、required cleanup recovery failure、および durable publication failure は終了コード 1 とする。

issue の件数、category、impact、または human action だけを理由に非 0 を返してはならない。終了コードは本コマンド自身の処理結果だけを表し、他 workload の成功判定へ伝播させない。
