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
- realization apply fork の実行経路を担い、oracle 差分の始点を確定して追従 agent を run worktree で実行し、想定外変更・agent commit・遅延 child を検査したうえで差分と生成 INDEX を処理単位として commit する。
- 処理結果を joinable または error の run state と fork report に反映し、cleanup 警告、変更パス、Codex return code、受理済み feedback observation を後続の run join／abandon 判断へ渡す。

## Read this when
- realization の oracle 差分を追従する fork run の開始条件、差分範囲の固定、agent 実行、変更検査、commit、joinable 公開の流れを確認したいとき。
- apply fork の失敗時に preflight／agent commit や未許可変更をどう隔離・rollback し、error report と cleanup warning を保存するか確認したいとき。

## Do not read this when
- 通常の realization apply の agent 指示や仕様そのものを確認したいときは、apply fork の実行管理ではなく対応する realization apply の仕様・launch 定義を直接読む。
- 既存 run の join／abandon 操作や一般的な editing run ライフサイクルだけを調べるときは、この apply 固有の fork 差分追従処理ではなく共通 run ライフサイクルの対象を読む。

## hash
- 3bf4b968b8db9501671e1ec9c2015fba2f3c8ddf1433425df2ea4a2868471ba3
