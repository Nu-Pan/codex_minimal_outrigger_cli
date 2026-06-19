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

- `cmoc indexing` の `INDEX.md` 目次情報生成用 prompt 正本で、`index_entry.json` への入口です。
- `build_indexing_index_entry_parameter()` は対象パス・対象内容・兄弟エントリ情報を組み立てて、目次情報生成の呼び出しパラメータを返します。
- `resolve_real_path()` と `build_complete_prompt()`、`render_as_markdown()` を使い、構造化出力付きの呼び出しを構成します。

## Read this when

- `cmoc indexing` の各エントリに対する目次情報をどう生成するか確認したいとき。
- `target_path`、`target_content`、`sibling_entries` を prompt にどう渡すか把握したいとき。
- `index_entry.json` の Structured Output schema と対応を確認したいとき。

## Do not read this when

- `cmoc indexing` のディレクトリ列挙や git commit 処理だけを確認したいとき。
- `index_entry.json` の JSON schema だけを直接確認したいとき。
- 目次生成ではなく、別サブコマンドの agent call parameter を探しているとき。

## hash

- c95e74c4b53fd50116c89a28aca55207fd4ab76a70522acc5cf07d207aadcc4b
