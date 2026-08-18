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
- `cmoc indexing` 用の AI エージェント呼び出しパラメータを構築する関数を定義する。対象ファイルやディレクトリの内容を埋め込んだ完全なプロンプトを生成し、Structured Output schema、モデル設定、読み取り専用アクセス、実行 cwd などをまとめて `AgentCallParameter` として返す。

## Read this when
- `cmoc indexing` の目次エントリー生成 agent call のプロンプト、モデル・推論設定、ファイルアクセスモード、Structured Output schema、起動パラメータを変更または確認するとき。

## Do not read this when
- 目次エントリーの出力項目や JSON schema 自体を確認したいときは、同じディレクトリの schema ファイルを直接読む。
- `cmoc indexing` の一般的な実行フローや、プロンプト生成処理そのものを変更したいときは、呼び出し側または `build_complete_prompt` の実装を直接読む。

## hash
- 510fa29ad324f26063d971bade4a3684e3ca9b8d9e4e46d95a54e1646115ea6c
