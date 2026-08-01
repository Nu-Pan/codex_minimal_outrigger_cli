# `conflict_resolution.py`

## Summary
- `cmoc session join` で発生した merge conflict marker を解消する AI エージェント呼び出しパラメータの正本実装。対象パスを解決し、競合解消用 prompt、リポジトリ書き込み権限、最高品質のモデル設定、実行 cwd などを組み立てる。

## Read this when
- `cmoc session join` の merge conflict 解消処理を変更・調査するとき
- 競合解消用 prompt の内容、対象ファイル指定、agent call のモデル・権限・実行設定を確認するとき

## Do not read this when
- 通常の `session join` 処理や merge 操作そのものを調査するとき
- 一般的な prompt 生成処理や共通の agent call パラメータ定義を確認するときは、まずそれぞれの実装元を直接読む

## hash
- 9460bd3db98112c6933beed25d59278c5042fe00760fc656b83b2bcd3ac9c8f7
