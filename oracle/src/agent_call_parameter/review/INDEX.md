# `oracles`

## Summary

- このディレクトリは `cmoc review oracle` 向けの Structured Output schema 群の入口です。
- `enumerate_finding.json`、`merge_finding.json`、`validate_finding_advocate.json`、`validate_finding_challenger.json`、`judge_finding.json` を案内します。
- 所見の列挙、統合、擁護、反証、採否判定の流れをたどるためのルーティング文書です。

## Read this when

- `cmoc review oracle` で使う JSON schema の一覧と役割を整理したいとき。
- 所見の列挙・統合・妥当性検証・採否判定のどの schema を読むべきか迷ったとき。
- このディレクトリ配下の schema を追加・修正・レビューする前に入口を確認したいとき。

## Do not read this when

- すでに対象の schema 名が分かっていて、`enumerate_finding.json` などを直接開くとき。
- `cmoc review oracle` の実行手順だけを確認したいとき。
- Structured Output ではなく、`oracle` 配下の自然言語仕様や別種のパラメータ定義を探しているとき。

## hash

- f371678c2aaf1ff6ccfa0066a68e841341a90b7eae888945e55ed5142a099abe
