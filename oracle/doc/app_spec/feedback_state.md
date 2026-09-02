# feedback の repository-local state

本書は、feedback remediation run が使用する repository-local state、immutable な intake wave、high-watermark、checkpoint、report cut、atomic publication、および cleanup を定める。raw observation と detector rule は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「feedback observation の収集」を正本とする。

## state の目的

feedback state は、現在の `human_required` issue と、進行中の feedback remediation run を安全に扱うための active state である。履歴 database にはしない。

長期保持してよい情報を次に示す。

- active state へ未反映の pending observation
- 直近の正常 publication で `human_required` と確定した issue の compact record
- recurrence threshold 未満の machine observation の bounded aggregate
- 中断、失敗、join 後の publication failure、または再検証から回復するための run manifest、intake wave、report cut、および正式な checkpoint
- publication 済み report と、現在の正常 publication を選ぶ current pointer

`fixed`、`already_resolved`、`not_actionable`、処理済み observation、および完了済み checkpoint を active state の履歴として残してはならない。issue commit、変更 path、および検証結果の監査情報は、feedback issue 一覧ではなく run report、invocation report、または subcommand log に保持してよい。

## 所有範囲と配置

feedback state は `{{repo-root}}` が所有する。branch、`{{work-root}}`、session、および run branch は所有単位にしない。

論理的な配置を次に示す。

```text
{{repo-root}}/.cmoc/gu/ar/feedback/
├── observation/v1/...
├── active/current.json
├── active/generation/{{generation-id}}/
│   ├── manifest.json
│   ├── issue/...
│   └── machine_aggregate/...
└── work/{{feedback-run-id}}/
    ├── manifest.json
    ├── wave/{{wave-sequence}}/...
    ├── checkpoint/...
    ├── report_cut.json
    └── publication_completion.json

{{repo-root}}/.cmoc/gu/ar/report/feedback/
├── {{time-stamp}}.md
├── incomplete/{{time-stamp}}.md
└── invocation/{{time-stamp}}.md
```

`observation/v1` の `v1` は raw observation 保存 layout の version であり、内包する reporter input schema の version とは独立する。reporter input version 2 の導入だけを理由に、既存 raw observation の path を移動しない。

`{{repo-root}}/.cmoc/gu` 全体を Git 追跡対象外とする。session と run の join または abandon は、feedback state を暗黙に取り込み、巻き戻し、複製、または削除してはならない。

`invocation/{{time-stamp}}.md` は `cmoc feedback report` の中断またはエラーを要約する primary report であり、feedback state または publication artifact ではない。current pointer の参照先にしない。内容と生成条件は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` を正本とする。

state root または current pointer が存在しない状態は、有効な初期状態とする。空 directory や `.gitkeep` は作らない。

## artifact の役割

state を構成する artifact の役割を次に示す。

| artifact | 役割 |
|---|---|
| active generation | 同じ正常 publication で確定した `human_required` issue と threshold 未満 aggregate の immutable な集合 |
| current pointer | 現在の正常な active generation と Markdown report を一意に選ぶ publication point |
| feedback run manifest | 1 invocation の入力、run identity、wave、join、publication、および cleanup の状態を結び付ける記録 |
| intake wave | その wave が処理する observation、active issue、正規化済み issue identity、および根拠の immutable な固定入力 |
| high-watermark | collector が durable に受理済みである observation の atomic な上限境界 |
| checkpoint | 受理済み normalization または remediation の入力、結果、検証、および commit を hash で結び付ける記録 |
| report cut | wave loop の自然完了後に封印する publication 入力。ordered wave、最終 high-watermark、base current pointer、全終端結果、および merge 対象を固定する |
| publication completion record | merge または no-op join 後の session commit、run branch の到達可能性、および最終 tree 検証結果を report cut と結び付ける immutable な記録 |
| `incomplete` 診断 report | `inconclusive` によって正常 publication が成立しなかった処理の確定済み結果と blocker を materialize した durable な Markdown report |

timestamp、Git commit、branch reachability、または directory の列挙順から current state を推測してはならない。current pointer が参照する generation manifest と正常 Markdown report の path および hash を検証できる場合だけ、その組を最新の正常 publication とする。current pointer は `incomplete` 診断 report を参照しない。

## JSON と排他制御

state の JSON は、UTF-8、object key の辞書順、末尾改行ありの canonical form で保存する。hash は canonical byte 列の SHA256 とする。

immutable artifact は、sibling temporary file への write、file flush、atomic rename、および parent directory の flush によって durable に保存する。同じ path への同じ byte 列の再保存は idempotent とする。同じ path に異なる byte 列がある場合は corruption として停止し、自動上書きしない。

run manifest の進行 state と artifact reference は、先行 state と新しい immutable artifact の hash を検証したうえで atomic に更新する。intake wave の固定入力、正式な checkpoint、および封印済み report cut を in-place で変更してはならない。

active state を変更する `cmoc feedback report` は、`{{repo-root}}` ごとの feedback writer 排他を使用する。排他は、最初の high-watermark を固定する前から publication、`incomplete` の確定、再開 state の確定、または失敗終了まで保持する。

lock の方式は実装裁量とする。所有者を安全に判定できない lock を暗黙に破棄してはならない。排他保持中も collector は新しい observation を durable 保存できなければならない。

## active generation

active generation には、次の record だけを含める。

- 直近の正常 publication で `human_required` と確定した active issue
- recurrence threshold 未満の machine aggregate

generation manifest は、generation ID、作成元の report cut、join 後の session commit、作成日時、および各 record の path と hash を固定する。全 record を保存して検証した後に manifest を保存する。valid な manifest がない generation を読み取ってはならない。

### issue identity

machine issue の canonical key は、detector rule が定める machine issue key とする。

agent observation から新しい issue を作る場合は、最初の observation ID から安定した canonical key を作る。normalization agent が既存 issue との同一性を選んだ場合は、既存の issue ID と canonical key を維持する。

issue ID は canonical key の hash から決定論的に生成する。同じ issue ID と異なる canonical key が見つかった場合は collision として停止し、暗黙に salt を追加してはならない。

active state に残っていない過去の agent issue と、後日の observation の同一性は判定しない。machine issue は canonical key が同じであれば、再発時にも同じ issue identity を使用する。

### active issue record

active issue record は、次回の候補絞り込み、remediation、および人間向け表示に必要な情報だけを保持する。

- issue identity、origin、category、summary、および impact
- occurrence count、affected session count、最初と最後の観測日時
- bounded な representative evidence、subject、および fingerprint
- 最新の `human_required` result の reason、current evidence、および human action
- machine issue の場合だけ、recurrence window を評価できる bounded summary

evidence は、削除予定の raw observation、intake wave、または report cut だけを参照してはならない。次回 report で再確認できる安定した subject と、人間が確認できる compact な説明を materialize する。secret を複製してはならない。

保持件数と集計情報は schema-fixed な上限を持つ。上限超過時の選択は、固定済み wave 入力に対して決定論的に行う。AI に保持対象を選ばせない。

`fixed`、`already_resolved`、および `not_actionable` の issue は、新しい generation に含めない。`inconclusive` が 1 件でもある場合は、新しい generation 自体を publication しない。

### threshold 未満の machine aggregate

machine observation は、rule の canonical key と recurrence window で集約する。threshold 未満の場合は issue を作らず、判定に必要な count、distinct dimension、time bucket、代表 evidence、および fingerprint だけを bounded aggregate として保持する。

threshold を満たした aggregate は issue candidate へ昇格し、同じ generation に aggregate として重複保存しない。window 外の occurrence を除いた結果が空なら aggregate を削除する。threshold 未満 aggregate は人間向け report に表示しない。

## intake wave と high-watermark

### intake wave

各 intake wave は、次の入力を固定する。

- 直前の high-watermark より後、今回の high-watermark 以前に durable 保存された pending observation
- 最初の wave の場合だけ、run 開始時の current pointer、全 active issue、および threshold 未満 aggregate
- observation schema と互換 view の version
- validation、normalization、deduplication、detector rule、および集約規則の version
- normalization 後の未処理 issue identity と bounded evidence

wave input は durable 保存後に変更しない。追加 evidence は後続 wave の入力として同じ issue identity へ関連付けてよいが、先行 wave を書き換えてはならない。

同じ run ですでに remediation call を実行した issue identity と、同じ run で `fixed | already_resolved | not_actionable | human_required` に確定した issue identity は、後続 wave の remediation 対象にしない。完全な重複 observation も新しい wave の理由にしない。

### high-watermark

high-watermark は、collector の durable な受理順序に対する単調増加境界とする。directory の列挙順、timestamp、quiet period、または observation 件数から推測してはならない。

wave 終了時は、対応する全 remediation reporter context の受付停止と drain を完了した後に high-watermark を atomic に確定する。前回境界より後、今回境界以前の observation を validation、normalization、および deduplication し、新しい未処理 issue identity があれば次の wave を作る。

新しい未処理 issue identity がなければ wave loop を自然完了し、最後の境界を最終 high-watermark とする。最終 high-watermark より後に受理された observation は、次回 invocation の pending input として残す。

## checkpoint と report cut

### checkpoint

normalization と issue remediation の output は、schema と宣言済みの決定論的事後条件を満たした後だけ正式な checkpoint として保存する。

issue remediation checkpoint は、少なくとも次の情報を hash で結び付ける。

- run、wave、issue identity、論理 agent call、builder、および schema
- 固定入力、正式な Structured Output、および終端結果
- realization file の net 差分、`changed_paths` の照合、および変更禁止対象の検査結果
- agent の検証結果と issue commit ID。差分がない場合は commit を作らなかったこと

不適合 output、correction の途中結果、失敗した agent call、差分検査失敗、commit 失敗、および rollback 前の差分を正式な issue result checkpoint にしてはならない。これらは invocation error の診断情報として分離する。

同じ run と同じ issue identity に正式な remediation checkpoint は高々 1 件とする。Structured Output correction、retry、および quota 待機後の resume は同じ論理 agent call の checkpoint に含める。

### report cut

単一の可変 report cut を intake に使用してはならない。report cut は、wave loop が自然完了した後に一度だけ封印する。

report cut は、少なくとも次の入力を固定する。

- ordered intake wave と各 wave の hash
- run 開始時の current pointer、active generation、および最終 high-watermark
- 処理した issue identity と終端結果
- issue commit、run branch HEAD、および merge 前の検証結果
- 正常 publication target、`incomplete` 診断 target、および cleanup target

merge または no-op join 後は、session tree の commit と最終 tree 検証結果を別の immutable な publication completion record として保存し、run manifest から report cut とともに参照する。封印済み report cut、wave input、issue result、最終 high-watermark、または cleanup target を変更してはならない。

## `incomplete` 診断 report

全 issue が終端結果に達し、1 件以上が `inconclusive` である場合は、run branch の session branch への merge または no-op join の成功後に `incomplete` 診断 report を保存する。`inconclusive` を `human_required` または active issue に変換してはならない。

`incomplete` 診断 report は、次へ durable に保存する。

```text
{{repo-root}}/.cmoc/gu/ar/report/feedback/incomplete/{{time-stamp}}.md
```

診断 report は、intake wave、report cut、または checkpoint を削除しても単独で読める内容として durable 保存し、path と hash を再検証する。保存しても新しい active generation を作らず、current pointer、直前の active state、および raw observation を維持する。

診断 report を durable に保存できなかった場合は、処理を `incomplete` として完了させない。raw observation、直前の current pointer、report cut、および再確認に必要な正式な checkpoint を保持し、正常 publication と cleanup を行わずにエラー終了する。

診断 report の保存後は、manifest が固定した完了済み work artifact だけを cleanup してよい。cleanup 後の次回 invocation は、join 後の session tree、pending observation、および直前の active state から新しい run を作り、`inconclusive` の issue を現在の tree で再確認する。

## 正常 report の atomic publication

正常 publication は、report cut が参照する run branch の session branch への merge または no-op join が成功し、join 後の tree を最終状態として検証した後にだけ開始する。

新しい正常 report は、次の順序で publication する。

1. `human_required` issue だけを含む新しい active generation の record と manifest を durable 保存する。
2. Markdown report を最終 path へ durable 保存する。
3. generation manifest と Markdown report の path および hash を再検証する。
4. 両方を参照する current pointer を atomic に切り替える。
5. current pointer の切替後にだけ、最終 high-watermark 以前の処理済み observation、切替前の generation、および完了済み work artifact を cleanup する。

current pointer の切替だけを publication point とする。切替前に異常終了した場合は、直前の pointer が引き続き current となる。staged artifact、run branch 上の結果、issue commit、または自動 join の成功だけを正常 report として扱ってはならない。

自動 join 後に publication point より前の処理が失敗した場合は、raw observation、直前の current pointer、および recovery に必要な run artifact を維持する。次の invocation は join 後 tree を再検証して同じ publication を idempotent に再開する。

cleanup は、current pointer と hash で結び付いた report cut を使用して idempotent に行う。cleanup が途中で失敗しても current pointer を巻き戻さない。次回の report は cleanup を完了してから新しい run を開始する。

処理済み observation と完了済み work artifact の cleanup を確定した後にだけ、feedback run の state と隔離資源を正常終了状態へ戻す。publication または cleanup の失敗中は `run.state=error` と隔離資源を維持する。

manifest にない対象または最終 high-watermark より後の observation を推測して削除してはならない。manifest または対象の hash が一致しない場合は corruption として停止する。

## run lifecycle との整合

run join と abandon が feedback state に与える影響は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「編集 run の共通仕様」を正本とする。どちらも raw observation と直前の current pointer を保持し、破棄した run commit に依存する `fixed` checkpoint を publication 可能な結果として残してはならない。
