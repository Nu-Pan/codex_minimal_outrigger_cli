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
- `cmoc indexing` が生成する agent call 用パラメータを構築する関数を定義する。対象ファイルの内容を埋め込んだ完全 prompt、読み取り専用のパス文脈、Structured Output schema、最小モデル・低推論 effort などの起動設定を組み立てる indexing preflight の実装入口。

## Read this when
- `cmoc indexing` の目次エントリー生成 agent call の prompt、モデル、推論 effort、ファイルアクセス権、cwd、Structured Output schema、preflight 設定を変更・確認するとき。

## Do not read this when
- 目次エントリーの JSON schema 自体の制約を確認するだけの場合は、対応する schema を直接読む。
- indexing 以外の agent call パラメータ構築や、prompt の共通生成規則を確認する場合は、それぞれの担当実装または共通 prompt builder を直接読む。

## hash
- c76b60d8d374bb449415c931bb74e62dda231a33d40313ec627b16e6c644fd78
