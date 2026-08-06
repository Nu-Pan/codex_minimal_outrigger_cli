# `join`

## Summary
- `cmoc session join` の Git merge conflict marker 解消用 agent call パラメータを構築する実装を含む。対象ファイルの実パス解決、専用 prompt、リポジトリ書き込み権限、最高品質のモデル・推論設定、事前 indexing 無効化をまとめて指定する下位実装への入口。

## Read this when
- `cmoc session join` の conflict marker 解消用 agent call 設定や prompt を変更・確認するとき。
- conflict 対象パスの解決、モデル・推論設定、ファイルアクセス権限、実行前 indexing 設定を調査するとき。

## Do not read this when
- 通常の merge conflict 解消処理や Git 操作そのものを調査するとき。
- `session join` と無関係な prompt builder や agent call パラメータを調査するとき。

## hash
- 012123618a709497734b870766c3f6be0445b1b118c1bca5c660e9771721e744
