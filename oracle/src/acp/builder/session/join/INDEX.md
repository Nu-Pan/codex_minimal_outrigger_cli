# `conflict_resolution.py`

## Summary

- `cmoc session join` の merge conflict marker 解消用 agent call parameter の正本です。
- conflict 対象ファイルの marker を解消する prompt と `AgentCallParameters` の入口です。
- この呼び出しはファイル編集を伴い、Structured Output は要求しません。

## Read this when

- `build_session_join_conflict_resolution_parameter()` が組み立てる prompt と `AgentCallParameters` の内容を確認したいとき。
- `cmoc session join` で conflict が発生したときに、Codex CLI へ何を依頼する仕様かを把握したいとき。
- conflict 解消時の禁止事項、特に `git add` と `git commit` の禁止を確認したいとき。

## Do not read this when

- すでに `cmoc session join` の conflict 解消用 prompt 仕様が分かっていて、このファイルを直接確認するとき。
- conflict 後の `git add`、`unmerged path` 検査、merge commit 作成など、cmoc 側の機械的処理だけを確認したいとき。
- `apply`、`review`、`indexing` など別サブコマンドの agent call parameter を探しているとき。

## hash

- a05c30e0a56dac74a563331c7d609ee7b47805a98f3d092b97db479e56a250e6
