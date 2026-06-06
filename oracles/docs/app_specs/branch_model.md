# cmoc branch model

## 概要

cmoc は、通常の `<local-branch>` から `<cmoc-session-branch>` を作り、必要に応じて `<cmoc-session-branch>` から `<cmoc-apply-branch>` を作る。

`<repository-default-branch>` は特別扱いしない。
ユーザーが `cmoc session fork` を実行した時点で checkout している `<local-branch>` をその session の `<cmoc-session-home-branch>` とする。

## git branch の種類

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

- `cmoc session fork` が作成する cmoc 管理 branch
- 命名規則は `cmoc/session/<session-id>`
- ユーザーはこの branch 上で oracles を編集・コミットし、`cmoc review oracles` や `cmoc apply fork` を呼び出す。
- `<cmoc-managed-branch>` の下位概念

### `<cmoc-session-home-branch>`

- `cmoc session fork` を実行した時点で checkout されていた `<local-branch>`
- session の分岐元であり、最終的な merge 先でもある

### `<cmoc-run-branch>`

- cmoc が 1 回のサブコマンド実行の作業内容を `<cmoc-session-branch>` から隔離するために作成する cmoc 管理 branch
- `<cmoc-apply-branch>`, `<cmoc-review-branch>` の上位概念
- ユーザーが直接作業を行うブランチではない
- `<cmoc-managed-branch>` の下位概念

## `<cmoc-run-home-commit>`

- `<cmoc-run-branch>` の分岐元 git commit
- 通常は、run 開始時点における`<cmoc-session-branch>` の HEAD

### `<cmoc-apply-branch>`

- `cmoc apply fork` が 1 回の apply 実行ごとに作成する cmoc 管理 branch。
- 命名規則は `cmoc/apply/<session-id>/<apply-run-id>`
- Codex CLI による実装修正 commit はこの branch に積む。
- `<cmoc-run-branch>` の下位概念

### `<cmoc-review-branch>`

- `cmoc review ...` が 1 回の実行毎に作成する cmoc 管理 branch
- 命名規則は `cmoc/review/<session-id>/<review-run_id>`
- レビュー中に発生した差分 commit (e.g. `INDEX.md` の更新) はこの branch に積む
- `<cmoc-run-branch>` の下位概念

## git worktree の種類

### `<cmoc-apply-worktree>`

- `cmoc apply fork`  が 1 回の apply 実行ごとに作成する、作業用 git worktree である
- 命名規則は `<repo-root>/.cmoc/worktrees/apply/<session-id>/<apply-run-id>`
