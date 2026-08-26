# `join`

## Summary
- session join の merge conflict 解消に使うエージェント呼び出し設定と専用 prompt を定義するファイル。競合対象パスの絶対パス解決、conflict marker の解消のみを求める方針、モデル・推論設定、リポジトリ書き込み権限を確認する入口。

## Read this when
- session join の merge conflict 解消処理を実装・変更・レビューするとき
- conflict 解消用エージェントの prompt、対象パス解決、モデル設定、ファイル権限を確認するとき
- conflict 解消時に余計な差分や仕様変更を避ける呼び出し条件を確認するとき

## Do not read this when
- 通常の session join の結合処理や conflict 以外のサブコマンドを確認するとき
- 一般的な prompt 生成や共通のエージェント呼び出し型を確認するとき
- 競合解消対象以外のファイル編集・リファクタリング方針を確認するとき

## hash
- a9737a6c2dc6c359d96a4b97a87bedf774a736724daba86c147c82a3bc4c00b7
