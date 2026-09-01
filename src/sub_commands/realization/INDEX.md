# `__init__.py`

## Summary
- realization workload サブコマンドのパッケージ入口。

## Read this when
- realization workload サブコマンドの実装や構成を確認するとき。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。

## hash
- 45f2cdf62d9edd181a1f1cc14734db2757e556059630746b1486c1bd5d1101b4

# `apply`

## Summary
- realization の apply 処理に関する workload を扱うディレクトリで、apply workload の実装を確認する入口。配下には apply の共通入口と、`cmoc realization apply fork` の実行を統括する実装がある。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の処理順序、成功・失敗時の run state、差分の許可範囲、commit/rollback、fork report、cleanup を確認または変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- realization apply の仕様や共通 editing run の契約を確認する場合は、対応する oracle/specification または共通 runtime 実装を直接読む。
- fork 以外の realization apply サブコマンドの固有処理だけを確認する場合は、各サブコマンドの実装を直接読む。

## hash
- 6cf3290d311d6d35194046bbeed7ea4ee6eaa5b1b8233f1c0893a54b7da0f0d9

# `refactor`

## Summary
- realization のリファクタリング処理をまとめるパッケージで、関連する処理への入口となる。
- realization refactor fork のライフサイクル全体を処理し、対象選択、file 単位の調査・修正、state 更新、commit、完了判定、report 公開までを一貫して担う。

## Read this when
- realization のリファクタリング処理の構成や入口を確認するとき。
- refactor fork の進捗、unresolved finding・rename の追跡、cleanup、run state、report 整合性、commit や割り込み時の処理を確認するとき。

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき。
- 単一 realization file のレビュー・修正 prompt、変更概要の分類・要約、refactor state の一般的な同期・保存・対象選択を直接確認したいとき。

## hash
- 84ab70b73b79351a0e8f785e819f8a4ad06a183784b47e782a24faa56c0c4b9a
