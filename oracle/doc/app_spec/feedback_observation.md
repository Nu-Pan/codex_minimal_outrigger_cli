# feedback observation の収集と保存

本書は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` が定義する observation の収集、検査、および raw 保存を定める。

## MCP reporter による自己申告

### agent-facing interface

agent-facing transport は、Codex が起動する call-scoped な local stdio MCP reporter/client に固定する。MCP server namespace は `cmoc_feedback` とし、公開する tool は `submit_observation` だけとする。MCP resource、prompt、および observation submission 以外の tool を公開してはならない。

`cmoc_feedback.submit_observation` の input は、`{{cmoc-root}}/oracle/src/oracle/feedback/reporter_input.json` に適合する JSON object そのものとする。repository、agent call ID、Codex call ID、保存先、または capability を input に追加してはならない。

tool result は、次のいずれかの JSON object とする。

```json
{"status":"accepted","observation_id":"fbo_...","redaction_count":0}
```

```json
{"status":"rejected","code":"...","message":"...","retryable":false}
```

`status=accepted` は受理と永続化の完了を表す。payload または call context を拒否する場合は、MCP protocol error や process exit code ではなく、`status=rejected` の構造化された domain result を返す。

rejection code は、次のいずれかとする。

- `schema_invalid`
- `payload_too_large`
- `path_outside_repo`
- `evidence_empty`
- `rate_limited`
- `suspected_secret`
- `context_invalid`
- `collector_unavailable`
- `protocol_mismatch`
- `transport_unavailable`

`rate_limited`, `collector_unavailable`, `transport_unavailable` だけ `retryable=true` を許容する。retryable は本命作業の retry を要求する意味ではない。

reporter または collector の起動失敗、利用不能、rejected result、および transport failure だけを理由に、本命 Codex workload を失敗または中断させてはならない。reporter が result を返せない状態も、本命 workload とは独立した非致命的な degradation とする。

### agent input schema の正本

agent が入力する JSON schema の唯一の正本は、`{{cmoc-root}}/oracle/src/oracle/feedback/reporter_input.json` とする。MCP reporter が tool discovery で提示する `inputSchema` と受け入れ検査は、同 schema から導出する。同じ field 定義を prompt、個別 AgentCallParameter builder、個別 Structured Output schema、または別の oracle file へ複製してはならない。

schema に含まれる agent 申告の原因、重要度、および重複判定用 hint は、確定事実または issue key として扱わない。

### prompt への共通 instruction

共通 instruction の文面と報告基準は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/parts/feedback_reporting_standard.py` の `build_feedback_reporting_standard` だけを正本とする。`build_complete_prompt` は同生成結果を全 agent call へ無条件に 1 回だけ注入する。個別 builder が有効化する option にしてはならない。

共通 instruction には `cmoc_feedback.submit_observation` を使うことだけを示す。schema、context field、入力例、文字数制限、受け入れ検査、および MCP reporter から collector までの内部 transport を複製してはならない。

### reporter の受け入れ検査

reporter と collector は、意味的な正しさではなく、安全に永続化できるかを検査する。

必須の機械検査は次のとおりとする。

- schema version、必須 field、型、enum、および `additionalProperties`
- schema が定める文字数と配列要素数
- payload 全体が UTF-8 で 32 KiB 以下であること
- path の正規化後も `{{repo-root}}` 内であること
- `file | oracle | log` evidence に path があり、evidence 全体が空でないこと
- 1 Codex call あたり accepted observation が 8 件以下であること
- 同じ Codex call から 60 秒以内に accepted observation が 3 件以下であること
- secret と高い確度で判定できる private key block、Authorization header、および既知 credential prefix のマスキング

evidence path は absolute path または `{{repo-root}}` 相対 path を受理し、相対 path は capability に拘束された repo-root を基準にする。存在する path は symlink 解決後、存在しない path は `.` と `..` を字句正規化した後に repo-root 内であることを検査する。repo-root 外へ解決される path は拒否する。

マスキング後も evidence の意味が残る場合は、`[REDACTED:{{kind}}]` へ置換して受理し、`redaction_count` を返す。必須 evidence が空になる場合、または安全に部分置換できない場合は `suspected_secret` として拒否する。entropy だけを根拠とする広範な secret 判定は行わない。

原因の正しさ、重要度の妥当性、実際に人間対応が必要か、および既存 issue と同一かは受理条件にしない。

### collector が付与する context

agent に実行文脈を入力させてはならない。collector は、call-scoped capability から次の情報を付与する。

- observation ID と RFC 3339 形式の発生日時
- cmoc session ID、run ID、run kind
- subcommand 名と subcommand invocation ID
- agent call ID、agent call kind、Codex call ID、および判明している場合の Codex session ID
- `{{repo-root}}` と `{{work-root}}`
- 発生時点の `{{work-root}}` の HEAD commit
- subcommand log と Codex call log の path
- reporter version、reporter protocol version、および observation schema version
- file、oracle、log evidence の正規化済み path、SHA256、および hash を取得できなかった理由

agent call ID は Structured Output 補正を含む論理 agent call で共有する。Codex call ID は初回、補正、および TUI process ごとに分ける。

### sandbox、transport、および lifecycle

agent の送信から raw observation の保存までのデータフローを次に示す。

```text
Codex MCP tool
  -> call-scoped local stdio MCP reporter/client
  -> invocation-scoped collector IPC
  -> cmoc collector
  -> .cmoc/gu の raw observation
```

local stdio MCP reporter/client は feedback file を直接書かない。invocation-scoped collector は Codex の command sandbox 外で request を受け、collector だけが raw observation を atomic に保存する。agent は保存先を直接操作してはならない。

cmoc は initial call、Structured Output の correction call、および TUI call の開始前に、その Codex call 専用の MCP reporter と call-scoped capability を利用可能にする。`read-only`、`workspace-write`、`codex exec`、および TUI は、同じ agent-facing MCP transport を使用する。

agent または agent が実行する shell command は collector IPC へ直接接続してはならない。この transport のために、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` が定める sandbox、permission profile、および network access の境界を変更してはならない。`dangerously_allow_all_unix_sockets` または同等の広い許可を成立条件にしてはならない。

collector は payload ではなく capability に結び付いた context を保存に使用する。capability は推測困難かつ Codex call ごとに一意とし、発行対象の repository、work-root、agent call、および Codex call 以外に使用できないようにする。capability value を prompt、Codex argv、Codex call log、または submit payload に含めてはならない。

MCP reporter は observation submission 以外の arbitrary file access、command execution、または collector 管理操作を提供してはならない。unknown、別 call 用、または失効済みの capability による request は `context_invalid` として拒否する。

collector は「durability と retention」が定める atomic な永続化を完了した後だけ accepted を返す。

Codex process の異常終了またはユーザーによる TUI 終了を含め、Codex call の終了時は次の順序でその call だけを終了する。

1. その capability に対する新規 request の受付を止める。
2. 受付済み request を drain し、accepted とする observation の永続化を完了する。
3. その capability と MCP context を無効化する。

parallel call ごとに capability、context、drain、および無効化を分離する。一つの call の停止または無効化によって、稼働中の別 call を停止または無効化してはならない。

correction call は元の agent call ID を共有する一方、新しい Codex call ID、capability、および MCP context を使用する。TUI では、一つの TUI process の全 turn を通して同じ Codex call ID、capability、および MCP reporter context を維持し、TUI process の終了時に上記の順序で無効化する。

stdio MCP process と invocation-scoped collector の間の IPC 方式と framing、内部 module path、capability を同 process へ安全に渡す具体方式、および環境変数名は、本節の安全要件を満たす限り実装裁量とする。

## 機械的な log 検出

### detector の責務境界

detector は、構造化 log event から diagnostic observation を作るだけとする。検出の成否と内容を、task の失敗、成果物の拒否、run state、終了コード、retry、または recovery の条件にしてはならない。

detector は event が flush された後に rule を評価する。rule に一致した occurrence は、通知 threshold 未満でも raw observation として保存する。threshold を満たすかの集約は `cmoc feedback report` が行う。

machine observation は agent 用 reporter transport を経由しない。detector は検出結果を cmoc collector へ渡し、collector だけが observation store へ保存する。検出または保存の失敗は構造化 log event と warning に留め、本命 subcommand の結果を変更しない。

### event contract

機械検出に使用できる event は、producer の oracle 仕様で次の field が安定契約として定義されているものに限る。

- `event_schema_version`
- repository 内で一意な `event_id`
- 安定した `event_type`
- `occurred_at`
- rule が参照する型付き field
- subcommand invocation と、該当する場合の session、run、agent call、Codex call への対応

message、stderr、command 全文などの自由文を、rule の判定または issue key に使用してはならない。自由文は occurrence の evidence として保持してよい。

### rule registry

detector rule は allowlist とし、各 rule は次の情報を持つ。

- version を含む安定した `rule_id`
- 入力 event type、schema version、および参照 field
- reporter input schema と同じ enum に従う issue category
- 人間向けの短い summary と、反復時に生じる impact
- 人間が取り得る具体的な対応
- notification threshold と recurrence window
- 除外する期待動作
- `subject_type` と低カーディナリティの `normalized_subject_id` の構築方法

machine issue key は、次の canonical UTF-8 byte 列とする。

```text
{{rule_id}}\0{{subject_type}}\0{{normalized_subject_id}}
```

recurrence の distinct scope は、cmoc session ID がある observation では同 ID、session 外の observation では subcommand invocation ID とする。threshold の集計に使う scope ID は occurrence 情報であり、issue key には含めない。

次の高カーディナリティ情報を issue key に含めてはならない。

- timestamp
- session ID、run ID、agent call ID、Codex call ID
- raw command または error message の全文
- 一時 path
- random ID

### 初期 allowlist

初期 rule は、producer 側で安定 event を定義できる次の 2 件だけとする。

| `rule_id` | category | event と参照 field | subject | threshold | 人間の対応 | 除外 |
|---|---|---|---|---|---|---|
| `feedback.reporter_unavailable.v1` | `tooling` | `feedback.reporter_unavailable` v1 の `component`, `failure_code` | `reporter_component`, `{{component}}:{{failure_code}}` | 30 日以内に異なる recurrence scope で 2 回 | doctor の結果、reporter/collector version、transport を確認する | payload 拒否、rate limit、agent が reporter を呼ばなかった場合 |
| `codex.structured_output_validation_exhausted.v1` | `tooling` | `codex.structured_output_validation_exhausted` v1 の `agent_call_kind` | `agent_call_kind`, 同 field | 30 日以内に異なる agent call かつ異なる recurrence scope で 2 回 | 対応する builder、schema、および決定論的事後条件を確認する | 補正成功、Structured Output を使わない call、ユーザー中断 |

各初期 rule の summary と impact は次のとおりとする。

- `feedback.reporter_unavailable.v1`
    - summary: feedback reporter または collector が反復して利用できない。
    - impact: agent の自己申告 observation が欠落し、人間対応対象の発見が不完全になる。
- `codex.structured_output_validation_exhausted.v1`
    - summary: 同じ agent call kind で Structured Output の受理失敗が反復している。
    - impact: 補正 call の quota を消費した後に workload が失敗し、同じ作業が反復する。

`feedback.reporter_unavailable` v1 は、共通 event field に加えて次の field を持つ。

- `component`: `reporter | collector | transport`
- `failure_code`: `missing | version_mismatch | collector_unavailable | transport_unavailable | protocol_error`

`codex.structured_output_validation_exhausted` v1 は、共通 event field に加えて次の field を持つ。

- `agent_call_kind`: builder ごとに固定した低カーディナリティ識別子
- `schema_sha256`: evidence として保持する schema hash
- `last_failure_stage`: `json_parse | schema_validation | deterministic_postcondition | resume_unavailable | artifact_changed`

sandbox escalation については、oracle が要求する期待動作か、同じ原因か、および安定した subject を現在の log event から判定できない。そのため初期 rule を定義しない。これらを型付き field として producer が正本仕様化した後に限り、allowlist へ追加してよい。

## raw observation の保存

### 保存先と file 単位

raw observation は git 追跡対象外の次の領域へ、1 observation 1 file で保存する。

```text
{{repo-root}}/.cmoc/gu/ar/feedback/observation/v1/YYYY/MM/DD/{{observation-id}}.json
```

reporter observation ID は `fbo_` と UUIDv7 の組み合わせとする。machine observation ID は、`rule_id + "\0" + event_id` の SHA256 先頭 32 hexadecimal digit に `fbo_` を付け、同じ event の再検出で同じ ID になるようにする。

collector は同じ ID の file を create-exclusive で作る。同じ ID と同じ SHA256 の再送は既存 observation ID を返す。同じ ID で内容が異なる場合は corruption として拒否する。

path の `YYYY/MM/DD` は `observed_at` から決定する。同じ machine event を後日に再検出しても、保存 path を変えてはならない。

### observation envelope schema

raw file のトップレベルは、次の field を持つ JSON object とする。`null` を許容すると明記した field 以外は必須とする。

```json
{
  "schema_version": 1,
  "observation_id": "fbo_...",
  "source": "agent_report | machine_rule",
  "observed_at": "RFC 3339 timestamp",
  "context": {
    "repo_root": "/absolute/path",
    "work_root": "/absolute/path",
    "head_commit": "git commit ID",
    "cmoc_session_id": "... | null",
    "run_id": "... | null",
    "run_kind": "realization_apply | realization_refactor | null",
    "subcommand": "...",
    "subcommand_invocation_id": "...",
    "agent_call_id": "... | null",
    "agent_call_kind": "... | null",
    "codex_call_id": "... | null",
    "codex_session_id": "... | null",
    "log_paths": ["/absolute/path"]
  },
  "versions": {
    "reporter": "... | null",
    "reporter_protocol": "... | null",
    "observation_schema": 1,
    "rule_id": "... | null"
  },
  "payload": {},
  "evidence_fingerprints": [],
  "source_event": null
}
```

`source=agent_report` の `payload` は、secret masking 後の reporter input とする。`source=machine_rule` の `payload` は、`rule_id`, `rule_version`, `category`, `subject_type`, `normalized_subject_id`, `summary`, `impact`, `human_action`, `event_fields` を必須とする。

`evidence_fingerprints` の各要素は、`evidence_index`, `normalized_path`, `state`, `sha256` を持つ。`state` は `hashed | missing | not_file | unreadable` とする。`state=hashed` だけ `sha256` を文字列とし、それ以外は `null` とする。

`source_event` は machine observation だけ object とし、`event_id`, `event_type`, `event_schema_version`, `log_path`, `event_sha256` を持つ。`event_sha256` は canonical event 1 件の SHA256 とし、追記中の log file 全体は hash 対象にしない。agent observation では `null` とする。

### durability と retention

observation は sibling temporary file への write、file flush、atomic rename、および parent directory の flush が完了してから accepted とする。accepted は repository が存在する local filesystem 上の durability だけを保証し、別 clone、別 machine、または hardware failure に対する backup を保証しない。

accepted response 後に observation が未保存となる状態や sibling temporary file が残る状態を許容してはならない。

raw observation は normalization 後も変更または自動削除しない。初期仕様では retention を無期限とし、自動 pruning と prune subcommand を提供しない。pruning を追加する場合は、少なくとも repository-local な effective ingestion receipt が存在する observation だけを対象とし、未処理 observation を削除しない別仕様を先に定義する。

通常のサブコマンド完了サマリーは、詳細を展開せず次の 2 値だけを表示する。

- repository-local な effective ingestion receipt がない raw observation 数
- 直前の正常な local feedback report の report snapshot 後に増えた raw observation 数

直前の正常な local feedback report がない場合は、後者を前者と同数とする。report record はあるが対応する report snapshot がない、hash が一致しない、または正常 report の連鎖を一意に解決できない場合も同じ fallback を使用し、理由を warning として示す。raw observation の report snapshot と normalized state の state snapshot を混同してはならない。

未処理 observation が 100 件以上、または最古の未処理 observation が 7 日以上前の場合は、`cmoc feedback report` の実行を促す warning を追加する。この warning と件数計算の失敗は、サブコマンドの終了コードまたは run state を変更しない。
