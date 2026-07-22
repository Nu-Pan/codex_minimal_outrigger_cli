# `cmoc realization refactor fork`

## 目的

- realization refactor は、oracle file と realization file を起点とするファイル単位の追従調査を、current fork で保留した unresolved target 以外の調査要求がなくなるまで繰り返す workload である。
- 所見調査・修正を行う agent call には commit 差分や変更要約を渡さず、oracle file、realization file、および standard から修正すべき点を見つけさせる。
- 短い変更ループを担う realization apply とは workload を分ける。
- fork, join, abandon の共通 lifecycle は `{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` を正本とする。

## refactor state

### 保存先と JSON schema

- 正本の保存先は `{{work-root}}/.cmoc/gt/ar/realization/refactor/state.json` とする。
- JSON のトップレベルは、正規化済みの `{{work-root}}` 相対 path を key、次の object を value とする object である。

    ```json
    {
      "oracle/doc/example.md": {
        "investigation_required": true,
        "last_investigation_result": "not_investigated",
        "last_investigated_sha256": null,
        "last_investigated_at": null
      }
    }
    ```

- `investigation_required` は boolean とする。
- `last_investigation_result` は `not_investigated | no_findings | findings` とする。
- `last_investigated_sha256` は調査時点の file 内容に対する SHA256 文字列または `null` とする。
- `last_investigated_at` は `{{time-stamp}}` または `null` とする。
- `not_investigated` の entry は hash と日時をともに `null` とする。
- absolute path と `..` による `{{work-root}}` 外参照を禁止する。
- JSON object の記載順に意味を持たせない。
- state file は agent ではなく cmoc が更新する。

### entry 集合の同期

- entry の対象は、同期時点で存在する全 oracle file と全 realization file の和集合とする。
- state 同期の完了時には、対象 file と entry に過不足があってはいけない。
- 人間の編集直後まで常時一致することは要求せず、doctor preprocess、refactor の各処理単位、および run join 後など、cmoc が同期を完了した時点の不変条件とする。
- 新規 file には次の entry を作成する。
    - `investigation_required=true`
    - `last_investigation_result=not_investigated`
    - `last_investigated_sha256=null`
    - `last_investigated_at=null`
- 削除 file の entry は削除する。
- rename は削除と追加として同期する。
- 現在の file の SHA256 が `last_investigated_sha256` と異なる場合は、既存の調査履歴を保持したまま `investigation_required=true` にする。

## current fork の unresolved target 集合

- unresolved target 集合は current fork だけで使用する。
- 集合の要素は、正規化済みの `{{work-root}}` 相対 target path とする。
- unresolved target 集合を refactor state に永続化してはいけない。この集合のために refactor state の schema を変更してはいけない。
- unresolved target 集合を、次回 fork の選択を制御する skip または checkpoint として永続化してはいけない。
- 前回の fork の unresolved target 集合を新しい fork へ引き継いではいけない。前回の fork で unresolved になった entry は、`last_investigation_result=findings` と `investigation_required=true` により再び調査対象になり得る。

## 引数と想定内差分

- 引数なし。
- 処理 file 数や loop 回数による上限は設けない。
- agent が変更する realization file、cmoc が更新する refactor state、および cmoc が生成する任意階層の `INDEX.md` を想定内差分とする。
- agent は realization file だけを変更する。refactor state と `INDEX.md` は cmoc が更新する。

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
- current fork の unresolved target 集合に含まれる path を、同じ fork で再選択してはいけない。
- `last_investigation_result=not_investigated` の entry を先に選ぶ。
- その後は `last_investigated_at` の古い順に選び、同値なら path の昇順とする。
- JSON object の記載順を選択順として使用してはいけない。

### 1 処理単位

1. 調査対象 file の現在の SHA256 を調査時点の hash として取得する。
2. `build_realization_refactor_fork_file_review_and_fix_parameter` に調査対象 path だけを渡し、所見調査、realization file の修正、および検証を 1 回の agent call で行う。
3. agent call が正常終了した場合、調査時点の hash、日時、および所見有無を対象 entry に保存する。
    - 所見なし: `last_investigation_result=no_findings`, `investigation_required=false`
    - 所見あり: `last_investigation_result=findings`, `investigation_required=true`
    - `resolution.status=unresolved` の所見が 1 件以上ある場合も所見ありとして扱い、`investigation_required=true` を維持する。
4. agent call が変更した全 realization file を `investigation_required=true` にする。
5. 追加、rename、削除後の entry 集合を同じ処理単位で同期する。
6. realization file の差分、refactor state の更新、および cmoc が生成した `INDEX.md` を同じ処理単位の commit として確定する。
7. response に `resolution.status=unresolved` の所見が 1 件以上ある場合は、処理単位の確定後に対象 path を current fork の unresolved target 集合へ追加する。
8. unresolved target 集合を除いた調査対象が残っていれば、次の対象を選ぶ。

- 所見が空の場合、agent は差分を発生させてはいけない。
- agent の差分は返却した所見のいずれかに対応しなければならない。
- agent call には commit 差分、変更 commit の列、または変更要約を注入してはいけない。
- unresolved を含むことだけを理由に、処理単位を rollback したり refactor loop を停止したりしてはいけない。
- unresolved を含む処理単位でも、realization file の差分、refactor state、および `INDEX.md` を整合した単位として確定する。

## 完了

- current fork の unresolved target 集合を除いた `investigation_required=true` の entry がなくなった時点で、refactor loop を完了する。
- unresolved target 集合が空の場合は `natural_completion` とする。このとき、全 entry が `investigation_required=false` でなければならない。
- unresolved target 集合が 1 件以上ある場合は `completed_with_unresolved` とする。このとき、`investigation_required=true` の entry の path 集合は current fork の unresolved target 集合と一致しなければならない。
- `natural_completion` と `completed_with_unresolved` では、`run.state` を `joinable` にする。
- `completed_with_unresolved` は正常系とする。Python 例外、エラー用 call stack、または `run.state=error` を使用してはいけない。
- state object は空にせず、各 file の調査履歴を保持する。
- `natural_completion` は、全 oracle file と realization file に調査要求が残っていないことを表す。
- `completed_with_unresolved` は、current fork で調査可能な target をすべて処理し、未解決の調査要求だけを次回 fork へ残したことを表す。
- いずれの完了も、ファイル単位調査で全問題を発見できることや LLM の回答品質を保証しない。

## ユーザー中断

- この fork は中断可能サブコマンドとし、共通動作は `{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` を正本とする。
- `Ctrl+C` は agent call 中を含む任意のタイミングで受け付ける。
- 実行中の処理単位を commit まで完了するか、その処理単位全体を rollback する。realization file と refactor state の片方だけを確定してはいけない。
- 中断後は `run.state` を `joinable` にする。
- 中断後に許可する lifecycle 操作は `cmoc run join` または `cmoc run abandon` だけとする。
- 確定済みの部分結果から続きを行う場合は、先に `cmoc run join` し、その後に新しい `cmoc realization refactor fork` を開始する。同じ run branch または worktree を保持して再開してはいけない。

## その他のエラー

- Codex CLI call の失敗、想定外 path の変更、処理単位の確定失敗などにより処理を続行できない場合は、処理単位を commit または rollback により整合させ、`run.state` を `error` にする。
- 続行不能なエラーは、`resolution.status=unresolved` の所見と区別する。
- 確定済み commit と refactor state は保持する。

## fork report、終了 log、および終了コード

- report は Markdown + YAML Front Matter とする。
- 共通 run 項目に加え、refactor state のフル path と `completion_reason` を含める。
- `completion_reason` は `natural_completion | completed_with_unresolved | user_interruption | error` とする。
- 本文には以下を含める。
    - unresolved target の件数と path。
    - `resolution.status=unresolved` の所見ごとの title、`resolution.summary` による未解決理由、および対応する Codex call log または Structured Output のフル path。
    - current fork で処理した target の件数。1 回以上処理単位を確定した target path を重複なく数える。
    - 未調査 target の件数。`investigation_required=true` であり、current fork の unresolved target 集合に含まれない entry を数える。
    - 処理単位ごとの所見数。
    - entry 総数、調査要求あり件数、および各 `last_investigation_result` の件数。
    - run branch 上の変更内容の要約。
- `completed_with_unresolved` の report では、未調査 target の件数を 0 とする。調査要求あり件数は unresolved target の件数と一致しなければならない。
- `natural_completion` と `completed_with_unresolved` の変更要約は `build_realization_refactor_fork_change_summary_parameter` で生成する。
- run branch の tree 差分が空の場合は要約用 agent call を行わず、変更なしと記録する。
- ユーザー中断後またはエラー後は新しい agent call を行わず、確定済みの変更 path と所見情報から要約する。
- `{{repo-root}}/.cmoc/gu/ar/report/realization/refactor/fork/{{time-stamp}}.md` に保存する。report 本文は stdout に流さず、保存先のフル path を表示する。
- 終了 log には `completion_reason`、unresolved target の件数、および report のフル path を含める。
- `natural_completion`、`completed_with_unresolved`、および `user_interruption` は正常系の終了コードとし、`error` は非 0 とする。
- report と終了 log の `completion_reason` から、完全な自然完了、unresolved 付き完了、ユーザー中断、およびエラーを判別可能にする。

## join 後 hook

- workload 固有の hook は持たない。merge 後の refactor state 同期は共通 lifecycle が行う。
