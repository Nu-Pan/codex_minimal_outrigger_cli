# `oracle`

## Summary
- ACP builder の共通データモデルと、cmoc の各機能が使用する Codex CLI agent call の prompt・起動パラメータ構築を扱う領域です。feedback、indexing、oracle、realization、session、tui、quota probe の呼び出し定義と Structured Output の出力契約を下位要素から確認できます。

## Read this when
- agent call のモデル、推論強度、ファイルアクセスモード、prompt、cwd、Structured Output schema、indexing preflight の共通契約を確認・変更するとき
- feedback、indexing、oracle、realization、session join、tui、quota probe の agent call の prompt や起動条件を調査するとき
- 特定機能の agent call 定義へ進む前に、共通パラメータや列挙型の定義を確認するとき

## Do not read this when
- Codex CLI の実際の実行処理やバックエンドモデル名への変換規則を確認したいとき
- agent call が参照する oracle file、realization file、feedback state、既存 INDEX.md の内容を確認したいとき
- prompt 生成、構造化文書、パス解決、ファイルアクセス policy の共通実装を直接確認すれば足りるとき

## hash
- 1b95990a401c67a9a6194f1fdbd9cf6fce188a7ccef4c0867a3bd983d7bbf33b
