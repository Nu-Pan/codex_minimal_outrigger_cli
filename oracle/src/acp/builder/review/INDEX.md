# `oracle`

## Summary

- この `review/oracle` ディレクトリのルーティング文書で、`enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py` と各対応 `*.json` への入口を案内する。
- `cmoc review oracle` の新規所見列挙、所見整理、妥当理由列挙、否定理由列挙、採否判定の 5 系統を切り分けて示す。
- 各 `*.py` は prompt 正本、各 `*.json` は対応する Structured Output schema を表す。

## Read this when

- `cmoc review oracle` の 5 系統の入口をひとまとめに把握したいとき。
- `enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py` の役割分担を整理したいとき。
- 各 `*.py` が prompt 正本で、各 `*.json` が対応する Structured Output schema である対応関係を確認したいとき。
- 新規所見列挙、所見整理、妥当理由列挙、否定理由列挙、採否判定のどこから読むべきか迷ったとき。

## Do not read this when

- すでに `enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py` のいずれか、または対応する `*.json` を直接確認する対象が決まっているとき。
- `cmoc review oracle` の 5 系統のうち 1 つだけを直接見たいとき。
- `cmoc review oracle` 以外のサブコマンドや、レビュー用 Structured Output schema 以外の仕様を探しているとき。
- 所見の列挙、整理、擁護理由列挙、否定理由列挙、採否判定のいずれにも当てはまらない文書を探しているとき。

## hash

- da391888efa47b3e5ed93fd4c44f5ef7ac12e80550728b003cff6d4e94809b94
