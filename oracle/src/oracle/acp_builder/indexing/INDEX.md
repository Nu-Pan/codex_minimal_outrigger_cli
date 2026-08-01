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
- `cmoc indexing` が生成する INDEX.md エントリー用の agent call パラメータを構築する正本実装。対象パス・内容・cwd から prompt、Structured Output schema、読み取り専用設定、モデル設定を組み立てる。
- prompt の path context 解決、エントリー生成規則、対象本文の埋め込み、indexing preflight 無効化など、目次情報生成呼び出しの設定入口となる。

## Read this when
- `cmoc indexing` の INDEX.md エントリー生成 prompt や agent call 設定を変更・調査するとき
- 対象パスの解決、Structured Output schema の指定、モデル・推論・アクセスモードの設定を確認するとき

## Do not read this when
- INDEX.md の一般的なルーティング規則やエントリー記述方針だけを確認したいとき
- `cmoc indexing` 以外の prompt 構築や agent call パラメータを調査するとき

## hash
- 002ab294bd67ef207783024b63bf6f0b815a73114be63126196da093d25769fd
