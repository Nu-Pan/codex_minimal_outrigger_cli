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
- realization refactor fork の CLI 実行を統括するフルサイクル処理。run の初期化、対象ファイルの選択、agent による調査・修正、差分検証、state 更新、処理単位の commit、中断・エラー時の cleanup、完了判定、変更概要と fork report の保存までを一貫して扱う。
- realization/refactor の fork lifecycle、current fork 内の unresolved findings、investigation_required state、joinable/error への遷移を確認するための実装上の入口。

## Read this when
- realization refactor fork の開始・完了・中断・エラー処理を変更または調査するとき
- refactor target の選択、agent 出力の検証、realization file 以外の差分拒否、state 同期、commit 単位を確認するとき
- unresolved findings、完了不変条件、変更概要、fork report の生成内容を変更または調査するとき

## Do not read this when
- 単一ファイルの refactor agent 用 prompt や所見 schema の詳細だけを確認したいときは、対応する builder 実装を直接読む
- refactor state の永続化・target 選択そのものを調査するときは、commons.runtime_refactor の実装を直接読む
- run lifecycle の共通操作や report の共通形式だけを確認したいときは、対応する commons モジュールを直接読む

## hash
- 5bba2eb5d8c304ca96397a22e569a665ae595123a9adce157a43329e15060be6
