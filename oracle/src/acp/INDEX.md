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

- `<cmoc-root>/oracle/src/acp/prompt_parts/` のルーティング文書で、`complete_prompt.py` を中心に `oracle` / `realization` の基本説明、標準、レビュー標準、ファイルアクセス規則、`INDEX.md` エントリー規範への入口をまとめます。
- この階層は、`apply_review_standard.py`、`complete_prompt.py`、`file_access_rule.py`、`index_entry_standard.py`、`oracle_and_realization_basic.py`、`oracle_review_standard.py`、`oracle_standard.py`、`realization_standard.py` への入口を切り分ける起点です。
- AI 呼び出し用 prompt の組み立て順と、`INDEX.md` に書くべき目次項目の方針を整理するための案内です。

## Read this when

- この階層のどの断片から読むべきかを整理したいとき。
- 完全な prompt の構成要素と追加条件を把握したいとき。
- `oracle` / `realization` の基本概念、標準方針、レビュー標準、ファイルアクセス規則、`INDEX.md` 規範を確認したいとき。

## Do not read this when

- すでに `complete_prompt.py` や各標準ファイルへ直接進む対象が決まっているとき。
- この階層全体ではなく、`oracle` 正本仕様や別階層の案内だけを探しているとき。
- `INDEX.md` の生成ルールではなく、個別の helper や実装詳細だけを確認したいとき。

## hash

- 94f2e9190a90b3e3910c9ed5feb107de55d8ba734b0c7681f53e74656e4953e2
