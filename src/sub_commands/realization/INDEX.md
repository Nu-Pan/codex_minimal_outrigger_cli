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
- realization のリファクタリング処理を提供するパッケージ。関連サブコマンドの実行入口と、refactor fork の対象選択から完了判定・レポート生成までのライフサイクルを扱う。

## Read this when
- realization refactor のサブコマンド構成や実行入口を確認するとき。
- refactor fork の対象選択、agent による調査・修正、差分検証、state 同期、unresolved finding、完了判定、report 生成を調査・変更するとき。

## Do not read this when
- realization refactor の対象選択や state 同期だけを確認する場合。
- agent 用 Structured Output の schema や prompt 構築だけを確認する場合。
- 共通 run lifecycle、process tracking、report 描画の汎用処理だけを確認する場合。

## hash
- 2c9dd678109e8f320f4611f4981065afd0b358e9ed3f66d8009ef6ed18d2ed2b
