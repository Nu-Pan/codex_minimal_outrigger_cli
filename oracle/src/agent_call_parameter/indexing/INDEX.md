# `index_entry.json`

## Summary

- `INDEX.md` 用の目次情報を表す Structured Output schema である。
- 必要な項目は `summary`、`read_this_when`、`do_not_read_this_when` の 3 つである。
- 機械的な識別情報は含めず、ルーティング説明の自然言語だけを受け付ける。

## Read this when

- `INDEX.md` 用の目次情報を JSON でどう返すか確認したいとき。
- 対象を紹介する要約、読むべき条件、読まなくてよい条件の 3 分類を揃えたいとき。
- `cmoc indexing` の出力 schema を把握して、生成結果の検証をしたいとき。

## Do not read this when

- 目次情報の markdown レンダリング方法や、`INDEX.md` への書き込み手順だけを確認したいとき。
- インデクシング以外の Structured Output schema や別の agent call parameter を探しているとき。
- 出力に含めるべき項目がすでに分かっていて、JSON の形だけを再確認したいとき。

## hash

- 39fab97858c4e81c5ec3ebe8a1c0d3cfcc3d798ffbe3631ddcf5ba639eac9916

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

- a20416e04751eb42b0c412c2bf861746c3527cdc2e78eb01d9738e6e20b991b7
