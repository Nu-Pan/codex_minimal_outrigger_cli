# `conflict_resolution.py`

## Summary

- `cmoc session join` の merge conflict marker 解消用 agent call parameter の正本です。
- `conflict_resolution.py` は conflict 対象ファイルの marker を解消する prompt を定義します。
- この呼び出しはファイル編集を伴い、Structured Output は要求しません。

## Read this when

- `build_session_join_conflict_resolution_parameter()` がどのように prompt と `AgentCallParameters` を組み立てるか確認したいとき。
- `cmoc session join` で conflict 発生時に Codex CLI へ何を依頼するか確認したいとき。
- conflict 解消時の禁止事項、特に git add と git commit の禁止を確認したいとき。

## Do not read this when

- conflict 後に cmoc が実行する git add、unmerged path 検査、merge commit 作成の機械的処理だけを確認したいとき。
- `cmoc session join` 以外のサブコマンドの Codex CLI 呼び出し仕様を探しているとき。
- すでに conflict 解消の prompt 仕様が分かっていて、`conflict_resolution.py` 本体を直接確認するとき。

## hash

- 9ec4e9f7636874141cefe73e8db074c055dc4c70d48338a647ff790ae25373e6
