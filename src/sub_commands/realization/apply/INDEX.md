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
- `cmoc realization apply fork` の CLI 実行本体。apply 差分の始点特定、oracle raw diff 構築、realization 追従 agent 実行、変更検査・commit、run の joinable 更新、fork report 保存までを一連の workload として扱う。

## Read this when
- `cmoc realization apply fork` の処理フロー、agent 実行、差分検査、commit、run 状態遷移、fork report の生成を変更または調査するとき。
- 想定外変更、agent 異常終了、rollback、error state への遷移を確認するとき。

## Do not read this when
- apply fork の launch parameter 構築だけを変更または調査するときは、launch parameter 実装を直接読む。
- run lifecycle の共通処理や report 形式だけを確認するときは、それぞれの共通モジュールを直接読む。
- realization apply fork 以外のサブコマンドの実行フローを調査するとき。

## hash
- a0f734776e45916ca08bcebf56bd3d43d8ead84d874b2ceb4d17dd9197957617
