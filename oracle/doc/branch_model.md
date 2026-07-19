# cmoc の branch model

## 概要

- cmoc は `{{local-branch}}` から `{{cmoc-session-branch}}` を作る。
- run は `{{cmoc-session-branch}}` から共通の `{{cmoc-run-branch}}` を作る。
- workload の種類は branch、commit、worktree の別名ではなく、run state と report で表す。
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
- ユーザーはこの branch 上で oracle の変更を確認し、各種サブコマンドを呼び出す。

### `{{cmoc-session-home-branch}}`

- `cmoc session fork` 実行時に checkout されていた `{{local-branch}}` である。
- session の分岐元であり、最終的な merge 先でもある。

### `{{cmoc-run-branch}}`

- run を `{{cmoc-session-branch}}` から隔離するための `{{cmoc-managed-branch}}` である。
- 命名規則は workload にかかわらず `cmoc/run/{{session-id}}/{{run-id}}` とする。
- run の差分を git commit として積み上げ、ユーザーが直接作業する branch にはしない。
- 1 つの branch は 1 つの run instance だけに対応する。

## git commit

### `{{cmoc-session-fork-commit}}`

- `{{cmoc-session-branch}}` の分岐元 commit である。
- 通常は session fork 時点の `{{cmoc-session-home-branch}}` HEAD である。

### `{{cmoc-session-join-commit}}`

- `{{cmoc-session-branch}}` を `{{cmoc-session-home-branch}}` へ merge した commit である。

### `{{cmoc-run-fork-commit}}`

- `{{cmoc-run-branch}}` の分岐元 commit である。
- run 開始時点の `{{cmoc-session-branch}}` HEAD である。
- apply が注入する差分の終点、run join 時の差分検査、および run report は、この名前を一貫して使用する。
- 同じ commit に workload ごとの別名を割り当ててはいけない。

### `{{cmoc-run-join-commit}}`

- `{{cmoc-run-branch}}` を `{{cmoc-session-branch}}` へ merge した commit である。
- workload ごとの別名を割り当ててはいけない。

## git worktree

### `{{cmoc-run-worktree}}`

- run を `{{repo-root}}` から隔離するための git linked worktree である。
- `{{run-root}}` は `{{repo-root}}/.cmoc/gu/worktree/{{session-id}}/{{run-id}}` とする。
- `{{cmoc-run-branch}}` を checkout し、run の workload を実行する。
- workload ごとの別名を割り当ててはいけない。
