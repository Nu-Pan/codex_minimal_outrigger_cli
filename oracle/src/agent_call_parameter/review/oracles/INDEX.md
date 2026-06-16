# `enumerate_finding.json`

## Summary

- このディレクトリは `cmoc review oracle` 用の Structured Output schema をまとめた目次です。
- `enumerate_finding.json`、`merge_finding.json`、`validate_finding_advocate.json`、`validate_finding_challenger.json`、`judge_finding.json` への入口になります。
- 所見の列挙、集約、検証、判定というレビュー処理の段階ごとに参照先を切り分けるためのルーティング文書です。

## Read this when

- `cmoc review oracle` で使う Structured Output schema の入口をまとめて把握したいとき。
- 所見の列挙、マージ、妥当性検証、採否判定の各段階で、どの JSON schema を使うか確認したいとき。
- レビュー用 schema を追加・修正・レビューする前に、このディレクトリの役割を整理したいとき。

## Do not read this when

- すでに対象の JSON schema 名が分かっていて、この目次を経由せずに `enumerate_finding.json`、`merge_finding.json`、`validate_finding_advocate.json`、`validate_finding_challenger.json`、`judge_finding.json` のいずれかを直接確認するとき。
- `cmoc review oracle` 以外のサブコマンドや、`docs/` 配下の自然言語仕様だけを確認したいとき。
- Structured Output schema の一覧ではなく、個別 schema の内容や修正だけを見たいとき。

## hash

- fb3a61d69e2fd17f7aa95187bbc047f506a87a5b2de70995c4bd66f949401c86

# `judge_finding.json`

## Summary

- `<cmoc-root>/oracle/src/agent_call_parameter/review/oracles/` 配下の Structured Output schema への入口です。
- `enumerate_finding.json`、`merge_finding.json`、`validate_finding_advocate.json`、`validate_finding_challenger.json`、`judge_finding.json` を案内します。
- `cmoc review oracle` における所見の列挙・統合・妥当性検証・採否判定の各段階で使う JSON schema を切り分けるための目次です。

## Read this when

- `cmoc review oracle` 用の Structured Output schema の場所と役割を確認したいとき。
- 所見の列挙、統合、妥当性検証、採否判定のどれを参照すべきか迷ったとき。
- `judge_finding.json` を含む review oracle schema を追加・修正・レビューするとき。

## Do not read this when

- 個別の schema ファイルがすでに分かっていて、`enumerate_finding.json`、`merge_finding.json`、`validate_finding_advocate.json`、`validate_finding_challenger.json`、`judge_finding.json` のいずれかへ直接進めるとき。
- `cmoc review oracle` の実行手順や評価フローだけを確認したいとき。
- Structured Output ではなく、`oracle` 配下の自然言語仕様や開発規約を探しているとき。

## hash

- 082224582304b30326232c20a0ddc1d173467848fd6990d8cd48d5832b9672db

# `merge_finding.json`

## Summary

- `cmoc review oracle` の Structured Output schema をまとめた目次です。
- `enumerate_finding.json`、`merge_finding.json`、`validate_finding_advocate.json`、`validate_finding_challenger.json`、`judge_finding.json` を案内します。
- 所見の列挙・統合・妥当性検証・採否判定の各段階で参照する schema を切り分ける入口です。

## Read this when

- `cmoc review oracle` で使う Structured Output schema の置き場所と役割分担を確認したいとき。
- 所見の列挙、マージ、妥当性検証、採否判定のどの schema を使うか迷ったとき。
- `review_oracle` 用の JSON schema を追加・修正・レビューするとき。

## Do not read this when

- `enumerate_finding.json`、`merge_finding.json`、`validate_finding_advocate.json`、`validate_finding_challenger.json`、`judge_finding.json` のいずれかを既に特定していて、そのファイルを直接確認するとき。
- `cmoc review oracle` の実行手順やレポート形式だけを確認したいとき。
- `oracle` 配下の自然言語仕様や開発規約を探していて、Structured Output schema は不要なとき。

## hash

- f868a37cdad381d03923be50d6124465def9d8bf9a30c5e2b422bc15d6462dd0

# `validate_finding_advocate.json`

## Summary

- このディレクトリは `cmoc review oracle` 向けの Structured Output schema をまとめる入口です。
- `enumerate_finding.json` は新規所見の列挙結果を、`merge_finding.json` は所見マージ操作を定義します。
- `validate_finding_challenger.json` と `validate_finding_advocate.json` は所見の否定・擁護理由を、それぞれ `judge_finding.json` は採用可否の判定を定義します。

## Read this when

- `<cmoc-root>/oracle/src/agent_call_parameter/review/oracles/` 配下の Structured Output schema の役割分担をまとめて把握したいとき。
- `enumerate_finding.json`、`merge_finding.json`、`validate_finding_challenger.json`、`validate_finding_advocate.json`、`judge_finding.json` のどれを読むべきか迷ったとき。
- `cmoc review oracle` の所見列挙・マージ・妥当性検証・採否判定に使う JSON schema の入口を確認したいとき。

## Do not read this when

- `validate_finding_advocate.json` など、対象の Structured Output schema がすでに分かっていて、このディレクトリの目次を経由せず直接開くとき。
- `cmoc review oracle` 以外の `agent_call_parameter` や、レビュー以外の agent 呼び出しパラメータを確認したいとき。
- この階層の個別 schema ではなく、`oracle` 全体の共通ルールや別ディレクトリのルーティングだけを確認したいとき。

## hash

- 13b65613e2180ae59ac57ee18ec599068795bfea9ce54363fbccf4484de3159c

# `validate_finding_challenger.json`

## Summary

- この `oracles/` ディレクトリの目次で、`cmoc review oracle` の所見検証・採否判定で使う agent call parameter 用 schema を案内します。
- `enumerate_finding.json`、`merge_finding.json`、`judge_finding.json`、`validate_finding_advocate.json`、`validate_finding_challenger.json` への入口です。
- レビュー所見の列挙・マージ・妥当性検証・採否判定を、役割ごとにたどるためのハブです。

## Read this when

- review 用 Structured Output schema の置き場所と役割分担を確認したいとき。
- `validate_finding_challenger.json` を含む sibling schema へ進むべきか迷ったとき。
- `cmoc review oracle` の所見検証フローで使う JSON schema 群を追加・修正・レビューしているとき。

## Do not read this when

- 個別の JSON schema がすでに分かっていて、`enumerate_finding.json` や `validate_finding_challenger.json` を直接読むとき。
- `cmoc review oracle` の実行手順や評価フローだけを確認したいとき。
- Structured Output ではなく、`<work-root>/oracle/doc` 配下の自然言語仕様や開発規約を探しているとき。

## hash

- 13b65613e2180ae59ac57ee18ec599068795bfea9ce54363fbccf4484de3159c
