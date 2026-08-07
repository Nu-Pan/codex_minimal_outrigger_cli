# feedback の repository-local normalized state

本書は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` が定義する issue、machine assessment、human disposition、および増分処理 state の永続形式を定める。raw observation と machine rule の正本は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` とする。

## 所有単位と保存先

feedback の永続データは、すべて repository-local state として次の root 配下へ保存する。

```text
{{repo-root}}/.cmoc/gu/ar/feedback/
├── observation/
├── issue/{{issue-id}}/identity.json
├── issue/{{issue-id}}/revision/{{revision-id}}.json
├── issue/{{issue-id}}/occurrence/{{observation-id}}.json
├── issue/{{issue-id}}/assessment/{{assessment-id}}.json
├── issue/{{issue-id}}/disposition/{{decision-id}}.json
├── ingestion/{{observation-id}}.json
├── report/{{report-id}}.json
├── report_snapshot/{{report-id}}.json
├── normalization_checkpoint/{{normalization-unit-id}}.json
├── normalization_unit/{{normalization-unit-id}}.json
└── state_snapshot/{{state-snapshot-id}}.json
```

Markdown の feedback report は、次の既存領域へ保存してよい。

```text
{{repo-root}}/.cmoc/gu/ar/report/feedback/
```

この state の所有単位は `{{repo-root}}` である。`{{work-root}}`、現在の branch、session、および run は所有単位にしない。session または run の join と abandon は、この state を取り込み、破棄、巻き戻し、または複製してはならない。

`{{repo-root}}/.cmoc/gu` 全体を Git 追跡対象外とする。別 clone、別 machine、Git remote、または hardware failure に対する複製と backup は保証しない。

root が存在しない状態は初期状態として有効とする。最初の writer が必要な directory を作る。空 directory または `.gitkeep` は作らない。

## file と record の共通規則

単一の巨大な append-only file、全 observation ID を持つ cursor、および issue 全体を毎回書き換える snapshot は使用しない。増分処理済みかは observation ごとの effective ingestion receipt で判定する。

全 JSON file は UTF-8、object key の辞書順、末尾改行ありの canonical form で保存する。`identity.json` は初回作成後に変更しない。それ以外の record も新しい ID の file を追加し、既存 file を書き換えない。immutable file と同じ path に同じ byte 列を再保存する操作は idempotent とする。同じ path に異なる byte 列がある場合は corruption として停止し、自動上書きしない。

## issue ID

machine issue の canonical key は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の rule registry が定める machine issue key とする。agent report から新規作成する issue の canonical key は `agent\0{{最初の observation ID}}` とする。

issue ID は、canonical key の SHA256 を lowercase base32 とし、その先頭 26 文字へ `fbi_` を付けた値とする。`identity.json` に canonical key 全文を保存する。同じ issue ID で異なる canonical key が見つかった場合は collision として処理を停止し、別 salt で暗黙に継続してはならない。

## record schema

`identity.json` は、次の field を持つ。

- `schema_version`: 1
- `issue_id`
- `origin`: `agent_report | machine_rule`
- `canonical_key`
- `created_from_observation_id`
- `created_at`

revision record は、次の field を持つ。

- `schema_version`: 1
- `revision_id`: `revision_id` field を除いた record 本文の canonical SHA256
- `issue_id`
- `created_at`
- `source_observation_ids`: 1 件以上の重複なし配列
- `category`: `{{cmoc-root}}/oracle/src/oracle/feedback/reporter_input.json` の category enum。agent report の新規 issue では observation の値、machine issue では rule の値を使用する
- `summary`
- `human_action`
- `impact`
- `cause_assessment`: `certainty` と `description`。`certainty` は `supported | suspected | unknown`
- `related_issue_ids`: 重複なし配列

occurrence record は、次の field を持つ。

- `schema_version`: 1
- `issue_id`
- `observation_id`
- `observation_sha256`
- `observed_at`
- `cmoc_session_id`: nullable
- `subcommand_invocation_id`
- `log_paths`

assessment record は、次の field を持つ。

- `schema_version`: 1
- `assessment_id`: `assessment_id` field を除いた record 本文の canonical SHA256
- `issue_id`
- `assessed_at`
- `presence`: `unknown | likely_present | likely_absent`
- `freshness`: `current | needs_revalidation | unavailable`
- `reason_code`: `observation_matches_current | normalizer_assessment | fingerprint_changed | fingerprint_unavailable`
- `reason`
- `compared_fingerprints`: path、旧 SHA256、現在 SHA256、および取得状態の配列

disposition record は、次の field を持つ。

- `schema_version`: 1
- `decision_id`
- `issue_id`
- `decided_at`
- `state`: `open | acknowledged | resolved | ignored | superseded`
- `note`: 空文字を許容する人間の説明
- `superseded_by`: `state=superseded` では別 issue ID、それ以外では `null`

ingestion receipt は、次の field を持つ。

- `schema_version`: 1
- `observation_id`
- `observation_sha256`
- `processed_at`
- `normalization_unit_id`
- `normalizer_version`
- `status`: `integrated | invalid`
- `issue_ids`: integrated では 1 件以上、それ以外では空配列
- `validation_errors`: invalid だけ 1 件以上、それ以外では空配列

report record は、次の field を持つ。

- `schema_version`: 2
- `report_id`
- `generated_at`
- `report_snapshot_sha256`
- `report_snapshot_observation_count`
- `processed_observation_count`
- `deferred_observation_count`
- `report_path`
- `report_sha256`
- `result`
- `normalization_unit_ids`
- `state_snapshot_id`: 有効な state snapshot を確定できない `result=error` だけ `null`
- `previous_successful_report_id`: 直前の正常な local report が存在しない場合は `null`

`revision_id` と `assessment_id` は lowercase hexadecimal とする。`decision_id` は `fbd_` と UUIDv7、`report_id` は `fbr_` と UUIDv7 の組み合わせとする。normalization unit ID は、入力 observation ID、候補 revision ID、および normalizer schema SHA256 の canonical byte 列から求めた SHA256 に `fbu_` を付ける。

`normalizer_version` は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.py` と `{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.json` の SHA256 を path 順に連結して求めた SHA256 とする。normalization agent call を使わない deterministic unit も、処理規則との互換性を判別できる cmoc feedback schema version を同 field に記録する。

## normalization unit の確定と再利用

normalization unit が生成する identity、revision、occurrence、assessment、および ingestion receipt は、関連する全 record の schema、hash、および参照整合性を検証し、全 file を durable に保存した後だけ確定済みとする。確定の印は、次の unit manifest である。

```text
{{repo-root}}/.cmoc/gu/ar/feedback/normalization_unit/{{normalization-unit-id}}.json
```

unit manifest は、少なくとも unit ID、入力 observation の ID と hash、候補 revision ID、normalizer schema hash、normalizer version、生成した全 record の path と SHA256、および正式な normalization agent output checkpoint の SHA256 を持つ。agent call を使用しない場合は checkpoint の SHA256 を `null` とする。

writer は unit manifest を最後に durable 保存する。unit manifest 自体も immutable とする。temporary file、atomic rename、file と directory の flush、および recovery metadata の具体方式は、次の外部挙動を満たす限り実装裁量とする。

- valid な unit manifest がない unit の一部 record を effective state として読み取らない。
- valid な unit manifest と一致する全 record がある unit だけを確定済みとして再利用する。
- manifest があるにもかかわらず record または必要な checkpoint の欠落、hash 不一致、または参照不整合がある場合は corruption として停止する。
- manifest 確定前の異常終了で残った temporary file または orphan record を検出する。期待 hash と一致して安全に再開できる場合だけ再利用し、それ以外は effective state を変更せず手動対応が必要な path を示す。

正式な normalization agent output は、次へ immutable checkpoint として durable 保存する。

```text
{{repo-root}}/.cmoc/gu/ar/feedback/normalization_checkpoint/{{normalization-unit-id}}.json
```

checkpoint の入力 observation hash、候補 revision ID、schema hash、および正式な Structured Output が現在の unit と一致する場合は再利用する。同じ unit のために normalization agent call を再実行してはならない。確定済み unit manifest または effective ingestion receipt がある observation を再実行しても、重複 record、重複 unit、または重複 normalization agent call を生成してはならない。unit の確定だけを理由に checkpoint を削除しない。

## effective record

normalization が生成した record は、valid な確定済み unit manifest に列挙されている場合だけ effective とする。human disposition は 1 record 単位で atomic かつ durable に保存し、同じ repository-level writer 排他制御の下で effective にする。

issue の source observation ID 集合は、effective occurrence record の `observation_id` 集合とする。revision に source ID を持たせるだけで occurrence record を省略してはならない。

effective revision は、`source_observation_ids` が指す observation の最大 `observed_at`、次に `revision_id` の辞書順で最大の record とする。effective assessment は `assessed_at`、次に `assessment_id` の辞書順で最大の record とする。

effective human disposition は、`decided_at`、次に `decision_id` の辞書順で最大の record とする。disposition record を作る主体は人間、または人間の明示操作をそのまま記録する専用 UI に限る。human disposition を更新する具体的な UI は本仕様では固定しない。

## 排他制御と整合性検査

normalized state、normalization unit、report record、および state snapshot を更新する writer は、`{{repo-root}}` ごとに共通の writer 排他制御へ従う。同じ repository で複数の `cmoc feedback report` が normalized state を同時更新してはならない。human disposition の writer も、report の snapshot と競合しないよう同じ排他制御へ従う。

排他の lock file、lease、待機、および stale owner 回復の具体方式は実装裁量とする。ただし、所有者を安全に判定できない lock を暗黙に破棄してはならない。排他を取得できない呼び出しは state を変更せず、競合中であることを示して待機または終了する。

writer は更新前後に、effective record、unit manifest、ingestion receipt、report record、および snapshot の schema、hash、参照整合性を検証する。異常終了後の次回実行は、確定済み unit を保持し、未確定 unit だけを安全に再開する。安全に再開できない場合は、それまで有効だった state を変更せず停止する。

## state snapshot と正常 report の連鎖

state snapshot は、作成時点の effective normalized feedback state を後から再確認するための immutable manifest である。raw observation の入力集合を固定する report snapshot とは別の record とし、相互に代用してはならない。

state snapshot は、少なくとも次の情報を canonical な順序で持つ。

- `schema_version`
- `state_snapshot_id`
- 作成日時
- snapshot に含まれる確定済み normalization unit ID
- 全 effective ingestion receipt の path と SHA256
- issue ごとの identity record の path と SHA256
- issue ごとの effective revision、effective assessment、および effective human disposition の path と SHA256。存在しない record は `null`
- issue ごとの全 effective occurrence record の path と SHA256

`state_snapshot_id` は、同 field を除いた canonical snapshot 本文の SHA256 に `fbs_` を付けた値とする。writer 排他制御中に全参照を検証し、snapshot file を durable 保存する。対応する report record を保存した後も変更または自動削除しない。retention を branch、commit、または branch reachability に依存させない。

`result=ok | attention` の report を正常な local report とする。正常 report record は、自身の `state_snapshot_id` と、直前の正常 report の `report_id` を `previous_successful_report_id` に記録する。正常 report がまだない場合は `null` とする。

writer 排他制御の下で predecessor を一意に決め、state snapshot と report record を durable 保存した後だけ新しい正常 report を連鎖の先頭とする。正常 report の前後関係、前回差分、および snapshot retention を timestamp だけで決めてはならない。`result=partial | interrupted | error` の report は正常 report の連鎖を進めない。
