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
- `cmoc realization apply fork` の差分追従処理を実装する CLI モジュール。realization apply agent を実行し、oracle 差分に基づく変更と INDEX 更新を検査・commit して joinable run として公開する。失敗時は子プロセス停止、変更 rollback、error state 更新、fork report 保存まで行う。

## Read this when
- `cmoc realization apply fork` の実行フロー、run の joinable/error 遷移、apply agent の差分検査・commit・rollback を変更または調査するとき。
- fork report、想定外差分、開始途中の run 回収、Codex 子プロセス追跡の挙動を確認するとき。

## Do not read this when
- 通常の realization apply agent の prompt 構築だけを変更するときは、launch parameter builder を直接読む。
- run の共通ライフサイクルや状態管理自体を変更するときは、runtime_run_lifecycle の実装・正本仕様を直接読む。

## hash
- a0b27674190850f2882e9ebdf4e84f773670ecf1d7349f019f73eb4cad2bf90f
