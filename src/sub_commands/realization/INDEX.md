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
- `realization apply` に関する処理をまとめるディレクトリで、apply workload の実装と `cmoc realization apply fork` のCLIオーケストレーションを確認する入口。fork実行の差分検査、run lifecycle、成果物のcommit、joinable run・fork report生成、異常時のrollbackやcleanupも扱う。

## Read this when
- realization の apply workload の内容を調査・変更するとき
- `cmoc realization apply fork` の実行フロー、成功時のjoinable化、fork report、差分始点、agent変更の検査を調べるとき
- apply fork の異常終了時のrollback、error state、cleanup warning、agent commit検出、許可される変更範囲やINDEX生成差分を確認するとき

## Do not read this when
- apply workload や apply fork 以外の処理を扱うとき
- realization apply agent の実行パラメータ構築だけを調べるときは、launch parameter builder を直接読む
- editing run の共通ライフサイクル、git変更分類、process tracking、report書式の一般実装だけを調べるときは、インポート先の共通runtimeモジュールを直接読む
- 正本仕様そのものを確認するとき

## hash
- 1498cc25f67b10fe93ce86fb281921772690e0c2121f14905ff683b0d4b8b0bd

# `refactor`

## Summary
- realization のリファクタリング処理をまとめるパッケージ。refactor fork の full-cycle 実行と、対象選択から agent 呼び出し、変更・状態検証、finding 追跡、完了判定、cleanup、report 生成までの lifecycle への入口を提供する。

## Read this when
- realization のリファクタリング処理の構成や入口を確認するとき。
- realization refactor fork の実行フロー、処理単位の commit、state 更新、unresolved finding の完了条件を調査・変更するとき。
- agent による変更検証、INDEX 更新、run の joinable/error/interruption 処理、fork report の生成を追跡するとき。

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき。
- realization refactor の agent prompt や change summary の入力形式だけを確認するときは、対応する builder 実装を直接読む。
- 編集 run の一般的な状態遷移や worktree isolation の正本仕様だけを確認するときは、対応する oracle doc を直接読む。

## hash
- 8722271f8ae83385f3107e553bf82bbf341bc068c0623c5da0fe30bfbb6fca7b
