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
- `cmoc indexing` が対象ファイルまたはディレクトリの INDEX.md エントリー生成を依頼する agent call のパラメータを構築する。
- 完全 prompt に対象パス、読み取り専用アクセス、エントリー生成規定、対象本文を組み込み、Structured Output schema と agent call の cwd を設定する。
- インデックス生成の大量呼び出しを前提に、最小モデル・低推論 effort・preflight 無効など経済性重視の起動設定を定義する。

## Read this when
- `cmoc indexing` の INDEX.md エントリー生成 agent の prompt、モデル設定、アクセスモード、Structured Output 設定を変更・確認するとき。
- indexing preflight の agent call パラメータや agent call cwd の構築経路を追うとき。

## Do not read this when
- INDEX.md の既存ルーティング内容だけを確認したいとき。
- INDEX.md エントリー生成結果の JSON schema 自体を確認したいときは、同じ indexing 用 schema ファイルを直接読む。
- prompt の一般的な組み立て規則を確認したいときは、`build_complete_prompt` などの prompt builder 実装を直接読む。

## hash
- 6a10dbc368f876913fa0b11970d24095d94e6346982b5814eb412dde50e0e1fc
