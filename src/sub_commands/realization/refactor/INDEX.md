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
- realization refactor fork の full-cycle CLI workload。対象選択から file 単位の agent 調査・修正、差分検証、state 更新、処理単位 commit、unresolved 管理、完了判定、joinable/error report 保存までを一つの lifecycle として扱う。

## Read this when
- realization refactor fork の実行フロー、処理単位の commit、中断・例外時 cleanup、unresolved finding、完了条件、fork report の挙動を変更または調査するとき。
- refactor state と INDEX 更新、Codex child process の停止、run state の joinable/error 遷移を確認するとき。

## Do not read this when
- realization refactor の agent call 内部仕様や finding の生成形式だけを確認する場合は、file review 用の parameter builder を読む。
- change summary の Structured Output や差分要約だけを確認する場合は、change summary 用の parameter builder を直接読む。
- 一般的な run lifecycle、state 管理、report 出力の共通処理だけを確認する場合は、対応する commons モジュールを直接読む。

## hash
- e0526fb5934e06239b3dddd01f0276af2c7382ebab3e17a44154b55b06db5e84
