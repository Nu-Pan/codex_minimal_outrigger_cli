# `fork`

## Summary
- `cmoc realization apply fork` 実行時に、oracle の変更を realization file 全体へ反映するための `codex exec` 用 AgentCallParameter を構築する正本コード。prompt、権限、差分、実行用 worktree、モデル設定を組み立てる入口。

## Read this when
- `cmoc realization apply fork` の AgentCallParameter 生成、prompt 構成、oracle 差分の渡し方、実行用 worktree や commit 範囲を変更・検証するとき。

## Do not read this when
- 通常の realization 実装・テストを調査するとき。
- `cmoc realization apply fork` 以外の agent call 起動処理を調査するとき。
- oracle 変更に追従する realization 実装そのものを調査するとき。

## hash
- df0ac058f0b1345005f75f1387a66622bc7d4f7f051302ff227b8bdeaa3e8b0d
