# `launch_exec.py`

## Summary
- Oracle の変更を realization file 全体へ反映する `codex exec` 用 AgentCallParameter と完全 prompt を構築する。commit 範囲と oracle の raw git diff を prompt に埋め込み、linked worktree を実行 cwd として realization 追従作業を委譲する。

## Read this when
- realization apply fork の起動 prompt や AgentCallParameter の構築方法を確認するとき
- oracle file の差分を realization implementation・test・ancillary へ反映する agent call の設定を変更するとき

## Do not read this when
- 通常の realization 実装やテストの内容を変更するとき
- oracle file の仕様や一般的な prompt 構築処理を確認するときは、まず対応する oracle file や prompt builder の実装を直接読む

## hash
- 7f875634aa2c257952fb6139d9233765d2bc07a694143986722c9183c525bcde
