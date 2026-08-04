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
- `cmoc realization apply fork` の実行本体。realization apply agent を fork worktree で実行し、oracle 差分に基づく変更を検査・commit して joinable run として公開する。異常時は変更の rollback、error state 更新、fork report 保存までを担う。

## Read this when
- `cmoc realization apply fork` の CLI 動作、run lifecycle、agent 差分の許可範囲、commit・joinable/error 遷移、fork report の生成を確認または変更するとき。

## Do not read this when
- apply agent に渡す launch parameter の内容だけを確認するときは、launch parameter builder を直接読む。
- run の join・abandon 処理や共通 lifecycle の実装を確認するときは、対応する共通 runtime/lifecycle 実装を直接読む。
- realization apply の正本仕様を確認するときは、この実装ではなく oracle の仕様文書を読む。

## hash
- 35192bf98268d902ed56c9eca3fd5c08e6651cb9cfa9f22ffcd9cef48f20f4d0
