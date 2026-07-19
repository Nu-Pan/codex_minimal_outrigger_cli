# `cmoc realization refactor fork`

## 目的

- realization refactor は、oracle file と realization file を起点とするファイル単位の追従調査を、調査要求がなくなるまで繰り返す workload である。
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

## 引数と想定内差分

- 引数なし。
- 処理 file 数や loop 回数による上限は設けない。
- agent が変更する realization file、cmoc が更新する refactor state、および cmoc が生成する任意階層の `INDEX.md` を想定内差分とする。
- agent は realization file だけを変更する。refactor state と `INDEX.md` は cmoc が更新する。

## full refactor cycle

1. doctor preprocess と編集 run の共通 fork 開始処理を行う。
2. run worktree 上で refactor state を同期する。
3. `investigation_required=true` の entry が 1 件以上あれば、その要求を引き継ぐ。
4. 全 entry が `investigation_required=false` なら、全 entry を `true` にして新しい full refactor cycle を開始する。
5. cycle 開始に伴う state 更新を run branch に commit し、refactor loop を開始する。

## refactor loop

### 調査対象の選択

- `investigation_required=true` の entry だけを調査対象とする。
- `last_investigation_result=not_investigated` の entry を先に選ぶ。
- その後は `last_investigated_at` の古い順に選び、同値なら path の昇順とする。
- JSON object の記載順を選択順として使用してはいけない。

### 1 処理単位

1. 調査対象 file の現在の SHA256 を調査時点の hash として取得する。
2. `build_realization_refactor_fork_file_review_and_fix_parameter` に調査対象 path だけを渡し、所見調査、realization file の修正、および検証を 1 回の agent call で行う。
3. agent call が正常終了した場合、調査時点の hash、日時、および所見有無を対象 entry に保存する。
    - 所見なし: `last_investigation_result=no_findings`, `investigation_required=false`
    - 所見あり: `last_investigation_result=findings`, `investigation_required=true`
4. agent call が変更した全 realization file を `investigation_required=true` にする。
5. 追加、rename、削除後の entry 集合を同じ処理単位で同期する。
6. realization file の差分、refactor state の更新、および cmoc が生成した `INDEX.md` を同じ処理単位の commit として確定する。
7. 調査要求が残っていれば次の対象を選ぶ。

- 所見が空の場合、agent は差分を発生させてはいけない。
- agent の差分は返却した所見のいずれかに対応しなければならない。
- agent call には commit 差分、変更 commit の列、または変更要約を注入してはいけない。

### unresolved の停止条件

- `resolution.status=unresolved` の所見を、同じ状態のまま無制限に再試行してはいけない。
- unresolved を含む response を受け取った場合は、対象 entry の調査要求を残す。
- 実行中の処理単位を整合した commit として確定するか、その処理単位全体を rollback する。
- current fork の loop を停止し、`run.state` を `error` にする。
- その後に許可する lifecycle 操作は `cmoc run join` または `cmoc run abandon` だけとする。

## 完了

- 全 entry が `investigation_required=false` になった時点を自然完了とする。
- 自然完了時は `run.state` を `joinable` にする。
- state object は空にせず、各 file の調査履歴を保持する。
- 完了は全 oracle file と realization file に調査要求が残っていないことを表すが、ファイル単位調査で全問題を発見できることや LLM の回答品質を保証しない。

## ユーザー中断

- この fork は中断可能サブコマンドとし、共通動作は `{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` を正本とする。
- `Ctrl+C` は agent call 中を含む任意のタイミングで受け付ける。
- 実行中の処理単位を commit まで完了するか、その処理単位全体を rollback する。realization file と refactor state の片方だけを確定してはいけない。
- 中断後は `run.state` を `joinable` にする。
- 中断後に許可する lifecycle 操作は `cmoc run join` または `cmoc run abandon` だけとする。
- 確定済みの部分結果から続きを行う場合は、先に `cmoc run join` し、その後に新しい `cmoc realization refactor fork` を開始する。同じ run branch または worktree を保持して再開してはいけない。

## その他のエラー

- agent call の失敗などにより処理を続行できない場合は、処理単位を commit または rollback により整合させ、`run.state` を `error` にする。
- 確定済み commit と refactor state は保持する。

## fork report と終了コード

- report は Markdown + YAML Front Matter とする。
- 共通 run 項目に加え、refactor state のフル path を含める。
- 本文に以下を含める。
    - 自然完了、ユーザー中断、unresolved、その他のエラーの区分。
    - 処理単位ごとの所見数。
    - entry 総数、調査要求あり件数、および各 `last_investigation_result` の件数。
    - run branch 上の変更内容の要約。
- 自然完了時の変更要約は `build_realization_refactor_fork_change_summary_parameter` で生成する。
- run branch の tree 差分が空の場合は要約用 agent call を行わず、変更なしと記録する。
- ユーザー中断後またはエラー後は新しい agent call を行わず、確定済みの変更 path と所見情報から要約する。
- `{{repo-root}}/.cmoc/gu/ar/report/realization/refactor/fork/{{time-stamp}}.md` に保存する。report 本文は stdout に流さず、保存先のフル path を表示する。
- 自然完了とユーザー中断は正常系の終了コード、エラーは非 0 とする。report の区分から自然完了とユーザー中断を判別可能にする。

## join 後 hook

- workload 固有の hook は持たない。merge 後の refactor state 同期は共通 lifecycle が行う。
