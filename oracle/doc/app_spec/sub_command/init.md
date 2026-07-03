
# `cmoc init`

## 概要

- `<repo-root>` を cmoc による作業が可能な状態に初期化する

## 引数

- 引数なし

## 事前条件

- `cmoc init` 固有の事前に満たすべき条件は無い

## 実行手順

1. `<work-root>/.cmoc` が git 追跡対象外であることを保証する
2. `<work-root>/.agents` が git 追跡対象であることを保証する
3. ここまでの作業で発生した差分を git commit する

## 「`<repo-root>/.cmoc` が git 追跡対象外であることを保証する」の詳細

- 必要な操作
    - `/.cmoc/` を `<work-root>/.gitignore` に追加する
    - 既に tracked な `<work-root>/.cmoc` 配下ファイルは追跡を解除する (e.g. `git rm --cached`)
- `<repo-root>/.cmoc` 追跡対象外保証の完了判定は、以下の両方を満たすこととする
    - `git ls-files -- <repo-root>/.cmoc` の出力が空である
    - `git check-ignore -q <repo-root>/.cmoc/.__cmoc_ignore_probe__` が成功する
        - これは `<work-root>/.cmoc` 配下に将来作成されるファイルが git ignore 対象になることを確認するための probe path である
    - よって、実ファイルを作成する必要はない


## 「`<work-root>/.agents` が git 追跡対象であることを保証する」の詳細

- 必要な操作
    - `<work-root>/.agents` が存在しなければ作成する
    - `<work-root>/.agents` が空ディレクトリならば `<work-root>/.agents/.gitkeep` を作成する
    - `<work-root>/.agents` ツリー内 git 追跡対象外ならば `<work-root>/.agents/.gitkeep` を git 追跡対象に追加する
- 必要な理由
    - `<work-root>/.agents` は agent 操作禁止領域なので、差分が出る余地をなくしたい
    - なので、最初から作っておく
