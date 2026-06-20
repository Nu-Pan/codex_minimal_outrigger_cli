# `builder`

## Summary

- この `builder` ディレクトリのルーティング文書で、`apply/`、`indexing/`、`review/`、`session/` への入口です。
- `apply/` は `cmoc apply fork` の変更要約・ファイル監査・要修正点改善・実装修正を、`indexing/` は `INDEX.md` 目次生成を、`review/` は `cmoc review oracle` の所見処理を、`session/` は `cmoc session join` の conflict 解消を案内します。
- この階層では、どのサブコマンド用の agent call parameter を読むべきかを切り分けます。

## Read this when

- `builder` 配下で、`apply`、`indexing`、`review`、`session` のどれから読むべきか整理したいとき。
- `cmoc apply fork`、`cmoc indexing`、`cmoc review oracle`、`cmoc session join` の呼び出し仕様の入口をまとめて把握したいとき。
- この階層の目次を確認してから、下位の `INDEX.md` や個別ファイルへ進みたいとき。

## Do not read this when

- すでに読む対象が `apply/`、`indexing/`、`review/`、`session/` のいずれかに決まっていて、この階層の目次を経由する必要がないとき。
- `change_summary.py`、`index_entry.py`、`enumerate_finding.py`、`conflict_resolution.py` などの個別ファイルを直接確認したいとき。
- この階層の案内ではなく、下位の `INDEX.md` や各個別仕様だけを確認したいとき。

## hash

- 7790185fcc9878717e8da25d5fdbeba40cc3ccdd5a16f9ccabeb3bde7dad8c03

# `prompt_parts`

## Summary

- この `prompt_parts` ディレクトリのルーティング文書で、`complete_prompt.py` を中心に prompt 断片の組み立てと各標準・規則の入口を案内する。
- `file_access_rule.py`、`oracle_and_realization_basic.py`、`oracle_standard.py`、`realization_standard.py`、`oracle_review_standard.py`、`apply_review_standard.py` を束ね、AI 呼び出し用 prompt に入る要素の役割分担を示す。
- 完全な prompt の構成、ファイル読み書き規則、`oracle` / `realization` の前提、標準、レビュー観点を確認するための目次である。

## Read this when

- `build_complete_prompt()` がどの prompt 断片をどの順序で結合するか確認したいとき。
- ファイル読み書き規則、`oracle` / `realization` の基本定義、`oracle` 標準、`realization` 標準、レビュー観点をまとめて把握したいとき。
- Structured Output schema を伴う prompt の末尾に何が追加されるか、または prompt 断片を追加・整理する前にこのディレクトリ全体の役割を押さえたいとき。

## Do not read this when

- すでに `complete_prompt.py`、`file_access_rule.py`、`oracle_and_realization_basic.py`、`oracle_standard.py`、`realization_standard.py`、`oracle_review_standard.py`、`apply_review_standard.py` のうち読む対象が決まっていて、この目次を経由する必要がないとき。
- `agent call parameter` 全体や `builder/` 側の仕様を探していて、この `prompt_parts/` 階層の案内が不要なとき。
- `oracle` の正本仕様や開発規約だけを確認したいときで、この prompt 断片の入口が不要なとき。

## hash

- 8e3f4873cff9f73924d58988600dee86119999e31955f166089c0965f9a31015
