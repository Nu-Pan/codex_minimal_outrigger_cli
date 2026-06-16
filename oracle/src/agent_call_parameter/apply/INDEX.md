# `fork`

## Summary

- `cmoc apply fork` のファイル単位監査用 agent call parameter をまとめるディレクトリです。
- `file_audit_finding.py` は監査用の呼び出しパラメータ生成を、`file_audit_finding.json` は要修正点一覧の Structured Output schema を定義します。
- 監査対象ファイルを起点に、`oracle file` と `realization file` の差分や致命的問題を洗い出すための入口です。

## Read this when

- `cmoc apply fork` のファイル単位監査 prompt と Structured Output schema の入口をまとめて把握したいとき。
- `file_audit_finding.py` と `file_audit_finding.json` のどちらを読むべきか迷ったとき。
- 監査対象ファイルを起点に、`oracle file` と `realization file` の不整合や要修正点の確認を行いたいとき。

## Do not read this when

- `cmoc apply fork` 以外のサブコマンドや、別の agent call parameter の仕様を確認したいとき。
- 対象ファイルがすでに分かっていて、このディレクトリの目次を経由せずに `file_audit_finding.py` または `file_audit_finding.json` を直接確認するとき。
- `oracle` 全体の共通ルールや、`INDEX.md` の生成方針だけを確認したいとき。

## hash

- c216bf42e358d89bc62e7e815c2e5609a156b9902a829de65706d51e0f3b22ce
