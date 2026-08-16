# `join`

## Summary
- `cmoc session join` の Git merge conflict 解消に使う agent call の構築定義。競合パスの実体解決、conflict marker のみを解消するための prompt、アクセス方針、モデル・推論設定、実行コンテキストを確認する入口。

## Read this when
- `cmoc session join` の merge conflict 解消処理における agent call の prompt または起動パラメータを変更・確認するとき
- 競合対象パスの prompt への組み込みや、conflict 解消時のモデル・実行設定を調査するとき

## Do not read this when
- session join の通常の結合処理や、conflict 解消以外の prompt 構築を調べるとき
- 競合解消対象のファイル内容や Git 操作の実装を直接確認したいとき

## hash
- 6e351b69d576e58dfc2be09ce1cc0b47209433e7adf82dc37dc71fd5f7387d2c
