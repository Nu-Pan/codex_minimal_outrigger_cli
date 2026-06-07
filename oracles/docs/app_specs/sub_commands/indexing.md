
# `cmoc indexing`

## 概要

- `cmoc indexing` は現在の `<repo-root>` に対してインデクシングを実行する
- インデクシングの結果は自動的に git にコミットされる

## 引数

- 引数なし

## 事前条件

以下の場合はエラー終了する。

- git 未コミット差分が存在する

## 実行手順

- インデクシングを明示的に実行
- インデクシングによって発生した差分を git commit

## インデクシングとは

- `<cmoc-root>/oracles/docs/app_specs/indexing.md` を参照

