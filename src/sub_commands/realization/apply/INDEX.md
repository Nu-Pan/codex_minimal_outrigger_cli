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
- `cmoc realization apply fork` の CLI 実行フローを担当する。apply 差分の始点特定、oracle diff 構築、realization 追従 agent 実行、差分検査・commit、run 状態更新、fork report 保存までを一体で扱う。

## Read this when
- `cmoc realization apply fork` の実行フロー、失敗時の rollback・error state 遷移、想定外差分の検証を変更または調査するとき。

## Do not read this when
- fork 用の launch parameter 生成だけを変更するときは、専用の builder 実装を直接読む。
- run の共通ライフサイクルや report 形式だけを確認するときは、`sub_commands.run.lifecycle` または `sub_commands.run.report` を直接読む。

## hash
- 74233c437ddbe1d9a03da526a7effbb1c8c7bcdf299100ac1d5d5b7b0271a82d
