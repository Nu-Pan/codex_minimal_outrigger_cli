# `__init__py`

## Summary

- この `agent_call_parameter` パッケージのルーティング文書で、`base.py`、`prompt_builder/`、`apply/`、`review/`、`indexing/`、`session/` への入口です。
- `base.py` は `AgentCallParameters` などの共通型を定義し、`prompt_builder/` は prompt 組み立て、`apply/`、`review/`、`indexing/`、`session/` は各サブコマンドで発生する Codex CLI 呼び出し仕様をまとめます。
- `__init__py` はこのパッケージの Python モジュール入口として、他モジュールからの参照点になります。

## Read this when

- `AgentCallParameters`、`ModelClass`、`ReasoningEffort` の定義場所を確認したいとき。
- AI エージェント向け prompt の組み立てと、`apply` / `review` / `indexing` / `session` のどの入口を読むべきか迷ったとき。
- `agent_call_parameter` 配下で共有される呼び出しパラメータや、サブコマンド別の構成をまとめて把握したいとき。
- このパッケージ配下の `INDEX.md` を追加・修正する前に、全体の役割分担を整理したいとき。

## Do not read this when

- すでに `base.py`、`prompt_builder/complete_prompt.py`、`apply/fork/file_audit_finding.py`、`review/oracles/` など目的のファイルが分かっていて、直接開くとき。
- `cmoc apply fork`、`cmoc review oracle`、`cmoc indexing`、`cmoc session join` の個別手順だけを確認したいとき。
- このパッケージではなく、`oracle` 全体の自然言語仕様や別系統の Structured Output schema を探しているとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `apply`

## Summary

- この `apply` ディレクトリのルーティング文書で、`fork/` への入口です。
- `fork/` は `cmoc apply fork` のファイル単位監査用 agent call parameter をまとめ、`file_audit_finding.py` と `file_audit_finding.json` を案内します。
- 監査対象ファイルを起点に、`oracle file` と `realization file` の差分や致命的問題を調べるための目次です。

## Read this when

- `cmoc apply fork` のファイル単位監査 prompt と Structured Output schema の入口をまとめて把握したいとき。
- `fork/INDEX.md` か `file_audit_finding.py` / `file_audit_finding.json` のどちらを読むべきか迷ったとき。
- 監査対象ファイルを起点に、`oracle file` と `realization file` の不整合や要修正点を確認したいとき。
- この階層の `INDEX.md` を追加・修正する前に、下位ファイルへの分岐を確認したいとき。

## Do not read this when

- `cmoc apply fork` 以外のサブコマンドや、別の agent call parameter を探しているとき。
- 対象ファイルがすでに分かっていて、`fork/INDEX.md` や `file_audit_finding.py` / `file_audit_finding.json` を直接開くとき。
- `oracle` 全体の共通ルールや、`INDEX.md` の生成方針だけを確認したいとき。

## hash

- 0e14b9610d06bb13f5edc11b5367e29eb11afe7f1c8d4c73a3f3e5fe48f49b15

# `base.py`

## Summary

- `<cmoc-root>/oracle/src/agent_call_parameter/base.py` は、AI コーディングエージェント呼び出し用の基本データ型をまとめる入口です。
- `BackendType`、`ModelClass`、`ReasoningEffort`、`AgentCallParameters` を案内し、バックエンド種別、モデル選択、推論強度、プロンプト本文、Structured Output schema パスの所在を示します。
- `agent_call_parameter` 配下の各サブコマンド実装が共通して参照する、呼び出しパラメータ基盤の目次です。

## Read this when

- `<cmoc-root>/oracle/src/agent_call_parameter/base.py` にある共通の呼び出しパラメータ定義を確認したいとき。
- `AgentCallParameters` の項目や、`ModelClass` / `ReasoningEffort` の選択肢を把握したいとき。
- AI エージェント呼び出しの共通基盤が `apply/` や `review/` からどう使われるかをたどりたいとき。

## Do not read this when

- すでに `AgentCallParameters`、`ModelClass`、`ReasoningEffort` の定義を把握していて、`base.py` を直接確認するとき。
- `prompt_builder/` の個別実装や Structured Output schema だけを確認したいとき。
- `apply/` や `review/` の個別フローを追いたくて、この共通基盤を経由する必要がないとき。

## hash

- d8b4a5b9ddd34f3b5884cb2bf121eea14a4e12c61f5cc4fe3e8bc5a05c27c557

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

- すでに `build_complete_prompt()` など目的のファイルが分かっていて、この目次を経由せずに `complete_prompt.py`、`file_access_rule.py`、`oracle_and_realization_basic.py`、`oracle_standard.py`、`realization_standard.py` を直接確認するとき。
- `prompt_builder` 配下のうち、特定の 1 ファイルだけを確認したいとき。
- `agent_call_parameter` の別ディレクトリや、別フローの agent call parameter を探しているとき。

## hash

- 97f2e74a805d7916ccce5ff2fd98ac2f4f9ac02f498b3d4fdac49cf7fe55a134

# `indexing`

## Summary

- `cmoc indexing` と Codex CLI 実行前メンテナンスにおける `INDEX.md` 目次情報生成用 agent call parameter への入口です。
- `indexing/` は `index_entry.py` と `index_entry.json` を案内します。
- 目次作成対象 1 件ごとに Codex CLI へ自然言語ルーティング説明を生成させる呼び出し仕様をまとめます。

## Read this when

- `cmoc indexing` で発生する Codex CLI 呼び出し仕様を確認したいとき。
- `INDEX.md` の目次情報生成 prompt と Structured Output schema を探しているとき。

## Do not read this when

- apply、review、session join の agent call parameter を探しているとき。
- インデクシングのディレクトリ列挙、hash 計算、git commit 処理だけを確認したいとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `review`

## Summary

- `cmoc review oracle` の Codex CLI 呼び出し仕様への入口です。
- `oracles/` を案内し、所見の列挙・統合・妥当性検証・採否判定に使う prompt と schema へ分岐します。
- `agent_call_parameter/review` 配下の目次として、レビュー用 agent call parameter をたどる起点です。

## Read this when

- `cmoc review oracle` 用の prompt/schema 入口をまとめて確認したいとき。
- `oracles/` に進む前に、レビュー用 Codex CLI 呼び出しの役割分担を把握したいとき。
- どのレビュー用 Python 関数または JSON schema を開くべきか迷ったとき。

## Do not read this when

- 対象の関数や schema 名がすでに分かっていて、`oracles/INDEX.md` や個別ファイルを直接開くとき。
- `cmoc review oracle` の run isolation やレポート生成だけを確認したいとき。
- `apply/`、`indexing/`、`session/` など別の agent call parameter を探しているとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `session`

## Summary

- `cmoc session` 系サブコマンドで発生する Codex CLI 呼び出し仕様への入口です。
- `session/` は `join/` を案内し、merge conflict marker 解消用 agent call parameter をまとめます。
- Structured Output を要求しない、ファイル編集を伴う Codex CLI 呼び出し仕様を扱います。

## Read this when

- `cmoc session join` の conflict 解消時に Codex CLI へ何を依頼するか確認したいとき。
- session 系サブコマンドの agent call parameter を探しているとき。

## Do not read this when

- apply、review、indexing の agent call parameter を探しているとき。
- session 状態ファイル更新や branch 削除など Codex CLI 以外の制御処理だけを確認したいとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
