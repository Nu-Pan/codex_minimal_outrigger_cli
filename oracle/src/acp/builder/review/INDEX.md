# `oracles`

## Summary

- この `review/oracles` ディレクトリのルーティング文書で、`enumerate_finding`、`merge_finding`、`validate_finding_advocate`、`validate_finding_challenger`、`judge_finding` の各 prompt と対応 schema への入口です。
- `enumerate_finding` は新規所見列挙、`merge_finding` は所見整理、`validate_finding_advocate` は妥当理由列挙、`validate_finding_challenger` は否定理由列挙、`judge_finding` は採否判定を案内します。
- 各 `.py` は prompt 正本、各 `.json` は対応する Structured Output schema を表します。

## Read this when

- `cmoc review oracle` のレビュー用 oracle 群で、どの prompt 本体や schema に進むべきかを整理したいとき。
- 新規所見列挙、所見マージ、所見が妥当である理由の列挙、所見が妥当ではない理由の列挙、採否判定のどれを使うかを切り分けたいとき。
- 各 `.py` が参照する対応 `.json` の Structured Output schema を確認したいとき。
- レビュー対象 oracle file と関連所見を入力に取る各フローの入口を把握したいとき。

## Do not read this when

- すでに読む対象の `enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py`、または各 `.json` が決まっていて、この階層の目次を経由せず直接開くとき。
- 新規所見列挙・所見マージ・妥当理由列挙・否定理由列挙・採否判定のうち、特定の 1 本だけを確認したいとき。
- `cmoc review oracle` 以外のサブコマンドや、レビュー用 Structured Output schema 以外の仕様を探しているとき。

## hash

- 80408f801d1ae49e96966a02f80e45833661d36d8bdf32c4e6efdb1151413988
