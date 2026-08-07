# `cmoc feedback report`

本書は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` が定義する delayed normalization と feedback report の挙動を定める。raw observation は `{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md`、repository-local record schema と整合性は `{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` を正本とする。

## 引数

- 位置引数は受け取らない。
- `--all` を受け取る。
    - 既定表示で省略する全 disposition 済み issue、threshold 未満の machine issue、全 revision、全 assessment、および全 occurrence を表示する。
    - 既定値は false とする。
- `--migration-source {{local-branch}}` を受け取る。
    - 一回限りの旧 state 移行で divergent な local branch がある場合に、人間が移行元を明示するためだけに使用する。
    - 移行完了後は受け付けない。
    - branch の選択規則と非選択 state の保存は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の移行契約に従う。

## 事前条件と repository-local state

doctor preprocess の後、次の条件をすべて満たす場合だけ実行する。

- main worktree 上の active な `{{cmoc-session-branch}}` が checkout されている。
- 対応する session state の `session.state=active` である。
- `run.state=ready` である。
- repository-level feedback writer 排他を取得できる。

一回限りの旧 state 移行で tracked file の削除 commit が必要な場合だけ、git working tree と staging area に未コミット差分がないことを追加で要求する。通常の report は Git commit を作成しないため、Git の clean 状態を事前条件にしない。

report は編集 run を作らず、session state と run state を変更しない。normalized feedback state は `{{repo-root}}` に属し、現在の branch には属さない。session または run の join と abandon は、確定済み unit、ingestion receipt、report record、checkpoint、および snapshot を取り込み、破棄、または巻き戻さない。

## 一回限りの移行

writer 排他を取得した後、normalized state、ingestion receipt、旧 report baseline のいずれかを読む前に、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` が定める移行完了を検証する。migration receipt がない場合は、同仕様に従って移行を実行する。

branch divergence、schema 違反、hash 不一致、参照不整合、または baseline の再構築不能により移行を完了できない場合は、feedback report をエラー終了する。旧 state、移行前から有効だった新 state、および検証済みの移行 archive は保持する。移行の失敗を、別 workload の成功判定、run state、retry、または終了コードへ伝播させない。

移行完了後の通常処理は、旧 state を読み取り元、保存先、rollback 元、または差分基準にしてはならない。

移行完了を確認した後、repository-local feedback state の schema、hash、参照整合性、および確定済み unit を検証する。違反または破損がある場合は、effective state を変更せずエラー終了する。

## report snapshot と増分処理

コマンド開始時に、存在する raw observation の path、ID、および SHA256 を固定した immutable な report snapshot を作り、次へ atomic かつ durable に保存する。

```text
{{repo-root}}/.cmoc/gu/ar/feedback/report_snapshot/{{report-id}}.json
```

report snapshot は、この report が処理する raw observation 集合だけを表す。normalized feedback state を表す state snapshot とは別の record であり、相互に代用してはならない。

report 自身の normalization agent call が新しい observation を生成した場合、その observation は report snapshot に加えず次回 report へ回す。直前の正常な local report 後の増加数は、直前の正常 report の report snapshot に含まれず、repository-local な effective ingestion receipt がない observation の件数とする。

report snapshot は変更または自動削除しない。retention を Git branch、commit、または branch reachability に依存させない。別 clone または別 machine への複製は保証しない。

effective ingestion receipt の observation ID と SHA256 が一致する observation は処理済みとする。ID は一致するが SHA256 が異なる場合は corruption としてエラー終了する。

増分処理は、次の順序で行う。

1. observation schema を検証し、observation ID と SHA256 で重複を除去する。
2. machine observation を、rule の canonical key による完全一致で統合する。
3. agent observation と既存 issue の比較候補を、category、正規化済み evidence subject、および既存 occurrence の fingerprint で機械的に絞り込む。deduplication hint は検索 hint にだけ使用する。
4. 完全一致では決められない候補だけを normalization agent call へ渡す。
5. observation 発生時点と現在の evidence file または config fingerprint を比較する。
6. normalized issue state と ingestion receipt を durable な normalization unit として確定する。
7. report snapshot に対する feedback report を決定論的にレンダリングする。

schema 不正な raw observation は改変せず、`status=invalid` の ingestion receipt と validation error を保存する。同じ不正 observation を毎回再検証しない。report では producer または保存領域の問題として差分要約へ表示する。

## normalization agent call

曖昧な候補だけに `build_feedback_normalize_issue_parameter` を 1 回使用する。builder は `{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.py`、専用 schema は `{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.json` を正本とする。

normalization agent の入力は、次の情報に限定する。

- 検証済みの構造化 observation
- 機械的に絞り込んだ既存 issue 候補
- 現在状態の確認に必要な repository 内参照 path

raw Codex call log、元の Codex session、および候補外 issue を読み直してはならない。file access mode は `READONLY` とし、normalization agent は feedback state を編集しない。

normalization agent が既存 issue を選んだ場合も、cmoc は元 observation と新しい occurrence を保持する。新規 issue を選び、既存問題が変質した可能性がある場合は `related_issue_ids` を revision に残す。元 issue を削除または自動で superseded にしてはならない。

新規 issue の category は source observation の category とする。既存 issue へ統合する場合は effective revision の category を維持し、normalization agent に category を推測または変更させない。

## notification threshold

machine issue は threshold 未満でも normalized issue と occurrence を保持するが、既定 report の issue 一覧へ表示しない。rule の recurrence window 内で threshold を満たした時点から表示する。

agent report は 1 件でも人間が明示的に報告した observation であるため、machine rule の recurrence threshold を適用しない。ただし normalization により既存 issue と統合してよい。

## machine assessment と鮮度

過去の `{{work-root}}` を再構築できるとは仮定しない。observation は発生時点の evidence と fingerprint を保持し、report は現在状態への鮮度だけを評価する。

- 比較対象 fingerprint が前回 assessment と一致する場合は、既存の presence と `freshness=current` を維持してよい。
- fingerprint が変わった場合は、`presence=unknown`, `freshness=needs_revalidation` の新しい assessment を追加する。
- 現在の fingerprint を取得できない場合は、`freshness=unavailable` とする。
- 問題が別の問題へ変質した可能性がある場合は、新しい issue と relation を作り、元 issue を上書きしない。
- 新しい observation が disposition 済み issue と一致しても、disposition を変更しない。

normalization agent call を行った unit では、専用 Structured Output の `presence_assessment` を assessment record の presence と reason に使用する。agent call を行わない unit では、observation の fingerprint と現在値が一致する場合だけ `presence=likely_present` とし、それ以外は `unknown` とする。`likely_absent` を fingerprint の変化だけから機械的に設定してはならない。

fingerprint の変化、`likely_absent`、または normalization agent の判断だけを根拠に、human disposition を `resolved`, `ignored`, `superseded` へ変更してはならない。

## 処理単位、確定、および再開

normalization unit は、次のいずれかとする。

- 同じ machine canonical key を持つ未処理 observation の集合
- 1 件の agent observation と、その絞り込み済み候補
- 1 issue に対する fingerprint assessment

unit ID、unit manifest、effective record、および integrity check は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` を正本とする。各 unit は、生成する全 record を検証して durable 保存し、unit manifest を最後に確定してから次へ進む。Git commit、Git tree、または HEAD は unit の確定に使用しない。

normalization agent の正式な出力を受理した時点で、同仕様が定める checkpoint を atomic かつ durable に保存する。同じ入力、候補、および schema で再実行する場合は checkpoint を検証して再利用し、同じ observation のために quota を再消費しない。unit の確定後も checkpoint を削除しない。

中断または一部失敗時は、確定済み unit manifest と checkpoint を維持する。実行中 unit は、全 record と unit manifest を安全に確定できる場合だけ確定する。それ以外は未確定のまま effective state から除外し、次回 report が recovery metadata と checkpoint から再開する。未確定 unit の一部を Git rollback または file の部分削除で有効化してはならない。

同じ report snapshot を再実行した場合は、effective ingestion receipt、確定済み unit manifest、および checkpoint を再利用する。同じ observation に対する重複 record、重複 normalization unit、または重複 normalization agent call を生成してはならない。

## report と state snapshot の確定

report snapshot の処理が完了、一部失敗、またはユーザー中断で停止した後、effective state の整合性を再検証する。整合している場合は、現在の effective normalized state を immutable state snapshot として保存し、Markdown report と report record を durable に保存する。

report record は、対応する state snapshot と Markdown report の durable 保存および hash 検証後に、最後の publication record として保存する。report record がない artifact を正常 report として読み取ってはならない。

state snapshot と report record の schema、正常 report の predecessor、および retention は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` を正本とする。report record と front matter の `normalization_unit_ids` には、この report で確定または再利用した normalization unit ID を処理順に記録する。Git commit ID は記録しない。

保存途中の異常終了後は、report path、report hash、state snapshot、および report record の対応を検証する。全 artifact が一致する場合だけ既存出力を再利用する。一部だけが残り安全に確定できない場合は、新しい正常 report として扱わず、手動対応が必要な path を示す。

effective state の corruption、writer 排他の喪失、または durable 保存の失敗がある場合は、state が整合していると偽って report を確定しない。それまでの確定済み unit、checkpoint、report snapshot、および以前の正常 report を保持する。

## ユーザー中断

このコマンドは中断可能サブコマンドとし、共通動作は `{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` を正本とする。中断要求後は新しい normalization unit または Codex call を開始しない。処理単位の確定規則に従い、整合した effective state から `result=interrupted` の report を保存する。

## report の保存先と front matter

report は Markdown + YAML Front Matter とし、次へ保存する。

```text
{{repo-root}}/.cmoc/gu/ar/report/feedback/{{time-stamp}}.md
```

front matter は、次の field を持つ。

- `command`: `cmoc feedback report`
- `generated_at`
- `repo_root`
- `session_branch`: 実行 context であり、feedback state の所有者または差分基準ではない
- `report_snapshot_sha256`
- `report_snapshot_observation_count`
- `processed_observation_count`
- `deferred_observation_count`
- `invalid_observation_count`
- `normalization_agent_call_count`
- `new_or_changed_issue_count`
- `recurrent_open_issue_count`
- `needs_revalidation_issue_count`
- `disposition_change_count`
- `suppressed_machine_issue_count`
- `all`: boolean
- `normalization_unit_ids`
- `state_snapshot_id`
- `previous_successful_report_id`
- `result`

`result` は、次のいずれかとする。

- `ok`: 処理が完了し、既定表示の対象 issue がない。
- `attention`: 処理が完了し、既定表示の対象 issue または invalid observation がある。
- `partial`: 一部 unit の処理に失敗したが、確定済み state から report を保存できた。
- `interrupted`: ユーザー中断までの確定済み state から report を保存した。
- `error`: 有効な report または整合した repository-local state を確定できなかった。

本仕様で「正常完了した feedback report」とは、`result=ok | attention` の report を指す。

## report 差分の基準

直前の正常な local report は、正常 report record の predecessor 連鎖から一意に決める。移行直後で新方式の正常 report がない場合は、migration receipt が示す legacy baseline を predecessor とする。branch reachability、過去 commit の tree、または timestamp の大小で選んではならない。

新しい正常 report は、直前の正常 report に対応する immutable state snapshot と、今回確定した state snapshot を比較する。新規 revision、assessment、disposition、および occurrence の差分は、snapshot が列挙する record ID と SHA256 で判定する。record 内の timestamp だけで差分を判定してはならない。

直前の正常 report がない場合は、現在の effective state を初回差分として扱う。predecessor、state snapshot、または参照 hash を一意に検証できない場合は、新しい正常 report を確定せずエラーとする。raw observation の report snapshot を normalized state の差分基準に使用してはならない。

## 既定表示

既定 report は raw occurrence を展開せず、issue を次の順序で提示する。

1. 直前の正常 report 後に新規作成された issue、または effective revision が変化した issue
2. 複数 session で再発している、effective disposition が未決定または `open | acknowledged` の issue
3. effective assessment が `needs_revalidation` の issue
4. `resolved | ignored | superseded` など、直前の正常 report 後の disposition 差分要約

各 issue の先頭には、次の情報を簡潔に示す。

- issue ID、問題の要約、および人間の対応候補
- occurrence 数と affected cmoc session 数
- 最初と最後の観測日時
- machine assessment の presence と freshness
- effective human disposition。未決定の場合は `not_disposed` と表示する
- 代表的な evidence
- issue directory、raw observation、および log への参照

全 revision、全 assessment、全 disposition、全 occurrence、および threshold 未満 issue は `--all` の場合だけ表示する。

## 終了コード

- `ok` と `attention` は終了コード 0 とする。
- `error` は終了コード 1 とする。
- `partial` は終了コード 2 とする。
- `interrupted` は、共通のユーザー中断規則に従う正常系として終了コード 0 とする。

issue の件数、severity、presence、freshness、または human disposition だけを理由に非 0 を返してはならない。この終了コードは `cmoc feedback report` 自身の処理結果だけを表し、他 workload の成功判定へ伝播させない。
