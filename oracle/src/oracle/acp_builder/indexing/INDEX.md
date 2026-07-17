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
- `cmoc indexing` の目次情報生成に使う agent 呼び出しパラメータの組み立てを扱う。ここでは、どのモデル設定・権限制御・入力束ね方で indexing 用の呼び出しを作るかを確認する。

## Read this when
- `cmoc indexing` で、目次情報生成用の agent 呼び出しをどう構築しているかを確認したいとき。
- indexing preflight 用の呼び出し条件や、目次情報生成向けの入力の渡し方を確認したいとき。

## Do not read this when
- indexing の実行本体や、生成された目次情報そのものを確認したいときは、より下流の処理を読む。
- prompt 文面の共通組み立てや他のサブコマンド向け呼び出し設定を見たいだけなら、この対象ではなく関連する共通 builder を読む。

## hash
- ab8a1e72f4e4cd9b8b37bbd93cbdd712d05f0e5d2c308ee8cb9f5fb65e6b89f3
