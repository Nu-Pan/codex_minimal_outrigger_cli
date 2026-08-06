# feedback の tracked normalized state

本書は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` が定義する issue、machine assessment、および human disposition の永続形式を定める。raw observation と machine rule の正本は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` とする。

## 保存先と構成

normalized issue と増分処理 state は、git 追跡対象の次の領域へ保存する。

```text
{{work-root}}/.cmoc/gt/ar/feedback/
├── issue/{{issue-id}}/identity.json
├── issue/{{issue-id}}/revision/{{revision-id}}.json
├── issue/{{issue-id}}/occurrence/{{observation-id}}.json
├── issue/{{issue-id}}/assessment/{{assessment-id}}.json
├── issue/{{issue-id}}/disposition/{{decision-id}}.json
├── ingestion/{{observation-id}}.json
└── report/{{report-id}}.json
```

単一の巨大な append-only file、全 observation ID を持つ cursor、および issue 全体を毎回書き換える snapshot は使用しない。増分処理済みかは observation ごとの ingestion receipt で判定する。

root が存在しない状態は、まだ report を実行していない空の schema version 1 state として有効とする。`cmoc feedback report` が最初の record とともに必要な directory を作り、空 directory または `.gitkeep` だけを追跡しない。

全 JSON file は UTF-8、object key の辞書順、末尾改行ありの canonical form で保存する。`identity.json` は初回作成後に変更しない。それ以外も新しい ID の record を追加し、既存 record を書き換えない。

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

- `schema_version`: 1
- `report_id`
- `generated_at`
- `snapshot_manifest_sha256`
- `snapshot_observation_count`
- `processed_observation_count`
- `deferred_observation_count`
- `report_path`
- `report_sha256`
- `result`
- `state_commit_ids`

`revision_id` と `assessment_id` は lowercase hexadecimal とする。`decision_id` は `fbd_` と UUIDv7、`report_id` は `fbr_` と UUIDv7 の組み合わせとする。normalization unit ID は、入力 observation ID、候補 revision ID、および normalizer schema SHA256 の canonical byte 列から求めた SHA256 に `fbu_` を付ける。

`normalizer_version` は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.py` と `{{cmoc-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.json` の SHA256 を path 順に連結して求めた SHA256 とする。normalization agent call を使わない deterministic unit も、処理規則との互換性を判別できる cmoc feedback schema version を同 field に記録する。

## effective record

issue の source observation ID 集合は、occurrence record の `observation_id` 集合とする。revision に source ID を持たせるだけで occurrence record を省略してはならない。

effective revision は、`source_observation_ids` が指す observation の最大 `observed_at`、次に `revision_id` の辞書順で最大の record とする。effective assessment は `assessed_at`、次に `assessment_id` の辞書順で最大の record とする。

effective human disposition は、`decided_at`、次に `decision_id` の辞書順で最大の record とする。disposition record を作る主体は人間、または人間の明示操作をそのまま記録する専用 UI に限る。human disposition を更新する具体的な UI は本仕様では固定しない。

## branch merge

record を細分化して append-only にすることで、異なる branch が別 observation を処理した場合は file 集合の和として merge できるようにする。

同じ path の record が両 branch に存在する場合、byte-for-byte で同一なら 1 件へ統合する。内容が異なる場合は、observation、normalization、または human disposition の消失につながるため自動解決しない。session join は generic conflict resolution agent へ渡さず merge を中止し、人間へ conflict path を提示する。
