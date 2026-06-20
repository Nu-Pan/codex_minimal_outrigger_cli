# `acp`

## Summary

- この `acp` ディレクトリのルーティング文書で、`builder/` と `prompt_parts/` への入口です。
- `builder/` は `cmoc apply fork`、`cmoc indexing`、`cmoc review oracle`、`cmoc session join` の呼び出し仕様を案内し、`prompt_parts/` は prompt 断片と完全 prompt の組み立てを案内します。
- この階層は、AI コーディングエージェント呼び出しに関する仕様と prompt 構成を切り分けるための起点です。

## Read this when

- `<cmoc-root>/oracle/src/acp` 配下で、まず `builder/` と `prompt_parts/` のどちらから読むべきか整理したいとき。
- `cmoc` のサブコマンド別呼び出し仕様と、prompt 断片・完全 prompt の組み立て方をまとめて把握したいとき。
- この階層の `INDEX.md` を作成・修正する前に、下位ディレクトリの役割分担を先に確認したいとき。
- AI コーディングエージェント呼び出しに関する仕様と prompt 構成の入口を確認したいとき。

## Do not read this when

- すでに読む対象が `builder/` または `prompt_parts/` に決まっていて、この階層の入口を経由する必要がないとき。
- `cmoc apply fork`、`cmoc indexing`、`cmoc review oracle`、`cmoc session join` のうち、特定の 1 系統だけを直接確認したいとき。
- `change_summary.py`、`index_entry.py`、`enumerate_finding.py`、`conflict_resolution.py` など、下位の個別ファイルをそのまま開きたいとき。
- この階層の案内ではなく、`oracle` 全体の別ルートや開発規約だけを確認したいとき。

## hash

- 5856c42c109fc0082a2c1371f144349ee7afb288e895a1244b648a9b6203c0cb

# `basic`

## Summary

- この `basic` ディレクトリのルーティング文書で、`acp.py`、`path_model.py`、`standard.py`、`struct_doc.py` への入口です。
- `acp.py` は AI コーディングエージェント呼び出し用の共通型を、`path_model.py` は root token 付きパス解決を、`standard.py` は標準表現を、`struct_doc.py` は階層文書の markdown レンダリングを案内します。
- この階層は、cmoc の共通基盤をまとめて扱うための目次です。

## Read this when

- `<cmoc-root>/oracle/src/basic` 配下で、どの基盤ファイルから読むべきか整理したいとき。
- `AgentCallParameter` と、その構成要素である `ModelClass`、`ReasoningEffort`、`FileAccessMode` の所在を確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` の解決規則や、標準表現、StructDoc の役割をまとめて把握したいとき。
- この階層の下位 `INDEX.md` や個別ファイルへ進む前に、役割分担を先に整理したいとき。

## Do not read this when

- すでに読む対象が `acp.py`、`path_model.py`、`standard.py`、`struct_doc.py` のいずれかに決まっていて、この階層の目次を経由する必要がないとき。
- `ModelClass`、`ReasoningEffort`、`FileAccessMode`、`AgentCallParameter` の定義内容を直接確認したいとき。
- パス解決、標準表現、StructDoc のうち、個別機能だけを直接確認したいとき。
- `oracle` 全体の別ルートや開発規約だけを確認したいとき。

## hash

- 07aeefbe503f3e32cc1f44d82804d059c12ddbfd89e486b8c65d8d7865e6fa2f

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
