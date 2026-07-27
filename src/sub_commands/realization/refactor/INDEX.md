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
- realization refactor fork の full-cycle CLI workload を実装する。refactor state と INDEX の初期化、realization file 単位の agent 調査・修正、差分検証、処理単位の commit、完了判定、変更概要生成、fork report 保存までを一つの lifecycle として管理する。
- current fork 内の unresolved finding、処理済み target、state の investigation_required を追跡し、自然完了・unresolved 付き完了・中断・error の各結果を joinable run と report に反映する。

## Read this when
- realization refactor fork の CLI 実行フロー、処理単位の調査・修正、commit、state 更新、完了判定を変更または調査するとき
- refactor agent の Structured Output 検証、想定外差分の拒否、unresolved finding の追跡を確認するとき
- 中断・例外時の rollback、run state 更新、fork report 生成の挙動を確認するとき

## Do not read this when
- realization refactor の agent parameter 自体を変更するときは、file review 用または change summary 用の builder を直接読む
- refactor state のデータ構造や target 選択ロジックだけを変更するときは、commons.runtime_refactor を直接読む
- run lifecycle の共通操作、process tracking、report の共通形式だけを確認するときは、対応する commons runtime module を直接読む

## hash
- 41a67e693843b34286618e1f930951eefd641b0ccfb19e98ddc50f8e093b8dca
