# feedback の repository-local state

本書は、feedback report が使用する repository-local state、report cut、checkpoint、atomic publication、および cleanup を定める。raw observation と detector rule は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` を正本とする。

## state の目的

feedback state は、現在の未解決問題と、進行中の report を安全に扱うための active state である。履歴 database にはしない。

長期保持してよい情報を次に示す。

- active state へ未反映の pending observation
- 現在 `unresolved` である issue の compact record
- recurrence threshold 未満の machine observation の bounded aggregate
- 中断または失敗から report を再開するための report cut と正式な checkpoint
- publication 済みの正常 Markdown report
- durable 保存済みの `incomplete` 診断 report
- 現在の active generation と正常 Markdown report を選ぶ current pointer

解決済み issue、処理済み observation、および完了済み checkpoint を active state の履歴として残してはならない。過去の Markdown report の retention は、active state の compaction と分離する。

## 所有範囲と配置

feedback state は `{{repo-root}}` が所有する。branch、`{{work-root}}`、session、および run は所有単位にしない。

論理的な配置を次に示す。

```text
{{repo-root}}/.cmoc/gu/ar/feedback/
├── observation/v1/...
├── active/current.json
├── active/generation/{{generation-id}}/
│   ├── manifest.json
│   ├── issue/...
│   └── machine_aggregate/...
└── work/{{report-cut-id}}/
    ├── manifest.json
    ├── reference/...
    └── checkpoint/...

{{repo-root}}/.cmoc/gu/ar/report/feedback/
├── {{time-stamp}}.md
├── incomplete/{{time-stamp}}.md
└── invocation/{{time-stamp}}.md
```

`{{repo-root}}/.cmoc/gu` 全体を Git 追跡対象外とする。session と run の join または abandon は、feedback state を取り込み、破棄、巻き戻し、または複製してはならない。

`invocation/{{time-stamp}}.md` は `cmoc feedback report` の中断またはエラーを要約する primary report であり、feedback state または publication artifact ではない。current pointer の参照先にしない。内容と生成条件は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` を正本とする。

state root または current pointer が存在しない状態は、有効な初期状態とする。空 directory や `.gitkeep` は作らない。

## artifact の役割

state を構成する artifact の役割を次に示す。

| artifact | 役割 |
|---|---|
| active generation | 同じ report で確定した active issue と threshold 未満 aggregate の immutable な集合 |
| current pointer | 現在の正常な active generation と Markdown report を一意に選ぶ publication point |
| report cut manifest | 1 回の report に使用する固定入力と処理状態の正本 |
| reference | candidate の現在状態を検証するため、report cut に固定した repository content、fingerprint、または probe result |
| checkpoint | 受理済み normalization または verification output の再利用可能な記録 |
| `incomplete` 診断 report | `inconclusive` によって正常 publication が成立しなかった cut の確定済み判定と blocker を materialize した durable な Markdown report |

timestamp、Git commit、branch reachability、または directory の列挙順から current state を推測してはならない。current pointer が参照する generation manifest と正常 Markdown report の path および hash を検証できる場合だけ、その組を最新の正常 publication とする。current pointer は `incomplete` 診断 report を参照しない。

## JSON と排他制御

state の JSON は、UTF-8、object key の辞書順、末尾改行ありの canonical form で保存する。hash は canonical byte 列の SHA256 とする。

immutable artifact は、sibling temporary file への write、file flush、atomic rename、および parent directory の flush によって durable に保存する。同じ path への同じ byte 列の再保存は idempotent とする。同じ path に異なる byte 列がある場合は corruption として停止し、自動上書きしない。

active state を変更する `cmoc feedback report` は、`{{repo-root}}` ごとの feedback writer 排他を使用する。排他は、report cut の固定前から publication、再開 state の確定、または失敗終了まで保持する。

lock の方式は実装裁量とする。所有者を安全に判定できない lock を暗黙に破棄してはならない。cut 固定後も collector は新しい observation を保存できなければならない。

## active generation

active generation には、次の record だけを含める。

- 直近の正常 report で `unresolved` と検証された active issue
- recurrence threshold 未満の machine aggregate

generation manifest は、generation ID、作成元の report cut、作成日時、および各 record の path と hash を固定する。全 record を保存して検証した後に manifest を保存する。valid な manifest がない generation を読み取ってはならない。

### issue identity

machine issue の canonical key は、detector rule が定める machine issue key とする。

agent observation から新しい issue を作る場合は、最初の observation ID から安定した canonical key を作る。normalization agent が既存 issue との同一性を選んだ場合は、既存の issue ID と canonical key を維持する。

issue ID は canonical key の hash から決定論的に生成する。同じ issue ID と異なる canonical key が見つかった場合は collision として停止し、暗黙に salt を追加してはならない。

active state に残っていない過去の agent issue と、後日の observation の同一性は判定しない。machine issue は canonical key が同じであれば、再発時にも同じ issue identity を使用する。

### active issue record

active issue record は、次回の候補絞り込み、verification、および人間向け表示に必要な情報だけを保持する。

- issue identity、origin、category、summary、および impact
- occurrence count、affected session count、最初と最後の観測日時
- bounded な representative evidence、subject、および fingerprint
- 最新の `unresolved` verification の reason、current evidence、および human action
- machine issue の場合だけ、recurrence window を評価できる bounded summary

evidence は、削除予定の raw observation や report cut だけを参照してはならない。次回 report で再確認できる安定した subject と、人間が確認できる compact な説明を materialize する。secret を複製してはならない。

保持件数と集計情報は schema-fixed な上限を持つ。上限超過時の選択は、report cut の固定入力に対して決定論的に行う。AI に保持対象を選ばせない。

`resolved` または `not_actionable` の issue は、新しい generation に含めない。`inconclusive` が 1 件でもある場合は、新しい generation 自体を publication しない。

### threshold 未満の machine aggregate

machine observation は、rule の canonical key と recurrence window で集約する。threshold 未満の場合は issue を作らず、判定に必要な count、distinct dimension、time bucket、代表 evidence、および fingerprint だけを bounded aggregate として保持する。

threshold を満たした aggregate は issue candidate へ昇格し、同じ generation に aggregate として重複保存しない。window 外の occurrence を除いた結果が空なら aggregate を削除する。threshold 未満 aggregate は人間向け report に表示しない。

## report cut と checkpoint

### report cut

report cut manifest は、少なくとも次の入力を固定する。

- 今回処理する pending observation
- cut 開始時の current pointer、active issue、および machine aggregate
- candidate の現在状態を確認する reference
- allowlist 済み current-state probe の入力と結果
- normalization、verification、schema、および決定論的処理規則の version

reference には cut 内で一意な ID と種別を付ける。保存内容には raw observation と同等以上の secret masking を適用する。live repository state の後読みを report cut の代わりにしてはならない。

repository content の capture 中に値が変化した場合は、未確定 cut を破棄して再取得するか、state を変更せずエラー終了する。異なる時点の内容を 1 つの cut として扱ってはならない。

cut の固定後は入力を変更しない。後から追加された observation は次回の cut へ残す。処理状態、checkpoint reference、正常 publication target、診断 report target、および cleanup target だけを atomic に追記または更新してよい。

同じ repository で、再開対象の report cut は高々 1 件とする。完了した cut を履歴として蓄積しない。

### checkpoint

normalization と verification の output は、schema と決定論的事後条件を満たした後だけ正式な checkpoint として保存する。verification verdict が `inconclusive` であるかにかかわらず、受理済み output には同じ checkpoint 規則を適用する。checkpoint は、入力、builder、schema、および output を hash で結び付ける。

同じ report cut と同じ入力で再開する場合は、整合する checkpoint を再利用する。未完了 call、不適合 output、correction の途中結果、および失敗履歴を checkpoint として保存してはならない。

中断または失敗時は、再開に必要な report cut、reference、および正式な checkpoint だけを保持する。正常 publication 後は、active issue record に materialize した情報を除き削除する。

`inconclusive` は有効な verdict だが、正常 publication へ進めない report processing blocker とする。

## `incomplete` 診断 report

全 candidate の正式な verification checkpoint がそろい、1 件以上が `inconclusive` である場合は、その report cut を `incomplete` として終端させる。`inconclusive` を `unresolved` または active issue に変換してはならない。

`incomplete` 診断 report は、次へ durable に保存する。

```text
{{repo-root}}/.cmoc/gu/ar/report/feedback/incomplete/{{time-stamp}}.md
```

診断 report は、sibling temporary file への write、file flush、atomic rename、および parent directory の flush によって保存する。report cut reference または checkpoint を削除しても単独で読める内容を最終 file に materialize する。最終 file の path と hash を再検証し、report cut manifest に記録してから cut を terminal な `incomplete` とする。

診断 report の durable 保存は、正常 publication から独立した state transition とする。保存しても、次の state を変更しない。

- 新しい active generation を作成または publication しない。
- current pointer を切り替えない。
- 直前の正常 publication を current のまま維持する。
- report cut が処理した raw observation を cleanup しない。
- active issue と threshold 未満 machine aggregate を置き換えない。

診断 report の durable 保存後は、report cut を terminal な `incomplete` として記録する。次の明示的な `cmoc feedback report` は同じ cut の checkpoint を再利用せず、新しい cut を作る。新しい cut を作る前に、terminal な cut の work artifact を manifest に従って削除する。この削除に raw observation を含めてはならない。

診断 report を durable に保存できなかった場合は、cut を `incomplete` として完了させない。再開に必要な report cut、reference、および正式な checkpoint を保持し、正常 publication と raw observation の cleanup を行わずにエラー終了する。

## 正常 report の atomic publication

新しい正常 report は、次の順序で publication する。`incomplete` 診断 report の保存に、この publication 手順または current pointer を使用してはならない。

1. 新しい active generation の record と manifest を durable 保存する。
2. Markdown report を最終 path へ durable 保存する。
3. generation manifest と Markdown report の path および hash を再検証する。
4. 両方を参照する current pointer を atomic に切り替える。
5. current pointer の切替後に、処理済み observation、切替前の generation、および完了済み work artifact を cleanup する。

current pointer の切替だけを publication point とする。切替前に異常終了した場合は、直前の pointer が引き続き current となる。staged artifact を正常 report として扱ってはならない。

cleanup は、current pointer と hash で結び付いた report cut manifest を使用して idempotent に行う。cleanup が途中で失敗しても current pointer を巻き戻さない。次回の report は cleanup を完了してから新しい cut を作る。

`incomplete` 診断 report の保存は、publication 後の cleanup を開始する条件にならない。

manifest にない対象を推測して削除してはならない。manifest または対象の hash が一致しない場合は corruption として停止する。
