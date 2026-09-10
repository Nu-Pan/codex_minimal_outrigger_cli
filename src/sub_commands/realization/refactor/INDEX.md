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
- `cmoc realization refactor fork` の full-cycle workload を実装し、run 初期化、realization file の調査・修正、current fork 内の unresolved findings 管理、完了判定、変更概要と report 公開を一つの lifecycle として扱う。
- 対象 file ごとの agent 呼び出し、変更 path・commit の検証、refactor state と INDEX の同期、処理単位の commit、rename を含む unresolved findings の追跡を担う。
- 中断・例外時には Codex 子プロセス停止、rollback、run state 更新、error/interruption report 生成までを処理する。

## Read this when
- realization refactor fork の run lifecycle、処理単位、完了理由、report 公開の流れを確認・変更するとき。
- 対象 file の agent call と Structured Output、変更 path、commit、INDEX refresh の検証を確認するとき。
- unresolved findings、refactor state の完了不変条件、rename 後の追跡、中断・cleanup failure・error state の扱いを調査するとき。

## Do not read this when
- refactor 対象の選定や state 永続化そのものだけを確認したい場合は、refactor state を直接扱う実装へ進む。
- 単一 realization file の agent 用 prompt や出力契約だけを確認したい場合は、file review builder を直接読む。
- 変更概要の生成・分類だけを確認したい場合は、change summary builder を直接読む。
- editing run、Git commit、process tracking、共通 report 書き込みの一般仕様だけを確認したい場合は、対応する共通 runtime 実装や正本仕様を直接読む。

## hash
- d5963edeaa2a5c06a3febebd425fa49dbdef490daaf8b91eb7df4bfafd45ff02
