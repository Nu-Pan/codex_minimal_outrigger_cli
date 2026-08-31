# `join`

## Summary
- `cmoc session join` の merge conflict marker 解消に使うエージェント呼び出しパラメータを構築する。
- conflict 対象パスを解決して prompt に渡し、専用の conflict resolution policy、書き込み権限、完了条件、起動設定を組み立てる。

## Read this when
- `cmoc session join` の conflict marker 解消で、対象パスの解決や prompt への埋め込み方を確認・変更するとき。
- conflict 解消時のファイルアクセス権限、oracle・realization・routing policy の指定、preflight 無効化、完了条件を確認・変更するとき。

## Do not read this when
- merge conflict marker の具体的な解消処理や対象ファイルの内容を確認したいときは、conflict 対象ファイルを直接読む。
- 通常の `session join` の処理フローや、一般的な prompt 構築・広範な edit/refactor policy の定義だけを確認したいときは、より直接的な対象を読む。

## hash
- 2e61ea38837d55d7b51462967943257eefadbc06397404588c50a6f3983a44bd
