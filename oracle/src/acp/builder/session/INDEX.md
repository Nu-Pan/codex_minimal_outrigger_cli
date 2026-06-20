# `join`

## Summary

- この `join` ディレクトリのルーティング文書で、`conflict_resolution.py` への入口です。
- `conflict_resolution.py` は `cmoc session join` の merge conflict marker 解消用 agent call parameter をまとめます。
- Structured Output を要求しない、ファイル編集を伴う `session join` の呼び出し仕様を案内します。

## Read this when

- `cmoc session join` で conflict が発生したときに、Codex CLI へ何を依頼する仕様か確認したいとき。
- `build_session_join_conflict_resolution_parameter()` が組み立てる prompt と `AgentCallParameters` の所在を確認したいとき。
- conflict 解消時の禁止事項、特に `git add` と `git commit` の禁止を確認したいとき。
- この階層から `conflict_resolution.py` へ進むべきか迷ったとき。

## Do not read this when

- `cmoc session join` 以外の session 状態管理や git 操作だけを確認したいとき。
- すでに目的のファイルが `conflict_resolution.py` だと分かっていて、この目次を経由せず直接開くとき。
- `apply`、`review`、`indexing` など別サブコマンドの agent call parameter を探しているとき。

## hash

- 51eb14ded23a71985441098a20da86d73d213509c631b89034fc0b204e97ed98
