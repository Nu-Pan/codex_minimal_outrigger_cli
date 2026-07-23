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
- `cmoc realization apply fork` サブコマンドの実行処理を担う。oracle の差分を基準に realization apply agent を起動し、変更検証・INDEX 更新・commit・joinable 状態への遷移・fork report 保存までを一連の workload として管理する。
- agent 実行失敗や想定外差分などのエラー時には、作業差分の rollback、error state 更新、エラーレポート保存を行う。

## Read this when
- `cmoc realization apply fork` の処理フロー、run state、差分検証、commit、fork report の挙動を確認または変更するとき
- realization apply agent の起動パラメータや、apply run の成功・失敗時処理との連携を調査するとき

## Do not read this when
- realization apply agent の起動パラメータ生成だけを確認する場合は、専用の launch parameter 実装を直接読む
- run の共通ライフサイクルや report 生成の汎用処理だけを確認する場合は、対応する lifecycle・report 実装を直接読む

## hash
- cd332bc5435fa570cdf99cb785668c8970a65bc8e5a7e38a20f431b1d2b490ff
