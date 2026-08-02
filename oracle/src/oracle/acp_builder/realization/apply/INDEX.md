# `fork`

## Summary
- `cmoc realization apply fork` 向けの codex exec 起動パラメータを構築する実装。oracle file の差分、commit 範囲、linked worktree を prompt に組み込み、realization file への差分追従を FLAGSHIP モデルへ委譲する入口。

## Read this when
- oracle file の変更を realization file へ追従させる AgentCallParameter を構築・変更するとき
- realization apply fork の prompt、作業範囲、差分参照、モデル設定、worktree 設定を確認するとき
- 差分追従の完了条件や realization write の委譲方法を調査するとき

## Do not read this when
- realization apply fork の差分適用ロジックやテストだけを調べるとき
- 一般的な prompt 構築処理を調べるとき
- AgentCallParameter や path context の共通定義を調べるとき

## hash
- 3ce433d3436f0bdbab513ab255c879387e1240ebed7d75aed3f349f086bed814
