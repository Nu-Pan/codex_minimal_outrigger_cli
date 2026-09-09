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
- `cmoc indexing` が対象ファイルまたはディレクトリの本文を根拠に INDEX.md エントリーを生成するための agent 呼び出しパラメータを構築する。
- プロンプト、読み取り専用アクセス、対象パスと cwd の解決、Structured Output schema、indexing preflight 無効化をまとめて定義する。

## Read this when
- `cmoc indexing` の INDEX.md エントリー生成 agent のプロンプト内容や起動パラメータを確認・変更するとき。
- 対象パス、対象本文、agent call の cwd、出力スキーマの受け渡し方を確認するとき。

## Do not read this when
- INDEX.md の既存エントリーやルーティング規則そのものを確認したいとき。
- エントリー生成後の INDEX.md 更新処理や、Structured Output schema の項目定義を直接確認したいとき。

## hash
- 234b06444cd61d87482412559eb2d8601711f26a258c04ea15c7636a8d598c8c
