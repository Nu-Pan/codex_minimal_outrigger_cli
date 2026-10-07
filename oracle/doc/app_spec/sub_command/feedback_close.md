# `cmoc feedback close`

人間が外部で解決を確認した `inconclusive` 案件を、理由を伴う宣言によって終了する。close の本処理では agent を呼ばず、外部解決の妥当性を再判定しない。

用語と agent の結果分類は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「用語と結果分類」、保存と状態遷移は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「案件 ID と状態遷移」「最新状態の atomic publication」を正本とする。

## CLI 契約

```text
cmoc feedback close <案件ID> --reason "外部で修正し、人間が解決を確認した"
```

- 位置引数は案件 ID を 1 つ受け取る。issue ID、report ID、または同じ identity の最新案件への読み替えは行わない。
- `--reason` を必須とし、空文字列と空白だけの値を拒否する。
- `--report` は要求せず、受け取らない。対象は repository の最新状態と、指定した案件 ID の確定済み履歴から解決する。
- 本処理は feedback state と report・log を更新する機械的な操作であり、編集 run、issue commit、または join を作らない。

## 対象と理由

新しく close できるのは、current pointer が選ぶ active generation に存在し、最新の agent 判定が `inconclusive` である案件だけとする。理由は、その案件を人間が外部で解決したという宣言として受理し、妥当性の agent 検証は要求しない。

保存する人間の理由と、直前の agent result・reason・根拠を分ける。`fixed` や `already_resolved` の agent result を生成せず、他の案件の判定も変更しない。

## 事前条件

1. `{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「概要」「成功条件と保証範囲」に従い doctor preprocess を完了する。
2. 対象 repository を特定し、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「JSON と排他制御」に従う writer 排他を取得する。
3. current pointer、active、history、および未完了操作の schema・path・hash と対応関係を検証する。
4. 未終了の feedback run や未完了の publication・cleanup がないことを確認する。同じ close の recovery に限り、本書の「保存失敗と recovery」に従って再開する。
5. 排他内で指定された案件 ID とその最新の判定を確認する。

close は編集 run を開始しないため、active session branch と worktree・staging area の clean 状態を固有の条件にはしない。doctor preprocess の共通責務は省略しない。

進行中、自動 join 前に停止中、または recovery 待ちの feedback run が同じ repository にある場合は、close を開始しない。その run の状態に応じた join・abandon または feedback report recovery を案内する。close を使って run の固定入力や封印済み結果を変更してはならない。

## 対象不在・対象外・再実行・競合

事前条件の検証後、次のように扱う。

| 状態 | 挙動 |
|---|---|
| 指定案件が active にあり、最新の判定が `inconclusive` | 新しい close を確定する。 |
| 同じ案件 ID の手動クローズが確定済み | `already_closed` として正常終了する。元の理由・日時・履歴を変更せず、再度 state を publication しない。 |
| 指定案件が見つからない | 対象不在としてエラー終了する。issue identity などから代わりの案件を選ばない。 |
| 最新判定が `human_required`、または自動判定によりすでに終了した案件 | 対象外としてエラー終了する。終了した理由を確認できる場合はその参照を示す。 |
| ID の形式不正、理由の欠落・空白、排他取得失敗、未完了操作との競合、または state の不整合 | 理由と必要な次の操作を示してエラー終了する。 |

確定済み close の再実行では、今回の非空の理由が元の理由と異なっていても、保存済み理由を置換・追記しない。今回の入力は今回の実行記録にだけ残す。同じ issue identity の新しい案件が active にあっても、それに作用しない。

同時実行は共通の writer 排他で直列化し、取得後の current を使って対象条件を再検証する。準備した base current pointer と現在の pointer が一致しなければ、その更新を公開せず競合として扱う。別の writer の結果を上書きしない。

## close の確定と最新状態

対象案件 ID、直前の record とその hash、base current pointer、人間の理由・日時、元の実行 ID、および publication target を、再開できる作業記録へ固定する。保存の途中で固定入力を別の対象や理由へ付け替えない。

`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「案件 ID と状態遷移」「history の保存と参照」「最新状態の atomic publication」に従って確定する。成功後に current を読むと、対象はすでに現在の案件一覧から除かれ、理由と経緯は history から確認できる。次の feedback report の実行を反映条件にしない。

close 後の一覧の表示は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「現在の案件一覧」に従う。残る案件に応じた要約は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「最新状態の要約」に従い、close 自体の成否と区別する。他に `inconclusive` が残る場合も close を確定できる。

入力の消費・保持・cleanup は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「入力の消費と cleanup」に従う。close のために pending observation を取り込んだり、collector の新しい high-watermark を消費境界にしたりしない。

## 保存失敗と recovery

確定点前後の保持、atomicity、および再適用防止は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「最新状態の atomic publication」に従う。保存に失敗した invocation はエラー終了し、確定済みの内容と未完了処理を report・log に示す。

未 publication の作業記録がある場合は、同じ案件 ID と固定済みの理由による close の再実行でだけ recovery する。base、対象 record、および保存済み artifact を検証できれば、同じ generation・history・report target を再利用する。理由や対象が異なる操作とは競合として扱い、黙って置換しない。

publication 済みで cleanup などが未完了の場合は、同じ案件 ID の close の再実行でその後処理だけを完了する。元の close をもう一度適用したり、すでに除かれた案件の不在を失敗理由にしたりしない。完了後は `already_closed` とし、確定済み理由は維持する。

固定入力や確定状況を一意に検証できない場合は、資源を保持してエラー終了する。別の close と新しい feedback report は未完了操作を飛び越えて開始しない。recovery に agent の再判定、raw observation の再取り込み、または履歴の推測を使わない。

## primary report と終了結果

実行 ID、共通掲載内容、primary report の表示、および terminal result の共通規則は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「実行 ID の開始表示」「primary report」「terminal result」に従う。エラーの分類と report 保存自体の失敗は、`{{cmoc-root}}/oracle/doc/app_spec/error_handling.md` の「エラーハンドリング規則」に従う。

close report は Markdown と YAML Front Matter で構成し、次へ保存する。publication する report の掲載時点と、保存後に確定する処理結果の記録先は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「publication report と終了時の記録」に従う。

```text
{{repo-root}}/.cmoc/gu/report/feedback/close/{{execution-id}}.md
```

新しい close の publication target には、最初に固定した実行 ID を使用する。その report には対象案件 ID と issue ID、元の判定、人間の理由・日時、更新前後の generation、history への参照、および更新後の現在の案件一覧を含める。close による更新であり、他の案件の再確認を行っていないことを判別可能にする。

正常に完了した新規 close では、その publication 済み report を primary report とする。確定済み close の再実行で recovery が不要な場合は、今回の実行 ID で `already_closed` の report を作り、元の close と現在の state を参照する。この report を current pointer の参照先にしない。

recovery では元の publication report を書き換えず、未保存なら固定済み target へ保存し、保存済みなら path と hash を検証して再利用する。正常に recovery を完了した場合は、その report の保存確認を primary report の要件を満たすものとする。再開した実行には新しい実行 ID を付与し、今回の入力・作業・終端結果と共通掲載内容をその実行のサブコマンドログに残して、元の実行・report・close との対応を示す。

エラー時は、今回の実行 ID を使った次の invocation report を primary report とする。

```text
{{repo-root}}/.cmoc/gu/report/feedback/invocation/{{execution-id}}.md
```

事前条件違反で本処理を開始しなかった場合も対象とする。確認できた入力と state、理由、publication の成立有無、未実行・未完了の処理、次の操作、および関連ログを記載し、確定できない値や成功した操作を作らない。

| 終端結果 | 共通分類 | 終了コード |
|---|---|---|
| `closed`：今回の close を publication し、必要な後処理まで完了 | `natural_completion` | 0 |
| `already_closed`：同じ案件の確定済み close を確認し、必要なら残った後処理を完了 | `natural_completion` | 0 |
| `error`：入力・対象・事前条件の違反、競合、保存または recovery の失敗 | `error` | 1 |

terminal result では、close の結果と最新状態の要約・残件数を区別して示す。残る `inconclusive` の存在だけで close を失敗にしない。保存途中の process interruption は成功や `incomplete` へ変換せず、上記の recovery に必要な記録を保持する。
