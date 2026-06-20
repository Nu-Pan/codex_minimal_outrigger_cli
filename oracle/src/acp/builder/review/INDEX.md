# `oracle`

## Summary

- この `review/oracle` ディレクトリのルーティング文書で、`enumerate_finding`、`merge_finding`、`validate_finding_advocate`、`validate_finding_challenger`、`judge_finding` の各 prompt と対応 schema への入口です。
- `enumerate_finding` は新規所見列挙、`merge_finding` は所見整理、`validate_finding_advocate` は妥当理由列挙、`validate_finding_challenger` は否定理由列挙、`judge_finding` は採否判定を案内します。
- 各 `.py` は prompt 正本、各 `.json` は対応する Structured Output schema を表します。

## Read this when

- `cmoc review oracle` のレビュー用 oracle 群で、どの prompt 本体や schema に進むべきかを整理したいとき。
- レビュー対象 oracle file と関連所見を入力に取る各フローの入口を把握したいとき。
- 各 `.py` が参照する対応 `.json` の Structured Output schema を確認したいとき。

## Do not read this when

- すでに `enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py`、または対応する `.json` のどれを開くか決まっていて、この目次を経由する必要がないとき。
- 新規所見列挙・所見マージ・妥当理由列挙・否定理由列挙・採否判定のうち、特定の 1 系統だけを直接確認したいとき。
- `cmoc review oracle` 以外のサブコマンドや、レビュー用 Structured Output schema 以外の仕様を探しているとき。

## hash

- 517debc47300b025f816f1da2867ae3ead456ecd95b3bbeab7eb3244b31c6a67
