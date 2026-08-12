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
- realization refactor fork の full-cycle workload を実行する中核実装。対象 realization file の選択、agent による調査・修正、差分と commit の検証、refactor state の更新、INDEX 同期、unresolved findings の current fork 内管理、完了判定、joinable/error/interruption 時の cleanup と fork report 作成までを一つの lifecycle として担う。
- realization refactor fork の実行経路、処理単位の commit・中断復旧・エラー処理・完了理由、report 内容や変更概要の挙動を確認または変更するときの入口となる。対象 file 単体の agent prompt や change summary の詳細だけを確認する場合は、それぞれの builder 実装を直接読む。

## Read this when
- realization refactor fork の CLI 実行 lifecycle や処理順序を調査するとき
- 対象選択、findings と unresolved の整合、refactor state 更新、完了条件を確認するとき
- agent の変更検証、commit 防止、INDEX refresh、run の rollback・joinable・error 処理を確認するとき
- fork report や completion log の生成内容・完了理由を確認するとき

## Do not read this when
- file review agent の入力形式や調査・修正プロンプトだけを確認する場合
- 正常完了時の変更概要生成の入力・Structured Output を確認する場合
- refactor state の一般的な保存・同期仕様だけを確認する場合
- run isolation や interruption の正本仕様を確認する場合は、対応する oracle specification を直接読む

## hash
- 7d96a660ba6633bf0155193ffce66368eb778489f881705e0911c072378bc409
