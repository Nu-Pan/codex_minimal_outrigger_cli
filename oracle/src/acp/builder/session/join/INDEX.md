# `conflict_resolution.py`

## Summary

- この `conflict_resolution.py` のルーティング文書で、`cmoc session join` の merge conflict marker 解消用 agent call parameter への入口です。
- このファイルは conflict 対象ファイルの marker を解消する prompt と `AgentCallParameters` の正本で、Structured Output は要求しません。
- この階層は、`session join` の conflict 解消に必要な禁止事項と入力仕様を確認する起点です。

## Read this when

- `cmoc session join` で conflict が発生し、Codex CLI に何を依頼する仕様か確認したいとき。
- `build_session_join_conflict_resolution_parameter()` が組み立てる prompt と `AgentCallParameters` の内容を確認したいとき。
- conflict 解消時の禁止事項、特に `git add` と `git commit` の禁止を確認したいとき。

## Do not read this when

- すでに `cmoc session join` の conflict 解消用 prompt 仕様が分かっていて、このファイルを直接確認するとき。
- conflict 後の `git add`、`unmerged path` 検査、merge commit 作成など、cmoc 側の機械的処理だけを確認したいとき。
- `apply`、`review`、`indexing` など別サブコマンドの agent call parameter を探しているとき。

## hash

- 178b29ee724b5e7ba01760409af66a822e2463ff42db68de5125061b5a4138ab
