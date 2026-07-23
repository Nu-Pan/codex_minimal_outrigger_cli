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
- `cmoc realization apply fork` サブコマンドの実行本体。oracle 差分を起点に realization 追従 agent を実行し、変更検査・インデックス更新・commit・joinable 化・fork report 保存までを管理する。異常時は rollback、error state 更新、エラーレポート保存を行う。

## Read this when
- `cmoc realization apply fork` の実行フロー、agent 起動、変更検査、commit、run state、fork report の挙動を確認・変更するとき。

## Do not read this when
- realization apply fork の agent 起動パラメータ生成だけを変更するときは、専用の launch_exec 実装を直接読む。
- run の共通ライフサイクルや report 生成の仕様だけを確認するときは、各共通モジュールを直接読む。

## hash
- 054b895ba3d705b5f0d37395d64911c77188f8824d375e8567be9c5a46c7df99
