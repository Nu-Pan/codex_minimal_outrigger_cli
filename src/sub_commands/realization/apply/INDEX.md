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
- `realization apply fork` の CLI 実行本体。editing run を開始し、oracle 差分を基に realization apply agent を実行して変更を検査・commitし、joinable または error 状態と fork report を生成する。apply fork の実行フロー、差分制御、失敗時の回収処理を確認する入口。

## Read this when
- `cmoc realization apply fork` の実行フロー、run state 遷移、fork report、agent の変更検査や commit 防止を調査・変更するとき。
- realization apply の成功時または失敗時に、差分 rollback、cleanup、joinable 公開の挙動を確認するとき。

## Do not read this when
- realization apply agent のプロンプト生成や launch parameter の内容だけを確認したいときは、専用の builder 実装を直接読む。
- editing run 全般の状態管理や共通 rollback の仕様・実装だけを確認したいときは、共通 runtime lifecycle または対応する正本仕様を直接読む。

## hash
- 32672a3d0eba873cf76ce7ff78f2247b6dc0767d89c3bfa16b579b96493ae22b
