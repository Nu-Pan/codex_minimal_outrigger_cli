# `launch_exec.py`

## Summary
- `cmoc realization apply fork` の差分追従用 AgentCallParameter を構築する起動定義。始点・終点 commit と oracle file の raw git diff を prompt に組み込み、指定 worktree、realization 書き込み権限、モデル・推論設定、起動時 indexing を定める。

## Read this when
- oracle file の変更を realization file へ反映する差分追従 Agent の prompt または起動パラメータを確認・変更するとき
- `realization_apply_change` として commit 範囲や oracle file の raw git diff を Agent prompt に渡す処理を調査するとき

## Do not read this when
- 差分追従 Agent の起動定義ではなく、個別の oracle file や realization file の実装内容を直接調査するとき
- AgentCallParameter の共通仕様や prompt の共通生成処理だけを確認する場合は、それぞれの定義元を直接読むとき

## hash
- 84e2a2eba68693d9f57bff0816b1c669a01e4eb320ac7cb4fd1a4ec789dfa54e
