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
- `cmoc realization apply fork` の CLI 実行処理を担当する。差分始点の特定、oracle diff の構築、realization apply agent の実行、想定外差分の検査、INDEX 更新を含む変更の commit、run state の joinable/error 更新、fork report 保存までの一連の workload を管理する。
- run の開始・追跡・停止・rollback・状態更新などは共通 runtime lifecycle を利用し、失敗時には差分を戻して error report を保存する。realization apply の CLI 実装と run lifecycle の接続を確認するための入口である。

## Read this when
- `cmoc realization apply fork` の動作、例外処理、run state、fork report、差分検査または commit 処理を変更・調査するとき
- realization apply agent の起動条件、oracle diff の渡し方、INDEX 更新を含む処理単位の扱いを確認するとき

## Do not read this when
- Codex builder が生成する launch parameter の内容だけを確認したいときは、対応する builder 実装を直接読む
- run lifecycle の共通仕様や process tracking の共通実装だけを確認したいときは、参照先の共通 runtime モジュールを直接読む
- `realization apply` 以外のサブコマンドの CLI 実装を調査するとき

## hash
- 1f32258d5e27e474668a838a600e2514e30810c5f57d5eda1d845a5e4654f413
