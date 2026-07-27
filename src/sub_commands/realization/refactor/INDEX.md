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
- realization refactor fork の CLI 実行を担う full-cycle workload。refactor run の初期化、対象 realization file の選択・調査・修正、差分検証、state 更新、処理単位の commit、完了判定、変更概要生成、joinable/error report の保存までを一つの lifecycle として扱う。
- 中断時の子プロセス停止、作業単位の rollback、run state 更新、開始途中の run 回収を含む。対象 file ごとの findings と unresolved 状態を current fork 内で管理し、完了時に refactor state と unresolved targets の整合性を検証する。

## Read this when
- `cmoc realization refactor fork` の CLI 挙動、run lifecycle、処理単位の commit、interrupt/error cleanup を変更または調査するとき
- realization refactor の target selection、findings の Structured Output 検証、refactor state 更新、完了条件、fork report の内容を確認するとき
- refactor agent が予期しない差分を作った場合や、unresolved findings と report の整合性を追跡するとき

## Do not read this when
- 通常の realization file の個別リファクタリング内容を調査・変更するときは、対象 realization file と refactor agent の処理定義を直接読む
- refactor state のデータ構造や target 選択ロジックだけを調査するときは、`commons.runtime_refactor` の実装を直接読む
- 一般的な editing run の join、abandon、report 処理だけを調査するときは、対応する runtime lifecycle/report 実装を直接読む

## hash
- 0e934f792c518eaff32e8c83d9df2318d46a914abb7ace16e922cf4102a22ef2
