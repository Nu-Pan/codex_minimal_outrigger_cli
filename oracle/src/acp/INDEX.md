# `builder`

## Summary

- この `builder` ディレクトリのルーティング文書で、`apply/`、`indexing/`、`review/`、`session/` への入口です。
- `apply/` は `cmoc apply fork`、`indexing/` は `cmoc indexing`、`review/` は `cmoc review oracle`、`session/` は `cmoc session join` の入口を案内します。
- この階層では、どのサブコマンド用の agent call parameter を読むべきかを切り分けます。

## Read this when

- `<cmoc-root>/oracle/src/acp/builder` 配下で、まず `apply/`、`indexing/`、`review/`、`session/` のどこから読むべきか整理したいとき。
- `cmoc apply fork`、`cmoc indexing`、`cmoc review oracle`、`cmoc session join` の呼び出し仕様の入口をまとめて把握したいとき。
- この階層の目次を確認してから、下位の `INDEX.md` や個別仕様へ進みたいとき。

## Do not read this when

- すでに進む先が `apply/`、`indexing/`、`review/`、`session/` のいずれかに決まっていて、この階層の入口説明が不要なとき。
- `change_summary.py`、`file_audit_finding.py`、`refine_fixing_point.py`、`consume_fixing_point.py`、`index_entry.py`、`enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py`、`conflict_resolution.py` など、個別ファイルを直接確認したいとき。
- この階層の案内ではなく、下位の `INDEX.md` や個別仕様だけを確認したいとき。

## hash

- 3563271065c2d657c9b3a58a161b7c03358881e5c657f99d0459d0ae88d3bc20

# `prompt_parts`

## Summary

- `<cmoc-root>/oracle/src/acp/prompt_parts/` のルーティング文書で、`complete_prompt.py` を中心に完全な prompt を構成する断片群への入口をまとめます。
- `oracle_and_realization_basic.py`、`file_access_rule.py`、`oracle_standard.py`、`realization_standard.py`、`oracle_review_standard.py`、`apply_review_standard.py`、`index_entry_standard.py` への入口を切り分けます。
- AI 呼び出し用 prompt の組み立て順や、`INDEX.md` エントリーに書くべきルーティング規範を整理するための案内です。

## Read this when

- この階層でまずどの断片から読むべきか整理したいとき。
- 完全な prompt の構成要素や追加条件を把握したいとき。
- `oracle` / `realization` の基本、ファイルアクセス規則、各種標準、`INDEX.md` 規範をまとめて確認したいとき。

## Do not read this when

- すでに `complete_prompt.py` や各標準ファイルへ直接進む対象が決まっていて、この目次を経由する必要がないとき。
- この階層全体ではなく、個別の helper や実装詳細だけを確認したいとき。
- `oracle` 正本仕様や別階層の案内を探しているとき。

## hash

- d08501a7ac6e9ec11d097e0f2c47ab9658e8471f2f5777e493a7010eb343bf93
