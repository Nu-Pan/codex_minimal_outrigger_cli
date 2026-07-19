# `cmoc realization apply fork`

## 目的

- realization apply は、直近の git commit 群から読み取れる oracle file の変更を realization file へ素早く反映する workload である。
- fork の正常終了時には、少なくとも注入した commit 差分から読み取れる変更について、oracle file と realization file の間に齟齬がない状態にする。
- ファイル単位の網羅的な追従は non-goal とし、realization refactor が担う。
- fork, join, abandon の共通 lifecycle は `{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` を正本とする。

## 引数

- 引数なし。

## 追従対象差分

- 差分の終点は `{{cmoc-run-fork-commit}}` とする。
- 差分の始点は以下とする。
    - `session.last_joined_apply_fork_commit` が存在する場合は、その commit。
    - 初回の場合は `session.session_fork_commit`。
- cmoc は始点と終点の commit ID、および両端のいずれかで oracle file だった path に対する rename を考慮した raw git diff を agent call prompt に注入する。
- realization file、`INDEX.md`、その他の非 oracle file の差分は注入しない。
- 差分に現れた file だけを作業範囲としてはいけない。追従対象は `{{work-root}}` リポジトリ全体とする。
- 差分は今回追従すべき oracle 変更を特定する根拠であり、realization file の変更内容を正本仕様へ逆流させる根拠ではない。

## agent call と file access

- `build_realization_apply_fork_launch_exec_parameter` が、追従対象 commit 範囲と raw oracle diff を含む完全 prompt を `AgentCallParameter.prompt` として返す。
- `{{cmoc-run-worktree}}` を cwd とする `codex exec` を 1 回だけ本命 agent call として実行する。Codex CLI の TUI は起動しない。
- 本命の追従作業を複数の agent call に分割してはいけない。
- 収束判定のために同じ作業を反復してはいけない。
- 本命 agent call 終了後に、別の agent call で作業を補完してはいけない。
- prompt は、注入差分、リポジトリ全体の関連 oracle file と realization file、および適用される standard を根拠に、必要な implementation、test、ancillary を修正して検証するよう要求する。
- file access mode は `REALIZATION_WRITE` とし、agent は realization file だけを変更する。

## 想定内差分

- agent が変更する realization file。
- cmoc が生成する任意階層の `INDEX.md`。
- agent は `INDEX.md` を変更せず、cmoc が生成する。

## 実行手順

1. doctor preprocess と編集 run の共通 fork 開始処理を行う。
2. 追従対象差分を構築する。
3. `build_realization_apply_fork_launch_exec_parameter` で AgentCallParameter を構築する。
4. その AgentCallParameter を変更せず、`{{cmoc-run-worktree}}` を cwd とする `codex exec` で実行する。
5. agent の realization file 差分と cmoc が生成した `INDEX.md` を検査し、run branch に commit する。
6. `run.state` を `joinable` にして結果を report する。

## エラー

- 本命 agent call を正常に開始または終了できない場合、差分を整合した単位へ commit または rollback できない場合、あるいは後処理に失敗した場合は `run.state` を `error` にする。
- エラー後は `cmoc run join` で確定済み成果物を取り込むか、`cmoc run abandon` で run を破棄する。

## fork report と終了コード

- report は Markdown + YAML Front Matter とする。
- 共通 run 項目に加え、差分の始点 commit、Codex CLI の終了結果、および変更 path を含める。
- 差分の終点は共通項目の `{{cmoc-run-fork-commit}}` で表し、同じ commit を別項目として重複掲載しない。
- AI による意味的な変更要約は生成しない。
- `{{repo-root}}/.cmoc/gu/ar/report/realization/apply/fork/{{time-stamp}}.md` に保存する。report 本文は stdout に流さず、保存先のフル path を表示する。
- `joinable` での終了は終了コード 0、`error` での終了は非 0 とする。

## join 後 hook

- merge 成功時だけ、`session.last_joined_apply_fork_commit` をこの run の `{{cmoc-run-fork-commit}}` で更新する。
