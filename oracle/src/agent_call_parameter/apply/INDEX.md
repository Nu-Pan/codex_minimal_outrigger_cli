# `fork`

## Summary

- この `fork` ディレクトリのルーティング文書で、`file_audit_finding.py` と `file_audit_finding.json` への入口です。
- `file_audit_finding.py` は `cmoc apply fork` のファイル単位監査用 agent call parameter を構築し、`file_audit_finding.json` は要修正点一覧の Structured Output schema を定義します。
- 監査対象ファイルを起点に、`oracle file` と `realization file` の差分や致命的問題を洗い出すための目次です。

## Read this when

- `cmoc apply fork` のファイル単位監査 prompt と Structured Output schema の入口をまとめて把握したいとき。
- `file_audit_finding.py` と `file_audit_finding.json` のどちらを先に読むべきか迷ったとき。
- 監査対象ファイルを起点に、`oracle file` と `realization file` の不整合や要修正点を確認したいとき。

## Do not read this when

- `cmoc apply fork` の監査フローではなく、別の `agent_call_parameter` や別サブコマンドの仕様を確認したいとき。
- 対象ファイルがすでに分かっていて、この階層の目次を経由せずに `file_audit_finding.py` または `file_audit_finding.json` を直接開くとき。
- `oracle` 全体の共通規約や、`INDEX.md` の生成方針だけを確認したいとき。

## hash

- bcaf8768bcd06c7c2ca32d4a70cc7d35d2be2f11fb680902be99d2bcbe145661
