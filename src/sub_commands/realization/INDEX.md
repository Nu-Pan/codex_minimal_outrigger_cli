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
- realization のリファクタリング処理をまとめるパッケージ。fork 実行と関連処理への入口を提供する。
- realization refactor fork の CLI 実行全体を担当し、run lifecycle、対象ファイルの調査・修正、差分検証、state 更新、commit、unresolved 管理、完了判定、cleanup、report 出力を一貫して扱う。

## Read this when
- realization のリファクタリング処理の構成や入口を確認するとき。
- realization refactor fork の lifecycle、処理単位、unresolved finding 管理、完了条件、run state 遷移を変更または調査するとき。
- refactor agent の差分検証、state と INDEX の同期、commit 後の進捗記録、interruption/error 時の cleanup、fork report や完了ログを変更するとき。

## Do not read this when
- refactor 対象ファイルの個別調査・修正 prompt 生成を変更するとき。
- 変更概要の Structured Output 生成を変更するとき。
- refactor state の一般的な永続化・target 選択処理を変更するとき。
- run の共通 lifecycle や report 描画を変更するとき。

## hash
- 25129a8d09a86097b8bd9b61a1f29e6248d7f99498e017be061a3d0a9e07fc0b
