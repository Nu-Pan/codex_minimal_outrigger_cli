# `fork`

## Summary

- `cmoc apply fork` のルーティング文書で、変更要約・ファイル単位監査・要修正点リスト改善・要修正点 1 件の実装修正への入口を案内する。
- `change_summary.json` と `change_summary.py` は変更要約、`file_audit_finding.json` と `file_audit_finding.py` はファイル単位監査、`fixing_point_refinement.json` と `fixing_point_refinement.py` は要修正点リスト改善の入口である。
- `fixing_point_application.py` は要修正点 1 件を実際に修正する write-enabled な入口であり、Structured Output schema は使わない。

## Read this when

- `cmoc apply fork` 配下で、どの機能入口や Structured Output schema へ進むべきかを整理したいとき。
- 変更要約、ファイル単位監査、要修正点リスト改善、要修正点 1 件の実装修正の各入口をまとめて確認したいとき。
- `build_apply_fork_change_summary_parameter()`、`build_apply_fork_file_audit_parameter()`、`build_apply_fork_fixing_point_refinement_parameter()`、`build_apply_fork_fixing_point_application_parameter()` の対応関係を把握したいとき。

## Do not read this when

- すでに `cmoc apply fork` の対象が決まっていて、目的の `*.py` や `*.json` を直接開くとき。
- ファイル単位監査、要修正点リスト改善、要修正点 1 件の実装修正、変更要約のうち、読む対象が明確に一つへ絞れているとき。
- `cmoc review oracle` や `cmoc indexing` など、別系統の agent call parameter を探しているとき。

## hash

- 63f93c6596c9b9260bb65513d583e460f4e340a3476e630c1a79fc29be1b486f
