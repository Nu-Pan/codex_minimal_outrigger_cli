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
- `cmoc realization apply fork` サブコマンドの実行処理を担う。差分の始点特定、oracle diff 構築、realization apply agent の実行、変更検査・commit、run の joinable 更新、fork report 保存までを管理する。

## Read this when
- realization apply fork の実行フロー、run の joinable/error 遷移、agent 差分の検査や commit、fork report の生成を変更・調査するとき。

## Do not read this when
- realization apply の prompt 構築だけを変更・調査するときは、launch parameter builder を直接読む。run の共通ライフサイクルや状態管理だけを変更・調査するときは、commons の runtime lifecycle 実装を直接読む。

## hash
- 0f941f4192fc1c2b88e653e278c54c74be7bac14b5d0e162531892e300b691db
