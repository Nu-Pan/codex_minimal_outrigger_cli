# `conflict_resolution.py`

## Summary

- `cmoc session join` の merge conflict marker 解消用 agent call parameter の正本です。
- `conflict_resolution.py` は conflict 対象ファイルの marker を解消する prompt を定義します。
- この呼び出しはファイル編集を伴い、Structured Output は要求しません。

## Read this when

- `build_session_join_conflict_resolution_parameter()` が組み立てる prompt と `AgentCallParameters` の内容を確認したいとき。
- `cmoc session join` で conflict が発生したときに、Codex CLI へ何を依頼する仕様かを把握したいとき。
- conflict 解消時の禁止事項、特に `git add` と `git commit` の禁止を確認したいとき。

## Do not read this when

- すでに `cmoc session join` の conflict 解消用 prompt 仕様が分かっていて、`conflict_resolution.py` を直接確認するとき。
- conflict 後の `git add`、unmerged path 検査、merge commit 作成など、cmoc 側の機械的処理だけを確認したいとき。
- `apply`、`review`、`indexing` など別サブコマンドの agent call parameter を探しているとき。

## hash

- 29316e8edb7222ab34cdc4ad070e6ffe3ffe87f99e64621ba852d535796bf84c
