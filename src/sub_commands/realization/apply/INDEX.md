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
- `cmoc realization apply fork` サブコマンドの実行本体。realization apply agent を fork run 内で起動し、oracle 差分の構築、agent 変更の検査・commit、run state の joinable/error 更新、fork report 保存、失敗時の rollback と cleanup を担う。

## Read this when
- `cmoc realization apply fork` の実行フロー、run lifecycle、agent 差分の許可範囲、commit 検査、joinable/error 公開処理を確認・変更するとき。
- apply agent の commit 検出、preflight commit の rollback、Codex child process の停止、fork report の生成を調査するとき。

## Do not read this when
- realization apply agent の起動パラメータ自体を変更する場合は、launch parameter builder の実装を直接読む。
- run state、rollback、index refresh、process tracking など共通 lifecycle の仕様や実装を確認する場合は、対応する oracle 文書または commons の実装を直接読む。
- `cmoc realization apply` の別サブコマンドの挙動だけを調査する場合。

## hash
- 10888e087cf6854ecea4cbf63ed399201482b2ad3bfd52a5898812f3063ff3f1
