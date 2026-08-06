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
- `realization apply fork` サブコマンドの実行オーケストレーションを担う実装。apply agent の起動、oracle 差分の構築、変更範囲と agent commit の検査、INDEX 生成を含む処理単位の commit、joinable/error 状態への遷移、fork report 保存までを扱う。realization apply fork の実行フロー、run の公開・回収、差分検査や失敗時 cleanup の挙動を確認するときの入口。

## Read this when
- `cmoc realization apply fork` の実行順序や run state 遷移を調査・変更するとき。
- apply agent の変更許可範囲、agent による commit 検出、INDEX 生成を含む commit 単位を確認するとき。
- fork report、cleanup warning、失敗時の rollback/error state 処理を確認するとき。

## Do not read this when
- realization apply agent 自体のプロンプトや差分適用規則を調べるときは、agent 起動 parameter の実装や対応する正本仕様を直接読む。
- 共通の run lifecycle、process tracking、git 差分操作の一般仕様だけを調べるときは、各共通モジュールを直接読む。
- apply fork と無関係な CLI サブコマンドの挙動を調べるとき。

## hash
- 4d9af47ed66821a0bbce8e1205042c0905e521b36e6270c5683c751421df619b
