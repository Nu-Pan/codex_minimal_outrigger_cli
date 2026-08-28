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
- `cmoc indexing` 用 agent call の prompt と起動パラメータを構築する。
- 対象パスと本文を prompt に埋め込み、読み取り専用のルーティング文書生成を設定する入口である。
- agent call の実行種別、cwd、Structured Output schema、indexing preflight 無効化を含む呼び出し条件を定義する。

## Read this when
- `cmoc indexing` が生成する INDEX.md エントリー用 prompt の内容や構成を変更するとき。
- indexing agent call の読み取り権限、cwd、Structured Output schema、preflight 設定を確認するとき。
- 対象本文を prompt に渡す方法や、パス placeholder の解決方法を確認するとき。

## Do not read this when
- INDEX.md エントリーの出力項目や JSON schema 自体を変更・確認するとき。
- agent call の実行処理や indexing サブコマンドの本体を調査するとき。
- ルーティング文書の内容ではなく、一般的な agent call パラメータの仕様を確認するとき。

## hash
- 87bd07d7912a435030cc1580ba4202f8d0b0d73922b440a9b81f7757ae2044bc
