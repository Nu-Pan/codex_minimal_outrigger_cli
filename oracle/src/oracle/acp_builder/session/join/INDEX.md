# `conflict_resolution.py`

## Summary
- `cmoc session join` における git merge conflict marker 解消担当エージェントの起動パラメータを構築する。対象パスを実パスへ解決し、専用 prompt、リポジトリ書き込み権限、作業ディレクトリ、モデル・推論設定をまとめて返す。

## Read this when
- `session join` の conflict 解消処理の prompt 文面やエージェント起動パラメータを変更・確認するとき
- conflicted_paths の解決方法、対象ファイル一覧の prompt への埋め込み、conflict 解消用のアクセス方針を確認するとき

## Do not read this when
- merge conflict 解消ロジックそのものや git 操作の実装を確認するとき
- 一般的な prompt 構築や通常の agent call パラメータを確認するときは、それぞれの専用 builder・parameter 定義を直接読む

## hash
- b5bdddc2984a038b80ee96b550c7a546ca10c9deb079b4aa8a3dc184e5702812
