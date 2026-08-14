# feedback observation の収集

本書は、observation の報告基準、収集経路、受け入れ検査、機械的検出、および raw 保存を定める。issue の同一性や現在状態は判断しない。

## agent による報告

### 報告基準

agent は、現在の workload だけでは解消できず、現在の作業外にいる人間の対応によって次のいずれかが可能になる問題だけを報告する。

- 再発を防止する
- 反復的な浪費を減らす
- 外部挙動を左右する人間意図を確定する

通常の workload 内で解決した問題、仕様どおりの制約、および具体的な根拠がない改善案は報告しない。報告対象を発見した時点で reporter を使用し、その後も可能な限り本命 workload を継続する。報告対象がなければ、feedback 用の出力や reporter call を行わない。

reporter の利用不能または submission の拒否は、本命 workload の成功条件を変更しない。

### prompt instruction

全 agent call に注入する正確な文面は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/parts/feedback_reporting_standard.py` の `build_feedback_reporting_standard` を正本とする。報告基準の意味は、本書を正本とする。

`build_complete_prompt` は、同 instruction を全 agent call へ 1 回だけ注入する。個別 builder の option にしたり、入力 schema や内部 transport の説明を prompt へ複製したりしてはならない。

### MCP interface

agent-facing interface は、Codex call ごとに起動する local stdio MCP reporter/client とする。MCP namespace は `cmoc_feedback` とし、`submit_observation` だけを公開する。MCP resource、prompt、任意の file access、command execution、または collector 管理機能を公開してはならない。

input は、`{{cmoc-root}}/oracle/src/oracle/feedback/reporter_input.json` に適合する JSON object とする。同 schema を tool discovery と受け入れ検査の両方に使用する。repository、call ID、保存先、または capability を agent input に追加してはならない。

tool result は、次のいずれかとする。

```json
{"status":"accepted","observation_id":"fbo_...","redaction_count":0}
```

```json
{"status":"rejected","code":"...","message":"...","retryable":false}
```

`accepted` は、受け入れ検査と durable な保存が完了したことを表す。入力または context を拒否する場合は、MCP protocol error ではなく `rejected` を返す。

rejection code は、次の値に限定する。

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

`retryable=true` を許容するのは、`rate_limited`、`collector_unavailable`、`transport_unavailable` だけとする。retryable は、本命 workload の retry を要求する意味ではない。

### 受け入れ検査

reporter と collector は、安全に保存できるかだけを検査する。原因、重要度、人間対応の必要性、および既存 issue との同一性は判断しない。

受け入れには、次の条件をすべて要求する。

- input schema に適合する。
- payload 全体が UTF-8 で 32 KiB 以下である。
- `file | oracle | log` evidence の path が正規化後も capability に拘束された `{{repo-root}}` 内にある。
- evidence が空ではない。
- accepted observation は 1 Codex call あたり 8 件以下である。
- accepted observation は同じ Codex call から 60 秒以内に 3 件以下である。
- private key block、Authorization header、および既知 credential prefix を安全にマスキングできる。

存在する evidence path は symlink 解決後に検査する。存在しない path は `.` と `..` を字句正規化して検査する。

マスキング後も evidence の意味が残る場合は、`[REDACTED:{{kind}}]` へ置換して受理する。必須 evidence が空になる場合、または安全に部分置換できない場合は、`suspected_secret` として拒否する。entropy だけを根拠とする広範な secret 判定は行わない。

## collector と transport

### context の確定

agent に実行 context を入力させてはならない。collector は、call-scoped capability から次の context を確定する。

- observation、session、run、subcommand、agent call、および Codex call の識別情報
- `{{repo-root}}`、`{{work-root}}`、観測時の HEAD commit
- subcommand log と Codex call log
- reporter、protocol、observation schema、および detector rule の version
- evidence path の正規化結果、fingerprint、および fingerprint を取得できなかった理由

agent call ID は Structured Output の correction call と共有する。Codex call ID と capability は、初回 call、correction call、および TUI process ごとに分ける。

### 保存経路

raw observation は、次の経路だけで保存する。

```text
Codex MCP tool
  -> call-scoped local stdio MCP reporter/client
  -> invocation-scoped collector IPC
  -> cmoc collector
  -> repository-local raw observation
```

collector だけが `.cmoc/gu` へ書き込む。reporter/client と agent は feedback file を直接操作しない。machine observation は reporter/client を経由せず、detector から collector へ渡す。

capability は Codex call ごとに一意とし、対象 repository、work-root、agent call、および Codex call へ拘束する。capability value を prompt、Codex argv、Codex call log、または submission payload に含めてはならない。agent や agent が実行する command から collector IPC へ直接接続させてはならない。

この transport のために sandbox、permission profile、または network access の境界を広げてはならない。IPC framing、内部 module、capability の受け渡し方法、および環境変数名は、上記の境界を満たす限り実装裁量とする。

### call の終了

Codex call の終了時は、その call について次の順序で処理する。

1. 新しい request の受付を止める。
2. 受付済み request を処理し、accepted observation の保存を完了する。
3. capability と MCP context を無効化する。

parallel call の lifecycle は互いに分離する。TUI では、1 process の全 turn で同じ Codex call context を使用し、process 終了時に無効化する。

reporter または collector の起動失敗、transport failure、および `rejected` result は、feedback の degradation として warning または構造化 event に記録する。本命 Codex workload を失敗または中断させない。

## 機械的な log 検出

### detector の境界

detector は、allowlist 済み rule と安定した構造化 log event から machine observation を作る。自由文の message、stderr、または command 全文を判定や issue key に使用してはならない。

rule の評価は event の flush 後に行う。rule に一致した occurrence は、recurrence threshold 未満でも raw observation として保存する。集約と threshold 判定は `cmoc feedback report` が行う。

検出または保存の失敗は、warning と構造化 log event に留める。本命 subcommand の結果、run state、retry、または recovery を変更しない。

### rule registry

detector rule は、次の情報を固定する。

- version を含む安定した `rule_id`
- 入力 event type、schema version、および参照する型付き field
- category、summary、impact、および人間が取り得る対応
- recurrence threshold、window、および distinct scope
- 除外する期待動作
- 低カーディナリティの `subject_type` と `normalized_subject_id` の構築方法

machine issue key は、次の canonical UTF-8 byte 列とする。

```text
{{rule_id}}\0{{subject_type}}\0{{normalized_subject_id}}
```

timestamp、session ID、run ID、call ID、自由文、一時 path、および random ID を issue key に含めてはならない。

初期 allowlist は、次の 2 rule に限定する。

| `rule_id` | 対象 | threshold | 除外する状態 |
|---|---|---|---|
| `feedback.reporter_unavailable.v1` | reporter、collector、または transport の利用不能 | 30 日以内に異なる recurrence scope で 2 回 | payload 拒否、rate limit、agent が reporter を呼ばなかった場合 |
| `codex.structured_output_validation_exhausted.v1` | 同じ agent call kind での Structured Output 受理失敗 | 30 日以内に異なる agent call かつ異なる recurrence scope で 2 回 | 補正成功、Structured Output を使わない call、ユーザー中断 |

最初の rule は、`component` と `failure_code` を subject に使用する。2 番目の rule は、低カーディナリティの `agent_call_kind` を subject に使用し、schema hash と最後の failure stage を evidence として保持する。

sandbox escalation は、期待動作との区別と安定した subject を既存 event から決定できないため、初期 rule に含めない。必要な型付き field を producer が正本仕様化した後にだけ追加してよい。

## raw observation の保存

### 保存単位

raw observation は、1 observation 1 file で次へ保存する。

```text
{{repo-root}}/.cmoc/gu/ar/feedback/observation/v1/YYYY/MM/DD/{{observation-id}}.json
```

agent submission の ID は `fbo_` と UUIDv7 の組み合わせとする。machine observation の ID は `rule_id` と event ID から決定論的に生成し、同じ event の再検出で同じ ID にする。

同じ ID と同じ canonical hash の再送は idempotent とする。同じ ID で内容が異なる場合は corruption として拒否する。

raw record には、次の情報だけを保持する。

- schema version、observation ID、source、および観測日時
- collector が確定した call context と version
- secret masking 後の submission または detector payload
- evidence fingerprint
- machine observation の場合だけ、元の構造化 event の識別情報と hash

### durability と retention

accepted を返す前に、sibling temporary file への write、file flush、atomic rename、および parent directory の flush を完了する。accepted は local filesystem 上の保存だけを保証し、別 clone、別 machine、または hardware failure に対する backup を保証しない。

raw observation は、新しい current pointer への正常 publication が完了するまで pending として保持する。report cut、checkpoint、または staged report を作成しただけでは削除しない。

publication 後は、同 report cut が処理した raw observation だけを idempotent に cleanup する。cut 固定後に追加された observation、別の未完了 cut が参照する observation、および validation を通過できなかった observation を削除してはならない。

通常の非対話サブコマンドの terminal result には、pending observation 数だけを表示する。100 件以上ある場合、または最古の pending observation が 7 日以上前の場合は、`cmoc feedback report` の実行を促す warning を加える。件数を算出できない場合も warning とする。件数、算出失敗、または warning によって、サブコマンド固有の `result`、終了コード、run state、retry、または成功判定を変更してはならない。
