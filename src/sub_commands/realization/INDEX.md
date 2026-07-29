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
- realization のリファクタリング処理を扱うパッケージ。fork の実行ライフサイクルを中心に、対象選択、agent 調査・修正、差分検証、state 同期、commit、unresolved 管理、report 保存までの入口となる。

## Read this when
- realization refactor fork の実行フロー、処理単位の commit、差分検証、state 同期、完了判定、report 保存を確認・変更するとき。

## Do not read this when
- refactor agent の prompt や Structured Output schema だけを変更するとき。
- run lifecycle の共通処理や report 出力の一般仕様を確認するとき。
- refactor state の共通データ構造や target 選択ロジックだけを変更するとき。

## hash
- 1fad6143f27c478c7639bcd90cd7d74f8c510318cca17d4e4c11119cc01af5e9
