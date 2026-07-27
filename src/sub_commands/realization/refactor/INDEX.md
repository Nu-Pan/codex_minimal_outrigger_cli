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
- realization refactor fork の一連のライフサイクルを実行する CLI ワークロード。refactor state の初期化、realization file ごとの agent 調査・修正、差分検証、処理単位の commit、未解決所見の管理、完了判定、joinable/error report の生成までを一つの状態共有下で扱う。

## Read this when
- realization refactor fork の実行フロー、対象選択、処理単位の commit、unresolved finding の扱いを変更・調査するとき。
- 中断・例外時の run cleanup、state 遷移、report 保存、完了条件を確認するとき。
- fork report の完了理由、変更概要、調査状態集計、Codex call log の出力を確認するとき。

## Do not read this when
- refactor 対象選択や state 同期の共通ロジックだけを調査する場合は、commons.runtime_refactor の実装を直接読む。
- 単一ファイルの agent review・修正 parameter を調査する場合は、file_review_and_fix の実装を直接読む。
- 変更概要の生成 parameter だけを調査する場合は、change_summary の実装を直接読む。
- 一般的な editing run の lifecycle や report 共通処理だけを調査する場合は、対応する commons の lifecycle/report 実装を直接読む。

## hash
- 1f8fc4996b83bbb7ef1c9e6067fb94e77ff1f6dd6a5592111cb3c7e5e3390432
