# `oracles`

## Summary

- `cmoc review oracle` の所見関連 agent call parameter への入口で、`enumerate_finding.py/json`、`merge_finding.py/json`、`validate_finding_advocate.py/json`、`validate_finding_challenger.py/json`、`judge_finding.py/json` をまとめます。
- 新規所見の列挙、所見リストの統合、擁護理由列挙、否定理由列挙、採否判定の 5 系統を案内します。
- いずれも読み取り専用の oracle file を対象に、Structured Output を返すレビュー用呼び出しです。

## Read this when

- `cmoc review oracle` の prompt と JSON schema の対応をまとめて確認したいとき。
- 新規所見列挙、所見マージ、妥当理由列挙、否定理由列挙、採否判定のどれを使うべきか迷ったとき。
- `oracles/` 配下の Python 実装と Structured Output schema の入口を整理したいとき。
- それぞれの所見処理が返す JSON 形式や入力前提を確認したいとき。

## Do not read this when

- すでに対象ファイル名が分かっていて、`enumerate_finding.py`、`enumerate_finding.json`、`merge_finding.py`、`merge_finding.json`、`validate_finding_advocate.py`、`validate_finding_advocate.json`、`validate_finding_challenger.py`、`validate_finding_challenger.json`、`judge_finding.py`、`judge_finding.json` を直接開くとき。
- `cmoc apply fork`、`cmoc indexing`、`cmoc session join` の agent call parameter を探しているとき。
- レポート生成や run isolation など、Codex CLI 以外の制御処理だけを確認したいとき。
- 特定の 1 つの schema だけを確認したいとき。

## hash

- a1c936593502523f774b0749e8b6480a1431493d2c8979d870d0ed812a3bc683
