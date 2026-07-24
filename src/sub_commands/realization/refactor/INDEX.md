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
- realization refactor fork の CLI 実行ライフサイクルを統括する。editing run と refactor state を初期化し、対象 realization file ごとの agent 調査・修正・差分検証・commit を順に実行する。
- current fork 内の unresolved finding、state の investigation_required、完了理由を整合させ、正常完了・中断・エラー時の cleanup、run state 更新、fork report 出力、完了ログ生成までを一貫して扱う。
- ファイル単位の処理は関連する agent parameter builder に委譲し、Git 差分分類、INDEX 更新、state 集計、変更概要、未解決所見の report 表示を補助関数で構成する。

## Read this when
- cmoc realization refactor fork の実行順序、対象選択、処理単位の commit、unresolved 管理、完了判定を変更・調査するとき
- realization refactor の中断・エラー時における child process 停止、rollback、run state、report の挙動を確認するとき
- refactor state と managed branch の差分から fork report や completion log を生成する処理を確認するとき

## Do not read this when
- realization refactor の agent 入力 parameter 自体を変更するときは、各 parameter builder を直接読む
- refactor state のデータモデルや対象選択ロジックだけを変更するときは、commons.runtime_refactor を直接読む
- run の共通ライフサイクル、Git 差分、INDEX 更新の汎用仕様だけを確認するときは、対応する commons runtime module を直接読む

## hash
- 0811ff1ad232e10140ea3a80205f9ab71e9136ca4fabc546385b93211095ea75
