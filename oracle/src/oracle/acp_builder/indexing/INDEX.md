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
- `cmoc indexing` の目次情報生成に使う agent 呼び出しパラメータの組み立てを扱う。ここでは、どのモデル設定・権限制御・入力束ね方で indexing 用の呼び出しを作るかを確認する。

## Read this when
- `cmoc indexing` で、目次情報生成用の agent 呼び出しをどう構築しているかを確認したいとき。
- indexing preflight 用の呼び出し条件や、目次情報生成向けの入力の渡し方を確認したいとき。

## Do not read this when
- indexing の実行本体や、生成された目次情報そのものを確認したいときは、より下流の処理を読む。
- prompt 文面の共通組み立てや他のサブコマンド向け呼び出し設定を見たいだけなら、この対象ではなく関連する共通 builder を読む。

## hash
- ab8a1e72f4e4cd9b8b37bbd93cbdd712d05f0e5d2c308ee8cb9f5fb65e6b89f3
