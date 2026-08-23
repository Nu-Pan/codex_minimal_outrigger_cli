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
- `cmoc indexing` が目次エントリー生成用の agent call を起動する際に使う、prompt・パスコンテキスト・実行パラメータの構築定義。
- 対象本文を埋め込んだ完全 prompt を生成し、読み取り専用・最小モデル・低推論コスト・indexing preflight 無効などの設定を返す。
- 同階層の個別構築定義ではなく、`cmoc indexing` のエントリー生成呼び出しの設定や prompt 構成を変更・確認するときの入口。

## Read this when
- `cmoc indexing` の agent 向け prompt 文面を変更するとき
- index entry 生成用 agent call のモデル、推論コスト、アクセスモード、cwd、preflight 設定を確認・変更するとき
- 対象本文やパスコンテキストをどのように完全 prompt に組み込むか調べるとき

## Do not read this when
- `cmoc indexing` の一般的なサブコマンド処理や CLI 引数解析を調べるとき
- Structured Output のスキーマ項目や JSON 形式だけを確認するとき
- indexing 以外の agent call パラメータ構築を直接調べるとき

## hash
- 8890f2a7535b397ef759dd3aa88769713b4c7642b22017379219b657596cf4f2
