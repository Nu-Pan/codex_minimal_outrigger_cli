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
- `cmoc indexing` が目次情報を生成する agent 呼び出しの prompt と起動パラメータを構築する定義。対象パスと作業ディレクトリから完全な prompt、読み取り専用設定、構造化出力 schema、preflight 無効化を含む呼び出しパラメータを組み立てる。

## Read this when
- `cmoc indexing` の INDEX.md エントリー生成 agent 呼び出しについて、prompt の規定や起動パラメータの構成を確認・変更するとき。
- indexing 用 agent のパス context、読み取り専用アクセス、構造化出力 schema、preflight 設定の関係を追うとき。

## Do not read this when
- INDEX.md エントリーの出力項目や schema の形式だけを確認したいとき。
- indexing agent が実際に参照する対象本文や、生成された INDEX.md の内容を確認・変更したいとき。

## hash
- 2e9ef09b27305d3ed50a7e1bc9a11f8c8fdd096f88bfc0ca6452da860e805ec9
