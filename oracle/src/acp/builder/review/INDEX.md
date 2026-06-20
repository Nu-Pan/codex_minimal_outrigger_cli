# `oracle`

## Summary

- この `review/oracle` ディレクトリのルーティング文書で、`enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py` と各対応 `*.json` への入口です。
- `cmoc review oracle` の新規所見列挙、所見整理、妥当理由列挙、否定理由列挙、採否判定の 5 系統を案内します。
- 各 `*.py` は prompt 正本、各 `*.json` は対応する Structured Output schema を表します。

## Read this when

- どの review oracle 系統に進むべきか整理したいとき。
- `cmoc review oracle` の prompt 本体と Structured Output schema の対応を確認したいとき。
- レビュー対象 oracle file と関連所見を入力に取る各フローの入口を把握したいとき。
- 新規所見列挙、所見整理、擁護理由列挙、否定理由列挙、採否判定を切り分けたいとき。

## Do not read this when

- すでに開く対象が `enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py`、または対応する `*.json` に決まっているとき。
- 5 系統のうち 1 つだけを直接確認したいとき。
- `cmoc review oracle` 以外のサブコマンドや、レビュー用 Structured Output schema 以外の仕様を探しているとき。

## hash

- 176365d36c8a0ad68f75cdfae556e0997b26952bb3322feec835f7e49a259361
