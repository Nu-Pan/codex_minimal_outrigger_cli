# `fork`

## Summary
- `realization apply fork` 用の `codex exec` 起動パラメータと完全 prompt を構築する oracle src。oracle の差分、commit 範囲、linked worktree を realization 追従 agent の prompt に組み込む。

## Read this when
- `realization apply fork` の agent call 起動処理を変更・調査するとき
- oracle diff や linked worktree を realization 追従 prompt に渡す処理を確認するとき
- AgentCallParameter の model、reasoning、file access、indexing 設定を変更するとき

## Do not read this when
- `realization apply fork` 以外の agent call prompt を変更するとき
- prompt の共通生成仕様だけを確認したいとき
- 実際の realization implementation や test の追従内容を調査するとき

## hash
- 4949b02bcbcb9af030190aa535664f9b17ae3a17e3df6d6c031c879d89971903
