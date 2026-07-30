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
- realization のリファクタリング処理をまとめるパッケージ。リファクタリング fork の実行ライフサイクル管理と、その関連処理への入口を担う。
- fork の初期化、対象 file の調査・修正、差分・commit 検証、unresolved 所見の追跡、完了判定、cleanup、report 保存までを扱う。

## Read this when
- realization のリファクタリング処理の構成や入口を確認するとき
- refactor fork の実行順序、対象選択、commit、完了条件、report 保存を調査・変更するとき
- refactor state と unresolved findings の対応や、fork の中断・エラー時の cleanup を確認するとき

## Do not read this when
- realization refactor の agent parameter 構築を確認するとき
- refactor state のデータ構造や対象同期処理を確認するとき
- run 共通の isolation・lifecycle・report 処理を確認するとき
- realization refactor の利用者向け仕様だけを確認するとき

## hash
- c04ee45aa14eb9dd462da340a59c931e8d1df15c0de6d96b39cb5e84bde78aef
