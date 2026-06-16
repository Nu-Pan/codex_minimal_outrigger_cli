# `conflict_resolution.py`

## Summary

- `cmoc session join` の merge conflict marker 解消用 agent call parameter への入口です。
- `conflict_resolution.py` は conflict 対象ファイルに残った marker を解消する作業 prompt を定義します。
- この呼び出しはファイル編集を伴い、Structured Output は要求しません。

## Read this when

- `cmoc session join` が conflict 発生時に Codex CLI へ何を依頼するか確認したいとき。
- conflict 解消時の禁止事項、特に git add と git commit の禁止を確認したいとき。
- oracle file の conflict 解消例外規則を prompt 側でどう扱うか確認したいとき。

## Do not read this when

- conflict 後に cmoc が実行する git add、unmerged path 検査、merge commit 作成の機械的処理だけを確認したいとき。
- session join 以外のサブコマンドの Codex CLI 呼び出し仕様を探しているとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
