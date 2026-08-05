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
- `cmoc indexing` が対象ファイルまたはディレクトリ向けの INDEX.md エントリー生成 agent call を構築するための正本実装。パスコンテキスト、生成規則、対象本文、出力スキーマを組み合わせた読み取り専用 prompt と、最小モデル・低推論 effort の実行パラメータを定義する。

## Read this when
- `cmoc indexing` の INDEX.md エントリー生成 prompt、agent call パラメータ、Structured Output 設定を変更または調査するとき。

## Do not read this when
- INDEX.md の一般的なルーティング方針や生成結果の内容を確認したいときは、対応する INDEX.md または実際の対象本文を直接読む。
- `cmoc indexing` の実行処理や prompt 全体の共通組み立て規則を調査するときは、関連する indexing 実装または complete prompt builder を読む。

## hash
- fe1519d0ccdd0a35074ca2949b84e67e849ab649934c2bb10c2c0e0922ea0cad
