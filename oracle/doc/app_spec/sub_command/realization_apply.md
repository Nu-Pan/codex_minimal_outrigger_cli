# `cmoc realization apply fork|join|abandon`

## 目的

- `cmoc realization apply` は、直近の git commit 群から読み取れる oracle file の変更を realization file へ素早く反映する workload である。
- `cmoc oracle edit` と交互に、10～30 分程度の短い仕様変更・実装変更ループで使うことを想定する。
- fork の正常終了時には、少なくとも注入した commit 差分から読み取れる変更について、oracle file と realization file の間に齟齬がない状態にする。
- ファイル単位の網羅的な追従は non-goal とし、`cmoc realization refactor` が担う。

## `cmoc realization apply fork`

### 引数

- 引数なし。
- 旧 `cmoc apply fork` の `--scope` は提供しない。

### 追従対象差分

- 差分の終点は、fork 開始時点の `{{cmoc-session-branch}}` HEAD である `{{realization-oracle-snapshot-commit}}` とする。
- 差分の始点は以下とする。
    - `session.last_joined_realization_apply_oracle_snapshot_commit` が存在する場合は、その commit。
    - 初回の場合は `session.session_start_commit`。
- cmoc は始点と終点の commit ID、および両端のいずれかで oracle file だった path に対する rename を考慮した raw git diff を TUI prompt に注入する。
- realization file、`INDEX.md`、その他の非 oracle file の差分は注入しない。
- 差分に現れたファイルだけを作業範囲としてはいけない。追従対象は `{{work-root}}` リポジトリ全体とする。
- 差分は「今回追従すべき仕様変更」を特定する根拠であり、realization file の変更内容を正本仕様へ逆流させる根拠ではない。

### 実行手順

1. `{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_run.md` の共通 fork 開始処理を行う。
2. `build_realization_apply_fork_launch_tui_parameter` で TUI 起動パラメータを構築する。
3. `{{cmoc-realization-apply-worktree}}` を cwd として Codex CLI の TUI を 1 セッション起動する。
4. TUI が正常終了したら、agent が発生させた realization file の差分と cmoc が生成した `INDEX.md` を commit する。
5. `realization_run.state` を `completed` にする。
6. 結果をレポートする。

### Codex CLI 呼び出し

- 実装追従を行う本命の Codex CLI 呼び出しは TUI 1 セッションだけとする。
- cmoc が追従作業を複数の agent call に分割したり、収束判定のために同じ作業を繰り返したりしてはいけない。
- TUI prompt は、追従対象差分、リポジトリ全体の関連 oracle file と realization file、適用される standard を根拠に必要な実装・テスト・補助ファイルを修正するよう要求する。
- TUI prompt は、注入差分から読み取れる oracle 変更との齟齬を残さず、必要な検証を完了することを goal に含める。
- agent は oracle file を変更してはいけない。

### エラー

- TUI を正常に開始・終了できない場合、または後処理に失敗した場合は `realization_run.state` を `error` にする。
- TUI 1 セッションの終了後に、cmoc が別の Codex CLI 呼び出しで作業を補完してはいけない。

### report と終了コード

- fork report は Markdown + YAML Front Matter とする。
- YAML Front Matter に、`{{cmoc-session-branch}}`, `{{cmoc-session-fork-commit}}`, 差分の始点 commit, `{{realization-oracle-snapshot-commit}}`, `{{cmoc-realization-apply-branch}}`, `{{cmoc-realization-apply-fork-commit}}`, `{{cmoc-realization-apply-worktree}}` を含める。
- 本文に、完了またはエラーの区分、TUI の終了結果、変更 path を含める。
- AI による意味的な変更要約は生成しない。
- `{{repo-root}}/.cmoc/gu/ar/report/realization/apply/fork/{{time-stamp}}.md` に保存する。report 本文は stdout に流さず、保存先のフル path を表示する。
- 完了は終了コード 0、エラーは非 0 とする。

## `cmoc realization apply join`

- apply run の成果物を `{{cmoc-session-branch}}` へ merge する。
- 引数、事前条件、想定外差分、merge、状態更新、cleanup は `{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_run.md` の join を正本とする。

## `cmoc realization apply abandon`

- 未 join の apply run を破棄する。
- 引数、事前条件、破棄範囲、状態更新、cleanup は `{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_run.md` の abandon を正本とする。
