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

# `base.py`

## Summary

- この `base.py` の目次文書で、AI コーディングエージェント呼び出し用の基本データ型をまとめる入口です。
- `BackendType`、`ModelClass`、`ReasoningEffort`、`FileAccessMode`、`AgentCallParameters` を案内し、バックエンド種別、モデル選択、推論強度、ファイルアクセスモード、プロンプト本文、Structured Output schema パスの所在を示します。
- `agent_call_parameter` 配下の各サブコマンド実装が共通して参照する、呼び出しパラメータ基盤の目次です。

## Read this when

- `<cmoc-root>/oracle/src/agent_call_parameter/base.py` にある共通の呼び出しパラメータ定義を確認したいとき。
- `AgentCallParameters` の項目や、`ModelClass` / `ReasoningEffort` / `FileAccessMode` の役割を把握したいとき。
- AI コーディングエージェント呼び出しの共通基盤が各サブコマンド実装からどう使われるかをたどりたいとき。

## Do not read this when

- すでに `BackendType`、`ModelClass`、`ReasoningEffort`、`FileAccessMode`、`AgentCallParameters` の定義内容を把握していて、このファイルの中身を直接確認するだけのとき。
- `prompt_parts/` の個別実装や Structured Output schema だけを確認したいとき。
- `apply/` や `review/` の個別フローを追いたくて、この共通基盤を経由する必要がないとき。

## hash

- 59bc6778ae5e1c0bf4500b96e90a4850209152901930572db9ce8d693b829d50

# `builder`

## Summary

- この `builder` ディレクトリのルーティング文書で、`apply/`、`indexing/`、`review/`、`session/` への入口です。
- `apply/` は `cmoc apply fork` の変更要約・ファイル監査・要修正点改善・実装修正を、`indexing/` は `INDEX.md` 目次生成を、`review/` は `cmoc review oracle` の所見処理を、`session/` は `cmoc session join` の conflict 解消を案内します。
- この階層では、どのサブコマンド用の agent call parameter を読むべきかを切り分けます。

## Read this when

- `builder` 配下で、`apply`、`indexing`、`review`、`session` のどれから読むべきか整理したいとき。
- `cmoc apply fork`、`cmoc indexing`、`cmoc review oracle`、`cmoc session join` の呼び出し仕様の入口をまとめて把握したいとき。
- この階層の目次を確認してから、下位の `INDEX.md` や個別ファイルへ進みたいとき。

## Do not read this when

- すでに読む対象が `apply/`、`indexing/`、`review/`、`session/` のいずれかに決まっていて、この階層の目次を経由する必要がないとき。
- `change_summary.py`、`file_audit_finding.py`、`index_entry.py`、`enumerate_finding.py`、`conflict_resolution.py` などの個別ファイルを直接開きたいとき。
- この階層の案内ではなく、各下位ディレクトリの `INDEX.md` や個別仕様だけを確認したいとき。

## hash

- 385e5f6181ccc5c2986e5e97e405a643062fd7f7ae52161166aa1b4daa02c71f

# `prompt_parts`

## Summary

- `<cmoc-root>/oracle/src/agent_call_parameter/prompt_parts/` ディレクトリのルーティング文書で、`complete_prompt.py` を中心に prompt 断片の組み立てと各標準の入口を案内する。
- `file_access_rule.py`、`oracle_and_realization_basic.py`、`oracle_standard.py`、`realization_standard.py` をまとめ、AI 呼び出し用 prompt に入る要素の役割分担を示す。
- Structured Output 指示やファイル読み書き規則を含む完全な prompt 構成を確認するための目次である。

## Read this when

- `build_complete_prompt()` がどの断片を結合するか確認したいとき。
- ファイル読み書き規則、oracle / realization の基本定義、oracle 標準、realization 標準のどれを読むべきか迷ったとき。
- prompt 断片を追加・整理する前に、このディレクトリ全体の役割を把握したいとき。
- Structured Output schema を要求する prompt の末尾に何が追加されるか確認したいとき。

## Do not read this when

- すでに `complete_prompt.py`、`file_access_rule.py`、`oracle_and_realization_basic.py`、`oracle_standard.py`、`realization_standard.py` の目的が分かっていて、個別ファイルへ直接進めるとき。
- prompt 組み立てではなく、`agent_call_parameter` 全体の共通型や別サブコマンドの仕様を探しているとき。
- `oracle` 正本仕様や開発規約そのものを確認したいだけで、このディレクトリの入口が不要なとき。

## hash

- f800904ba87e10d636f3a0f2ad297bc40fa37229755eb3442718de5b81cbab98
