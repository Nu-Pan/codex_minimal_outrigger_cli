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
- `cmoc indexing` で、対象ファイルまたはディレクトリの内容から `INDEX.md` 用エントリーを生成するための agent call parameter を組み立てる prompt 正本。
- ルーティング文書作成担当としての role、Structured Output schema に従う goal、readonly の file access mode、既存 `INDEX.md` を読まずオリジナル本文を根拠にする生成規則、対象内容の埋め込みを定義する。
- 生成した complete prompt を markdown 化し、効率重視モデル・低 reasoning・readonly・同名 JSON schema 出力先を持つ agent call parameter として返す。

## Read this when
- `cmoc indexing` のうち、個別対象の `INDEX.md` エントリー生成用 prompt や agent call parameter の内容を確認・変更したいとき。
- エントリー生成時に AI へ渡す role、summary、goal、file access mode、補助 prompt、placeholder、index entry standard の適用有無を確認したいとき。
- 対象がディレクトリの場合に直下の目次内容を対象内容として扱う前提や、生成結果の JSON schema 出力先を確認したいとき。

## Do not read this when
- `cmoc indexing` 全体の CLI 起動、対象探索、ファイル書き込み、既存目次更新処理を調べたいだけのときは、それぞれを担う実装へ進む。
- complete prompt の汎用組み立て規則、構造化 markdown の描画、path placeholder 解決、agent call parameter 型そのものを調べたいときは、それぞれの定義元を読む。
- 人間が守るべき `INDEX.md` エントリー品質基準そのものを確認したいときは、基準を定義する正本仕様を読む。

## hash
- b700d4d32d1442f6c130f4a14239ff09202788fcb071a19e010f5eba0a7e4b3e
