# `acp`

## Summary

- この `acp` ディレクトリのルーティング文書で、`builder/` と `prompt_parts/` への入口をまとめます。
- `builder/` は `cmoc apply fork`、`cmoc indexing`、`cmoc review oracle`、`cmoc session join` に対応する agent call parameter の入口を案内します。
- `prompt_parts/` は complete prompt を組み立てる断片群と、各種標準文書への入口を整理します。

## Read this when

- `<cmoc-root>/oracle/src/acp` 配下で、まず `builder/` と `prompt_parts/` のどちらから読むべきか整理したいとき。
- AI 呼び出し用 prompt の組み立てと、サブコマンド別 agent call parameter の役割分担をまとめて把握したいとき。
- この階層の目次を確認してから、下位の `INDEX.md` や個別仕様へ進みたいとき。

## Do not read this when

- すでに進む先が `builder/` か `prompt_parts/` に決まっていて、この階層の入口説明が不要なとき。
- `cmoc apply fork`、`cmoc indexing`、`cmoc review oracle`、`cmoc session join` の個別仕様を直接確認したいとき。
- 完全な prompt 本体や個別の prompt 断片、Structured Output schema を探しているとき。

## hash

- 2e6c1986021c1fc98a8b9017536b812e752a8f099fa3616dfb1c640ace4607a0

# `basic`

## Summary

- この `basic` ディレクトリのルーティング文書で、`acp.py`、`standard.py`、`struct_doc.py`、`path_model.py` への入口をまとめます。
- `acp.py` は AI コーディングエージェント呼び出し用の共通型、`standard.py` は標準文書の共通表現、`struct_doc.py` は構造化文書の markdown レンダリング、`path_model.py` は root token を含むパス解決の入口です。
- この階層は、cmoc の共通基盤を切り分けて把握するための起点です。

## Read this when

- `<cmoc-root>/oracle/src/basic` 配下で、`acp.py`、`standard.py`、`struct_doc.py`、`path_model.py` のどこから読むべきか整理したいとき。
- AI コーディングエージェント呼び出しの型、標準文書の共通形式、階層化された markdown レンダリング、root token を含むパス解決をまとめて把握したいとき。
- この階層の共通基盤を先に確認してから、下位の個別仕様へ進みたいとき。

## Do not read this when

- `acp.py`、`standard.py`、`struct_doc.py`、`path_model.py` のうち、読む対象がすでに決まっていて、この階層の入口説明が不要なとき。
- AI 呼び出しパラメータ、標準表現、構造化文書、パス解決のうち、特定の一つだけを直接確認したいとき。
- この階層全体の案内ではなく、個別ファイルの実装や定義をそのまま読みたいとき。

## hash

- ccb0ea9b43d7107045ac9101c60dda53152d3652d772a08e709c57b473f7cc12

# `config`

## Summary

- この `<cmoc-root>/oracle/src/config` ディレクトリのルーティング文書で、`cmoc_config.py` への入口をまとめます。
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

- e333b5511ee2e06b89ac77f9d8ea837a274f30698f6317c5dda1e45925b1239f
