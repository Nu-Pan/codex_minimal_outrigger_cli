# `fork`

## Summary

- この `fork` ディレクトリのルーティング文書で、`change_summary.*`、`file_audit_finding.*`、`fixing_point_refinement.*`、`fixing_point_application.py` への入口です。
- `change_summary.*` は変更要約、`file_audit_finding.*` はファイル単位監査、`fixing_point_refinement.*` は要修正点リスト改善、`fixing_point_application.py` は要修正点 1 件の実装修正を案内します。
- `fixing_point_application.py` は Structured Output を使わない write-enabled な入口で、他の 3 系統は Structured Output schema を伴う read-only な入口です。

## Read this when

- `cmoc apply fork` 配下で、変更要約・ファイル単位監査・要修正点リスト改善・要修正点 1 件の実装修正のどれへ進むべきか整理したいとき。
- `change_summary.*`、`file_audit_finding.*`、`fixing_point_refinement.*`、`fixing_point_application.py` の役割分担をまとめて把握したいとき。
- このディレクトリの `INDEX.md` を作成・修正する前に、下位ファイルの入口構成を確認したいとき。
- read-only の呼び出しと write-enabled の呼び出しの違いを、この階層で整理したいとき。

## Do not read this when

- すでに読む対象が `change_summary.py`、`change_summary.json`、`file_audit_finding.py`、`file_audit_finding.json`、`fixing_point_refinement.py`、`fixing_point_refinement.json`、`fixing_point_application.py` のいずれかに決まっていて、この目次を経由する必要がないとき。
- `cmoc apply fork` のうち、変更要約、ファイル単位監査、要修正点リスト改善、要修正点 1 件の実装修正のどれか一つだけを直接確認したいとき。
- Structured Output schema そのものではなく、個別の prompt 実装や JSON schema を直接読みたいとき。
- `cmoc review oracle`、`cmoc indexing`、`cmoc session join` など、別系統の agent call parameter を探しているとき。

## hash

- 28222ed6ec12f4a1391ff197118294a069179f23cdc85c2086268b042f2ab690
