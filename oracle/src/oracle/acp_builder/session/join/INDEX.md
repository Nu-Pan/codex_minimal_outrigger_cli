# `conflict_resolution.py`

## Summary
- `cmoc session join` における merge conflict marker 解消用のエージェント呼び出しパラメータを構築する定義。対象パスを実パスへ解決し、conflict 解消に限定した prompt、最高品質のモデル・推論設定、リポジトリ書き込み権限などをまとめて返す。

## Read this when
- `session join` の conflict 解消処理で、対象ファイル、prompt、アクセス制御、モデル設定、実行パラメータの構築を確認・変更するとき。
- merge conflict marker 解消用エージェント呼び出しの起動条件や preflight 無効化の設定を調べるとき。

## Do not read this when
- conflict 解消処理の実装本体や `session join` のコマンド制御を直接確認したいときは、それぞれの実装対象を読む。
- 一般的な prompt 生成規則、パス解決、エージェント呼び出し型、構造化文書の仕様だけを調べるときは、対応する共通モジュールを直接読む。

## hash
- 20562b78f1fd1f4559e019ccfe81bf61df51f97c9ff9741654c076fe2c9c6552
