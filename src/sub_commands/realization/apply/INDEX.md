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
- `cmoc realization apply fork` サブコマンドの実行処理を担当する。realization apply agent を実行し、oracle 差分に基づく変更を検証・commit して joinable run として公開する。失敗時は変更を rollback し、error state と fork report を保存する。

## Read this when
- `cmoc realization apply fork` の実行フロー、run の作成・状態更新、apply agent の起動、差分検証、commit、fork report を調査・変更するとき。
- realization apply run の想定外差分、エラー処理、rollback、joinable/error state の挙動を確認するとき。

## Do not read this when
- realization apply agent の起動パラメータ自体を変更する場合は、起動パラメータ構築モジュールを直接読む。
- run の共通ライフサイクル、状態管理、差分検査の共通実装を変更する場合は、`commons.runtime_run*` の該当モジュールを直接読む。
- `cmoc realization apply fork` 以外のサブコマンドの実行処理だけを調査するとき。

## hash
- 7aa503542a64edfbb4c6d5243a01dabdfa27e7ee68b15eae27b0adec84b53bc7
