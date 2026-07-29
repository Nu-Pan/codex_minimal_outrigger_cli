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
- realization refactor fork の full-cycle CLI workload。realization file の選択、単位ごとの agent 調査・修正、差分検証、state 同期、commit、unresolved 管理、完了判定、joinable/error report 保存までを一貫して扱う。
- fork 全体で共有する run context と処理進捗を保持するため、target 選択から report 生成までを単一の lifecycle として実装している。

## Read this when
- realization refactor fork の実行フロー、処理単位の commit、unresolved finding の追跡、完了条件を変更・調査するとき。
- agent call 後の realization 差分検証、INDEX/state 更新、interrupt・error cleanup、joinable report の挙動を確認するとき。

## Do not read this when
- refactor agent の Structured Output schema や file 単位の調査・修正 prompt だけを変更するときは、対応する builder module を直接読む。
- run lifecycle の共通処理、process tracking、report 出力の一般仕様だけを確認するときは、対応する commons module または oracle 文書を直接読む。
- refactor state の共通データ構造や target 選択ロジックだけを変更するときは、runtime_refactor module を直接読む。

## hash
- 1ddd0030e6631891407ce2defe6a86560d6b192b54af6ddb134f30eb34191871
