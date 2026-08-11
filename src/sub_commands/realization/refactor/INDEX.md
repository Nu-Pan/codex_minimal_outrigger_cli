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
- realization refactor fork の CLI 実行全体を管理するワークロード実装。refactor state の初期化・INDEX 同期から、realization file 単位の agent 調査・修正、差分と commit の検証、unresolved 所見の current fork 内追跡、完了条件の検査、joinable/error/interruption 状態の cleanup、fork report と完了ログの生成までを一つの lifecycle として扱う。realization refactor fork の実行フロー、処理単位の commit や agent 変更制約、unresolved 管理、完了判定、report 内容を確認・変更するときの入口である。

## Read this when
- realization refactor fork サブコマンドの全体 lifecycle、実行状態遷移、処理単位の進捗管理を調査するとき
- refactor state と INDEX の初期化・同期、realization file の選択、agent call 後の差分検証や commit 処理を変更するとき
- unresolved finding の追跡、rename 後の state path との整合、natural completion と completed_with_unresolved の判定を確認するとき
- 中断・例外時の child process 停止、rollback、run state 更新、fork report 生成の挙動を確認するとき

## Do not read this when
- realization refactor fork の agent 用入力パラメータや所見 schema の詳細だけを確認したい場合は、対応する builder 実装を直接読む
- refactor state の一般的なデータ構造や target 選択規則だけを確認したい場合は、runtime_refactor の実装を直接読む
- run isolation、editing run、INDEX 更新など共通 runtime の一般仕様だけを確認したい場合は、参照されている共通 runtime または oracle 仕様を直接読む
- fork report の共通レンダリング形式だけを確認したい場合は、runtime_run_report の実装を直接読む

## hash
- af7adfc3aa36830eafcb73330378bf8485e91a9b1fbb7889d61f77f5fa7f06fa
