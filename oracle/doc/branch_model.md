# cmoc branch model

## 概要

- cmoc は `{{local-branch}}` から `{{cmoc-session-branch}}` を作る。
- realization 作業では、`{{cmoc-session-branch}}` から workload ごとの `{{cmoc-realization-run-branch}}` を作る。
- `{{repository-default-branch}}` は特別扱いしない。
- `cmoc session fork` 実行時に checkout されている `{{local-branch}}` を `{{cmoc-session-home-branch}}` とする。

## git branch

### `{{repository-default-branch}}`

- cmoc 管理ではない、その git repository の既定 branch である。
- 典型的には `main`, `master` である。

### `{{local-branch}}`

- cmoc 管理ではない通常の git local branch である。

### `{{remote-tracking-branch}}`

- cmoc 管理ではない通常の remote-tracking branch である。

### `{{cmoc-managed-branch}}`

- cmoc が管理する branch の総称である。

### `{{cmoc-session-branch}}`

- `cmoc session fork` が作成する `{{cmoc-managed-branch}}` である。
- 命名規則は `cmoc/session/{{session-id}}` とする。
- ユーザーはこの branch 上で oracle を編集・commit し、各種サブコマンドを呼び出す。

### `{{cmoc-session-home-branch}}`

- `cmoc session fork` 実行時に checkout されていた `{{local-branch}}` である。
- session の分岐元であり、最終的な merge 先でもある。

### `{{cmoc-run-branch}}`

- 1 回のサブコマンド実行を `{{cmoc-session-branch}}` から隔離するための `{{cmoc-managed-branch}}` である。
- 個別仕様が具体名を定めない場合の命名規則は `cmoc/run/{{session-id}}/{{run-id}}` とする。
- run の差分を git commit として積み上げ、ユーザーが直接作業する branch にはしない。
- 抽象概念であり、具体名はサブコマンドごとに定める。
    - `{{cmoc-[sub-command-name]-branch}}` とする。
    - e.g. review run: `{{cmoc-review-branch}}`

### `{{cmoc-realization-run-branch}}`

- realization run における `{{cmoc-run-branch}}` の総称である。
- apply run では `{{cmoc-realization-apply-branch}}` を指す。
- refactor run では `{{cmoc-realization-refactor-branch}}` を指す。

### `{{cmoc-realization-apply-branch}}`

- `cmoc realization apply fork` が新規作成する branch である。
- 命名規則は `cmoc/realization/apply/{{session-id}}/{{run-id}}` とする。

### `{{cmoc-realization-refactor-branch}}`

- `cmoc realization refactor fork` が新規作成する branch である。
- 命名規則は `cmoc/realization/refactor/{{session-id}}/{{run-id}}` とする。
- refactor fork のユーザー中断後は削除せず、次回 fork で再利用する。

## git commit

### `{{cmoc-session-fork-commit}}`

- `{{cmoc-session-branch}}` の分岐元 commit である。
- 通常は session fork 時点の `{{cmoc-session-home-branch}}` HEAD である。

### `{{cmoc-session-join-commit}}`

- `{{cmoc-session-branch}}` を `{{cmoc-session-home-branch}}` へ merge した commit である。

### `{{cmoc-run-fork-commit}}`

- `{{cmoc-run-branch}}` の分岐元 commit である。
- 通常は run 開始時点の `{{cmoc-session-branch}}` HEAD である。
- サブコマンドごとの具体名は `{{cmoc-[sub-command-name]-fork-commit}}` とする。
- realization workload ごとの具体名は `{{cmoc-realization-apply-fork-commit}}`, `{{cmoc-realization-refactor-fork-commit}}` とする。

### `{{cmoc-run-join-commit}}`

- `{{cmoc-run-branch}}` を `{{cmoc-session-branch}}` へ merge した commit である。
- サブコマンドごとの具体名は `{{cmoc-[sub-command-name]-join-commit}}` とする。
- realization workload ごとの具体名は `{{cmoc-realization-apply-join-commit}}`, `{{cmoc-realization-refactor-join-commit}}` とする。

### `{{realization-oracle-snapshot-commit}}`

- realization run 開始時点の `{{cmoc-session-branch}}` HEAD である。
- `{{cmoc-run-fork-commit}}` と同じ commit を指すが、oracle の参照 snapshot という責務を明示する名前である。

## git worktree

### `{{cmoc-run-worktree}}`

- run を `{{repo-root}}` から隔離するための git linked worktree である。
- `{{run-root}}` は `{{repo-root}}/.cmoc/gu/worktree/{{session-id}}/{{run-id}}` とする。
- 抽象概念であり、具体名はサブコマンドごとに定める。
    - `{{cmoc-[sub-command-name]-worktree}}` とする。
    - e.g. review run: `{{cmoc-review-worktree}}`

### `{{cmoc-realization-run-worktree}}`

- realization run における `{{cmoc-run-worktree}}` の総称である。
- apply run では `{{cmoc-realization-apply-worktree}}` を指す。
- refactor run では `{{cmoc-realization-refactor-worktree}}` を指す。
