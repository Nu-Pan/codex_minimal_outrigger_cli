# `cmoc realization refactor fork`

## 目的

realization refactor は、oracle file と realization file を起点に、ファイル単位の追従調査を繰り返す workload である。current fork で保留した unresolved target 以外の調査要求がなくなるまで続ける。短い変更ループを担う realization apply とは workload を分ける。

所見、追従要否、および適合性の判断基準は、`{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization.md` の「oracle file に対する realization file の適合性」を正本とする。installed skill の有無によって、所見、追従要否、適合性、または完了の判定基準を変えてはいけない。

所見調査・修正 call の正確な prompt 文面、prompt part の選択、workload 固有の起動パラメータ、およびその選択理由は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/realization/refactor/fork/file_review_and_fix.py` の `build_realization_refactor_fork_file_review_and_fix_parameter` へ委譲する。fork、join、abandon の共通 lifecycle は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「編集 run の共通仕様」を正本とする。

## refactor state

### 保存先と JSON schema

refactor state の保存先は `{{work-root}}/.cmoc/gt/realization/refactor/state.json` とする。

JSON のトップレベルは、正規化済みの `{{work-root}}` 相対 path を key、各 file の調査状態を value とする object である。調査状態は、次の field を持つ object とする。

| field | 型・値 |
|---|---|
| `investigation_required` | boolean |
| `last_investigation_result` | `not_investigated`、`no_findings`、`findings` のいずれか |
| `last_investigated_sha256` | 調査時点の file 内容に対する SHA256 文字列、または `null` |
| `last_investigated_at` | `{{time-stamp}}`、または `null` |

- `not_investigated` の entry は hash と日時をともに `null` とする。
- absolute path と `..` による `{{work-root}}` 外参照を禁止する。
- JSON object の記載順に意味を持たせない。
- state file は agent ではなく cmoc が更新する。

### entry 集合の同期

- entry の対象は、`{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization_file_enumeration.md` の「分類結果」に従い、同期時点で存在する全 oracle file と全 realization file の和集合とする。
- 対象 file と entry の過不足のない一致は、cmoc が同期を完了した時点の不変条件とする。同期時点には、doctor preprocess、refactor の各処理単位、run join 後などがある。人間の編集直後を含め、常時一致することは要求しない。
- 新規 file には次の entry を作成する。
    - `investigation_required=true`
    - `last_investigation_result=not_investigated`
    - `last_investigated_sha256=null`
    - `last_investigated_at=null`
- 削除 file の entry は削除する。
- rename は削除と追加として同期する。
- 現在の file の SHA256 が `last_investigated_sha256` と異なる場合は、既存の調査履歴を保持したまま `investigation_required=true` にする。

## current fork の unresolved target 集合

- unresolved target 集合は current fork だけで使用し、新しい fork へ引き継がない。
- 集合の要素は、正規化済みの `{{work-root}}` 相対 target path とする。
- refactor state または次回 fork の選択用 skip・checkpoint として永続化せず、この集合のために refactor state の schema を変更してはいけない。
- 前回の fork で unresolved になった entry は、`last_investigation_result=findings` と `investigation_required=true` により再び調査対象になり得る。

## 引数と想定内差分

- 引数なし。
- 処理 file 数や loop 回数による上限は設けない。
- agent が変更する realization file と cmoc が更新する refactor state を想定内差分とする。
- agent が変更する作業成果物は realization file だけとする。refactor state は cmoc が更新する。
- 一時作業領域の利用は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「一時作業領域」に従う。

## full refactor cycle

1. doctor preprocess と編集 run の共通 fork 開始処理を行う。
2. current fork の unresolved target 集合を空で初期化する。
3. run worktree 上で refactor state を同期する。
4. `investigation_required=true` の entry が 1 件以上あれば、その要求を引き継ぐ。
5. 全 entry が `investigation_required=false` なら、全 entry を `true` にして新しい full refactor cycle を開始する。
6. cycle 開始に伴う state 更新を run branch に commit し、refactor loop を開始する。

## refactor loop

### 調査対象の選択

- `investigation_required=true` であり、かつ path が current fork の unresolved target 集合に含まれない entry だけを調査対象とする。
- `last_investigation_result=not_investigated` の entry を先に選ぶ。
- その後は `last_investigated_at` の古い順に選び、同値なら path の昇順とする。

### 1 処理単位

1. 調査対象 file の現在の SHA256 を調査時点の hash として取得する。
2. `build_realization_refactor_fork_file_review_and_fix_parameter` の作業入力には調査対象 path だけを渡し、所見調査、realization file の修正、および検証を 1 回の agent call で行う。
3. agent call が正常終了した後、本節の「Structured Output の受理と正規化」に従って、機械的検証に合格した Structured Output と、その agent call による realization file の差分から処理結果を決定する。
4. 調査時点の hash、日時、および正規化後の所見有無を対象 entry に保存する。
    - 所見なし: `last_investigation_result=no_findings`, `investigation_required=false`
    - 所見あり: `last_investigation_result=findings`, `investigation_required=true`
5. agent call が変更した全 realization file を `investigation_required=true` にする。
6. 追加、rename、削除後の entry 集合を同じ処理単位で同期する。
7. realization file の差分と refactor state の更新を同じ処理単位の commit として確定する。
8. 正規化後の処理結果に `resolution.status=unresolved` の所見が 1 件以上ある場合は、処理単位の確定後に対象 path を current fork の unresolved target 集合へ追加する。
9. unresolved target 集合を除いた調査対象が残っていれば、次の対象を選ぶ。

#### Structured Output の受理と正規化

cmoc は、申告された変更 path 集合と実際の変更 path 集合が一致する場合だけ Structured Output を受理する。両集合は次のように定め、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「機械的検証と正式な結果」に従って照合する。

| 集合 | 定義 |
|---|---|
| 実際の変更 path 集合 | agent call の開始時点を基準として出力時点に残る realization file の net 差分を、schema の `changed_paths` と同じ path 表現へ正規化した集合。 |
| 申告された変更 path 集合 | 全所見の `changed_paths` の和集合。同じ path を複数の所見が申告してよいが、`evidences[].path` は含めない。 |

受理した Structured Output から、次の条件で処理結果を決定する。

| 条件 | 処理結果 |
|---|---|
| `findings` が空である。 | 所見なしとする。 |
| `findings` が 1 件以上あり、全所見の `resolution.status` が `fixed` で、実際の変更 path 集合が空である。 | 所見なしへ正規化する。 |
| それ以外。 | 返された所見を処理結果の所見とする。 |

`resolution.status=fixed` は agent の自己申告であり、その申告だけで修正の意味的な正しさが証明されたと扱ってはいけない。所見なしへの正規化は cmoc の処理判定だけに適用し、agent が返した元の Structured Output と Codex call log は、破棄または改変せず調査可能な実行記録として保持する。

所見なしへ正規化した処理単位にも、agent が空の `findings` を返した場合と同じ処理と完了判定を適用する。synthetic `unresolved` への変換や、人間による判断、手動修正、手動承認を要求する workflow の追加は行わない。

#### 処理単位の境界

処理単位の commit 受理条件として、cmoc は想定外 path の変更と変更禁止対象への書き込みを、`changed_paths` の照合とは別に検査する。差分検証の共通規則は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「agent call の差分検証」を正本とする。

所見なしへの正規化によって、`changed_paths` の照合、想定外 path と変更禁止対象の検査、または処理単位の commit・rollback 失敗に対する検査を緩和しない。また、unresolved を含むことだけを理由に、処理単位を rollback したり refactor loop を停止したりしてはいけない。

agent call には commit 差分、変更 commit の列、または変更要約を注入してはいけない。

## 完了

path が current fork の unresolved target 集合に含まれない `investigation_required=true` の entry がなくなった時点で、refactor loop を完了する。完了理由は次の条件で決定する。

| 完了理由 | 条件と残る調査要求 |
|---|---|
| `natural_completion` | unresolved target 集合が空であり、全 oracle file と realization file の entry が `investigation_required=false` である。 |
| `completed_with_unresolved` | unresolved target 集合が 1 件以上あり、`investigation_required=true` の entry の path 集合がその集合と一致する。 |

どちらも正常系として `run.state` を `joinable` にし、各 file の調査履歴を state object に保持する。`completed_with_unresolved` を Python 例外、エラー用 call stack、または `run.state=error` で扱ってはならない。

いずれの完了も、ファイル単位調査で全問題を発見できること、LLM の回答品質、または agent の申告や作業内容の意味的な正しさを保証しない。

## ユーザー中断

- この fork は中断可能サブコマンドとし、共通動作は `{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` の「サブコマンドのユーザー中断」を正本とする。
- `Ctrl+C` は agent call 中を含む任意のタイミングで受け付ける。
- 実行中の処理単位を commit まで完了するか、その処理単位全体を rollback する。realization file と refactor state の片方だけを確定してはいけない。
- 中断後は `run.state` を `joinable` にする。
- 中断後に許可する lifecycle 操作は `cmoc run join` または `cmoc run abandon` だけとする。
- 確定済みの部分結果から続きを行う場合は、先に `cmoc run join` し、その後に新しい `cmoc realization refactor fork` を開始する。同じ run branch または worktree を保持して再開してはいけない。

## その他のエラー

- Codex CLI call の失敗、想定外 path の変更、処理単位の確定失敗などにより処理を続行できない場合は、処理単位を commit または rollback により整合させ、`run.state` を `error` にする。
- 続行不能なエラーは、`resolution.status=unresolved` の所見と区別する。
- 確定済み commit と refactor state は保持する。

## feedback との境界

realization refactor の成果物と feedback の境界は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「既存 workload との境界」を正本とする。

## fork report、終了 log、および終了コード

### 保存と掲載内容

すべての終了経路で report を保存する。共通 fork 事前条件違反など、run branch、run worktree、refactor state、または通常の report 生成処理より前に確定したエラーも対象とする。

report は `{{repo-root}}/.cmoc/gu/report/realization/refactor/fork/{{time-stamp}}.md` に保存し、primary report とする。共通 run 項目に加え、refactor state のフル path と `completion_reason` を含める。`completion_reason` は `natural_completion | completed_with_unresolved | user_interruption | error` とする。

本文には次の内容を含める。

- unresolved target の件数と path。
- `resolution.status=unresolved` の所見ごとの title、`resolution.summary` による未解決理由、および対応する Codex call log または Structured Output のフル path。
- current fork で処理した target の件数。1 回以上処理単位を確定した target path を重複なく数える。
- 未調査 target の件数。`investigation_required=true` であり、current fork の unresolved target 集合に含まれない entry を数える。
- 正規化後の処理結果に基づく処理単位ごとの所見数。所見なしへ正規化した処理単位は 0 件とする。
- entry 総数、調査要求あり件数、および各 `last_investigation_result` の件数。
- run branch 上の変更内容の要約。

report 生成時点で確定していない項目は `null` または未実行とする。エラーになった処理段階、確定済みの部分作業、エラー、および関連ログは記録する。

### 変更要約

`natural_completion` と `completed_with_unresolved` の変更要約は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/realization/refactor/fork/change_summary.py` の `build_realization_refactor_fork_change_summary_parameter` で生成する。正確な prompt 文面、prompt part の選択、builder の引数、起動パラメータの構築方法と選択理由は同関数へ委譲する。

要約対象は、`{{cmoc-run-worktree}}` の repository における `{{cmoc-run-fork-commit}}` から、要約対象を確定した時点の run branch HEAD までの tree 差分全体とする。cmoc は両端を commit ID に確定して要約 agent に渡し、後続の追加 commit によって、確定後に比較範囲を動かさない。

Git 差分の参照入力は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「Git 差分の参照入力」に従う。要約 agent は、既存の cwd と `{{work-root}}` を用い、指定範囲の差分を Git から取得して人間向けに要約する。この比較入力は、ファイル単位の所見調査・修正 call には追加しない。

指定範囲の tree 差分が空の場合は要約用 agent call を行わず、変更なしと記録する。ユーザー中断後またはエラー後も新しい agent call は行わず、確定済みの変更 path と所見情報から要約する。

### 終了 log と終了コード

サブコマンド終了イベントには `completion_reason`、unresolved target の件数、および report のフル path を含める。report、terminal result、およびサブコマンド終了イベントの `completion_reason` から、完全な自然完了、unresolved 付き完了、ユーザー中断、およびエラーを判別可能にする。

`natural_completion`、`completed_with_unresolved`、および `user_interruption` は正常系の終了コードとし、`error` は非 0 とする。

## join 後 hook

- workload 固有の hook は持たない。merge 後の refactor state 同期は共通 lifecycle が行う。
