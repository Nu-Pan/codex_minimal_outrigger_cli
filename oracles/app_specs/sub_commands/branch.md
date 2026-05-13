# `cmoc branch`

## 概要

- これから cmoc による開発作業を行うことになる専用 git ブランチである `<cmoc-branch>` を作成する
- 実態は git によるブランチ操作のショートカットである。

## 引数

- 引数なし

## 事前条件

- サブコマンド呼び出し時点で満たすべき `cmoc branch` 固有の事前条件は無い

## 実行手順

以下のような手順で処理を行う。

1. git checkout -b <cmoc-branch>
2. `<repo-root>/.cmoc` が git の追跡対象外であることを保証する

## `<cmoc-branch>` の命名規則

- `cmoc_<time-stamp>` とする
- ブランチ名が衝突（どう考えても有りえないが）した場合はリトライする
