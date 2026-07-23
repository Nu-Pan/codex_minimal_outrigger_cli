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
- realization refactor fork の full-cycle CLI workload を実装する入口。refactor run の初期化、対象 file ごとの調査・修正、変更検証と commit、unresolved 所見の追跡、完了判定、状態更新、fork report と完了ログの出力を一つの lifecycle として扱う。

## Read this when
- realization refactor fork の CLI 実行フロー、処理単位、refactor state の更新、unresolved 所見の扱い、完了条件、または fork report の生成を変更・調査するとき。
- 調査対象の差分検証、想定外 path の検出、割り込み・エラー時の rollback と run state 遷移を確認するとき。

## Do not read this when
- refactor state のデータ構造や target 選択ロジックだけを変更・調査するときは、対応する commons.runtime_refactor の実装を直接読む。
- file 単位の review agent parameter や change summary parameter の生成だけを変更・調査するときは、対応する builder module を直接読む。
- 一般的な run lifecycle、commit、差分分類、report 共通処理だけを確認するときは、対応する sub_commands.run の共通 module を直接読む。

## hash
- 239bfc08c5fe3590c02fcf18dd064db87f18087563e5dcd2213c8212c6e8a886
