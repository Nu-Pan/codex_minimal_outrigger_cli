# `agent_call_parameter`

## Summary

- `cmoc` の `agent_call_parameter` パッケージのルーティング文書で、`__init__py`、`base.py`、`prompt_builder/`、`apply/`、`review/` への入口です。
- `base.py` は共通型を、`prompt_builder/` は prompt 組み立てを、`apply/` と `review/` はそれぞれ `cmoc apply fork` と `cmoc review oracle` の入口をまとめます。
- この階層の共有パラメータと、サブコマンド別の分岐先を一望するための目次です。

## Read this when

- `AgentCallParameters`、`ModelClass`、`ReasoningEffort` の定義場所を確認したいとき。
- AI エージェント向け prompt の組み立てと、`apply` / `review` のどちらの入口を読むべきか迷ったとき。
- このパッケージ配下で共有される呼び出しパラメータや、サブコマンド別の構成をまとめて把握したいとき。
- このパッケージ配下の `INDEX.md` を追加・修正する前に、全体の役割分担を整理したいとき。

## Do not read this when

- すでに `base.py`、`prompt_builder/complete_prompt.py`、`apply/fork/file_audit_finding.py`、`review/oracles/` など目的のファイルが分かっていて、直接開くとき。
- `cmoc apply fork` や `cmoc review oracle` の個別手順だけを確認したいとき。
- このパッケージではなく、`oracle` 全体の自然言語仕様や別系統の Structured Output schema を探しているとき。

## hash

- 0a3b80a3a0767b545a0952ed75755a01a0eef092ef58499f07da668d506efb27

# `agent_call_parameters`

## Summary

- このディレクトリのルーティング文書で、`prompt_builder/` とその中心ファイルである `oracles_standards.py` への入口です。
- `oracles_standards.py` は、oracle file 向け standards を `StructDoc` にまとめる役割を持ち、`oracle standards` を prompt 用の構造化文書として組み立てます。
- 同階層で確認すべき中心ファイルは `<cmoc-root>/oracle/src/agent_call_parameters/prompt_builder/oracles_standards.py` です。

## Read this when

- `<cmoc-root>/oracle/src/agent_call_parameters/prompt_builder/oracles_standards.py` が何を組み立てるモジュールか確認したいとき。
- `Standard` と `Requirement` を使って oracle file 向けの規範をどう `StructDoc` 化しているか追いたいとき。
- oracle file の認知負荷最小化、正本仕様断片、未定義部分の扱い、文字数最小化、矛盾回避、用語統一、命名、ベストプラクティスとの優先関係、goal/non-goal の整理方針を確認したいとき。

## Do not read this when

- `<cmoc-root>/oracle/src/agent_call_parameters/prompt_builder/INDEX.md` か `<cmoc-root>/oracle/src/agent_call_parameters/prompt_builder/oracles_standards.py` の内容がすでに分かっていて、この階層の目次を経由せず直接確認するとき。
- `oracle` 配下の自然言語仕様や、`agent_call_parameter` 側の別系統のルーティング文書を確認したいだけで、このディレクトリは不要なとき。
- Structured Output schema や実装本体ではなく、別の prompt builder モジュールを探しているとき。

## hash

- def613560f21728c3ed4feeaceb3ced7837de9ef23f0673b7e93b3f6a0384ff4

# `utils`

## Summary

- `<cmoc-root>/oracle/src/utils/path_model.py` は、パス表記の基本ルールと root token 解決を扱い、`resolve_real_path()` と `resolve_token_path()` を通じて実パスとの相互変換を提供します。
- `<cmoc-root>/oracle/src/utils/standard.py` は、`Standard` と `Requirement` を定義し、標準文書を `StructDoc` に変換するための共通基盤です。
- `<cmoc-root>/oracle/src/utils/struct_doc.py` は、階層構造を持つ文章を `StructDoc` として保持し、`render_as_markdown()` で markdown に整形するヘルパーです。

## Read this when

- `<cmoc-root>/oracle/src/utils/path_model.py` で、`<cmoc-root>` / `<repo-root>` / `<run-root>` / `<work-root>` の root token 解決や実パスへの変換規則を確認したいとき。
- `<cmoc-root>/oracle/src/utils/standard.py` で、`Standard` / `Requirement` の共通表現と `StructDoc` への変換の流れを確認したいとき。
- `<cmoc-root>/oracle/src/utils/struct_doc.py` で、階層化された文章の保持方法や markdown レンダリング、`ntqs()` の挙動を確認したいとき。
- この階層のどのユーティリティを読むべきか迷ったときに、入口を整理したいとき。

## Do not read this when

- すでに目的の関数やクラスが分かっていて、`path_model.py`、`standard.py`、`struct_doc.py` の該当箇所へ直接進むとき。
- `oracle` 配下の個別仕様や開発規約だけを確認したいとき。
- パス解決ではなく、標準文書の変換や markdown レンダリングの細部だけを追いたいとき。
- この階層の共通入口ではなく、下位の実装やテストを個別に確認したいとき。

## hash

- d54c00dd69ff894985f306ad2c73be5359d63b1347a4b1024325e13ac084936c
