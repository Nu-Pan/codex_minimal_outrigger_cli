# `cmoc realization apply fork`

## 目的

- realization apply は、直近の git commit 群から読み取れる oracle file の変更を realization file へ素早く反映する workload である。
- fork の正常終了時には、少なくとも指定した commit 範囲から読み取れる oracle 変更について、oracle file と realization file の間に齟齬がない状態にする。
- ファイル単位の網羅的な追従は non-goal とし、realization refactor が担う。
- fork, join, abandon の共通 lifecycle は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「編集 run の共通仕様」を正本とする。

## 引数

- 引数なし。

## 追従対象差分

- 差分の終点は `{{cmoc-run-fork-commit}}` とする。
- 差分の始点は以下とする。
    - `session.last_joined_apply_fork_commit` が存在する場合は、その commit。
    - 初回の場合は `session.session_fork_commit`。
- Git 差分の参照入力は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「Git 差分の参照入力」に従う。
- cmoc は始点と終点を commit ID に確定して agent に渡す。agent は既存の cwd と `{{work-root}}` を用い、その repository の指定した両 commit 間の差分を Git から取得する。
- 対象は、両端のいずれかで oracle file だった path とし、rename を考慮する。追加・削除と oracle 内外をまたぐ rename を含め、現在の oracle 配下だけを候補集合にしてはならない。
- 上記に該当しない realization file、`INDEX.md`、その他の非 oracle file の変更は追従対象外とする。
- 差分に現れた file だけを作業範囲としてはいけない。関連する oracle file と realization file を `{{work-root}}` リポジトリ全体から調査する。
- 差分は今回追従すべき oracle 変更を特定する根拠であり、realization file の変更内容を正本仕様へ逆流させる根拠ではない。

## agent call と file access

- 追従要否と適合性の判断基準は、`{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization.md` の「oracle file に対する realization file の適合性」を正本とする。
- 正確な prompt 文面、prompt part の選択、builder の引数、起動パラメータの構築方法と選択理由は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/realization/apply/fork/launch_exec.py` の `build_realization_apply_fork_launch_exec_parameter` へ委譲する。
- `{{cmoc-run-worktree}}` を agent call の cwd とする `codex exec` を 1 回だけ本命 agent call として実行する。Codex CLI の TUI は起動しない。
- 本命の追従作業を複数の agent call に分割してはいけない。
- 収束判定のために同じ作業を反復してはいけない。
- 本命 agent call 終了後に、別の agent call で作業を補完してはいけない。
- installed skill の有無によって、追従要否、適合性、または完了の判定基準を変えてはいけない。
- agent は realization file だけを変更し、oracle file を変更してはならない。

## 想定内差分

- agent が変更する realization file。
- cmoc が生成する任意階層の `INDEX.md`。
- agent は `INDEX.md` を変更せず、cmoc が生成する。

## 実行手順

1. doctor preprocess と編集 run の共通 fork 開始処理を行う。
2. 追従対象差分の始点と終点を commit ID に確定する。
3. `build_realization_apply_fork_launch_exec_parameter` で AgentCallParameter を構築する。
4. その AgentCallParameter を変更せず、`{{cmoc-run-worktree}}` を agent call の cwd とする `codex exec` で実行する。
5. agent の realization file 差分と cmoc が生成した `INDEX.md` を検査し、run branch に commit する。
6. `run.state` を `joinable` にして結果を report する。

## エラー

- 本命 agent call を正常に開始または終了できない場合、差分を整合した単位へ commit または rollback できない場合、あるいは後処理に失敗した場合は `run.state` を `error` にする。
- エラー後は `cmoc run join` で確定済み成果物を取り込むか、`cmoc run abandon` で run を破棄する。

## fork report と終了コード

- `natural_completion` と `error` のすべての終了経路で report を保存する。共通 fork 事前条件違反など、run branch、run worktree、または本命 agent call の開始前に確定したエラーも対象とする。
- 共通 run 項目に加え、terminal result の共通分類、差分の始点 commit、Codex CLI の終了結果、変更 path、エラー、および関連ログを含める。
- YAML Front Matter には、この invocation で reporter が受理した feedback の `feedback_observation_count` と `feedback_observations` を含める。`feedback_observations` は `observation_id` と raw observation file の full `path` を持つ object の配列とする。0 件の場合も count は 0、配列は空とする。
- 差分の終点は共通項目の `{{cmoc-run-fork-commit}}` で表し、同じ commit を別項目として重複掲載しない。
- AI による意味的な変更要約は生成しない。
- `{{repo-root}}/.cmoc/gu/ar/report/realization/apply/fork/{{time-stamp}}.md` に保存し、この report を primary report とする。
- report 生成時点で確定していない共通 run 項目、差分の始点 commit、Codex CLI の終了結果、または変更 path は、`null` または未実行として記録する。
- `joinable` での終了は終了コード 0、`error` での終了は非 0 とする。

feedback の収集は本命 agent call の共通 reporter だけで行う。apply 固有の Structured Output field、終了後の発見用 agent call、または feedback 件数による終了コード変更を追加してはならない。詳細は `{{cmoc-root}}/oracle/doc/app_spec/feedback.md` を正本とする。

## join 後 hook

- merge 成功時だけ、`session.last_joined_apply_fork_commit` をこの run の `{{cmoc-run-fork-commit}}` で更新する。
