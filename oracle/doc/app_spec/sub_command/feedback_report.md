# `cmoc feedback report`

本書は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` が定義する issue candidate の機械処理、normalization、verification、および人間向け report の publication を定める。raw observation は `{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md`、repository-local active state と atomic publication は `{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` を正本とする。

## 引数

- 位置引数を受け取らない。
- サブコマンド固有 option を受け取らない。

## 事前条件と処理開始順序

次の順序で report を開始する。

1. doctor preprocess を実行する。
2. session と run の事前条件を検証する。
3. repository-level feedback writer 排他を取得する。
4. repository-local feedback state の schema、hash、path、および参照整合性を検証する。
5. current pointer の切替後に未完了の cleanup があれば、完了済み report cut manifest から再開する。
6. 再開可能な report cut があれば検証して再開し、なければ新しい report cut を固定する。

session と run の事前条件を次に示す。

- main worktree 上の active な `{{cmoc-session-branch}}` が checkout されている。
- 対応する session state の `session.state=active` である。
- `run.state=ready` である。

report は Git commit を作成しない。git working tree と staging area の clean 状態は事前条件にしない。

report は編集 run を作らず、session state と run state を変更しない。feedback state は `{{repo-root}}` に属し、現在の branch には属さない。

state root または current pointer が存在しない状態は有効な初期状態とする。既存 state に整合性違反または corruption がある場合は state を変更せず、正常 report を publication しない。

## report cut

新しい report cut は、doctor preprocess と repository-level feedback writer 排他取得の後に固定する。cut は今回の report 要求が評価する時点を表す。

cut では、少なくとも次の入力を固定する。

- 今回処理する全 pending observation
- current pointer が指す active generation、前回から保持している全 active issue、および全 bounded machine aggregate
- 各 candidate の現在状態を確認するための repository 内参照内容または fingerprint
- allowlist 済み current-state probe が必要な場合は、その入力と結果
- normalization、verification、および決定論的処理規則の version

cut の manifest、reference ID、hash、および durability は `{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` を正本とする。

cut の固定後に追加された observation は今回の manifest に加えず、次回 report の対象とする。normalization agent または verification agent が reporter へ新しい observation を送信した場合も同じとする。

report-time agent に live repository state を後から読ませてはならない。agent へ渡す現在参照は、report cut に固定した content、excerpt、fingerprint、または probe result に限定する。cut の参照だけでは現在状態を判断できない candidate は `inconclusive` とする。

current-state probe は、stable probe ID、型付き入力、固定した実行対象、timeout、出力上限、および secret masking が事前定義された allowlist entry だけを使用する。probe は read-only とし、repository、外部 state、または feedback state を変更してはならない。agent に command、引数、環境変数、または追加 probe を選ばせてはならない。適合する probe がない場合は arbitrary shell command で補わず、固定済み repository reference だけで検証する。

## 処理フロー

report cut は、次の順序で処理する。

1. observation と既存 active state の schema、hash、path、および参照整合性を機械検証する。
2. 完全に同じ observation を除去する。
3. machine observation を canonical key で集約する。
4. recurrence window 外の occurrence を集計から除外する。
5. threshold 未満の machine observation は issue を作らず、bounded aggregate として次の active generation 候補へ保持する。
6. agent observation の比較候補を category、evidence subject、および fingerprint などの安定情報で機械的に絞る。
7. issue の同一性を完全一致で決められない場合だけ normalization agent を使用する。
8. normalization 後の全 issue candidate と、前回から残る全 active issue を verification agent で検証する。
9. 全 candidate の検証が成功した場合だけ、Markdown report と新しい active generation を作成し、current pointer を切り替える。
10. current pointer の切替後に、処理済み raw observation、解決済みまたは報告対象外の issue、切替前の active generation、および完了済み一時 state を削除する。

機械的な順序を変更して、AI に validation、完全一致 deduplication、canonical key 集約、recurrence window、threshold、または候補絞り込みを代行させてはならない。

## validation と完全一致 deduplication

raw observation の schema と hash は、report cut manifest の値と一致しなければならない。同じ observation ID と同じ canonical SHA256 は同一 observation として 1 回だけ処理する。同じ ID で hash が異なる場合は corruption として停止する。

schema 不正、path 違反、参照不整合、または hash 不一致の observation を invalid receipt として処理済みにしてはならない。1 件でも validation を通過できない入力がある場合は、新しい正常 report と active generation を publication せず、問題の path と理由を console と subcommand log に示す。

完全一致 deduplication の結果は永続 state に保存しない。正常 publication 後は、同じ cut に含まれた重複 raw observation も処理済み入力として削除する。

## machine observation の集約

machine observation は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` が定める canonical key、recurrence scope、および rule-defined threshold dimension だけで決定論的に集約する。自由文、AI 判断、または session ID を canonical key へ追加してはならない。

前回の bounded aggregate と今回の observation を合わせ、rule の recurrence window 外にある occurrence と threshold dimension digest を先に除外する。window 内の distinct recurrence 条件が threshold を満たさない場合は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` が定める bounded aggregate だけを保持する。

threshold 未満の aggregate は issue candidate、active issue、または人間向け report の項目にしてはならない。threshold を満たした machine aggregate は 1 件の issue candidate とし、同じ canonical key の active issue がある場合は機械的に統合する。

## agent observation の候補絞り込み

agent observation は、次の安定情報で既存 issue candidate の比較候補を機械的に絞る。

- category
- evidence の subject type と正規化済み repository path
- observation 時点と report cut 時点の fingerprint
- agent が入力した deduplication hint

既存 issue candidate の候補 pool には、report cut 開始時の active issue と、同じ cut で先に形成した provisional issue candidate を含める。agent observation は `observed_at`、次に observation ID の辞書順で処理し、同じ cut 内の同一 issue を重複作成しない。

deduplication hint は検索 hint にだけ使用し、canonical key または同一性の確定根拠にしてはならない。機械的な完全一致で既存 issue candidate と同一と決まる場合は normalization agent を呼び出さない。

## normalization agent

曖昧な同一性判断だけに `build_feedback_normalize_issue_parameter` を使用する。builder は `{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.py`、専用 schema は `{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.json` を正本とする。

normalization agent の入力は、次の情報に限定する。

- 検証済みの構造化 observation
- 機械的に絞り込んだ既存 issue candidate。active issue と同じ cut の provisional issue candidate を含む

normalization agent は、既存 candidate と同一か、新しい issue かだけを返す。summary、impact、原因、現在の存在可能性、actionability、human action、verification verdict、または relation を生成してはならない。

raw Codex call log、元の Codex session、report cut の現在参照、feedback 保存 file、および候補外 issue を追加調査してはならない。file access mode は `READONLY` とし、feedback state を編集しない。

既存 issue を選ぶ output の issue ID は入力 candidate に含まれていなければならない。新規 issue を選ぶ場合は existing issue ID を `null` とする。schema と決定論的事後条件に適合しない output は、Codex call の共通 Structured Output 規則に従って補正する。正式な output を受理できない場合は report 全体を失敗させる。

## verification candidate

verification の対象集合は、次の candidate を issue identity で重複なく統合した集合とする。

- threshold を満たした machine issue candidate
- normalization 後の agent issue candidate
- report cut 開始時に current だった全 active issue

新しい observation がない active issue、fingerprint が変化していない active issue、および前回と同じ内容に見える active issue も省略してはならない。active issue を新しい generation へ持ち越すには、今回の report cut に対する新しい `unresolved` verdict が必要である。

candidate の summary、impact、occurrence aggregate、および参照対象は、機械的な統合結果から構築する。verification agent に candidate の追加、分割、統合、または探索を依頼してはならない。

## verification agent

各 candidate の検証には `build_feedback_verify_issue_parameter` を使用する。builder は `{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/verify_issue.py`、専用 schema は `{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/verify_issue.json` を正本とする。

agent call は 1 candidate と、その candidate に許可した report cut reference だけを入力とする。file access mode は `READONLY` とするが、report cut に含まれない file、live repository state、raw log、過去 session、別 candidate、または feedback state を読んではならない。

verification agent は、次の verdict から 1 つを返す。

- `unresolved`
    - report cut 時点でも問題が存在し、現在の作業外にいる人間の対応が必要である。
- `resolved`
    - 問題が report cut 時点では存在しない。
- `not_actionable`
    - 状態は存在しても、feedback の人間向け報告基準を満たさない。
- `inconclusive`
    - 許可された report cut reference だけでは判定できない。

verification agent は候補外の問題を探索しない。feedback state、repository file、config、または問題の根拠を自動修正してはならない。

## verification output の受理条件

Structured Output schema に加え、次の決定論的事後条件をすべて満たす output だけを正式な verification result として受理する。

- output の candidate ID が入力 candidate ID と完全一致する。
- current evidence の reference ID が、その candidate に許可された report cut reference に存在する。
- `unresolved | resolved | not_actionable` は 1 件以上の具体的な current evidence を持つ。
- `unresolved | resolved | not_actionable` の current evidence は、少なくとも 1 件の `repository_content | current_fingerprint | probe_result` を参照する。
- 過去の observation だけを current evidence とした `unresolved | resolved | not_actionable` を受理しない。
- `unresolved` は空でない具体的な human action を持つ。
- fingerprint だけでは問題の存在を意味的に確認できない場合、fingerprint の一致だけを根拠とした `unresolved` を受理しない。
- `resolved | not_actionable | inconclusive` の human action は `null` である。

`unresolved` の current evidence は、report cut の具体的な subject、path、location、field、または probe result を指し、問題が現在も存在する理由を人間が確認できる説明を含む。

schema validation または決定論的事後条件の補正を尽くしても正式な output を受理できない場合は、AI call failure とする。`inconclusive` は schema 上有効でも正常 publication を許可しない。

## 全候補が確定しない場合

次のいずれかが 1 件でも発生した場合は、新しい正常 report と active generation を publication しない。

- `inconclusive`
- normalization または verification の AI call failure
- Structured Output の受理失敗
- report cut、active state、または input の corruption
- current pointer を含む durable publication failure

未検証 candidate、`inconclusive` candidate、または前回の active issue を、新しい人間向け issue として提示してはならない。直前の current pointer が指す正常 report と active generation を、引き続き正常な最新状態として維持する。

失敗理由、candidate ID、再開可能性、および一時 state の path は console と subcommand log から判別可能にする。正式な checkpoint と再開 state の retention は `{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` に従う。

## 正常 publication

全 verification candidate が `unresolved | resolved | not_actionable` のいずれかへ確定した場合だけ、正常 publication へ進む。

新しい active generation には、次の record だけを含める。

- `unresolved` candidate ごとの compact active issue record
- recurrence threshold 未満の bounded machine aggregate

`resolved` と `not_actionable` の candidate は、新しい active generation と人間向け issue 一覧に含めない。処理済み observation は、current pointer の切替後に cleanup する。

正常 result は、次の 2 種類だけとする。

- `ok`: 全 candidate の検証が完了し、`unresolved` が 0 件である。
- `attention`: 全 candidate の検証が完了し、`unresolved` が 1 件以上ある。

active generation、Markdown report、current pointer、および切替後 cleanup の順序は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の atomic publication を正本とする。切替前の active generation または処理済み observation を current pointer の切替前に削除してはならない。

current pointer の durable な切替後に cleanup だけが失敗した場合は、publication 済みの `ok | attention` と current pointer を巻き戻さない。その invocation は cleanup 未完了の warning と manifest path を console と subcommand log に示す。次回 invocation は cleanup を再開し、完了できない場合は新しい report cut を作らずエラー終了する。

## ユーザー中断と再開

このコマンドは中断可能サブコマンドとし、共通動作は `{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` を正本とする。

中断要求後は、新しい normalization、verification、correction、retry、または Codex call を開始しない。実行中 call から正式な output を安全に受理できた場合は checkpoint として保存してよい。それ以外は未完了として扱う。

中断時は Markdown report、active generation、または current pointer を新たに publication しない。report cut manifest、固定済み reference、および正式な checkpoint だけを保持する。次回の `cmoc feedback report` は同じ report cut を検証して再開し、cut 固定後に追加された observation は次の cut へ残す。

中断による完了は共通規則どおり正常系とするが、`ok | attention` の正常 report result ではない。console と subcommand log から中断と再開対象 cut を判別可能にする。

## report の保存と表示

正常 report は Markdown + YAML Front Matter とし、次へ保存する。

```text
{{repo-root}}/.cmoc/gu/ar/report/feedback/{{time-stamp}}.md
```

front matter は、次の field に限定する。

- `command`: `cmoc feedback report`
- `generated_at`
- `repo_root`
- `session_branch`: 実行 context であり、feedback state の所有者ではない
- `report_cut_id`
- `report_cut_at`
- `active_generation_id`
- `verification_candidate_count`
- `unresolved_issue_count`
- `result`: `ok | attention`

issue 一覧には `unresolved` だけを issue ID の辞書順で表示する。各 issue には、次の現在情報を簡潔に示す。

- issue ID、category、summary、および impact
- verification agent が確定した human action
- report cut の対象を指す concrete current evidence
- occurrence count と affected session count
- 最初と最後の観測日時
- bounded な representative evidence

current evidence は cut-scoped reference ID を manifest で解決し、repository path、subject、probe ID、location、fingerprint、および finding のうち該当する情報を report 内へ materialize する。削除予定の work artifact だけを指す link にしてはならない。

次の情報は front matter、issue 一覧、差分要約、または補助 section に表示してはならない。

- `resolved` または `not_actionable` の candidate
- `inconclusive` または未検証の candidate
- threshold 未満の machine aggregate
- normalization、verification、または publication の途中結果
- 前回 report との差分

過去の Markdown report は、今回の issue 表示、deduplication、処理済み判定、state 差分、または今回の publication 可否の入力にしない。artifact 自体の retention は active state の compaction と分離する。

## 終了コード

- `ok` と `attention` は終了コード 0 とする。
- ユーザー中断は、共通の中断規則に従って終了コード 0 とする。
- validation failure、`inconclusive`、AI call failure、state corruption、required cleanup recovery failure、および durable publication failure は終了コード 1 とする。

issue の件数、category、impact、または human action だけを理由に非 0 を返してはならない。この終了コードは `cmoc feedback report` 自身の処理結果だけを表し、他 workload の成功判定へ伝播させない。
