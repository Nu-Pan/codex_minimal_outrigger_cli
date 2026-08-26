# `conflict_resolution.py`

## Summary
- session join で発生した merge conflict の解消に必要なエージェント呼び出しパラメータと prompt を構築する定義。競合対象パスを実リポジトリ内の絶対パスへ解決し、conflict marker の解消だけを要求する専用 prompt、最高品質のモデル・推論設定、リポジトリ書き込み権限などをまとめた呼び出し設定を返す。session join の conflict 解消フローから、対象ファイルの指定方法や起動時の policy を確認する入口となる。

## Read this when
- session join の merge conflict 解消処理を実装・変更・レビューするとき
- conflict marker 解消用エージェントの prompt、対象パスの解決、モデル設定、ファイルアクセス権限を確認するとき
- conflict 解消後に余計な差分や仕様変更を避けるための呼び出し条件を確認するとき

## Do not read this when
- 通常の session join の結合処理や conflict 以外のサブコマンドの仕様を確認するとき
- 一般的な prompt 生成や共通のエージェント呼び出し型を調べるときは、まずそれぞれの共通実装を直接読む
- 競合解消対象以外のファイル編集・リファクタリング方針を確認するとき

## hash
- 16a361687c62ecce1d1c4f33a4538448f62b74bcafe513190ba1f9f08c28f76e
