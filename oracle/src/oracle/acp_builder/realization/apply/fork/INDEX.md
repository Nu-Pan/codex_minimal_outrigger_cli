# `launch_exec.py`

## Summary
- 対象は、`cmoc realization apply fork` が差分追従用エージェントを起動するための prompt と AgentCallParameter を構築する入口。指定 commit 範囲、linked worktree、realization 書き込み権限、実行前 indexing を結び付け、oracle file の変更をリポジトリ全体の realization file へ反映する作業を定義する。

## Read this when
- `cmoc realization apply fork` の実装で、差分の始点・終点 commit と run worktree から起動パラメータや完全な作業 prompt を組み立てる経路を確認するとき。
- oracle file の変更を realization file に追従させる agent call の作業範囲、差分取得条件、rename を含む対象判定、完了条件を確認するとき。

## Do not read this when
- `cmoc realization apply fork` の実行処理そのもの、Git 差分取得の実装、または realization の具体的な反映処理を直接調べるとき。
- 一般的な prompt 構築や AgentCallParameter の共通仕様だけを確認したいときは、対応する共通実装を直接読む。

## hash
- 876d609de237c78fee621db6eaff66c92a25dfc2b5c7b820d1010f562adb13c5
