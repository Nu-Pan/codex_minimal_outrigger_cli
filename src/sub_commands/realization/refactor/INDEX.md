# `__init__.py`

## Summary
- realization のリファクタリング作業を扱うパッケージ。関連するリファクタリング処理への入口となる。

## Read this when
- realization のリファクタリング作業の内容や構成を確認するとき。

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき。

## hash
- d070e139f0ebc38e439ff4bf3b37f76a7a536a3424248e4afcc0525de0573746

# `fork.py`

## Summary
- realization refactor fork の CLI 実行ライフサイクルを担う。対象選択、file 単位の agent 調査・修正、差分検証、refactor state 更新、処理単位の commit、完了判定、joinable/error report の保存までを一つの進捗状態で管理する。

## Read this when
- realization refactor fork の実行フロー、割り込み・エラー時の cleanup、unresolved finding の管理、完了条件、fork report の内容を変更または調査するとき。

## Do not read this when
- refactor agent の入力 parameter や所見形式だけを確認したいときは、file review 用の builder を直接読む。
- change summary の Structured Output 生成だけを確認したいときは、change summary 用の builder を直接読む。
- run の一般的なライフサイクルや git 差分操作の共通実装だけを確認したいときは、commons の runtime run 関連モジュールを直接読む。

## hash
- b6949d89adf029a17ff5adaefd85ff6b17c04f9666ac15ae555196df7c40330c
