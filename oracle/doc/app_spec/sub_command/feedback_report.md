# `cmoc feedback report`

本書は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` が定義する delayed normalization と feedback report の挙動を定める。raw observation は `{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md`、tracked record schema は `{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` を正本とする。

## 引数

- 位置引数は受け取らない。
- `--all` を受け取る。
    - 既定表示で省略する全 disposition 済み issue、threshold 未満の machine issue、全 revision、全 assessment、および全 occurrence を表示する。
    - 既定値は false とする。

## 事前条件と更新 branch

doctor preprocess の後、次の条件をすべて満たす場合だけ実行する。

- main worktree 上の active な `{{cmoc-session-branch}}` が checkout されている。
- 対応する session state の `session.state=active` である。
- `run.state=ready` である。
- git working tree と staging area に未コミット差分がない。
- tracked feedback state に schema 違反または unresolved conflict marker がない。

report は編集 run を作らず、session state と run state を変更しない。tracked feedback state の commit は現在の `{{cmoc-session-branch}}` に作成し、後続の `cmoc session join` で home branch へ取り込む。

session を abandon した場合は、その session branch 上だけの normalized state commit も他の session 成果物と同様に破棄される。raw observation は `{{repo-root}}/.cmoc/gu` に残るため、後続 session の report が ingestion receipt のない observation を再処理する。

## snapshot と増分処理

コマンド開始時に、存在する raw observation の path、ID、および SHA256 を固定した snapshot manifest を作り、次へ atomic 保存する。

```text
{{repo-root}}/.cmoc/gu/ar/feedback/report_snapshot/{{report-id}}.json
```

report 自身の normalization agent call が新しい observation を生成した場合、その observation は snapshot に加えず次回 report へ回す。前回正常 report 後の増加数は、前回 snapshot manifest に含まれず、現在 branch に ingestion receipt がない observation の件数とする。

snapshot manifest は対応する report record が現在 repository のいずれかの branch から到達可能な間は自動削除しない。manifest が別 clone へ複製されることは保証しない。

ingestion receipt の observation ID と SHA256 が一致する observation は処理済みとする。ID は一致するが SHA256 が異なる場合は corruption としてエラー終了する。

増分処理は、次の順序で行う。

1. observation schema を検証し、observation ID と SHA256 で重複を除去する。
2. machine observation を、rule の canonical key による完全一致で統合する。
3. agent observation と既存 issue の比較候補を、category、正規化済み evidence subject、および既存 occurrence の fingerprint で機械的に絞り込む。deduplication hint は検索 hint にだけ使用する。
4. 完全一致では決められない候補だけを normalization agent call へ渡す。
5. observation 発生時点と現在の evidence file または config fingerprint を比較する。
6. normalized issue state と ingestion receipt を永続化する。
7. snapshot に対する feedback report を決定論的にレンダリングする。

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

machine issue は threshold 未満でも tracked issue と occurrence を保持するが、既定 report の issue 一覧へ表示しない。rule の recurrence window 内で threshold を満たした時点から表示する。

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

## 処理単位、commit、および再開

normalization unit は、次のいずれかとする。

- 同じ machine canonical key を持つ未処理 observation の集合
- 1 件の agent observation と、その絞り込み済み候補
- 1 issue に対する fingerprint assessment

各 unit は、生成する全 record を検証し、unit 単位の commit として確定してから次へ進む。commit 対象は `{{work-root}}/.cmoc/gt/ar/feedback` の当該 unit が生成した path だけとする。

normalization agent の正式な出力を受理した時点で、次の path に checkpoint を atomic 保存する。

```text
{{repo-root}}/.cmoc/gu/ar/feedback/normalization_checkpoint/{{normalization-unit-id}}.json
```

checkpoint は入力 observation hash、候補 issue revision ID、schema hash、および正式な Structured Output を持つ。同じ入力で再実行する場合は checkpoint を検証して再利用し、同じ observation のために quota を再消費しない。対応する tracked unit commit が成功した後だけ checkpoint を削除する。

中断または一部失敗時は、確定済み unit commit を維持する。実行中 unit が commit 前なら、その unit が作成した tracked path だけを当該 unit 開始時の HEAD へ戻し、raw observation、checkpoint、human disposition、および以前の unit commit を変更しない。次回 report は ingestion receipt と checkpoint から再開する。

snapshot の処理が完了、一部失敗、またはユーザー中断で停止した後、tracked state が整合していれば report record を最後の tracked commit として確定する。commit または rollback に失敗した場合は、作業ツリーを clean と偽って続行せず、手動対応が必要な path を報告する。

report record と report front matter の `state_commit_ids` には、この report で確定した normalization unit commit を順番に記録する。report record 自身を含む commit ID は自己参照になるため含めず、同 commit ID は command の完了 log と stdout に表示する。

## ユーザー中断

このコマンドは中断可能サブコマンドとし、共通動作は `{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` を正本とする。中断要求後は新しい normalization unit または Codex call を開始せず、処理単位の規則に従って `result=interrupted` の report まで確定する。

## report の保存先と front matter

report は Markdown + YAML Front Matter とし、次へ保存する。

```text
{{repo-root}}/.cmoc/gu/ar/report/feedback/{{time-stamp}}.md
```

front matter は、次の field を持つ。

- `command`: `cmoc feedback report`
- `generated_at`
- `repo_root`
- `session_branch`
- `snapshot_manifest_sha256`
- `snapshot_observation_count`
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
- `state_commit_ids`
- `result`

`result` は、次のいずれかとする。

- `ok`: 処理が完了し、既定表示の対象 issue がない。
- `attention`: 処理が完了し、既定表示の対象 issue または invalid observation がある。
- `partial`: 一部 unit の処理に失敗したが、確定済み state から report を保存できた。
- `interrupted`: ユーザー中断までの確定済み state から report を保存した。
- `error`: 有効な report または整合した tracked state を確定できなかった。

本仕様で「正常完了した feedback report」とは、`result=ok | attention` の report を指す。

前回正常 report は、現在 branch から到達可能な report record を `generated_at`、次に `report_id` の辞書順で並べた最大値とする。新規 revision、assessment、disposition、および occurrence の差分は、その report record を最初に含む commit の tree と現在の tracked feedback state を比較して決める。record 内の timestamp だけで差分を判定してはならない。

## 既定表示

既定 report は raw occurrence を展開せず、issue を次の順序で提示する。

1. 前回正常 report 後に新規作成された issue、または effective revision が変化した issue
2. 複数 session で再発している、effective disposition が未決定または `open | acknowledged` の issue
3. effective assessment が `needs_revalidation` の issue
4. `resolved | ignored | superseded` など、前回正常 report 後の disposition 差分要約

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
