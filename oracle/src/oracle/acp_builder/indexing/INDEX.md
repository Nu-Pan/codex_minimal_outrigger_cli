# `index_entry.json`

## Summary
- INDEX.md エントリーを生成するための Structured Output schema を定義する。
- 対象本文は、エントリーに含める人間向け要約、読むべき条件、読まなくてよい条件の3要素を必須にし、余分な項目を許可しないことで、ルーティング情報の出力契約を固定する。

## Read this when
- INDEX.md エントリー生成の出力形式を確認したいとき。
- ルーティング文書作成担当が、エントリーに含めるべき情報の単位や必須項目を確認したいとき。
- INDEX.md エントリー生成結果を検証する実装やテストで、期待する JSON 構造を確認したいとき。

## Do not read this when
- 個別のファイルやディレクトリについて、実際にどのような要約や読む条件を書くべきかを判断したいとき。
- INDEX.md のルーティング方針やエントリーの記述品質基準を確認したいとき。
- 対象ファイルの内容理解ではなく、cmoc の実装・テスト・CLI 挙動を確認したいとき。

## hash
- ae0ec45ebc0afcd5c1e83a5a01655b75075b0d0da3ce141b4e0913339ba56494

# `index_entry.py`

## Summary
- `cmoc indexing` サブコマンドで、指定対象の `INDEX.md` 用エントリーを生成するための agent call parameter を組み立てる prompt 正本。対象内容、ファイルアクセスプロファイル、placeholder、index entry standard を含む complete prompt を構築し、効率重視・低 reasoning の呼び出し設定として返す。

## Read this when
- `cmoc indexing` の目次情報生成用 agent call parameter の構築内容を確認したいとき。
- INDEX.md エントリー生成時に AI へ渡す role、summary、goal、補助 prompt、placeholder、file access profile を確認したいとき。
- 目次情報生成対象の本文を prompt に埋め込む方法や、出力 schema 指定ファイルの決め方を確認したいとき。

## Do not read this when
- 一般的な agent call parameter の型や列挙値そのものを確認したいだけの場合。
- complete prompt の汎用的な組み立て処理を確認したい場合。
- path placeholder の解決規則や file access profile の詳細を確認したい場合。

## hash
- 779843e1c7e7f3b495a485dd94662e91392e9dbd1c3452dda76ec260cbd28759
