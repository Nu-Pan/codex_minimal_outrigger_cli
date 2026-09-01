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
- realization refactor fork の full-cycle 実行経路を担い、対象選択から file 単位の調査・修正、state 更新、commit、完了判定、fork report 公開までを一貫して処理する。
- current fork 内の unresolved finding と rename を追跡し、正常完了・割り込み・error 時の cleanup、run state、report の整合性を管理する入口である。

## Read this when
- realization refactor fork 全体の lifecycle、処理単位の進捗、unresolved の完了条件、または joinable/error report の生成を確認したいとき。
- agent commit、想定外差分、遅延 descendant、割り込み時の rollback と run 回収の扱いを調査するとき。

## Do not read this when
- 単一 realization file の agent によるレビュー・修正 prompt の仕様だけを確認したいときは file review 用 builder を読む。
- 変更概要の分類・要約形式だけを確認したいときは change summary 用 builder を読む。
- refactor state の同期・保存・対象選択の一般処理だけを確認したいときは runtime refactor 実装を直接読む。

## hash
- 938cde45aede9ec0fed8f1eb7a740756235ff73a4035451c25084dd0fb990cc1
