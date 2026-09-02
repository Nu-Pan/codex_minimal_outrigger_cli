# `cmoc feedback report`

`cmoc feedback report` は、同一 invocation 内で feedback remediation run を作成し、安全な realization file の修正を issue 単位で commit して session branch へ自動 join する。正常 publication には、join 後も `human_required` である issue だけを掲載する。

raw observation は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「feedback observation の収集」を正本とする。結果分類は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「用語と結果分類」を正本とする。repository-local state は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「feedback の repository-local state」を正本とする。

## CLI 契約

- 位置引数を受け取らない。
- サブコマンド固有 option を受け取らない。
- 公開 CLI は `cmoc feedback report` のままとする。
- 正常経路では、利用者に別の fork、join、または remediation 操作を要求しない。
- doctor preprocess と必要な indexing preflight が作成する commit 以外に、session branch 上の既存差分を自動 commit してはならない。
- git 未コミット差分を自動 stash、commit、revert、または破棄してはならない。

## 事前条件と run の開始または再開

共通の開始処理は、次の順序で行う。

1. doctor preprocess を実行する。
2. main worktree で必要な indexing preflight を完了する。
3. `{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「active session context」の条件を確認する。
4. session worktree と staging area が clean であることを確認する。
5. repository-level feedback writer 排他を取得する。
6. current pointer、pending recovery、および既存 feedback state の schema、path、hash、branch reference の整合性を検証する。
7. 自動 join 済み feedback run の publication または publication 後 cleanup を再開できる場合は、後述する recovery を先に完了する。
8. recovery 対象がない場合は、session state の `run.state` が `ready` であることを確認する。
9. `run.kind=feedback_report` として `{{cmoc-run-branch}}` と `{{cmoc-run-worktree}}` を作成し、`run.state=running` とする。
10. collector の最初の high-watermark を確定し、最初の intake wave を固定する。

clean 検査は doctor preprocess と indexing preflight の完了後に行う。新しい run の開始経路では `run.state=ready` を必須とする。後述する join 後 recovery は新しい run を開始しないため、この事前条件の例外とする。

recovery 対象ではない active run が残っている場合、または事前条件に違反した場合は、新しい run を作らない。既存の worktree、staging area、raw observation、および current pointer を変更しない。

run の branch、commit、および worktree の定義は、`{{cmoc-root}}/oracle/doc/branch_model.md` の「cmoc の branch model」を正本とする。run の一般 lifecycle と隔離境界は、`{{cmoc-root}}/oracle/doc/app_spec/run_isolation.md` の「run 作業隔離規則」を正本とする。

## feedback remediation run

feedback remediation run は、1 回の `cmoc feedback report` invocation に対応する self-joining 編集 run とする。正常な wave loop の完了後は、同 invocation 内で run branch を session branch へ自動 join する。

run branch 上の想定内差分を次に示す。

- issue remediation agent が変更した realization file
- cmoc が変更した、realization file の変更に必要な tracked `INDEX.md`
- cmoc が同期した tracked refactor state
- workload 固有仕様が issue 処理単位で必要とするその他の tracked な機械生成物

repository-local feedback state、subcommand log、および Codex call log は `{{repo-root}}/.cmoc/gu` 側に保存し、run branch の commit に含めない。issue commit と正式な feedback checkpoint は、commit ID と hash で相互に結び付ける。

正常完了時の自動 join、ユーザー中断またはエラー後の `cmoc run join` と `cmoc run abandon`、想定内差分、および recovery の共通境界は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「編集 run の共通仕様」を正本とする。

## intake の validation と normalization

### validation

各 raw observation の schema、path、および canonical hash は、対応する intake wave と一致しなければならない。同じ observation ID で hash が異なる場合は corruption とする。

schema version 1 の pending observation は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「reporter input v1 の互換処理」に従って扱う。raw record を移行のために書き換えてはならない。

1 件でも validation を通過できない input がある場合は、正常 publication を行わない。invalid input を処理済みとして削除せず、path と理由を invocation report と subcommand log に示す。

### machine observation

machine observation は、detector rule が定める canonical key、recurrence window、および distinct dimension だけで集約する。自由文や AI 判断を identity または threshold 判定に使用してはならない。

threshold 未満の aggregate は、人間向け issue や remediation call の対象にしない。threshold を満たした aggregate は 1 件の issue candidate とし、同じ canonical key の active issue があれば機械的に統合する。

### agent observation と normalization

agent observation は、観測日時と observation ID による安定した順序で処理する。比較対象には、run 開始時の active issue と、同じ run で先に形成した issue candidate を含める。

agent が入力した deduplication hint は、候補検索にだけ使用する。issue identity の確定根拠にはしない。機械的な完全一致で同一と判断できる場合は、normalization agent を呼び出さない。

normalization agent は、入力した observation が既存 candidate と同じ issue か、新しい issue かだけを返す。normalization は issue identity を確定する責務であり、issue remediation call には数えない。

正確な prompt part、文面、workload 固有の起動パラメータ、およびその選択理由は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.py` の `build_feedback_normalize_issue_parameter` へ委譲する。Structured Output schema は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.json` の root schema（JSON Pointer `#`）へ委譲する。

normalization agent へ渡す情報を次に限定する。

- 検証済みの構造化 observation
- 機械的に絞り込んだ既存 issue candidate

normalization agent は、summary、impact、原因、現在性、actionability、remediation result、human action、または relation を生成しない。候補外の issue を探索しない。

既存 issue を選ぶ output の issue ID は、入力候補の issue ID と一致しなければならない。schema と宣言済みの決定論的事後条件に適合する output を受理できなければ、invocation error とする。

## 1 issue identity の処理単位

### call 回数と順序

正規化済み issue identity 1 件につき、同じ feedback remediation run 内で issue remediation agent call を最大 1 回実行する。

- remediation call は feedback 固有の安定した `agent_call_kind` を使用する。
- issue ID は runtime input とし、`agent_call_kind` に含めない。
- Structured Output correction、retry、および quota 待機後の resume は、同じ論理 agent call として数える。
- 同じ issue identity に複数の remediation agent を起動しない。
- issue remediation call は、同じ run branch の最新状態を順に参照できるよう逐次実行する。
- write 権限を持つ issue remediation call を並列実行しない。

各 wave 内の issue identity は、安定した issue ID 順で処理する。

### issue remediation agent call

issue remediation agent call は、1 issue の現在状態の確認、realization file だけで可能な修正、および修正後の検証を同じ call 内で行う。

正確な prompt part、文面、workload 固有の起動パラメータ、およびその選択理由は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/remediate_issue.py` の `build_feedback_remediate_issue_parameter` へ委譲する。Structured Output schema は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/remediate_issue.json` の root schema（JSON Pointer `#`）へ委譲する。

call の境界を次に示す。

- `FileAccessMode.REALIZATION_WRITE` を使用する。
- cwd は `{{cmoc-run-worktree}}` とする。
- oracle file は読めるが変更できない。
- realization file だけを agent の変更対象とする。
- agent に feedback state file、Git index、branch、commit、または worktree lifecycle を操作させない。
- agent に `git add` または `git commit` を実行させない。
- candidate 外の issue を remediation 対象として探索させない。

issue remediation call の既定は OpenAI の GPT-5.6 Luna、Reasoning Effort Max とする。provider、model、および reasoning effort の正確な設定値は、`{{cmoc-root}}/oracle/src/oracle/other/cmoc_config.py` の `CmocConfigCodex.agent_calls` が所有する。設定値を prompt 文面へ注入してはならない。

### Structured Output と結果分類

agent は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「用語と結果分類」が定める issue remediation result を 1 つ返す。`human_required` は、realization file の編集だけでは満たせない対応を具体的な evidence で確認できた場合だけ使用する。処理の失敗は result に変換せず、invocation error とする。

`inconclusive` があっても、残りの issue は可能な限り処理する。

### net 差分と機械的受理条件

cmoc は、論理 agent call の開始時点から正式な終了時点までの realization file の net 差分を算出する。Structured Output correction 中の差分不変性は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「補正 turn の実行条件」を正本とする。

正式な output には、schema に加えて次の決定論的事後条件をすべて要求する。

- output の issue ID が入力 issue identity と一致する。
- schema の `changed_paths` に重複がなく、そこから得る path 集合が実際の realization file の変更 path 集合と一致する。
- path は正規化済みの `{{work-root}}` 相対 path であり、追加と変更は終了時点、削除は開始時点、rename は rename 前後の path で表す。
- `fixed` は 1 件以上の実際の realization 差分と、成功した修正後 verification を持つ。
- `already_resolved`、`not_actionable`、および `inconclusive` は実際の差分を持たない。
- `human_required` が差分を持つ場合、その差分は独立して安全であり、必要な verification が成功している。

`changed_paths` の照合とは別に、run worktree の全 net 差分を検査する。oracle file、禁止 path、または workload の想定外 path に変更があれば、その処理単位を確定してはならない。

この検査は workload の commit 受理条件であり、file access mode 違反の判定またはリカバリとして扱わない。`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「ファイルアクセス制限違反の事後検証とリカバリ」を変更しない。

agent が返した `fixed` の自己申告だけを、意味的な正しさの証明として扱ってはならない。agent が必要な検証を実行して結果を報告し、cmoc が schema、決定論的事後条件、差分、および検証記録を照合できる場合だけ正式な結果とする。

### issue 単位の commit と rollback

受理済み結果ごとに、cmoc は次の処理を 1 つの整合した issue 単位として行う。

1. agent の realization 差分と verification result を検査する。
2. 必要な `INDEX.md`、refactor state、および tracked processing state を機械的に同期する。
3. 想定内差分と変更禁止対象を再検査し、run branch の 1 commit として確定する。
4. commit ID と正式な result を feedback checkpoint に durable 保存する。

実際の tracked 差分が空の場合は、空 commit を作らない。`already_resolved`、`not_actionable`、および差分のない `human_required` は、commit なしの正式な checkpoint としてよい。

`human_required` であっても、安全で独立して検証済みの部分修正は同じ issue commit に残してよい。安全に部分確定できない変更は、処理単位全体を agent call 開始時点へ rollback する。

commit が成功する前に `fixed` として publication、active state からの除外、または observation cleanup を行ってはならない。commit または rollback 後は、次の issue call を開始する前に run worktree と staging area が整合した clean 状態でなければならない。

処理単位の考え方は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の「1 処理単位」、「完了」、「ユーザー中断」、および「その他のエラー」を参考にする。ただし、refactor state の `investigation_required` または current fork の unresolved target 集合を feedback issue state として流用してはならない。

## intake wave loop

単一の可変 report cut は作らない。intake wave と high-watermark の state 契約は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「intake wave と high-watermark」を正本とする。

各 wave の終了時は、次の順序で停止判定を行う。

1. wave に含まれる全 issue identity を終端結果まで処理する。
2. wave の remediation agent call に対応する reporter context を close し、受付済み submission を drain する。
3. collector が durable に受理済みの observation に対する high-watermark を atomic に確定する。
4. 前回境界より後、今回の high-watermark 以前にある observation を validation、normalization、および deduplication する。
5. 新しい未処理 issue identity があれば、次の immutable な intake wave を作成する。
6. 新しい未処理 issue identity がなければ、wave loop を自然完了する。

次の入力だけを理由に、新しい remediation call または wave を増やしてはならない。

- 既知 issue の完全な重複 observation
- current run ですでに remediation call を実行した同一 issue identity
- current run で `fixed`、`already_resolved`、`not_actionable`、または `human_required` と確定した issue identity

同一 issue に追加された evidence は、最終判定の説明と occurrence 集計へ反映してよい。同じ run で 2 回目の remediation agent を起動してはならない。

最終 high-watermark より後に受理された observation は、次回の `cmoc feedback report` に pending として残す。quiet period、directory の列挙タイミング、または一定時間 observation がなかったことを停止条件にしてはならない。

新しい異なる issue が継続的に発生する限り自然完了しない。issue 数、wave 数、または実行時間による任意の上限を設けない。ユーザー中断と続行不能な失敗だけを別の停止経路とする。

## 自動 join と join 後の確定

wave loop が自然完了した場合は、全 issue の正式な checkpoint と最終 high-watermark を report cut に封印し、`run.state=joinable` とする。その後、同じ invocation 内で `cmoc run join` と同じ差分検査および merge 契約を使用して自動 join する。

自動 join 前に、`fixed` としての publication または observation cleanup を行ってはならない。

merge または no-op join と post-join の後、issue commit の到達可能性、変更 path、必要な機械生成物、および publication evidence を join 後の session tree に対して検証する。publication と workload 固有 cleanup が完了するまで `run.state=joinable` と隔離資源を維持する。

merge conflict、差分不整合、または join 後検査失敗では正常 publication を行わない。run を `error` とし、run branch、run worktree、issue commit、raw observation、直前の current pointer、および診断情報を保持する。

## publication

### 正常 publication

全 issue が `fixed | already_resolved | not_actionable | human_required` のいずれかに確定し、自動 join と join 後検査が成功した場合だけ正常 publication を行う。

新しい active generation と正常 Markdown report には、`human_required` だけを含める。

正常 result は、次の 2 種類とする。

- `ok`: `human_required` が 0 件
- `attention`: `human_required` が 1 件以上

atomic publication と cleanup の順序は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「正常 report の atomic publication」を正本とする。

issue commit ID、変更 path、agent verification、および cmoc の機械検査結果は、監査可能な run report、invocation report、または subcommand log に残してよい。自動修正済み issue の詳細を正常な feedback issue 一覧へ掲載してはならない。

### `incomplete`

`inconclusive` が 1 件以上ある場合も、残りの issue を可能な限り終端結果まで処理し、安全な issue commit を自動 join する。自動 join と join 後検査が成功した後に、正常 publication の代わりとして `incomplete` 診断 report を durable 保存する。

`incomplete` では、新しい active generation を作らず、current pointer と raw observation を維持する。`inconclusive` を `human_required` へ変換しない。

validation 失敗、agent call failure、Structured Output 受理失敗、差分検査失敗、commit 失敗、state corruption、merge 失敗、または durable report 保存失敗を `incomplete` として扱ってはならない。

### join 後の publication failure

自動 join 後の publication または cleanup に失敗した場合は、`run.state=error` とする。merge と publication point を巻き戻さず、raw observation、current pointer、および recovery に必要な run artifact を保持する。

次回の `cmoc feedback report` は、state と immutable artifact から同じ run の join 成功と未完了処理を一意に特定し、join 後 tree を再検証できる場合だけ、その publication または cleanup を idempotent に再開する。新しい wave または Codex call は開始しない。安全に再開できない場合は `run.state=error` と資源を維持する。

## ユーザー中断

本コマンドは中断可能サブコマンドとする。共通動作は、`{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` の「サブコマンドのユーザー中断」を正本とする。

`Ctrl+C` は issue remediation agent call 中を含む wave loop の実行中に受け付ける。要求後は新しい agent call や retry を開始せず、実行中の issue 処理単位を commit または rollback で整合させる。自動 join と publication は行わず、`run.state=joinable` として確定済み commit、raw observation、current pointer、および必要な checkpoint を保持する。

中断後は、`cmoc run join` で確定済み issue commit を session branch へ取り込むか、`cmoc run abandon` で run を破棄する。どちらの場合も feedback publication は行わず、次の `cmoc feedback report` が現在の session tree と pending observation を再確認する。

自動 join の開始後は、merge または no-op join、join 後 tree 検査、publication、および cleanup を中途半端な状態で中断しないため、workload 固有の不可分な finalization とする。この区間の process interruption または操作失敗はユーザー中断の部分結果へ変換せず、自動 join の成否に応じて本書の recovery または続行不能な失敗として扱う。

## 続行不能な失敗

続行不能な失敗では、実行中の issue 処理単位を正式な結果と commit まで確定できる場合だけ commit し、それ以外は処理単位全体を rollback する。その後 `run.state=error` とする。

確定済み issue commit、run branch、run worktree、raw observation、直前の current pointer、正式な checkpoint、および再確認に必要な診断情報を保持する。正常 publication、`incomplete` 診断 report、および observation cleanup は行わない。

agent call failure、tool 失敗、validation 失敗、差分検査失敗、commit 失敗、および orchestration 失敗を feedback issue または `human_required` に変換してはならない。

quota 枯渇、retry、Structured Output correction、および resume の扱いは、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の `codex exec` 呼び出し規約を正本とする。

## report の保存と表示

### 正常 report

正常 report は Markdown と YAML Front Matter で構成し、次へ保存する。

```text
{{repo-root}}/.cmoc/gu/ar/report/feedback/{{time-stamp}}.md
```

保存した正常 report を primary report とする。front matter には、少なくとも次の情報を含める。

- command、生成日時、repo root、および session branch
- feedback run ID、run branch、run fork commit、および run join commit。no-op join では run join commit を `null` とする
- report cut ID、最終 high-watermark、および wave 数
- remediation 対象 issue 数と `human_required` issue 数
- `result: ok | attention`

issue 一覧には、`human_required` だけを安定した issue ID 順で表示する。各 issue には、identity、category、summary、impact、human action、concrete current evidence、occurrence 集計、観測期間、および bounded representative evidence を簡潔に示す。

current evidence は、削除予定の wave または checkpoint だけを指す link にしない。人間が report から確認できる path、subject、probe、location、fingerprint、または finding を materialize する。

### `incomplete` 診断 report

`incomplete` 診断 report の durable 保存と state 境界は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「incomplete 診断 report」を正本とする。保存した診断 report を primary report とし、terminal result に `result: incomplete` を含める。

front matter には、run と report cut の情報、各終端結果の件数、および `result: incomplete` を含める。active generation ID は含めない。

本文の先頭で、正常 publication が成立しておらず、直前の正常 publication が current のままであることを明示する。本文には、次の独立したセクションを設ける。

1. `確定済みだが今回未 publication の human_required issue`
2. `inconclusive issue`

各項目は、診断 report 単独で reason と current evidence を確認できる内容にする。自動 join 済み修正の監査情報は、run report または subcommand log に保持する。

### 中断・エラー時の invocation report

`user_interruption` と `error` では、今回の invocation report を primary report として次へ保存する。

```text
{{repo-root}}/.cmoc/gu/ar/report/feedback/invocation/{{time-stamp}}.md
```

front matter と本文から、少なくとも次の情報を判別可能にする。

- command、生成日時、repo root、session branch、および terminal result
- run kind、run branch、run fork commit、run worktree、state before、および state after
- 完了した wave、high-watermark、処理済み issue、確定済み commit、および rollback
- 未実行の処理、維持した state、中断またはエラーの理由、次の操作、および関連ログ

invocation report は feedback publication または active state の一部ではなく、current pointer の参照先にしない。candidate を publication 済み issue または active issue として扱ってはならない。

## 終了コード

- `ok`、`attention`、`incomplete`、およびユーザー中断は終了コード 0 とする。
- validation 失敗、agent call failure、Structured Output 受理失敗、差分検査失敗、commit 失敗、state corruption、merge 失敗、required recovery 失敗、および durable report または publication の失敗は終了コード 1 とする。

終了コードは、今回の invocation が利用可能な終端結果を確定できたかを表す。直前の正常 report が current のまま残っていること、または一般的なエラー説明を出力できたことだけでは、今回の invocation が report result を確定したとはみなさない。

issue の件数、category、impact、`human_required` の有無、または fixed issue の件数だけを理由に非 0 を返してはならない。fixed issue の有無や件数を、他 workload の成功判定、retry、または recovery へ伝播させない。
