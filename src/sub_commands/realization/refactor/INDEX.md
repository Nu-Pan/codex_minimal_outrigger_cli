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
- realization refactor fork の CLI ワークロード全体を実行する実装。refactor state と INDEX の初期化、対象 file ごとの agent 調査・修正、差分と commit の検証、unresolved 所見の current fork 内追跡、完了判定、joinable/error/interruption 時の report 保存を一つの lifecycle として扱う。

## Read this when
- `cmoc realization refactor fork` の処理フロー、対象選択、agent call、処理単位 commit、unresolved 管理、完了条件を変更または調査するとき。
- refactor fork の run isolation、interrupt/error cleanup、INDEX refresh、report 出力の連携を確認するとき。
- fork の completion reason や変更概要、state 集計、unresolved findings の出力形式を確認するとき。

## Do not read this when
- 個別の refactor agent prompt や Structured Output の構築だけを変更・調査する場合は、対応する builder file を直接読む。
- refactor state のデータ構造や対象選択ロジックだけを変更・調査する場合は、`commons.runtime_refactor` の実装を直接読む。
- run lifecycle、process tracking、report 描画など共通機能の詳細だけを確認する場合は、対応する `commons.runtime_run*` モジュールを直接読む。

## hash
- 2ad0801c8568830f109f850b30c93fde7b86b30c2a991f16c5f1efc60bf4c270
