# `builder`

## Summary

- この `builder` ディレクトリのルーティング文書で、`apply/`、`indexing/`、`review/`、`session/` への入口をまとめます。
- `apply/` は `cmoc apply fork`、`indexing/` は `cmoc indexing`、`review/` は `cmoc review oracle`、`session/` は `cmoc session join` の入口を案内します。
- この階層では、どのサブコマンド用の agent call parameter を読むべきかを切り分けます。

## Read this when

- `<cmoc-root>/oracle/src/acp/builder` 配下で、まず `apply/`、`indexing/`、`review/`、`session/` のどこから読むべきか整理したいとき。
- `cmoc apply fork`、`cmoc indexing`、`cmoc review oracle`、`cmoc session join` の呼び出し仕様の入口をまとめて把握したいとき。
- この階層の目次を確認してから、下位の `INDEX.md` や個別仕様へ進みたいとき。

## Do not read this when

- すでに進む先が `apply/`、`indexing/`、`review/`、`session/` のいずれかに決まっていて、この階層の入口説明が不要なとき。
- `change_summary.py`、`file_finding_enumeration.py`、`finding_application.py`、`refine_finding.py`、`index_entry.py`、`index_entry.json`、`enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py`、`conflict_resolution.py` など、個別ファイルを直接確認したいとき。
- この階層の案内ではなく、下位の `INDEX.md` や個別仕様だけを確認したいとき。

## hash

- faa9559a2440affdebc30b13de8f419caf466d600f2234dd9ae21f8a1eabbcb2

# `prompt_parts`

## Summary

- この `prompt_parts` ディレクトリのルーティング文書で、`complete_prompt.py` を中心に agent 呼び出し用 prompt を組み立てる断片群への入口をまとめます。
- `oracle_and_realization_basic.py`、`file_access_rule.py`、`oracle_standard.py`、`realization_standard.py` など、prompt に差し込む基本知識と標準文書への入口を切り分けます。
- `oracle_review_standard.py`、`apply_review_standard.py`、`index_entry_standard.py` は、それぞれレビュー観点、所見列挙の規範、INDEX.md エントリー規範を与えます。

## Read this when

- この階層でまずどの prompt 断片を読むべきか整理したいとき。
- 完全な prompt の構成要素や、ファイルアクセス制約・oracle/realization の基本・各種標準をまとめて確認したいとき。
- `INDEX.md` に書くべきルーティング規範を確認したいとき。

## Do not read this when

- すでに `complete_prompt.py` や各標準ファイルへ直接進む対象が決まっていて、この目次を経由する必要がないとき。
- この階層全体ではなく、個別の helper 実装や標準文書本文だけを確認したいとき。
- `oracle` 正本仕様や別階層の案内を探していて、prompt 断片群の入口は不要なとき。

## hash

- 6c2f09844f632935366b8bcb2a2c492968bcac435ef9e94994eae14766c06281
