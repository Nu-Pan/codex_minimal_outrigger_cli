# feedback の repository-local active state

本書は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` が定義する active issue、threshold 未満の machine aggregate、report cut の一時 state、および atomic publication を定める。raw observation と machine rule の正本は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` とする。

## state の原則

feedback state は、現在の未解決問題を処理するための active state である。過去の判断を再構築する append-only ledger として使用してはならない。

長期保存してよい repository-local state は、次の情報に限定する。

- active state へまだ反映していない pending observation
- 現在 `unresolved` である active issue ごとの compact record 1 件
- recurrence threshold 未満の machine observation に必要な bounded aggregate
- 実行中、中断中、または安全な publication 再開中の report cut manifest と正式な checkpoint
- publication 済みの Markdown report
- 現在の active generation と正常 report を一意に選ぶ current pointer

解決済み issue、処理済み observation、および完了済み checkpoint を通常状態へ残してはならない。異常終了からの回復に必要な旧 generation と staged artifact は一時的に残ってよいが、current pointer の切替後に idempotent に削除する。

## 所有単位と保存先

feedback state は、すべて `{{repo-root}}` が所有する。現在の branch、`{{work-root}}`、session、および run は所有単位にしない。

保存領域の論理構成を次に示す。

```text
{{repo-root}}/.cmoc/gu/ar/feedback/
├── observation/v1/...
├── active/current.json
├── active/generation/{{generation-id}}/manifest.json
├── active/generation/{{generation-id}}/issue/{{issue-id}}.json
├── active/generation/{{generation-id}}/machine_aggregate/{{aggregate-id}}.json
└── work/{{report-cut-id}}/
    ├── manifest.json
    ├── reference/...
    └── checkpoint/
        ├── normalization/...
        └── verification/...
```

Markdown report は、次へ保存する。

```text
{{repo-root}}/.cmoc/gu/ar/report/feedback/{{time-stamp}}.md
```

`{{repo-root}}/.cmoc/gu` 全体を Git 追跡対象外とする。session または run の join と abandon は、この state を取り込み、破棄、巻き戻し、または複製してはならない。

state root または `active/current.json` が存在しない状態は、有効な初期状態とする。空 directory または `.gitkeep` は作らない。

## JSON と durability の共通規則

全 JSON file は UTF-8、object key の辞書順、末尾改行ありの canonical form で保存する。hash は canonical byte 列の SHA256 とする。

durable 保存は、sibling temporary file への write、file flush、atomic rename、および parent directory の flush を含む。immutable artifact と同じ path に同じ byte 列を再保存する操作は idempotent とする。同じ path に異なる byte 列がある場合は corruption として停止し、自動上書きしない。

active generation、current pointer、report cut manifest、および checkpoint は、schema、hash、path、参照先、および相互参照の整合性を使用前に検証する。検証に失敗した state を無視して新しい正常 report を publication してはならない。

## writer 排他制御

active state、report cut、および current pointer を更新する処理は、`{{repo-root}}` ごとの repository-level feedback writer 排他制御へ従う。同じ repository で複数の `cmoc feedback report` が同時に state を更新してはならない。

`cmoc feedback report` は、report cut の固定前から current pointer の切替、再開 state の確定、または失敗終了まで writer 排他を保持する。長時間の AI 検証を理由に、同じ repository で別の report writer を並行させてはならない。

排他の lock file、lease、待機、および stale owner 回復の具体方式は実装裁量とする。所有者を安全に判定できない lock を暗黙に破棄してはならない。排他を取得できない呼び出しは state を変更せず、競合中であることを示して待機または終了する。

raw observation の publication と report cut の境界は線形化する。cut 作成中だけ collector の atomic publication と協調する具体方式は実装裁量とする。cut 固定後は collector が新しい observation を保存できなければならない。

## active generation と current pointer

### generation manifest

active generation は、active issue record と threshold 未満の machine aggregate だけを含む。generation manifest は、少なくとも次の情報を持つ。

- `schema_version`
- `generation_id`
- generation を作成した `report_cut_id`
- 作成日時
- active issue record の path と SHA256 を issue ID 順に並べた配列
- machine aggregate record の path と SHA256 を canonical key 順に並べた配列

generation ID は `fbg_` と UUIDv7 の組み合わせとする。manifest は、列挙する全 record を durable 保存して検証した後に最後に保存する。valid な manifest がない generation を active state として読み取ってはならない。

### current pointer

`active/current.json` は、現在の正常 publication を一意に選ぶ唯一の pointer である。少なくとも次の情報を持つ。

- `schema_version`
- generation ID、manifest path、および manifest SHA256
- report cut ID と、publication に使用した report cut manifest の SHA256
- Markdown report path と SHA256
- publication 時刻
- `result`: `ok | attention`

current pointer が参照する generation と report の両方を検証できる場合だけ、その組み合わせを最新の正常 report と active state とする。timestamp、Markdown report の列挙順、Git commit、branch reachability、または predecessor chain から最新状態を推測してはならない。

current pointer が識別する report cut manifest は、切替後 cleanup が完了すれば存在しなくてよい。manifest が存在する場合は pointer の SHA256 と一致することを検証し、新しい report cut より先に cleanup を再開する。manifest が存在しないことだけを current pointer の corruption としてはならない。

## issue identity

machine issue の canonical key は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の rule registry が定める machine issue key とする。agent observation から新規作成する issue の canonical key は、`agent\0{{最初の observation ID}}` とする。

issue ID は、canonical key の SHA256 を lowercase base32 とし、その先頭 26 文字へ `fbi_` を付けた値とする。normalization agent が既存 active issue との同一性を選んだ場合は、その issue ID と canonical key を維持する。同じ issue ID で異なる canonical key が見つかった場合は collision として停止し、salt を暗黙に追加してはならない。

解決後に削除された agent issue と後日の observation が同一であるかを履歴から復元することは保証しない。machine issue は canonical key が同じであれば、再発時にも同じ issue ID となる。

## active issue record

active issue record は、直近の正常 report で `unresolved` と検証された issue につき 1 件だけ保存する。record は、次回の候補絞り込み、verification、および人間向け表示に必要な情報だけを持つ。

- `schema_version`
- issue ID、origin、および canonical key
- category、summary、および impact
- occurrence count と affected session count
- affected session count の更新に必要な bounded distinct-session digest と saturation marker
- 最初と最後の観測日時
- 最大 5 件の representative evidence
- 最大 5 件の evidence subject、repository path、または allowlist 済み probe ID
- 最大 5 件の最新 fingerprint
- 最新 verification の report cut ID、検証日時、reason、current evidence、および human action
- machine issue だけ、recurrence window 外を除外するための bounded time bucket と rule-defined threshold dimension summary

最新 verification は `unresolved` の受理条件を満たした情報だけを保存する。verdict 自体は active issue であることから `unresolved` と一意に決まるため、履歴用の verdict 配列を持たない。

representative evidence と current evidence は、raw observation や削除予定の work artifact への参照だけにしてはならない。次回 report cut で現在状態を再取得できる安定した subject と、Markdown report で人間が確認できる compact な説明を保持する。secret を複製してはならない。

active issue record を作る際は、verification output の cut-scoped reference ID を report cut manifest で解決し、repository path、subject、probe ID、location、および fingerprint のうち該当する安定情報を record へ materialize する。削除する report cut の reference ID だけを残してはならない。

representative evidence、reference target、fingerprint、distinct-session digest、および time bucket の上限超過処理は、report cut の固定入力に対する canonical order と schema-fixed bound だけで決定する。AI に保持対象を選ばせてはならない。

全 occurrence、revision、assessment、または過去 verification を保持してはならない。件数、affected session 数、最初と最後の観測日時は compact aggregate として更新する。distinct-session digest が schema の上限へ達した後は saturation marker を設定し、affected session count を下限値として `{{count}}+` と表示してよい。

machine issue の集計値は recurrence window 内の occurrence だけから計算する。bounded time bucket と rule-defined threshold dimension summary は、window 外の値を決定論的に除外できる情報を持つ一方、個々の occurrence record を保持してはならない。

verification が `resolved` または `not_actionable` とした issue は、新しい generation に含めない。`inconclusive` の issue を active issue として維持または新規作成することも禁止する。`inconclusive` が 1 件でもある場合は generation 自体を publication しないため、直前の active generation がそのまま current となる。

## threshold 未満の machine aggregate

machine observation は、rule の recurrence window 内にある occurrence だけを canonical key ごとに集約する。window 外の occurrence と scope marker は、新しい generation を作る前に除外する。

threshold 未満の machine observation は issue record を作らず、canonical key ごとに bounded aggregate 1 件だけを保存する。aggregate は、次の情報に限定する。

- schema version、aggregate ID、rule ID、および canonical key
- category、summary、impact、および detector が定めた human action
- recurrence window の境界
- occurrence count、affected session count、および rule が要求する distinct threshold dimension ごとの count
- window 外の値を除外するための bounded time bucket
- threshold 判定に必要な recurrence scope、agent call、または他の rule-defined dimension の digest と最終観測日時。各 dimension の件数は rule の threshold 未満に制限する
- 最初と最後の観測日時
- bounded な representative evidence と最新 fingerprint

aggregate ID は canonical key の SHA256 lowercase hexadecimal に `fba_` を付けた値とする。threshold を満たした aggregate は issue candidate へ昇格させ、同じ generation に threshold 未満 aggregate として重複保存しない。

threshold 未満 aggregate は人間向け report に表示しない。window 外の occurrence を除いた結果が空になった aggregate は削除する。

## report cut の一時 state

report cut は `work/{{report-cut-id}}/manifest.json` を正本とする。report cut ID は `fbc_` と UUIDv7 の組み合わせとする。

manifest は、少なくとも次の入力を canonical value と、artifact がある場合の path および SHA256 で固定する。

- schema version、report cut ID、および cut を固定した日時
- 今回処理する pending observation の ID、path、および SHA256
- cut 開始時の current pointer、active generation、全 active issue、および全 bounded machine aggregate
- candidate の現在状態を確認するために取得した repository 内参照内容または fingerprint
- allowlist 済み current-state probe を実行した場合の probe ID、入力、および結果
- normalization と verification の builder、schema、および決定論的処理規則の version
- cut の処理状態と、再開に必要な正式な checkpoint の path と SHA256
- publication 前に確定した新 generation、Markdown report、および切替後 cleanup target の path と SHA256

参照には cut 内で一意な reference ID と、`observation | repository_content | current_fingerprint | probe_result` の種別を付ける。repository content を保存するか、必要な excerpt と fingerprint だけを保存するかは、安全性と秘密情報の境界を満たす限り実装裁量とする。

report cut の参照は、元の call が読める repository 内対象だけから作る。保存する内容にも raw observation と同等以上の secret masking を適用する。live repository path を後から読み直すことを、report cut の代わりにしてはならない。

manifest を durable 保存する前に、captured repository content と fingerprint を同じ path の再取得結果で検証する。capture 中に値が変化した場合は未確定 cut を破棄して再取得するか、state を変更せずエラー終了する。異なる時点の repository content を 1 つの安定した cut として偽ってはならない。

cut 固定後に追加された observation は manifest へ追記せず、次回 report の pending observation とする。cut の input section にある active state、参照内容、fingerprint、および probe result も固定後に更新してはならない。processing status、checkpoint reference、および publication／cleanup section は、固定入力を変えない atomic update だけを許容する。current pointer には publication 直前の最終 manifest hash を記録する。

repository ごとに、再開対象の report cut は高々 1 件とする。別の cut の完了済み checkpoint または manifest を履歴として蓄積してはならない。

## checkpoint と再開

normalization と verification の正式な Structured Output は、対応する agent call の全受理条件を満たした後だけ checkpoint として durable 保存する。checkpoint は、入力 hash、candidate ID、builder hash、schema hash、正式な出力、および出力 hash を持つ。

同じ report cut と同じ入力で再開する場合は、整合する checkpoint を再利用し、同じ agent call の quota を再消費しない。入力、builder、schema、または決定論的事後条件が異なる checkpoint は再利用しない。

未完了 call、schema 不適合 output、または決定論的事後条件に違反した output を正式な checkpoint として保存してはならない。correction call の一時結果と失敗履歴を repository-local feedback state へ蓄積してはならない。

中断、AI call failure、または durable publication failure では、同じ report cut を安全に再開するための manifest と正式な checkpoint だけを保持する。正常 publication 後は active issue record に取り込まれた最新 verification を除き、cut の manifest、参照 snapshot、および全 checkpoint を削除する。

`inconclusive` は有効な verification verdict だが、同じ固定入力から正常 publication へ進めない terminal result とする。その cut は正常 report として publication せず、次の明示的な report 要求が新しい cut を作る前に一時 state を削除してよい。診断は subcommand log に残す。

## atomic publication と cleanup

新しい正常 report は、次の順序で publication する。

1. 新しい active generation の全 record と manifest を durable 保存する。
2. Markdown report を最終 path へ durable 保存する。
3. generation manifest と Markdown report の schema、path、および hash を再検証する。
4. 両方を参照する新しい `active/current.json` を sibling temporary file から atomic rename し、parent directory を flush する。
5. current pointer の切替後に、処理済み raw observation、旧 active generation、完了した report cut、一時 artifact、および legacy state を idempotent に削除する。

current pointer の切替だけを、active state と正常 report の publication point とする。切替前に旧 active generation または処理対象 observation を削除してはならない。

切替前に異常終了した場合は、直前の current pointer が引き続き唯一の正常 state を指す。staged generation または Markdown artifact を正常 report として扱ってはならない。

切替後の cleanup では、current pointer と hash が一致する完了済み report cut manifest を cleanup manifest として使用する。次の対象を順に削除し、各 directory の flush を完了する。

1. manifest が列挙する処理済み raw observation
2. 旧 active generation、legacy state、および staged artifact
3. 完了済み normalization／verification checkpoint と reference snapshot
4. cleanup manifest 自体と空になった work directory

cleanup manifest は最後に削除する。途中で失敗した場合は新しい current pointer を巻き戻さず、次回の feedback report が同じ manifest を検証して cleanup を完了してから、新しい report cut を作成する。manifest が先に失われ、処理済み raw observation を安全に識別できない状態は corruption として扱う。

current pointer が切替済みの cleanup では、manifest に列挙された削除対象が既に存在しないことを完了済みとして扱う。まだ存在する対象の hash 不一致、manifest 自体の hash 不一致、または manifest にない対象の推測削除は corruption として停止する。

publication 済み Markdown report の retention は active state の compaction と分離する。過去の Markdown report を deduplication、処理済み判定、active state の差分、または最新 report の選択に使用してはならない。

## legacy state からの一回限りの切替

append-only な issue、revision、occurrence、assessment、human disposition、ingestion receipt、normalization unit、report snapshot、state snapshot、または predecessor chain を持つ legacy state は、新しい active state と並行運用しない。

`active/current.json` がなく legacy state が存在する最初の report では、legacy state を read-only の移行入力として扱う。移行 cut は、全 raw observation と、legacy state から整合して読み取れる effective issue の compact projection を入力に含める。legacy machine record にも新しい recurrence window と threshold を機械適用し、threshold 未満は bounded aggregate とする。legacy human disposition は新しい verification verdict の代わりに使用しない。

legacy state の schema、hash、または参照整合性を確認できない場合は、新しい正常 report を publication せず、legacy state を変更しない。移行 cut の全候補を通常どおり verification できた場合だけ、新しい generation と report を atomic に publication する。

`active/current.json` へ切り替えるまでは、legacy state が一意に示す直前の正常 report を人間向けの latest normal report として維持する。この例外は移行失敗時に既存の正常 report を失わないためだけに使用し、legacy report または predecessor chain を新しい deduplication、candidate state、差分、または処理済み判定の入力にしてはならない。

current pointer の切替後は、legacy normalized state と履歴 record を idempotent に削除する。移行用 copy、legacy checkpoint、または旧履歴の backup を feedback state として永久保存してはならない。
