# `agent_call_parameter`

## Summary

- この `agent_call_parameter` ディレクトリのルーティング文書で、`base.py`、`builder/`、`prompt_parts/` への入口です。
- `base.py` は共有型と呼び出しパラメータ基盤を定義し、`builder/` はサブコマンド別の呼び出し仕様、`prompt_parts/` は prompt 断片と完全 prompt の組み立てを案内します。
- この階層は、AI コーディングエージェント呼び出しに共通する型・仕様・prompt 構成を切り分けるための起点です.

## Read this when

- `<cmoc-root>/oracle/src/agent_call_parameter` 配下で、まずどのファイルや下位ディレクトリから読むべきか整理したいとき。
- `AgentCallParameters` を中心に、AI コーディングエージェント呼び出しの共通基盤を把握したいとき。
- `builder/` と `prompt_parts/` の役割分担を先に確認してから、下位の個別仕様へ進みたいとき。
- この階層の `INDEX.md` を作成・修正する前に、全体の入口構成を把握したいとき.

## Do not read this when

- すでに `base.py`、`builder/INDEX.md`、`prompt_parts/INDEX.md` のいずれかを開く対象が決まっていて、この階層の案内を経由する必要がないとき。
- `AgentCallParameters`、`ModelClass`、`ReasoningEffort`、`FileAccessMode` の定義だけを直接確認したいとき。
- `complete_prompt.py` や各 prompt 断片など、個別ファイルの中身をそのまま確認したいとき。
- `agent_call_parameter` 以外の `oracle` 配下の別ルートや、開発規約だけを探しているとき.

## hash

- 160b62a89d8762ad35f541684ab2ccb1fe6a5d34ed6a8d2a8d46b0abdec1fd3a

# `cmoc_config`

## Summary

- `<cmoc-root>/oracle/src/cmoc_config/cmoc_config.py` は、cmoc 全体の設定をまとめる `CmocConfig` と、Codex CLI 向けの対応表を持つ `CmocConfigCodex` を定義する入口です。
- この設定は `<cmoc-root>/.cmoc/config.json` として永続化され、`BackendType`、`ModelClass`、`ReasoningEffort` を束ねる前提になっています。

## Read this when

- cmoc の設定項目をどこに集約しているか確認したいとき。
- `CmocConfig` と `CmocConfigCodex` の役割や、Codex CLI 向けの `model` / `reasoning_effort` 対応付けを把握したいとき。
- 設定を `<cmoc-root>/.cmoc/config.json` に永続化する前提や、Enum 値を value 化して保存する方針を確認したいとき。

## Do not read this when

- すでに `CmocConfig` と `CmocConfigCodex` の定義場所が分かっていて、この目次を経由せずに `cmoc_config.py` 本体を直接確認するとき。
- 設定の読み書き処理や JSON 変換の実装を探しているとき。
- `agent_call_parameter/base.py` の `BackendType`、`ModelClass`、`ReasoningEffort` だけを確認したいとき。

## hash

- 2660eef8145250bbc576a57fd446a50343d2ea949ce58845aaa6e488ba5bb7e9

# `utils`

## Summary

- この `utils` ディレクトリのルーティング文書で、`path_model.py`、`standard.py`、`struct_doc.py` への入口です。
- `path_model.py` は root token 付きパスの解決を、`standard.py` は oracle 文書の標準表現を、`struct_doc.py` は階層的な文章の markdown レンダリングを案内します。
- この階層は、パス表記・標準定義・構造化文章という cmoc の共通基盤をまとめて扱う目次です。

## Read this when

- `<work-root>/oracle/src/utils/` 配下で、`path_model.py`、`standard.py`、`struct_doc.py` のどれから読むべきか整理したいとき。
- `RootToken` による root 解決、`Standard` と `Requirement` の標準表現、`StructDoc` の markdown レンダリングをまとめて把握したいとき。
- `<cmoc-root>` / `<repo-root>` / `<run-root>` / `<work-root>` の扱い、共通標準文書、構造化文章ヘルパーの入口を確認したいとき。

## Do not read this when

- `path_model.py`、`standard.py`、`struct_doc.py` のうち、読む対象がすでに 1 つに決まっていて、このディレクトリの目次を経由せず直接開くとき。
- `<cmoc-root>` / `<repo-root>` / `<run-root>` / `<work-root>` の解決規則だけを確認したいときで、`standard.py` や `struct_doc.py` の案内が不要なとき。
- 標準文書の定義や markdown レンダリングだけを個別に確認したくて、この `utils/` 全体の役割整理が不要なとき。

## hash

- aae60079e816dfb3970a7251ecd44bc3940c55229b4834ab915d9cd366a07f14
