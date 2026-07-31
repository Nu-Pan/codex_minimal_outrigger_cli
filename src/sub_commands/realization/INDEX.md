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
- realization のリファクタリング処理を提供するパッケージ。リファクタリング作業全体の入口と、fork 実行の進捗・状態管理を担う。
- fork 実行では、run 初期化、INDEX と refactor state の同期、realization file ごとの agent 調査・修正、差分・commit 検証、unresolved 所見の追跡、完了判定、レポート保存までを扱う。

## Read this when
- realization refactor の処理フロー、実行状態、処理単位の commit、unresolved 管理、完了条件、fork report の挙動を調査・変更するとき。
- agent の差分・commit・evidence path の検証、割り込み・エラー時の rollback と cleanup を確認するとき。

## Do not read this when
- realization refactor の agent prompt や Structured Output の構築だけを変更するとき。
- run 共通ライフサイクル、差分分類、process tracking、report 生成の汎用仕様だけを調査・変更するとき。

## hash
- 3d7d99484de970c64c86246762bc0a3efe5fb65c0a7e36c788b24baff3d4e8ca
