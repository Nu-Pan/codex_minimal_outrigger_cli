# `enumerate_findings.json`

## Summary

- `<cmoc-root>/oracles/schemas/structured_output/review/oracles/` 配下の Structured Output schema をまとめた目次です。
- `enumerate_findings.json`、`merge_findings.json`、`validate_findings_challenger.json`、`validate_findings_advocate.json`、`judge_findings.json` へ分岐します。
- 所見の列挙・統合・妥当性検証・採否判定の各段階に応じて、読むべき schema を切り分ける入口です。

## Read this when

- `cmoc review oracles` で使う Structured Output schema の役割と使い分けを確認したいとき。
- 所見の列挙・統合・妥当性検証・採否判定のどの payload 仕様を読むべきか迷ったとき。
- schema を追加・修正・レビューしていて、関連する JSON ファイルを素早く確認したいとき。

## Do not read this when

- `cmoc review oracles` の利用手順や評価フローそのものだけを確認したいときは、`<cmoc-root>/oracles/docs/app_specs/sub_commands/review_oracles.md` を読むべきです。
- 実装本体や schema の読み込み処理を確認したいときは、`<cmoc-root>/src/sub_commands/review/oracles.py` を読むべきです。
- この階層ではなく、上位の `structured_output/` や `review/` 全体の目次だけを確認したいときは、このディレクトリを読む必要はありません。

## hash

- fb3a61d69e2fd17f7aa95187bbc047f506a87a5b2de70995c4bd66f949401c86

# `judge_findings.json`

## Summary

- `<cmoc-root>/oracles/schemas/structured_output/review/oracles` にあるレビュー用 Structured Output schema 群の入口です。
- 所見の列挙・マージ・検証・判定で使う schema を、用途ごとにたどるための目次です。
- `judge_findings.json` を含む各 schema は、`cmoc review oracles` の各段階で Codex CLI の出力形式を固定します。

## Read this when

- `cmoc review oracles` で使う Structured Output schema の種類と役割を確認したいとき。
- `enumerate_findings`、`merge_findings`、`validate_findings_advocate`、`validate_findings_challenger`、`judge_findings` のどれを使うか切り分けたいとき。
- レビュー工程ごとの JSON 出力形式を、`oracles/schemas/structured_output/review/oracles` 配下でたどりたいとき。

## Do not read this when

- `cmoc review oracles` 以外の処理や、レビュー報告本文そのものだけを確認したいとき。
- review 以外の Structured Output schema を探しているとき。
- `oracles` 全体のルーティング方針や、別ディレクトリの入口文書だけを確認したいとき。

## hash

- 082224582304b30326232c20a0ddc1d173467848fd6990d8cd48d5832b9672db

# `merge_findings.json`

## Summary

- `cmoc review oracles` の所見リストを重複排除・整合化するための Structured Output schema です。
- `kind` と `target_ids` で、既存所見の削除・置換・統合に必要な操作を表します。
- `finding` には新しい所見本体を入れ、削除だけなら `null` も許可します。

## Read this when

- 所見リストのマージループで、重複や矛盾を解消する操作を Codex CLI に出力させたいとき。
- 既存の所見を統合して代表所見に置き換える、または複数所見を削除する Structured Output を設計・修正したいとき。
- `cmoc review oracles` の merge 処理における入力・出力仕様を確認したいとき。

## Do not read this when

- 新規所見の列挙をしたいときは `enumerate_findings.json` を読むべきです。
- 所見の採否判定をしたいときは `judge_findings.json` を読むべきです。
- 所見の妥当性を支持・反証する理由を出したいときは `validate_findings_*.json` を読むべきです。

## hash

- f868a37cdad381d03923be50d6124465def9d8bf9a30c5e2b422bc15d6462dd0

# `validate_findings_advocate.json`

## Summary

- レビュー用の Structured Output スキーマで、`validate_findings_advocate` の出力形式を定義しています。
- 出力は `reasons` 配列のみで、各要素は理由を表す文字列です。

## Read this when

- `validate_findings_advocate` の入出力形式を確認したいとき。
- advocate 側の検証結果を Structured Output で受け取りたいとき。
- レビュー関連のスキーマ定義をたどりたいとき。

## Do not read this when

- `validate_findings_challenger` や `judge_findings` など別スキーマを確認したいとき。
- findings 本体の内容やレビュー手順だけを確認したいとき。
- JSON Schema の一般仕様や Structured Output の共通ルールだけを知りたいとき。

## hash

- 13b65613e2180ae59ac57ee18ec599068795bfea9ce54363fbccf4484de3159c

# `validate_findings_challenger.json`

## Summary

- `cmoc review oracles` 用の Structured Output schema をまとめた目次です。
- 所見の新規列挙、所見リストのマージ、妥当性検証、採否判定の schema への入口になります。

## Read this when

- `cmoc review oracles` で使う Structured Output schema の置き場所を確認したいとき。
- 所見の列挙・マージ・妥当性検証・採否判定で使う schema をまとめて把握したいとき。
- `enumerate_findings.json`、`merge_findings.json`、`validate_findings_advocate.json`、`validate_findings_challenger.json`、`judge_findings.json` の関係を確認したいとき。

## Do not read this when

- `cmoc review oracles` 以外のサブコマンド仕様や、`docs/` 配下の自然言語仕様を確認したいとき。
- Structured Output schema ではなく、`INDEX.md` の上位ルーティングや開発規約だけを確認したいとき。
- `oracles` 配下の別ディレクトリにある schema や仕様断片を探したいとき。

## hash

- 13b65613e2180ae59ac57ee18ec599068795bfea9ce54363fbccf4484de3159c
