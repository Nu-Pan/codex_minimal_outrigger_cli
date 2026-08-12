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
- `cmoc indexing` の目次情報生成エージェント向けに、完全な prompt と起動パラメータを構築するモジュール。対象本文、パスコンテキスト、構造化出力スキーマ、読み取り専用設定、実行時のモデル・推論設定を組み立てる入口を提供する。

## Read this when
- `cmoc indexing` の agent call が使用する prompt の内容や、目次情報生成用パラメータの設定を確認・変更するとき
- 目次情報生成処理の対象パス、agent call の cwd、構造化出力スキーマ、indexing preflight の実行設定を確認するとき

## Do not read this when
- 目次エントリーの出力形式そのものを確認したいときは、対応する Structured Output schema を直接読む
- `cmoc indexing` の実行フローや、生成後の INDEX.md 更新処理を確認したいときは、サブコマンドの実装を直接読む
- 一般的な agent call パラメータの型やモデル設定の定義を確認したいときは、共通の ACP builder 定義を直接読む

## hash
- 39c3a628f93ec970d6ecb34774d0506ee7be24700f074271ca27ada2d4ceca01
