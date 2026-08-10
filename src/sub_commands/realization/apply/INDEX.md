# `__init__.py`

## Summary
- realization の apply 処理に関する workload を扱うモジュール。apply workload の実装を確認する入口となる。

## Read this when
- realization の apply workload の内容を調査・変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。

## hash
- d6d2ca470e50cfd6872e3d6ceaaf3a134b7f0dc8205826c843ca70d79352d5f7

# `fork.py`

## Summary
- このファイルは `cmoc realization apply fork` サブコマンドの実行本体で、realization apply agent を隔離 run 上で起動し、oracle 差分を基準に成果物を検査・commit して joinable run と fork report を生成する。agent の想定外変更、commit、子プロセス、cleanup、rollback、error state も扱う。
- `src/sub_commands/realization/apply` 配下で、apply fork のCLIオーケストレーション、差分検査、run lifecycle、report 保存の入口となる。agent起動パラメータ自体やrun lifecycleの共通実装を確認する場合は、インポート先の専用モジュールへ進む。

## Read this when
- `cmoc realization apply fork` の実行フロー、成功時のjoinable化、fork report、差分始点、agent変更の検査を調べるとき
- apply fork の異常終了時のrollback、error state、cleanup warning、agent commit検出の挙動を調べるとき
- apply fork が許可する変更範囲やINDEX生成差分の扱いを確認するとき

## Do not read this when
- realization apply agent が受け取る実行パラメータの構築方法だけを調べるときは、launch parameter builder を直接読む
- editing run の共通ライフサイクル、git変更分類、process tracking、report書式の一般実装だけを調べるときは、インポート先の共通runtimeモジュールを直接読む
- apply fork以外のサブコマンドの動作や、正本仕様そのものを確認するとき

## hash
- c5898fbe87d9ed0b7cda721952d82bc499b54cf7caae98b8c46d93b35b7421d4
