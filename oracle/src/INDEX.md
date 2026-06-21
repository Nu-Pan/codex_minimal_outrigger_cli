# `acp`

## Summary

- この `acp` ディレクトリのルーティング文書で、`builder/` と `prompt_parts/` への入口をまとめます。
- `builder/` は各サブコマンド向けの agent call parameter の入口で、`prompt_parts/` は完全な prompt を構成する断片群の入口です。
- この階層は、AI 呼び出し仕様と prompt 構成要素の役割分担を切り分ける起点です。

## Read this when

- `<cmoc-root>/oracle/src/acp` 配下で、まず `builder/` と `prompt_parts/` のどこから読むべきか整理したいとき。
- AI 呼び出し用の agent call parameter を組み立てる入口と、prompt 断片の入口をまとめて把握したいとき。
- この階層の役割分担を確認してから、下位の `INDEX.md` や個別仕様へ進みたいとき。

## Do not read this when

- すでに `builder/` か `prompt_parts/` のどちらへ進むか決まっていて、この階層の入口説明が不要なとき。
- `cmoc apply fork`、`cmoc indexing`、`cmoc review oracle`、`cmoc session join` のいずれかの個別仕様を直接確認したいとき。
- `complete_prompt.py` や各 `*.py` / `*.json` など、下位の個別ファイルをそのまま開く目的で、この目次を経由する必要がないとき。

## hash

- d2fbff24b15528d1dcbfa68d920f1003cf14fccf0b45ad8b69c35812cece3175

# `basic`

## Summary

- この `basic` ディレクトリのルーティング文書で、`acp.py`、`path_model.py`、`standard.py`、`struct_doc.py` への入口をまとめます。
- `acp.py` は AI コーディングエージェント呼び出し用の共通型、`path_model.py` は root token を含むパス解決、`standard.py` は標準文書の定義と `StructDoc` 変換、`struct_doc.py` は階層文書の markdown レンダリングを案内します。
- この階層は、AI 呼び出しパラメータ、パス表記、標準文書、構造化文書レンダリングという共通基盤を切り分ける起点です。

## Read this when

- `<cmoc-root>/oracle/src/basic` 配下で、まずどの共通基盤ファイルを読むべきか整理したいとき。
- `ModelClass`、`ReasoningEffort`、`FileAccessMode`、`AgentCallParameter`、`RootToken`、`Standard`、`Requirement`、`StructDoc` の役割をまとめて把握したいとき。
- `<cmoc-root>` / `.<repo-root>` / `<run-root>` / `<work-root>` の解決、標準文書の整形、markdown レンダリングの入口を確認したいとき。

## Do not read this when

- `acp.py`、`path_model.py`、`standard.py`、`struct_doc.py` の個別内容がすでに分かっていて、該当ファイルへ直接進むとき。
- パス解決だけ、標準文書だけ、Structured markdown だけのように、単一の共通基盤だけを確認したいとき。
- この階層ではなく、`src` 全体の別ディレクトリや `oracle` の別ルートを探しているとき。

## hash

- 8c84639a17dab7e3959f328203def93ac4920d6dc56f8fb1cb0cc8f668c570e8

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
