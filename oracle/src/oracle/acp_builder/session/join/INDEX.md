# `conflict_resolution.py`

## Summary
- `cmoc session join` における Git merge conflict marker 解消用の agent call パラメータを構築する。対象パスを解決し、conflict 解消専用の prompt、最高品質のモデル・推論設定、リポジトリ書き込み権限などを指定する下位実装への入口。

## Read this when
- `cmoc session join` の conflict marker 解消 prompt や agent call 設定を変更・確認するとき。
- conflict 解消対象ファイルのパス解決、prompt 生成、モデル設定、実行前 indexing 設定を調査するとき。

## Do not read this when
- 通常の merge conflict 解消処理そのものや Git 操作の実装を調査するとき。
- session join と無関係な prompt builder や agent call パラメータを調査するときは、それぞれの直接の実装を読む。

## hash
- dfc44168527415b0ea1cdcc2dd290a6c89090a5fcad5ef8627db3495b085100b
