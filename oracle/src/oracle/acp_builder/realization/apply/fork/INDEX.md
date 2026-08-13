# `launch_exec.py`

## Summary
- `cmoc realization apply fork` 実行時の AgentCallParameter を構築する定義。差分対象の commit 範囲と oracle file の raw git diff を prompt に組み込み、run worktree を作業ディレクトリとして realization file の追従作業を起動する。prompt の構成、アクセスモード、モデル・推論設定、実行前 indexing の指定をまとめた realization apply の起動入口。

## Read this when
- `cmoc realization apply fork` の起動 prompt、対象差分の渡し方、run worktree、または AgentCallParameter の実行設定を変更・確認するとき。
- realization file への oracle file 差分追従処理の agent call 構築箇所を特定するとき。

## Do not read this when
- oracle file の差分追従ロジック自体、realization implementation の内容、または realization test の要件を確認したいとき。
- 一般的な prompt 構築や他の cmoc 実行系の起動パラメータを調べるときは、それぞれの担当対象を直接読む。

## hash
- d2b2ab740f019007b81141f242423bac661d4a897d22af93d78eceecc8467e11
