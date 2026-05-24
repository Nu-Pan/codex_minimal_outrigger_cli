# `cmoc branch`

## 概要

`cmoc branch` は、現在 checkout している通常の local branch を `<session-home-branch>` とし、その HEAD から `<cmoc-session-branch>` を作成する。

`<session-home-branch>` は、その session の分岐元であり、最終的な merge 先でもある。

`main` / `master` / repository default branch は特別扱いしない。

## 引数

- 引数なし

## 事前条件

`cmoc branch` は、通常の local branch 上でのみ実行できる。

以下の場合はエラー終了する。

- detached HEAD 上で実行された
- remote-tracking branch や commit hash など、local branch ではない場所から実行された
- `cmoc/session/...` や `cmoc/apply/...` など cmoc-managed branch 上で実行された
- git 未コミット差分が存在する
- 現在の `<session-home-branch>` に active な `<cmoc-session-branch>` が既に存在する

## 実行手順

1. 現在 checkout している通常の local branch 名を `<session-home-branch>` として取得する
2. 現在の HEAD commit を `<session-start-commit>` として取得する
3. `<repo-root>/.cmoc` が git の追跡対象外であることを保証する
4. 一意な `<session-id>` を生成する
5. `<cmoc-session-branch>` を作成して checkout する
6. `<repo-root>/.cmoc/sessions/<session-id>/session.json` に session metadata を保存する
7. 作成した `<cmoc-session-branch>` 名と `<session-home-branch>` 名を標準出力に表示する

## `<cmoc-session-branch>` の命名規則

- `<cmoc-session-branch>` はの実際のブランチ名の形式は `cmoc/session/<session-id>` とする。
ただし `<session-id>` == `<time-stamp>` とする
- e.g. `cmoc/session/2026-05-24_22-10_15_123`

## 任意 start point の扱い

- `cmoc branch` は任意の start point を受け取らない
- 分岐元を変えたい場合は、ユーザーが事前に目的の通常 local branch へ移動してから `cmoc branch` を実行する

## legacy branch

既存の `cmoc_<time-stamp>` 形式の branch は legacy session branch として扱ってよい。
ただし、新規の `cmoc branch` は legacy 形式の branch を作成しない。
