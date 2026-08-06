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
- `cmoc indexing` の目次情報生成用 agent call パラメータを構築する実装。対象内容を埋め込んだ完全 prompt、Structured Output schema、読み取り専用アクセス、低コストのモデル・推論設定、agent call の実行コンテキストを定義する。indexing 用 prompt 生成処理の入口。

## Read this when
- `cmoc indexing` の INDEX.md エントリー生成 prompt や agent call 設定を変更・調査するとき
- indexing 用 agent call のモデル、推論強度、ファイルアクセス権限、Structured Output schema の指定元を確認するとき

## Do not read this when
- 実際の INDEX.md 生成処理や indexing サブコマンドの実行フローを調査するとき
- Structured Output schema 自体の定義だけを確認するとき
- 一般的な prompt 構築処理や他の agent call 種別を調査するとき

## hash
- e09159d85f8b3c8cc12186ecac98dc67c859df93fbe389a7a4a47c36b6064b26
