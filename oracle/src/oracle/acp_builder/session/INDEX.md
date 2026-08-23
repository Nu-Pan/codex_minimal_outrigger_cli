# `join`

## Summary
- `cmoc session join` の git merge conflict marker 解消エージェント向け起動パラメータを構築する。対象ファイルの実パス解決、専用 prompt、リポジトリ書き込み権限、作業ディレクトリ、モデル・推論設定をまとめる入口。

## Read this when
- `session join` の conflict marker 解消用 prompt、対象ファイルの prompt への埋め込み、アクセス権限、作業ディレクトリ、モデル・推論設定を確認・変更するとき。

## Do not read this when
- merge conflict marker の解消処理そのものや git 操作を確認するとき。
- 一般的な prompt 構築や通常の agent call パラメータを確認するときは、対応する専用 builder・parameter 定義を直接読む。

## hash
- ca4d883a6afeb7b7a9b22a42963ef8a1093f11fdfdd021a7e794afbd73c10c5a
