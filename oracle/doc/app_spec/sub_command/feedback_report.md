# `cmoc feedback report`

`cmoc feedback report` は、pending observation と直前の active state を report cut に固定し、現在も人間対応が必要な issue だけを新しい active state と Markdown report へ publication する。1 件以上の candidate が `inconclusive` になった場合は正常 publication を行わず、確定済みの判定と blocker を `incomplete` 診断 report へ保存する。

raw observation は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「feedback observation の収集」を正本とする。feedback state の lifecycle は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「feedback の repository-local state」を正本とする。

## CLI 契約

- 位置引数を受け取らない。
- サブコマンド固有 option を受け取らない。
- Git commit を作成しない。
- git working tree と staging area の clean 状態を要求しない。
- 編集 run を作らず、session state と run state を変更しない。

## 事前条件

処理は、次の順序で開始する。

1. doctor preprocess を実行する。
2. main worktree で、`{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「active session context」の条件を確認する。
3. `{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の `run.state` が `ready` であることを確認する。
4. repository-level feedback writer 排他を取得する。
5. current pointer と既存 state の schema、path、hash、および参照整合性を検証する。
6. publication 後の cleanup が残っていれば、先に再開する。
7. terminal な `incomplete` cut の work artifact が残っていれば、state 仕様に従って削除する。
8. 再開可能な report cut があれば再利用し、なければ新しい cut を固定する。

state root または current pointer が存在しない状態は、有効な初期状態とする。既存 state に corruption がある場合は state を変更せず、新しい report を publication しない。

## report cut

report cut が固定する入力と更新可能な処理状態は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「report cut」を正本とする。

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
8. 全 candidate の正式な verification checkpoint をそろえる。
9. 全 candidate が `unresolved | resolved | not_actionable` のいずれかなら、新しい active generation と正常 Markdown report を作る。
10. 1 件以上が `inconclusive` なら、新しい active generation を作らず、`incomplete` 診断 report を作る。
11. 正常 report を作った場合だけ、state 仕様に従って current pointer を切り替え、その後に処理済み input と一時 state を cleanup する。

validation、完全一致 deduplication、machine key 集約、recurrence window、threshold、および候補絞り込みを AI に代行させてはならない。

受理済みの `inconclusive` verdict は、同じ cut の残りの candidate に対する verification を打ち切る理由にしない。別の失敗またはユーザー中断がない限り、全 candidate の verification を完了する。

## 機械処理

### validation

raw observation の schema、path、および canonical hash は、report cut manifest と一致しなければならない。同じ observation ID で hash が異なる場合は corruption とする。

1 件でも validation を通過できない input がある場合は、正常 publication を行わない。invalid input を処理済みとして削除せず、問題の path と理由をエラー terminal result とサブコマンドログに示す。

### machine observation

machine observation は、detector rule が定める canonical key、recurrence window、および distinct dimension だけで集約する。自由文や AI 判断を identity または threshold 判定に使用してはならない。

threshold 未満の aggregate は、人間向け issue や report 項目にしない。threshold を満たした aggregate は 1 件の issue candidate とし、同じ canonical key の active issue があれば機械的に統合する。

### agent observation

agent observation は、観測日時と observation ID による安定した順序で処理する。比較対象には、cut 開始時の active issue と、同じ cut で先に形成した provisional candidate を含める。

agent が入力した deduplication hint は、候補検索にだけ使用する。issue identity の確定根拠にはしない。機械的な完全一致で同一と判断できる場合は、normalization agent を呼び出さない。

## normalization

normalization agent は、入力した observation が既存 candidate と同じ issue か、新しい issue かだけを返す。

正確な prompt part、文面、workload 固有の起動パラメータ、およびその選択理由は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.py` の `build_feedback_normalize_issue_parameter` へ委譲する。Structured Output schema は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.json` の root schema（JSON Pointer `#`）へ委譲する。

normalization agent へ渡す情報を次に限定する。

- 検証済みの構造化 observation
- 機械的に絞り込んだ既存 candidate

normalization agent は、summary、impact、原因、現在性、actionability、human action、verification verdict、または relation を生成しない。候補外の issue を探索せず、repository と feedback state を変更しない。

既存 issue を選ぶ output の issue ID は、入力候補の issue ID と一致しなければならない。schema と決定論的事後条件に適合する output を受理できなければ、report 全体を失敗させる。

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

正確な prompt part、文面、workload 固有の起動パラメータ、およびその選択理由は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/verify_issue.py` の `build_feedback_verify_issue_parameter` へ委譲する。Structured Output schema は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/verify_issue.json` の root schema（JSON Pointer `#`）へ委譲する。

verification agent は候補外の問題を探索せず、repository、config、feedback state、または問題の根拠を変更しない。

### output の受理条件

schema に加え、次の条件をすべて満たす output だけを受理する。

- candidate ID が入力と一致する。
- current evidence は、その candidate に許可した reference ID だけを使用する。
- 同 3 verdict は、少なくとも 1 件の repository content、current fingerprint、または probe result を根拠にする。
- 過去の observation だけを current evidence にしない。
- fingerprint だけでは問題の存在を意味的に確認できない場合は、`inconclusive` とする。

schema または決定論的事後条件に適合する output を補正後も受理できなければ、AI call failure とする。

## 結果と正常 publication

### 正常 result

全 candidate が `unresolved | resolved | not_actionable` のいずれかへ確定した場合だけ、正常 publication を行う。

新しい active generation の record 構成は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「active generation」を正本とする。

正常 result は、次の 2 種類とする。

- `ok`: `unresolved` が 0 件
- `attention`: `unresolved` が 1 件以上

### `incomplete` result

全 candidate の verification output を受理でき、1 件以上が `inconclusive` であり、診断 report を durable に保存して report cut を terminal な `incomplete` として確定できた場合は `result: incomplete` とする。`inconclusive` は、正常 publication を完了できなかった report processing blocker であり、`unresolved` または active issue ではない。

`incomplete` の durable 保存、state transition、および cleanup の禁止は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「incomplete 診断 report」を正本とする。確定済み checkpoint を新しい active generation へ部分 publication してはならない。

validation failure、AI call failure、Structured Output の受理失敗、state corruption、または durable publication failure を `incomplete` として扱ってはならない。`inconclusive` の checkpoint があっても、全 candidate の verification output を受理できなければ `incomplete` 診断 report を作らない。

正常 publication と `incomplete` のどちらも成立しない場合は、新しい正常 publication を行わない。直前の current pointer を維持し、未検証 candidate や前回の active issue を新しい report として提示しない。

current pointer の切替後に cleanup だけが失敗した場合は、publication 済みの result を巻き戻さない。terminal result の warning に cleanup manifest path を含め、次回 invocation で cleanup を再開することを次の操作として示す。終了コードは 0 とする。

## ユーザー中断と再開

本コマンドは中断可能サブコマンドとする。共通動作は、`{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` を正本とする。

中断要求後は、新しい normalization、verification、correction、retry、または Codex call を開始しない。中断時は新しい active generation、正常 report、`incomplete` 診断 report、または current pointer を publication しない。

再開に必要な report cut、reference、および正式な checkpoint だけを保持する。次回の `cmoc feedback report` は同じ cut を検証して再開する。cut 固定後の observation は次の cut へ残す。

terminal な `incomplete` cut は、中断または失敗した cut の再開対象にしない。

## `incomplete` 後の再実行

人間が `inconclusive` の原因を修正した後は、次の明示的な `cmoc feedback report` で candidate を再検証する。この invocation は、直前の `incomplete` cut と checkpoint を再利用せず、新しい report cut と reference を固定する。raw observation と直前の正常 active state は、新しい cut の入力として維持する。

再検証後は、本書の「結果と正常 publication」に従って verdict を処理する。

## report の保存と表示

正常 report と `incomplete` 診断 report の front matter に共通する項目を次に示す。

- command
- 生成日時
- repo root
- 実行時の session branch

### 正常 report

正常 report は Markdown と YAML Front Matter で構成し、次へ保存する。

```text
{{repo-root}}/.cmoc/gu/ar/report/feedback/{{time-stamp}}.md
```

保存した正常 report を primary report とする。terminal result に `result: ok | attention` を含める。

front matter には、共通項目に加えて次の情報だけを含める。

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

### `incomplete` 診断 report

`incomplete` 診断 report は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「incomplete 診断 report」が定める path へ、正常 report と別の Markdown file として durable に保存する。

保存した `incomplete` 診断 report を primary report とする。terminal result に `result: incomplete` を含める。次の操作として、人間が `inconclusive` の原因を修正した後に `cmoc feedback report` を再実行することを示す。

`incomplete` 固有の front matter には、共通項目に加えて次の情報だけを含める。

- report cut の ID と固定日時
- verification candidate 数、`unresolved` 数、および `inconclusive` 数
- `result: incomplete`

active generation ID は含めない。診断 report の先頭には、正常 publication が成立していないことを明示する。直前の正常 publication が current のままであることも明示する。

診断 report の本文には、次の独立したセクションをこの順序で設ける。

1. `確定済みだが今回未 publication の unresolved candidate`
2. `inconclusive candidate`

確定済みの `unresolved` candidate は、安定した candidate ID 順で表示する。各 candidate には、identity、category、summary、impact、verification reason、human action、および concrete current evidence を示す。このセクションの verdict は診断情報であり、今回の新しい active generation へ publication 済みではないことを明示する。直前の正常 active generation に同じ issue が含まれる可能性と、今回の publication が成立していないことを混同させてはならない。

`inconclusive` candidate も、安定した candidate ID 順で表示する。各 candidate には、candidate ID、summary、判定不能となった reason、および確認できた current evidence を示す。current evidence が空の場合は、確認できた evidence がないことを明示する。

両セクションの current evidence は、削除され得る report cut reference だけを指す link にしない。人間が診断 report だけから確認できる path、subject、probe、location、fingerprint、または finding を materialize する。

### 中断・エラー時の invocation summary report

`user_interruption` と `error` では、正常 report または `incomplete` 診断 report の代わりに、今回の invocation summary report を primary report として保存する。事前条件違反など、report cut の固定前に確定したエラーも対象とする。

正常 report、`incomplete` 診断 report、または publication の失敗は、invocation summary report を伴う `error` とする。invocation summary report 自体を保存できない場合だけ、共通の report 保存基盤に関する internal failure とする。

invocation summary report は Markdown と YAML Front Matter で構成し、次へ保存する。

```text
{{repo-root}}/.cmoc/gu/ar/report/feedback/invocation/{{time-stamp}}.md
```

front matter には、次の情報を含める。

- command、生成日時、repo root、および確定できた場合の session branch
- terminal result の共通分類と終了コード
- report cut の ID と固定日時。cut を固定していない場合は `null`
- 正常 publication、`incomplete` 診断、および current pointer 更新の実行状況

本文には、今回の invocation で開始・完了した処理段階、確定済みの checkpoint と部分結果の件数、中断またはエラーの理由、維持した state、未実行の publication と cleanup、必要な次の操作、および関連する診断用サブコマンドログと Codex call log を要約する。

invocation summary report は feedback publication または active state の一部ではなく、current pointer の参照先にしない。candidate を publication 済みの issue または active issue として扱ってはならない。中断時の保存は、正式な feedback Markdown report の publication には該当しない。

## 終了コード

- `ok`、`attention`、`incomplete`、およびユーザー中断は終了コード 0 とする。
- validation failure、AI call failure、Structured Output の受理失敗、state corruption、required cleanup recovery failure、診断 report の durable 保存失敗、および durable publication failure は終了コード 1 とする。

終了コードは、今回の invocation が利用可能な report result を終端状態として確定できたかを表す。直前の正常 report が current のまま残っていること、または一般的なエラー説明を出力できたことだけでは、今回の invocation が report result を確定したとはみなさない。

issue の件数、category、impact、または human action だけを理由に非 0 を返してはならない。終了コードは本コマンド自身の処理結果だけを表し、他 workload の成功判定へ伝播させない。
