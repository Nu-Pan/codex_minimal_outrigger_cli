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
- `cmoc indexing` が目次エントリー生成用の agent call を構築する処理を扱う。対象本文を埋め込んだ完全 prompt、Structured Output schema、読み取り専用の path context、モデル・推論・実行設定をまとめて `AgentCallParameter` として返すため、indexing agent の起動条件や prompt 構成を変更・確認するときの入口になる。

## Read this when
- `cmoc indexing` の index entry 生成 agent の prompt 文面、対象本文の渡し方、Structured Output schema の指定、または agent call のモデル・推論・アクセス設定を変更・確認するとき。

## Do not read this when
- index entry の出力項目や JSON schema 自体を確認したいときは、直接 schema 対象を読む。
- indexing サブコマンドの実行フローや agent call の実装本体を確認したいときは、呼び出し側または agent 実行処理を直接読む。
- 目次対象ファイルの内容や既存 `INDEX.md` の編集方針だけを確認したいとき。

## hash
- 30e6981d24a8660180d46e030d9f984d240ed2bdaa6b7d85671d04e192153648
