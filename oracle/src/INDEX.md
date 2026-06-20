# `acp`

## Summary

- この `acp` ディレクトリのルーティング文書で、`builder/` と `prompt_parts/` への入口です。
- `builder/` はサブコマンド別の agent call parameter、`prompt_parts/` は prompt 組み立て用の断片を案内します。
- この階層は、AI 呼び出し仕様と prompt 構成のどちらを読むべきかを切り分ける起点です。

## Read this when

- `<cmoc-root>/oracle/src/acp` 配下で、まず `builder/` と `prompt_parts/` のどちらに進むべきか整理したいとき。
- `cmoc` の agent call parameter と prompt 断片の役割分担を、この階層から把握したいとき。
- 下位の `INDEX.md` や個別仕様へ進む前に、この階層全体の入口を先に確認したいとき。

## Do not read this when

- 読む対象がすでに `builder/` か `prompt_parts/` のどちらかに決まっていて、この階層の案内を経由する必要がないとき。
- `index_entry.py`、`complete_prompt.py`、`oracle_standard.py` など、個別ファイルを直接確認したいとき。
- `<cmoc-root>/oracle/src/acp` ではなく、`<cmoc-root>/oracle/src` の他の入口や別階層の仕様だけを確認したいとき。

## hash

- 829624a3345ba9820b2b41d49cf8f5e12e19c5449127e6bbc8bd62319275410e

# `basic`

## Summary

- この `basic` ディレクトリのルーティング文書で、`acp.py`、`path_model.py`、`standard.py`、`struct_doc.py` への入口です。
- `acp.py` は AI コーディングエージェント呼び出し用の共通型を、`path_model.py` は root token 付きパス解決を、`standard.py` は標準文書の変換基盤を、`struct_doc.py` は階層文書の Markdown レンダリング基盤を案内します。
- この階層は、cmoc の共通基盤を役割ごとに切り分けて読むための起点です。

## Read this when

- `<cmoc-root>/oracle/src/basic` 配下で、まずどの共通基盤ファイルから読むべきか整理したいとき。
- AI 呼び出し用の共通型、パス解決、標準文書変換、Markdown レンダリングの入口をまとめて把握したいとき。
- `ModelClass`、`ReasoningEffort`、`FileAccessMode`、`AgentCallParameter`、`RootToken`、`Standard`、`StructDoc` の役割を一望したいとき。

## Do not read this when

- `acp.py`、`path_model.py`、`standard.py`、`struct_doc.py` のうち、読む対象がすでに決まっていて、この階層の目次を経由する必要がないとき。
- この階層ではなく、`<work-root>/oracle/src` 配下の別ディレクトリや別のルーティング文書だけを確認したいとき。
- 個別ファイルの実装を直接確認したいとき。

## hash

- 5248ae85fd766038537e5133911331203f5f2155db5f61ae618ab64298936829

# `config`

## Summary

- この `<cmoc-root>/oracle/src/config` ディレクトリのルーティング文書で、`cmoc_config.py` への入口です。
- `CmocConfig` は cmoc 全体の設定を束ね、`CmocConfigCodex` は Codex CLI 向けのモデル・推論強度の対応表を持ちます。
- 設定は `<repo-root>/.cmoc/config.json` に永続化され、`cmoc init` によって生成・同期される前提です。

## Read this when

- cmoc の設定をどこに集約しているか確認したいとき。
- `<repo-root>/.cmoc/config.json` に保存される設定内容と、その更新前提を把握したいとき。
- Codex CLI 向けの `model` / `reasoning_effort` 対応付けを確認したいとき。

## Do not read this when

- すでに `<cmoc-root>/oracle/src/config/cmoc_config.py` を直接開いて、`CmocConfig` と `CmocConfigCodex` の定義本体を確認するとき。
- 設定の読み書き処理や JSON 変換の実装を探しているとき。
- `BackendType`、`ModelClass`、`ReasoningEffort` だけを確認したいとき。

## hash

- a826a2661c5af939ab480aa20fdb2c46bb8514c0a8a29d2bf5e10395204672e1
