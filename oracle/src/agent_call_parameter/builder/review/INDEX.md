# `oracles`

## Summary

- この `oracles` ディレクトリのルーティング文書で、`enumerate_finding.py/json`、`merge_finding.py/json`、`validate_finding_advocate.py/json`、`validate_finding_challenger.py/json`、`judge_finding.py/json` への入口です。
- 新規所見の列挙、所見リストの整理、妥当理由の列挙、否定理由の列挙、採否判定の 5 系統を案内します。
- いずれも `cmoc review oracle` の所見処理に使う、読み取り中心の prompt と Structured Output schema の対応をまとめます。

## Read this when

- `cmoc review oracle` の所見処理フロー全体をまとめて把握したいとき。
- 新規所見列挙、所見マージ、擁護理由列挙、否定理由列挙、採否判定のどれを使うべきか迷ったとき。
- `oracles/` 配下の Python 実装と JSON schema の対応関係を確認したいとき。
- 各所見処理が返す JSON 形式や入力前提を確認したいとき。

## Do not read this when

- すでに対象ファイル名が分かっていて、`enumerate_finding.py`、`enumerate_finding.json`、`merge_finding.py`、`merge_finding.json`、`validate_finding_advocate.py`、`validate_finding_advocate.json`、`validate_finding_challenger.py`、`validate_finding_challenger.json`、`judge_finding.py`、`judge_finding.json` を直接開くとき。
- `cmoc review oracle` 以外のサブコマンドの agent call parameter を探しているとき。
- 所見の列挙、統合、擁護理由列挙、否定理由列挙、採否判定のどれか 1 つだけを個別に確認したいとき。
- Structured Output schema ではなく、`review/oracles` 配下の実装コードだけを確認したいとき。

## hash

- c46e8a12d766e3b769b6843bb62d9ff2bfac66d1bd87172260de9661481ff5e1
