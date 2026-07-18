# `cmoc realization refactor fork|join|abandon`

## 目的

- `cmoc realization refactor` は、oracle file へのファイル単位の追従調査を、未調査ファイルがなくなるまで繰り返す workload である。
- 所見調査・修正を行う agent call には commit 差分や変更要約を渡さず、oracle file、realization file、および standard だけから修正すべき点を見つけさせる。
- 全候補ファイルを起点として調査することで網羅性を担保する。
- 短い変更ループを担う `cmoc realization apply` とは、workload とサブコマンドを分ける。

## refactor state

- 正本の保存先は `{{work-root}}/.cmoc/gt/ar/realization/refactor/state.json` とする。
- JSON のトップレベルは、調査待ちの repository file の path を保持する配列とする。
- 各要素は文字列とし、path は `{{work-root}}` からの正規化済み相対 path とする。絶対 path と `..` による `{{work-root}}` 外参照を禁止する。
- path の重複を禁止する。
- 配列に含まれる file は未追従、含まれない候補 file は追従済みとして扱う。
- 空の状態は `[]` とする。配列が空になった時点で refactor は完了する。
- この file は agent ではなく cmoc が更新する。

## `cmoc realization refactor fork`

### 引数

- 引数なし。
- 処理ファイル数やループ回数による上限は設けない。

### 新しい run の開始

1. `{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_run.md` の共通 fork 開始処理を行う。
2. refactor state が空の場合、現在存在する全候補 file を path の昇順で state に追加し、state の初期化を commit する。
3. refactor state が空でない場合は、その列を引き継ぐ。
4. refactor ループを開始する。

候補 file は、run branch 上で git 追跡されている全 repository file とする。削除済み file と refactor state 自身は候補に含めない。

### refactor ループ

1. refactor state の先頭 path を、state からまだ削除せずに調査対象とする。
2. 調査対象が既に存在しない、git 追跡対象ではない、oracle file / realization file のいずれでもない、または agent の読み取り禁止対象である場合は、分類結果を log に記録し、state から削除してその更新を commit し、ループ先頭へ戻る。
3. `build_realization_refactor_fork_file_review_and_fix_parameter` に oracle file または realization file である調査対象 path だけを渡し、所見調査・修正・検証を 1 回の agent call で行う。
4. agent call が正常に完了した場合、調査対象を state から削除する。
5. 1 件以上の所見が返り、調査対象が引き続き候補 file である場合は、調査対象を state の末尾へ再投入する。
6. 差分が発生した realization file を、rename 後の path で state の末尾へ追加する。削除済み file は追加しない。
7. 最も先頭側の要素を残す形で重複を除去する。
8. realization file の差分、refactor state の更新、cmoc が生成した `INDEX.md` を同じ処理単位の commit として確定する。
9. state が空なら完了し、それ以外はループ先頭へ戻る。

- 所見が空の場合、agent は差分を発生させてはいけない。
- agent の差分は返却した所見のいずれかに対応しなければならない。
- agent call には commit 差分、変更 commit の列、または変更要約を注入してはいけない。
- agent call の開始前に state から対象を削除しないことで、中断・失敗時にも未調査対象を失わないようにする。

### 完了

- refactor state が空になった場合、`realization_run.state` を `completed` にする。
- 完了は、全候補 file が分類確認され、全 oracle file と realization file が少なくとも 1 回は調査され、再調査要求も残っていないことを表す。
- ファイル単位調査で全ての問題を発見できることや、LLM の回答品質を保証するものではない。

### ユーザー中断と再開

- `cmoc realization refactor fork` は中断可能サブコマンドとし、共通動作は `{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` を正本とする。
- `Ctrl+C` は agent call 中を含む任意のタイミングで受け付ける。
- 実行中の処理単位を commit まで完了させるか、その処理単位の未確定差分を破棄する。realization file と refactor state の片方だけを確定してはいけない。
- 中断後は `realization_run.state` を `paused` にし、refactor branch、worktree、refactor state を保持する。
- 次回 `cmoc realization refactor fork` は、保存済み branch と worktree を使い、state の先頭から再開する。新しい run branch を作ってはいけない。
- `cmoc realization refactor join` で確定済みの部分結果を join することと、`cmoc realization refactor abandon` で破棄することも許容する。

### エラー

- 中断以外の理由で処理を続行できない場合は `realization_run.state` を `error` にする。
- 確定済みの commit と refactor state は保持する。

### report と終了コード

- fork report は Markdown + YAML Front Matter とする。
- YAML Front Matter に、`{{cmoc-session-branch}}`, `{{cmoc-session-fork-commit}}`, `{{realization-oracle-snapshot-commit}}`, `{{cmoc-realization-refactor-branch}}`, `{{cmoc-realization-refactor-fork-commit}}`, `{{cmoc-realization-refactor-worktree}}`, refactor state のフル path を含める。
- 本文に以下を含める。
    - 完了、中断、エラーの区分。
    - 処理単位ごとの所見数。
    - report 作成時点の調査待ち file 数。
    - refactor branch 上の変更内容の要約。
- 自然完了時の変更要約は `build_realization_refactor_fork_change_summary_parameter` で生成する。
- refactor branch の tree 差分が空の場合は agent call を行わず、変更なしと記録する。
- ユーザー中断後は新しい agent call を行わず、確定済みの変更 path と所見情報から要約を作る。
- エラーにより変更要約 agent call を安全に行えない場合も、確定済み情報から要約を作り、要約を縮退した理由を記録する。
- `{{repo-root}}/.cmoc/gu/ar/report/realization/refactor/fork/{{time-stamp}}.md` に保存する。report 本文は stdout に流さず、保存先のフル path を表示する。
- 完了、ユーザー中断、エラーを終了コードで区別可能にする。
- ユーザー中断は正常系であり、エラーを表す終了コードにしてはいけない。

## `cmoc realization refactor join`

- refactor run の確定済み成果物と refactor state を `{{cmoc-session-branch}}` へ merge する。
- `completed`, `paused`, `error` の refactor run を対象にできる。
- 引数、事前条件、想定外差分、merge、状態更新、cleanup は `{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_run.md` の join を正本とする。

## `cmoc realization refactor abandon`

- 未 join の refactor run と、その branch 上だけにある refactor state の更新を破棄する。
- 引数、事前条件、破棄範囲、状態更新、cleanup は `{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_run.md` の abandon を正本とする。
