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
- realization refactor fork の full-cycle 実行本体。対象選択、file 単位の調査・修正、refactor state 更新、commit、unresolved 管理、完了判定、fork report 保存を一つの run lifecycle として扱う。
- agent 実行後の差分・commit 検証、INDEX refresh、run state 更新、正常完了・中断・error 時の cleanup と report を担う実行経路。

## Read this when
- realization refactor fork の処理順序、対象反復、unresolved finding、refactor state の完了条件を確認・変更するとき。
- agent の変更、INDEX・state・commit の検証、run isolation、正常完了・中断・error 時の report と cleanup を調べるとき。

## Do not read this when
- 対象選択や refactor state 同期だけを確認したいときは、state 管理・target selection の実装を直接読む。
- file review agent や change summary の prompt・schema 契約だけを確認したいときは、各 builder 実装を直接読む。

## hash
- e9715522b987a4379c54b9c07e1064b7b0251410fc086f5509df7387d2435d2c
