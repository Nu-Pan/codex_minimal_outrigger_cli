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
- `cmoc realization apply fork` の実行本体。realization apply agent を追従用 run として起動し、差分・生成 INDEX・予期しない変更・agent の commit を検査して処理単位へ確定する。成功時は joinable state と fork report を保存し、失敗時は差分や preflight commit を整理して error state と report を保存する。

## Read this when
- realization apply fork の run 作成、oracle 差分範囲の確定、agent 実行、差分検査、commit、joinable 公開の挙動を確認するとき
- apply agent の commit 検出、遅延 Codex child の停止、preflight commit の rollback、cleanup warning の扱いを調査するとき
- realization apply fork report の成功・失敗時フィールド、accepted feedback observation、次アクションを確認するとき

## Do not read this when
- realization apply fork の agent 起動パラメータそのものを確認したいときは、launch parameter builder の実装を直接読む
- editing run の共通ライフサイクル、state 管理、rollback、index refresh の仕様や実装を確認したいときは、それぞれの共通 runtime または正本仕様を直接読む
- apply agent が実際に行う realization 差分の内容や追従ルールを確認したいときは、agent 用の指示文または realization apply の仕様を直接読む

## hash
- b30fec108c8bd6f48140f19d19c20336cb753eaf6e803fa9511b0df74ca87c3a
