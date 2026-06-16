# `index_entry.py`

## Summary

- `cmoc indexing` と Codex CLI 実行前メンテナンスで使う、`INDEX.md` 目次情報生成用 agent call parameter への入口です。
- `index_entry.py` は目次作成対象 1 件の説明、読むべき条件、読まなくて良い条件を生成する prompt を定義します。
- `index_entry.json` は目次情報生成結果の Structured Output schema を定義します。

## Read this when

- `INDEX.md` の目次情報を生成する Codex CLI 呼び出し仕様を確認したいとき。
- `build_indexing_index_entry_parameter()` が対象パスや対象内容をどう prompt に渡すか確認したいとき。
- 目次情報生成の Structured Output schema を確認したいとき。

## Do not read this when

- `cmoc indexing` の git commit 処理やディレクトリ列挙規則だけを確認したいとき。
- review や apply など、インデクシング以外の agent call parameter を探しているとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `index_entry.json`

## Summary

- `cmoc indexing` の目次情報生成結果を表す Structured Output schema です。
- `summary`、`read_this_when`、`do_not_read_this_when` の 3 項目を要求します。
- ファイル名や hash など機械的に決まる情報は含めず、自然言語のルーティング説明だけを扱います。

## Read this when

- 目次情報生成の JSON 形式を確認したいとき。
- `build_indexing_index_entry_parameter()` の返却 schema path が指す内容を確認したいとき。
- `INDEX.md` へのレンダリング前に Codex CLI 出力として必要な項目を確認したいとき。

## Do not read this when

- 目次情報の markdown レンダリングや hash 算出方法だけを確認したいとき。
- インデクシング以外の Structured Output schema を探しているとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
