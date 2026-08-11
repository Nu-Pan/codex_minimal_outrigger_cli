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
- `cmoc indexing` が目次エントリー生成用の agent call を起動するためのパラメータ構築を担当する。対象パスと本文から prompt、構造化出力 schema、cwd、読み取り専用設定などを組み立てる実装であり、indexing 処理の agent 呼び出し定義への入口となる。

## Read this when
- `cmoc indexing` の agent 呼び出しパラメータ、prompt、model・reasoning 設定、構造化出力 schema、または indexing preflight の設定を変更・確認するとき。

## Do not read this when
- 通常の index エントリー内容や INDEX.md のルーティング規則を確認したいときは、対象となる INDEX.md や別の indexing 実装を直接読む。
- agent call の基本型、アクセスモード、モデル設定の定義自体を確認したいときは、参照されている acp_builder の基本定義を読む。

## hash
- 6b7c879d30af3cfe0954165e3a59b0843b78654248bf7804b72ac65436efcdb4
