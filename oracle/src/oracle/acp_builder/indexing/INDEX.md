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
- `cmoc indexing` が対象ファイルまたはディレクトリ向けの INDEX.md エントリー生成 agent call を構築する処理を定義する。対象内容を埋め込んだ prompt、読み取り専用のアクセス設定、最小コストのモデル・推論設定、Structured Output schema、実行 cwd などの起動パラメータをまとめて生成する。

## Read this when
- `cmoc indexing` の INDEX.md エントリー生成で、agent prompt の構成や起動パラメータを変更・確認するとき。
- INDEX entry policy を適用した読み取り専用 agent call の設定、または indexing preflight を無効化する設計を確認するとき。

## Do not read this when
- INDEX.md の既存内容や一般的なルーティング方針だけを確認したいとき。
- INDEX エントリー生成以外の agent call パラメータ構築を調べるときは、該当する各 builder の定義を直接読む。

## hash
- 9808745aec3998fa5feaed251435e21b26df66acea773f182cb1db6e6a6960a8
