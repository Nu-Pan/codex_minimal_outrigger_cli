# `fork`

## Summary

- この `fork` ディレクトリのルーティング文書で、`change_summary.py`、`file_finding_enumeration.py`、`finding_application.py`、`refine_finding.py` への入口をまとめます。
- `change_summary.py` は変更要約、`file_finding_enumeration.py` はファイル単位の所見列挙、`finding_application.py` は所見 1 件の実装修正、`refine_finding.py` は所見リスト改善を案内します。
- この階層は、`cmoc apply fork` の read-only 系と write-enabled 系の役割分担を切り分ける起点です。

## Read this when

- `<cmoc-root>/oracle/src/acp/builder/apply/fork` 配下で、まずどのファイルから読むべきか整理したいとき。
- `cmoc apply fork` の変更要約、ファイル単位の所見列挙、所見 1 件の実装修正、所見リスト改善という役割分担をまとめて把握したいとき。
- read-only の Structured Output 系と、実装を書き換える write-enabled 系の違いをこの階層で整理したいとき。
- `change_summary.py` と `change_summary.json`、`file_finding_enumeration.py` と `finding_list.json` の対応関係を確認したいとき。

## Do not read this when

- すでに `change_summary.py`、`file_finding_enumeration.py`、`finding_application.py`、`refine_finding.py` のうち読む先が決まっていて、この目次を経由する必要がないとき。
- `cmoc apply fork` のうち、変更要約・所見列挙・所見適用・所見リスト改善のいずれか一つだけを直接確認したいとき。
- `change_summary.json` や `finding_list.json` の Structured Output schema だけを直接確認したいとき。

## hash

- ea05cfbc23201018185e49dde1bbcbe3915cb79faca29c736ee99d43fa0094a2
