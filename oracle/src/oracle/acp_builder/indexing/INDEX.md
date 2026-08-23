# `index_entry.json`

## Summary
- INDEX.md エントリーの出力形式を定義する JSON Schema。要約、読む条件、読まなくてよい条件を必須の配列として指定する。

## Read this when
- INDEX.md エントリーの構造や必須項目を確認するとき
- エントリー生成結果の JSON 形式を検証するとき

## Do not read this when
- 対象ファイルやディレクトリの実際の責務を調べるとき
- INDEX.md のルーティング内容そのものを判断するとき

## hash
- c3c1774e0701b503e36d145179eae32bee846e2ba685e8052d82c1fa177bfaff

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
