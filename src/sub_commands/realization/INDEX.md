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
- realization のリファクタリング処理を扱うパッケージ。パッケージ初期化と、refactor fork の実行ライフサイクル全体への入口を提供する。

## Read this when
- realization のリファクタリング処理の構成や入口を確認するとき。
- `cmoc realization refactor fork` の対象選択、agent 実行、state 管理、commit・report・完了判定のフローを調査または変更するとき。
- refactor fork の run isolation、interrupt/error cleanup、INDEX 更新、unresolved findings 管理を確認するとき。

## Do not read this when
- 個別の refactor agent prompt や Structured Output の構築だけを変更・調査するとき。
- refactor state のデータ構造や対象選択ロジックだけを変更・調査するとき。
- run lifecycle、process tracking、report 描画などの共通機能だけを確認するとき。
- realization のリファクタリング以外の処理を確認するとき。

## hash
- b501f451cbb3e1a3321f99526065aeeb886e971f4ffb619cd26512510a826870
