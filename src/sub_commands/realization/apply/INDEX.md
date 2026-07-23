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
- `cmoc realization apply fork` の差分追従 workload を実行する CLI 実装。realization apply 用の editing run を作成し、oracle 差分を基に agent を実行して変更を検査・commit し、joinable/error 状態と fork report を管理する。

## Read this when
- `cmoc realization apply fork` の実行フロー、agent 起動、realization 差分の検証、commit、rollback、run state または fork report の挙動を変更・調査するとき。

## Do not read this when
- realization apply の agent 起動パラメータ自体を変更する場合は、起動パラメータ構築実装を直接読む。
- run の共通 lifecycle、差分計算、状態管理の共通仕様だけを変更・調査する場合は、対応する lifecycle 実装を直接読む。
- fork report の形式だけを変更・調査する場合は、report 実装を直接読む。

## hash
- 1169f309186a763cd98e98c0cfc72cdd191be360705dfed6f9ca9088c8df50ae
