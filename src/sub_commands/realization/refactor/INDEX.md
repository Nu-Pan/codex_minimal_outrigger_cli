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
- realization refactor fork の一連の実行ライフサイクルを管理する CLI 実装。対象選択、file 単位の agent 調査・修正、差分と commit の検証、refactor state 同期、unresolved finding 管理、完了判定、joinable/error report 生成までを一つの workload として扱う。
- realization refactor fork の処理フロー、完了条件、中断・異常時の cleanup、run isolation、report 内容を変更・調査するときの主要な実装入口。

## Read this when
- realization refactor fork サブコマンドの挙動、処理単位、state 更新、unresolved の扱いを変更または調査するとき。
- refactor agent の差分検証、commit 禁止、rename、INDEX refresh、run の joinable/error 遷移を確認するとき。
- fork report の完了理由、変更概要、処理済み対象、未解決所見の生成内容を確認するとき。

## Do not read this when
- realization refactor の対象選択や state 同期だけを調査する場合は、commons.runtime_refactor の実装を直接読む。
- agent 用 Structured Output の schema や prompt 構築だけを調査する場合は、対応する refactor fork builder を直接読む。
- 共通 run lifecycle、process tracking、report 描画の汎用仕様だけを調査する場合は、対応する commons モジュールまたは oracle 文書を直接読む。

## hash
- dbc3541eb29e6b852748e6db44642fde7b524b30951bcc4e91bb5d11ec4379e9
