# `join`

## Summary
- `cmoc session join` の merge conflict marker 解消用エージェント呼び出しパラメータを構築する。
- 対象ファイルを実パスへ解決し、conflict 解消に限定した prompt、リポジトリ書き込み権限、最高品質のモデル・推論設定、preflight 無効化をまとめて返す。

## Read this when
- `session join` の conflict 解消処理で、対象ファイルのパス解決、prompt、アクセス制御、モデル・推論設定、実行パラメータを確認・変更するとき。
- merge conflict marker 解消用エージェントに渡す専用 policy、最高品質設定、preflight 無効化を調べるとき。

## Do not read this when
- conflict 解消処理の実装本体や `session join` コマンドの制御を直接確認したいときは、それぞれの実装対象を読む。
- 一般的な prompt 生成、パス解決、エージェント呼び出し型、構造化文書の仕様だけを調べるときは、対応する共通モジュールを直接読む。

## hash
- 5f67da64986bb7408848d46dc9465414233a535e7530ac0488562954ee51cae6
