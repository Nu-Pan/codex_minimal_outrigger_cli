# `fork`

## Summary
- `cmoc realization apply fork` における realization 追従用 AgentCallParameter の構築入口。commit 範囲と oracle file の raw diff を含む完全 prompt、作業用 worktree、アクセス権限、モデル・推論設定、実行前 indexing を定義する。

## Read this when
- realization apply fork の agent call が、どの変更情報を prompt に渡し、どの worktree と実行設定で realization 追従を起動するかを確認・変更するとき。

## Do not read this when
- oracle file の変更内容や realization implementation・test の実装を確認するとき。一般的な prompt 構築や別の実行系の起動設定を調べるとき。

## hash
- 22891687e09e3154e3096c69b80336e30077f279255ebe0a2416d46d08d5807e
