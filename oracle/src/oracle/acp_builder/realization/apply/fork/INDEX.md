# `launch_exec.py`

## Summary
- `cmoc realization apply fork` 用の `codex exec` 起動パラメータと完全 prompt を構築する oracle src。oracle の差分、commit 範囲、linked worktree を prompt に組み込み、realization 追従 agent の責務・完了条件・アクセス範囲を定義する。

## Read this when
- `realization apply fork` の agent call 起動処理を変更・調査するとき
- oracle diff や linked worktree を realization 追従 prompt に渡す処理を確認するとき
- AgentCallParameter の model、reasoning、file access、indexing 設定を変更するとき

## Do not read this when
- `realization apply fork` 以外の agent call prompt を変更するとき
- prompt の共通生成仕様だけを確認したいときは、まず `complete_prompt` の実装を読むとき
- 実際の realization implementation や test の追従内容を調査するとき

## hash
- fed553de0b9b837d52b9d5e1fc00a9bb98a10cca33ca1d225113897f3d66593a
