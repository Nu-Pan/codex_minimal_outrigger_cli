# `join`

## Summary
- `cmoc session join` で検出された git merge conflict を解消するエージェント呼び出しの構築定義。conflict 対象の実体パス、解消用 prompt、リポジトリ書き込み権限、作業ディレクトリ、モデル・推論設定をまとめる。conflict 解消呼び出しの設定を確認・変更する際の入口となる。

## Read this when
- `cmoc session join` の conflict marker 解消処理を変更するとき
- conflict 対象パスの解決、解消用 prompt、エージェントの権限・作業ディレクトリ・モデル設定を確認するとき

## Do not read this when
- 通常の session join のマージ処理や conflict 検出を確認するとき
- 一般的なエージェント呼び出しパラメータや共通 prompt 構築を確認するとき
- conflict 対象ファイルの内容や仕様を確認するとき

## hash
- 8e25e44c0cb4c05b48e29209c862dae396aca9af82c8ab023a195d5feda1b328
