# `acp`

## Summary

- この `acp` ディレクトリのルーティング文書で、`builder/` と `prompt_parts/` への入口をまとめます。
- `builder/` は `cmoc apply fork`、`cmoc indexing`、`cmoc review oracle`、`cmoc session join` の呼び出し入口を案内します。
- `prompt_parts/` は `complete_prompt.py` を中心に、AI 呼び出し用 prompt の断片群と `INDEX.md` 規範への入口を切り分けます。

## Read this when

- この階層でまず `builder/` と `prompt_parts/` のどちらから読むべきか整理したいとき。
- `cmoc apply fork`、`cmoc indexing`、`cmoc review oracle`、`cmoc session join` の呼び出し仕様をまとめて把握したいとき。
- 完全な prompt の構成要素や、`INDEX.md` に書くべきルーティング規範を確認したいとき。

## Do not read this when

- すでに進む先が `builder/` か `prompt_parts/` に決まっていて、この階層の入口説明が不要なとき。
- `change_summary.py`、`index_entry.py`、`complete_prompt.py` など、個別ファイルを直接確認したいとき。
- この階層の案内ではなく、下位の `INDEX.md` や個別仕様だけを確認したいとき。

## hash

- bd34416024eef6a60a4ecdda33f1f4fa6217d8d34021c647dd6b6731c2525e21

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
