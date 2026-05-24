# cmoc branch model

## 概要

cmoc は、通常の local branch から session branch を作り、必要に応じて session branch から apply branch を作る。

`main` / `master` / repository default branch は特別扱いしない。
ユーザーが `cmoc branch` を実行した時点で checkout している通常の local branch をその session の `<session-home-branch>` とする。

## branch の種類

### `<session-home-branch>`

`cmoc branch` を実行した時点で checkout されていた通常の local branch。
session の分岐元であり、最終的な merge 先でもある。

### `<cmoc-session-branch>`

`cmoc branch` が作成する cmoc 管理 branch。
命名規則は以下。

`cmoc/session/<session-id>`

ユーザーはこの branch 上で oracles を編集・commit し、`cmoc eval-oracles` や `cmoc apply` を呼び出す。

### `<cmoc-apply-branch>`

`cmoc apply` が 1 回の apply 実行ごとに作成する cmoc 管理 branch。
命名規則は以下。

`cmoc/apply/<session-id>/<apply-run-id>`

Codex CLI による実装修正 commit はこの branch に積む。
ユーザーが oracle 改訂作業を行う場所ではない。

## session の原則

1 つの `<session-home-branch>` に対して active な `<cmoc-session-branch>` は高々 1 つとする。

`<session-home-branch>` は通常の local branch でなければならない。
detached HEAD、remote-tracking branch、commit hash、cmoc-managed branch は `<session-home-branch>` として扱わない。

## apply の snapshot 原則

`cmoc apply` は、開始時点の `<cmoc-session-branch>` HEAD を `<oracle-snapshot-commit>` として固定し、その snapshot から `<cmoc-apply-branch>` を作成する。

apply 開始後に `<cmoc-session-branch>` が進んでも、実行中の apply はその変更を取り込まない。

apply の収束・未収束判定は `<oracle-snapshot-commit>` に対する判定である。
