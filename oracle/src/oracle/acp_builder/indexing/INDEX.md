# `index_entry.json`

## Summary
- INDEX.md エントリー生成 agent call の出力形式を定義する JSON Schema。
- 要約、読む条件、読まなくてよい条件を、それぞれ必須の文字列配列として指定する。

## Read this when
- INDEX.md エントリー生成結果の JSON 構造や必須項目を確認するとき。
- 生成結果が指定された出力形式を満たすか確認するとき。

## Do not read this when
- 対象ファイルやディレクトリの実際の責務を調べるとき。
- INDEX.md のルーティング内容やエントリー生成用 prompt の規則を確認するとき。

## hash
- 03e00cc984eeca5067e5dbe49c481a91c135c6aa06a633d90cc5a69c3ad05735

# `index_entry.py`

## Summary
- `cmoc indexing` が INDEX.md エントリー生成を依頼する agent call のパラメータを構築する。対象本文を埋め込んだ prompt、パス文脈、読み取り専用設定、モデル・推論設定、Structured Output schema、実行オプションを定義する。

## Read this when
- `cmoc indexing` の INDEX.md エントリー生成用 agent call の prompt や起動パラメータを確認・変更するとき
- 目次エントリー生成で使用するモデル、推論強度、ファイルアクセスモード、作業ディレクトリ、preflight 設定を確認するとき
- 対象パスの解決や prompt の Markdown 化を含む agent call 構築処理を確認するとき

## Do not read this when
- INDEX.md の既存ルーティング内容を確認したいとき
- 生成結果の出力項目や型を確認したいときは、対応する Structured Output schema を直接読む
- 完全な prompt の共通構築規則を確認したいときは、`complete_prompt` の定義を直接読む

## hash
- 6a10dbc368f876913fa0b11970d24095d94e6346982b5814eb412dde50e0e1fc
