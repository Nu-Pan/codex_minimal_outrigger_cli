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
- `cmoc realization apply fork` の実行本体として、差分始点を解決し、realization 追従 agent を tracked run 内で実行して差分を検査・commit し、joinable または error の run と fork report を公開する入口。

## Read this when
- realization apply の fork 実行フロー、agent の差分境界・commit 検査、INDEX 生成を含む処理単位、run state や fork report の公開動作を確認するとき。

## Do not read this when
- realization apply の launch parameter の組み立てだけを確認したいときは `launch_exec` 側を直接読む。
- run の join・abandon、一般的な editing run lifecycle、または report の共通実装だけを確認したいときは、それぞれの専用実装を直接読む。

## hash
- eb5f1df093651cc12c42ad80c06dbfe67bbf230af8893a7f4a22e8f4ed317970
