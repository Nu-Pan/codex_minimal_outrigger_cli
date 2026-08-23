# `join`

## Summary
- `cmoc session join` の merge conflict 解消を担当するエージェント呼び出しの定義。対象ファイルの実パス解決、conflict marker 解消に限定した prompt、書き込み権限、モデル・推論設定、preflight 設定を扱う。

## Read this when
- `cmoc session join` の conflict marker 解消処理を変更するとき
- conflict 解消用エージェントの prompt、対象パスの扱い、アクセス権限、モデル設定、preflight 設定を確認するとき

## Do not read this when
- 通常の session join 処理や merge 操作そのものを変更するとき
- 一般的な prompt 生成処理や共通のエージェント呼び出しパラメータを調べるとき

## hash
- 5291075737b2d9608400cde7dcd8ea893f17af62de7435dbc77201646f82b499
