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
- `cmoc indexing` で、対象ファイルまたはディレクトリの本文から `INDEX.md` 用エントリーを生成するための AI エージェント呼び出しパラメータを組み立てる正本仕様断片。
- ルーティング文書作成担当としての役割、Structured Output への準拠、既存目次を読まずオリジナル本文を根拠にする制約、対象内容の埋め込み、読み取り専用実行、indexing preflight を再帰させない設定をまとめて定義する。

## Read this when
- `cmoc indexing` の目次情報生成で AI に渡す prompt、role、goal、補助文脈、プレースホルダ、file access mode を確認または変更したいとき。
- INDEX エントリー生成時に、既存目次ではなく対象本文を根拠にする制約や、ディレクトリ対象では直下目次の内容を渡す前提を確認したいとき。
- indexing 用 agent call のモデル種別、reasoning effort、出力 schema、preflight 再帰抑止の扱いを確認したいとき。

## Do not read this when
- 生成された `INDEX.md` エントリーの内容そのものを確認したいだけのとき。
- 通常の agent call prompt 全体の組み立て規則を調べたいときは、complete prompt 側を読む方が直接的。
- パスプレースホルダの意味や実パス解決規則を調べたいときは、path model 側を読む方が直接的。

## hash
- 7a8bf8920c177f8942e106412a6779bd8f0c7ac42e07313c5174f5caa5e3b0da
