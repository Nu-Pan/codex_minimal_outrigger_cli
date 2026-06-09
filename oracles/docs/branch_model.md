# cmoc branch model

## 概要

cmoc は、通常の `<local-branch>` から `<cmoc-session-branch>` を作り、必要に応じて `<cmoc-session-branch>` から `<cmoc-apply-branch>` を作る。

`<repository-default-branch>` は特別扱いしない。
ユーザーが `cmoc session fork` を実行した時点で checkout している `<local-branch>` をその session の `<cmoc-session-home-branch>` とする。

## git branch

### `<repository-default-branch>`

- cmoc 管理ではない、その git リポジトリの本流の branch
- 典型的には `main`, `master` のこと

### `<local-branch>`

- cmoc 管理ではない通常の git local branch

### `<remote-tracking-branch>`

- cmoc 管理ではない通常の remote-tracking branch

### `<cmoc-managed-branch>`

- cmoc が管理する branch の総称

### `<cmoc-session-branch>`

- `cmoc session fork` が作成する `<cmoc-managed-branch>`
- 命名規則は `cmoc/session/<session-id>`
- ユーザーはこの branch 上で oracles を編集・コミットし、各種サブコマンドを呼び出す

### `<cmoc-session-home-branch>`

- `cmoc session fork` を実行した時点で checkout されていた `<local-branch>`
- `<cmoc-managed-branch>` の分岐元であり、最終的な merge 先でもある

### `<cmoc-run-branch>`

- cmoc が 1 回のサブコマンド実行 (run) の作業内容を `<cmoc-session-branch>` から隔離するために作成する `<cmoc-managed-branch>`
- 命名規則は `cmoc/run/<session-id>/<run-id>`
- cmoc の run 上で発生した差分は `<cmoc-run-branch>` に git commit として積み上げる
- ユーザーが直接作業を行うブランチではない
- `<cmoc-run-branch>` は抽象概念であり、具体的な名前はサブコマンドごとに決まる
    - `<cmoc-[sub-command-name]-branch>` とする
    - e.g. `cmoc apply ...`: `<cmoc-apply-branch>`
    - e.g. `cmoc review ...`: `<cmoc-review-branch>`

## git commit

## `<cmoc-session-fork-commit>`

- `<cmoc-session-branch>` の分岐元 git commit
- 通常は `cmoc session fork` 実行時点における `<cmoc-session-home-branch>` の HEAD

## `<cmoc-session-join-commit>`

- `<cmoc-session-branch>` --> `<cmoc-session-home-branch>` の git merge commit
- 通常は `cmoc session join` の実行時点における `<cmoc-session-home-branch>` の HEAD

## `<cmoc-run-fork-commit>`

- `<cmoc-run-branch>` の分岐元 git commit
- 通常は、run 開始時点における`<cmoc-session-branch>` の HEAD
- `<cmoc-run-fork-commit>` は抽象概念であり、具体的な名前はサブコマンドごとに決まる
    - `<cmoc-[sub-command-name]-fork-commit>` とする
    - e.g. `cmoc apply ...`: `<cmoc-apply-fork-commit>`
    - e.g. `cmoc review ...`: `<cmoc-review-fork-commit>`

## `<cmoc-run-join-commit>`

- `<cmoc-run-branch>` --> `<cmoc-session-branch>` の git merge commit 
- 通常は `cmoc apply join` の実行時点における `<cmoc-session-branch>` の HEAD
- `<cmoc-run-fork-commit>` は抽象概念であり、具体的な名前はサブコマンドごとに決まる
    - `<cmoc-[sub-command-name]-join-commit>` とする
    - e.g. `cmoc apply ...`: `<cmoc-apply-join-commit>`
    - e.g. `cmoc review ...`: `<cmoc-review-join-commit>`

## git worktree

### `<cmoc-run-worktree>`

- cmoc が 1 回のサブコマンド実行 (run) の作業内容を `<repo-root>` から隔離するために作成する cmoc 管理の git linked worktree
- 命名規則は `<run-root>` = `<repo-root>/.cmoc/worktrees/<session-id>/<run-id>`
- `<cmoc-run-worktree>` は抽象概念であり、具体的な名前はサブコマンドごとに決まる
    - `<cmoc-[sub-command-name]-worktree>` とする
    - e.g. `cmoc apply ...`: `<cmoc-apply-worktree>`
    - e.g. `cmoc review ...`: `<cmoc-review-worktree>`
