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
- `cmoc indexing` が対象ファイルまたはディレクトリの `INDEX.md` 用エントリーを生成するための agent 呼び出しパラメータを構築する。
- 読み取り専用の完全な prompt、対象パス、構造化出力スキーマ、agent の作業ディレクトリを組み立て、indexing preflight を無効にした呼び出し設定を返す。

## Read this when
- `cmoc indexing` の INDEX.md エントリー生成用 agent call の prompt 構成や起動パラメータを確認・変更するとき。
- 対象パスの解決、読み取り専用モード、補助 prompt、構造化出力スキーマ、preflight 設定の関係を追跡するとき。

## Do not read this when
- INDEX.md エントリーの出力項目や構造化出力スキーマ自体を確認したいときは、対応するスキーマ定義を直接読む。
- 一般的な prompt 完成処理や path context の実装を確認したいときは、それぞれの共通実装を直接読む。

## hash
- 1710918437f23582a6330d74bc56eee15fb0ba844cd4554d26c34a3b8a69fecf
