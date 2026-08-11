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
- realization refactor fork の CLI 実行全体を管理する単一 workload。run の初期化から対象 file ごとの agent 調査・修正、refactor state と INDEX の同期、処理単位の commit、完了判定、joinable/error/interruption 状態の report 保存までを一貫して扱う。
- current fork 内の unresolved finding、rename、変更 path、agent の commit 違反、cleanup 失敗を追跡し、完了理由と変更概要を確定するための上位 orchestration の入口。個別の agent prompt 生成や report 表示形式の詳細を確認する場合は、それぞれの builder・runtime・report 実装へ進む。

## Read this when
- realization refactor fork の実行順序、処理単位の lifecycle、run state の遷移、完了不変条件を調査するとき
- 対象 file の選択、agent call 後の差分検証、refactor state 更新、commit と unresolved 管理の関係を確認するとき
- 中断・例外・cleanup failure 時の rollback、error report、joinable 公開条件を確認するとき
- fork report の生成内容、completion reason、変更概要、未解決 finding の追跡方法を確認するとき

## Do not read this when
- 個別の realization file を直接修正・レビューする方法だけを確認したいときは、file review 用の builder または対象 realization file を読む
- refactor state のデータ構造や target 選択ロジックだけを確認したいときは、runtime_refactor の実装を直接読む
- run の一般的な isolation、編集 run の作成・join・abandon 契約だけを確認したいときは、対応する app specification または runtime lifecycle を直接読む
- INDEX.md の生成規則や routing だけを確認したいときは、indexing の仕様・実装を読む

## hash
- 0a3548b70ba94f748a122e1015af465927ffbe6c6afffb7c856356cef8ab62eb
