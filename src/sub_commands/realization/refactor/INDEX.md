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
- realization refactor fork の full-cycle CLI workload を実装する。refactor run の初期化、realization file 単位の調査・修正、state 同期、commit、完了判定、変更要約、fork report 保存までを単一の lifecycle として扱う。
- current fork 内の unresolved finding を対象ごとに管理し、処理済み対象、未調査対象、finding 数、変更 path、Codex call log を report と標準出力へ反映する。

## Read this when
- realization refactor fork の実行フロー、処理単位、完了条件、unresolved 管理、refactor state 更新を変更・調査するとき。
- fork report の生成内容や change summary、割り込み・例外時の rollback と run state 更新を確認するとき。

## Do not read this when
- 通常の realization refactor の state 操作だけを変更する場合は、直接 commons.runtime_refactor を読む。
- 一般的な run lifecycle や report 共通処理だけを変更する場合は、直接 sub_commands.run.lifecycle または sub_commands.run.report を読む。
- file 単位の agent parameter や change summary parameter の定義だけを確認する場合は、対応する builder module を直接読む。

## hash
- 268826701af4edb46f8b677d55ce247d29da630ed8962d824d334d1698da1cda
