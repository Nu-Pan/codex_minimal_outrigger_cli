# `fork`

## Summary

- この `fork` ディレクトリのルーティング文書で、`change_summary.py`、`file_audit_finding.py`、`refine_fixing_point.py`、`consume_fixing_point.py` への入口です。
- `change_summary.py` は `change_summary.json` を参照する変更要約、`file_audit_finding.py` は `finding_list.json` を参照するファイル単位監査、`refine_fixing_point.py` は同じく `finding_list.json` を参照する要修正点リスト改善を案内します。
- `consume_fixing_point.py` は要修正点 1 件を受け取って realization file を修正する write-enabled な入口で、Structured Output は要求しません。

## Read this when

- `cmoc apply fork` 配下で、変更要約・ファイル単位監査・要修正点リスト改善・要修正点 1 件の実装修正のどれへ進むべきか整理したいとき。
- `change_summary.py`、`file_audit_finding.py`、`refine_fixing_point.py`、`consume_fixing_point.py` の役割分担をまとめて把握したいとき。
- read-only の Structured Output 系と write-enabled な実装修正系の違いを、この階層で整理したいとき。
- `file_audit_finding.py` と `refine_fixing_point.py` が共通で参照する `finding_list.json` を含めて、出力先 schema の対応関係を押さえたいとき。

## Do not read this when

- すでに対象が `change_summary.py`、`change_summary.json`、`file_audit_finding.py`、`finding_list.json`、`refine_fixing_point.py`、`consume_fixing_point.py` のいずれかに決まっていて、この目次を経由する必要がないとき。
- `cmoc apply fork` のうち、変更要約、ファイル単位監査、要修正点リスト改善、要修正点 1 件の実装修正のいずれかを単独で確認したいとき。
- Structured Output schema そのものではなく、個別の prompt 実装や JSON schema を直接読みたいとき。
- この階層の役割分担ではなく、個別ファイルの実装や出力例を直接確認したいとき。

## hash

- a4eee3bb53121cabf62527911eb51447393bcedb36d370742fc6894034907e32
