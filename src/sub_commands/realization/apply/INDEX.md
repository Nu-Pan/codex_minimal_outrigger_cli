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
- `cmoc realization apply fork` サブコマンドの実行処理を担当する。realization apply agent を起動し、oracle 差分の構築、変更検査、INDEX 更新、commit、run の joinable 化、fork report 保存までを一連の workload として管理する。
- agent 実行失敗や想定外差分などの異常時には、追跡中プロセスの停止、変更の rollback、run の error 化、エラーレポート保存を行う。

## Read this when
- `cmoc realization apply fork` の挙動、run lifecycle、agent 起動、差分検査、commit、joinable/error state、fork report を変更または調査するとき。
- apply fork の失敗時 cleanup、既存 run の回収、想定外変更の扱いを確認するとき。

## Do not read this when
- realization apply の prompt 構築だけを変更または調査するときは、launch parameter builder を直接読む。
- run の join や abandon、共通 lifecycle 処理、report 形式そのものを変更または調査するときは、対応する共通 runtime モジュールや専用仕様を直接読む。

## hash
- 490928d6f1f32f804a7485a884ce503b6aaf30720af223b96bcb30720b8743fc
