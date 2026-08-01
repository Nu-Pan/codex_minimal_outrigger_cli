# `conflict_resolution.py`

## Summary
- `cmoc session join` における merge conflict marker 解消用の AI エージェント呼び出しパラメータを構築する正本ソース。競合対象パスを解決してプロンプトへ組み込み、最高品質・リポジトリ書き込み設定の呼び出しパラメータを返す。

## Read this when
- `cmoc session join` の merge conflict 解消 prompt、競合対象ファイルのパス解決、またはその agent call 設定を変更・確認するとき。

## Do not read this when
- 通常の prompt 生成や `session join` の conflict 解消以外の agent call を扱うときは、対応する prompt builder または session 実装を直接読む。

## hash
- 6610e8cc31e7f10ae10855dcfc41a28703a8b4c01ce85ea519333f5a9d5292bb
