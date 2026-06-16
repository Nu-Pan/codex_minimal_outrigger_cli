# `__init__py`

## Summary

- この `agent_call_parameter` パッケージのルーティング文書で、`base.py`、`prompt_builder/`、`apply/`、`review/` への入口です。
- `base.py` は `AgentCallParameters` などの共通型を定義し、`prompt_builder/` は prompt 組み立て、`apply/` と `review/` はそれぞれ `cmoc apply fork` と `cmoc review oracle` 系の入口をまとめます。
- `__init__py` はこのパッケージの Python モジュール入口として、他モジュールからの参照点になります。

## Read this when

- `AgentCallParameters`、`ModelClass`、`ReasoningEffort` の定義場所を確認したいとき。
- AI エージェント向け prompt の組み立てと、`apply` / `review` のどちらの入口を読むべきか迷ったとき。
- `agent_call_parameter` 配下で共有される呼び出しパラメータや、サブコマンド別の構成をまとめて把握したいとき。
- このパッケージ配下の `INDEX.md` を追加・修正する前に、全体の役割分担を整理したいとき。

## Do not read this when

- すでに `base.py`、`prompt_builder/complete_prompt.py`、`apply/fork/file_audit_finding.py`、`review/oracles/` など目的のファイルが分かっていて、直接開くとき。
- `cmoc apply fork` や `cmoc review oracle` の個別手順だけを確認したいとき。
- このパッケージではなく、`oracle` 全体の自然言語仕様や別系統の Structured Output schema を探しているとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `apply`

## Summary

- `cmoc apply fork` のファイル単位監査用 agent call parameter をまとめるディレクトリです。
- `file_audit_finding.py` は監査用の呼び出しパラメータ生成を、`file_audit_finding.json` は要修正点一覧の Structured Output schema を定義します。
- 監査対象ファイルを起点に、`oracle file` と `realization file` の差分や致命的問題を洗い出すための入口です。

## Read this when

- `cmoc apply fork` のファイル単位監査 prompt と Structured Output schema の入口をまとめて把握したいとき。
- `file_audit_finding.py` と `file_audit_finding.json` のどちらを読むべきか迷ったとき。
- 監査対象ファイルを起点に、`oracle file` と `realization file` の不整合や要修正点の確認を行いたいとき。

## Do not read this when

- `cmoc apply fork` 以外のサブコマンドや、別の agent call parameter の仕様を確認したいとき。
- 対象ファイルがすでに分かっていて、このディレクトリの目次を経由せずに `file_audit_finding.py` または `file_audit_finding.json` を直接確認するとき。
- `oracle` 全体の共通ルールや、`INDEX.md` の生成方針だけを確認したいとき。

## hash

- e03cd2dad9c36a9dd1daf724f3b5b1f4386c457733208a7fb976c03c02328cb9

# `base.py`

## Summary

- `<cmoc-root>/oracle/src/agent_call_parameter/base.py` は、AI コーディングエージェント呼び出し用の基本データ型を定義する入口です。
- `BackendType`、`ModelClass`、`ReasoningEffort`、`AgentCallParameters` をまとめ、バックエンド種別、モデル選択、推論強度、プロンプト本体、Structured Output schema パスを表します。
- `agent_call_parameter` 配下の各サブコマンド実装が共通して参照する、呼び出しパラメータ基盤の目次です。

## Read this when

- `AgentCallParameters` の項目や、`ModelClass` / `ReasoningEffort` の選択肢を確認したいとき。
- Codex CLI などの AI エージェント呼び出しパラメータを追加・変更するとき。
- `apply` / `review` 系の入口から、この共通基盤がどう使われるかをたどりたいとき。

## Do not read this when

- すでに目的のクラス定義が分かっていて、`base.py` を直接確認するとき。
- `prompt_builder` や Structured Output schema の内容だけを確認したいとき。
- この共通基盤ではなく、`apply` や `review` の個別フロー実装を直接追いたいとき。

## hash

- 0af3e724eb65cc3fcdddabeafe5adf5817a4e672c36e5bb62d280407120d3b12

# `prompt_builder`

## Summary

- このディレクトリは、`cmoc` の prompt 生成まわりをまとめたルーティング文書の入口です。
- `complete_prompt.py`、`file_access_rule.py`、`oracle_and_realization_basic.py`、`oracle_standard.py`、`realization_standard.py` を案内します。
- AI エージェントへ渡す完全な prompt の組み立てと、その前提になる規則・標準の所在をたどるための目次です。

## Read this when

- `<cmoc-root>/oracle/src/agent_call_parameter/prompt_builder/` 配下のプロンプト生成全体の入口を把握したいとき。
- `complete_prompt.py` がどの断片を組み合わせて最終的な prompt を作るか確認したいとき。
- ファイルアクセス規則、oracle / realization の基本概念、oracle 標準、realization 標準の役割分担を整理したいとき。
- このディレクトリ配下のルーティング文書を追加・修正する前に、どのファイルへ分岐するか確認したいとき。

## Do not read this when

- `build_complete_prompt()` など、読む対象のファイルがすでに特定できていて、この目次を経由せず直接 `complete_prompt.py`、`file_access_rule.py`、`oracle_and_realization_basic.py`、`oracle_standard.py`、`realization_standard.py` を確認するとき。
- `prompt_builder` 配下のうち、特定の 1 ファイルだけを確認したいとき。
- `<cmoc-root>/oracle/src/agent_call_parameter/` の別ディレクトリや、別フローの agent call parameter を探しているとき。

## hash

- 49d5c6fb1e46aff6daf61d4580fe6934b31257810f55ed39d4dfcf2a771e0cb5

# `review`

## Summary

- `cmoc review oracle` の Structured Output schema 群への入口です。
- `oracles/` を案内し、所見の列挙・統合・妥当性検証・採否判定に使う schema へ分岐します。
- `agent_call_parameter/review` 配下の目次として、レビュー用 schema をたどる起点です。

## Read this when

- `cmoc review oracle` 用の schema 入口をまとめて確認したいとき。
- `oracles/` に進む前に、レビュー用 schema 全体の役割分担を把握したいとき。
- どのレビュー用 JSON schema を開くべきか迷ったとき。

## Do not read this when

- 対象の schema 名がすでに分かっていて、`oracles/INDEX.md` や個別の JSON schema を直接開くとき。
- `cmoc review oracle` の実行手順だけを確認したいとき。
- Structured Output ではなく、`apply/` や `prompt_builder/` など別の agent call parameter を探しているとき。

## hash

- 61570d5602ba15e0dd3353f42b211234768a037f8860e235e7452880f88ebaa1
