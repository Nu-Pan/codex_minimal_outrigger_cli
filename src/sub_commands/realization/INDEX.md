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
- realization の apply 処理に関する workload を扱うディレクトリ。apply workload の実装と、`cmoc realization apply fork` の CLI 実行処理を確認する入口となる。

## Read this when
- realization の apply workload の内容を調査・変更するとき
- `cmoc realization apply fork` の動作、例外処理、run state、fork report、差分検査、commit 処理を調査・変更するとき

## Do not read this when
- apply workload 以外の処理を扱うとき
- Codex builder の launch parameter だけを確認したいとき
- run lifecycle の共通仕様や process tracking の共通実装だけを確認したいとき
- `realization apply` 以外のサブコマンドの CLI 実装を調査するとき

## hash
- 7123c72962aa3ce39b992061670779f554386532236de746f708fa03552b8d4e

# `refactor`

## Summary
- realization のリファクタリング処理を提供するパッケージ。fork 実行のライフサイクル管理と、関連する下位リファクタリング処理への入口を担う。

## Read this when
- realization refactor fork の実行ライフサイクル、処理単位の選択・commit、状態更新、finding 管理、完了・中断・異常終了時の処理を確認または変更するとき
- realization リファクタリング処理の構成や入口を確認するとき

## Do not read this when
- 単一 realization file の調査・修正ロジックだけを確認したいとき
- 変更概要生成だけを確認したいとき
- 一般的な run isolation、editing run、INDEX 更新、refactor state の仕様を確認したいとき

## hash
- 7eb9cac344b6ada13fd6ba6b1212667a808b684d98ed45e4eb75f1b20ee99d9a
