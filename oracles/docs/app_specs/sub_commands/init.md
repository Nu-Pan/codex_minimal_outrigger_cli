
# `cmoc init`

## 概要

- `<work-root>` を cmoc による作業が可能な状態に初期化する

## 引数

- 引数なし

## 事前条件

- `cmoc init` 固有の事前に満たすべき条件は無い

## 実行手順

1. `<work-root>/.cmoc` が git 追跡対象外であることを保証する
2. ここまでの作業で発生した差分を git commit する

## 「`<work-root>/.cmoc` が git 追跡対象外であることを保証する」の詳細

- 必要な操作
    - `/.cmoc/` を `<work-root>/.gitignore` に追加する
    - 既に tracked な `<work-root>/.cmoc` 配下ファイルは追跡を解除する (e.g. `git rm --cached`)
- `.cmoc` 追跡対象外保証の完了判定は、以下の両方を満たすこととする
    - `git ls-files -- .cmoc` の出力が空である
    - `git check-ignore -q .cmoc/.__cmoc_ignore_probe__` が成功する
        - これは `<work-root>/.cmoc` 配下に将来作成されるファイルが git ignore 対象になることを確認するための probe path
である
    - よって、実ファイルを作成する必要はない
