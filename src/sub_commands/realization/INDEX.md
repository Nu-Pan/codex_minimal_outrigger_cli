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
- realization のリファクタリング処理を構成するパッケージ。refactor 関連処理への入口を提供する。
- 対象 realization file の選択から、agent による調査・修正、差分・commit 検証、state 更新、所見追跡、完了判定、report 生成までの fork 実行単位を管理する。

## Read this when
- realization のリファクタリング処理の構成や実行フローを確認するとき
- `cmoc realization refactor fork` の lifecycle、変更範囲検証、state・unresolved 所見、fork report、cleanup を調査・変更するとき

## Do not read this when
- realization refactor の agent prompt や Structured Output schema だけを確認したいとき
- run lifecycle、refactor state、report 表示の共通処理だけを調べるとき
- 他の realization refactor サブコマンドの処理を調べるとき

## hash
- 7babd406f275e4c2dc1593b965ba10ba5d79d24dab4a16d248476082f04ca8d5
