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
- realization refactor fork の CLI 実行ライフサイクルを統括する workload。run の初期化、INDEX と refactor state の同期、realization file 単位の agent 調査・修正、差分と commit の検証、unresolved 所見の追跡、完了判定、joinable/error report の保存までを一つの進捗状態で扱う。

## Read this when
- realization refactor fork の処理フロー、run state、処理単位の commit、unresolved 管理、完了条件、fork report の挙動を変更または調査するとき。
- agent の差分・commit・evidence path の検証や、割り込み・エラー時の rollback と cleanup を確認するとき。

## Do not read this when
- realization refactor の agent prompt や Structured Output の構築だけを変更するときは、対応する builder 実装を直接読む。
- run の共通ライフサイクル、差分分類、process tracking、report 生成の汎用仕様だけを変更するときは、対応する commons 実装や oracle 文書を直接読む。

## hash
- 6149f7027dbb70c7d189dc87fc3ff5bfe40e42673b2901192f468306f6879b7d
