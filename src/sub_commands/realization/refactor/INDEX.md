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
- realization refactor fork の CLI 実行全体を管理する workload。対象の選択、file 単位の agent 調査・修正、差分検証、refactor state 更新、commit、unresolved 所見の追跡、完了判定、joinable/error report の生成を一つの lifecycle として扱う。

## Read this when
- realization refactor fork の実行フロー、処理単位、current fork 内の unresolved 管理、完了条件、割り込み・エラー時の cleanup、report 内容を変更または調査するとき。

## Do not read this when
- 個別 realization file のレビュー・修正ロジックだけを調べるときは file_review_and_fix を読む。
- refactor 実行結果の変更概要生成だけを調べるときは change_summary を読む。
- 共通の run lifecycle、state 管理、差分分類、report 書き込みの詳細だけを調べるときは、それぞれの commons 実装を直接読む。

## hash
- 8be2007d9ce2d1b5c1078f4ed63897b9d16e2795ee72f69d42690f8820024bf3
