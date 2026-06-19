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

- `<cmoc-root>/oracle/src/agent_call_parameter/base.py` は、AI コーディングエージェント呼び出し用の基本データ型をまとめる入口です。
- `BackendType`、`ModelClass`、`ReasoningEffort`、`FileAccessMode`、`AgentCallParameters` を案内し、バックエンド種別、モデル選択、推論強度、ファイルアクセスモード、プロンプト本文、Structured Output schema パスの所在を示します。
- `agent_call_parameter` 配下の各サブコマンド実装が共通して参照する、呼び出しパラメータ基盤の目次です。

## Read this when

- `<cmoc-root>/oracle/src/agent_call_parameter/base.py` にある共通の呼び出しパラメータ定義を確認したいとき。
- `AgentCallParameters` の項目や、`ModelClass` / `ReasoningEffort` / `FileAccessMode` の役割を把握したいとき。
- AI コーディングエージェント呼び出しの共通基盤が `apply/` や `review/` からどう使われるかをたどりたいとき。
- `<cmoc-root>/oracle/src/agent_call_parameter` 配下で、共通型の入口を探しているとき。

## Do not read this when

- すでに `AgentCallParameters`、`ModelClass`、`ReasoningEffort`、`FileAccessMode` の定義内容を把握していて、このファイルを直接確認するだけのとき。
- `prompt_builder/` の個別実装や Structured Output schema だけを確認したいとき。
- `apply/` や `review/` の個別フローを追いたくて、この共通基盤を経由する必要がないとき。

## hash

- 35f71d3079152fe12e55bb17ccfa74fe6f844f826c8aba5fe34b1deecd96d1ec

# `builder`

## Summary

- この `builder` ディレクトリのルーティング文書で、`apply/`、`indexing/`、`review/`、`session/` への入口です。
- `apply/` は `cmoc apply fork` の変更要約・ファイル監査・要修正点改善・実装修正を、`indexing/` は `INDEX.md` 目次生成を、`review/` は `cmoc review oracle` の所見処理を、`session/` は `cmoc session join` の conflict 解消を案内します。
- この階層では、どのサブコマンド用の agent call parameter を読むべきかを切り分けます。

## Read this when

- `builder` 配下で、どの入口から読むべきか迷ったとき。
- `apply` / `indexing` / `review` / `session` の役割差を整理してから下位の `INDEX.md` や個別ファイルに進みたいとき。
- この階層の目次を確認して、目的の Structured Output schema や呼び出し仕様へ進みたいとき。

## Do not read this when

- すでに `apply/`、`indexing/`、`review/`、`session/` のどれを読むか決まっていて、この階層の案内を経由する必要がないとき。
- `AgentCallParameters` や各サブコマンドの個別仕様を直接確認したいとき。
- この階層ではなく、下位ディレクトリの `INDEX.md` や個別ファイルをそのまま開くとき。

## hash

- 3c04be8f01d24d32a6e8094467a6668dca237f90cbafaa4d1ecba6618214eaeb

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

- 07ecdd968b8c01b249d46dcbfb55f8391f6be15903a42ad7fd99a56123b71425
