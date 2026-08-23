# `conflict_resolution.py`

## Summary
- `cmoc session join` で発生した merge conflict の解消担当エージェント呼び出しを構築する定義。対象ファイルの実パスを解決し、conflict marker 解消に限定した prompt、リポジトリ書き込み権限、最高品質のモデル・推論設定をまとめる。

## Read this when
- `cmoc session join` の conflict marker 解消処理を変更するとき
- conflict 解消用エージェントの prompt、対象パスの扱い、アクセス権限、モデル設定、preflight 設定を確認するとき

## Do not read this when
- 通常の session join 処理や merge 操作そのものを変更するとき
- 一般的な prompt 生成処理や共通のエージェント呼び出しパラメータを調べるときは、それぞれの共通実装を直接読む

## hash
- 638da5c79b6707285f6d094e92b8ef90a65dadc025f2f81de400d7fa7368e3bd
