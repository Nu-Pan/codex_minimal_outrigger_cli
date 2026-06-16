# `agent_call_parameter`

## Summary

- この `agent_call_parameter` ディレクトリのルーティング文書で、`base.py` と `apply/`、`indexing/`、`review/`、`session/` への入口です。
- `base.py` は共通の呼び出しパラメータ基盤をまとめ、各サブディレクトリはサブコマンド別の Codex CLI 呼び出し仕様を案内します。
- この階層では、どの仕様を読むべきかを素早く切り分けるための目次を提供します。

## Read this when

- `<cmoc-root>/oracle/src/agent_call_parameter` 配下のどの入口から読むべきか迷ったとき。
- `AgentCallParameters`、`ModelClass`、`ReasoningEffort`、`base.py`、`apply/`、`review/`、`indexing/`、`session/` の役割をまとめて把握したいとき。
- このパッケージ配下の目次を確認して、目的の Structured Output schema や呼び出し仕様へ進みたいとき。

## Do not read this when

- すでに `base.py`、`apply/`、`indexing/`、`review/`、`session/` のどれを読むか決まっていて、この階層の案内を経由する必要がないとき。
- `AgentCallParameters` や各サブコマンドの個別仕様を直接確認したいとき。
- この階層ではなく、下位ディレクトリの `INDEX.md` や個別ファイルをそのまま開くとき。

## hash

- 08f368f564c7fd9d2854460a8c0a8e4138bb840601c70bac45e21c42c0a41fad

# `prompt_parts`

## Summary

- この `prompt_parts` ディレクトリのルーティング文書で、`complete_prompt.py`、`file_access_rule.py`、`oracle_and_realization_basic.py`、`oracle_standard.py`、`realization_standard.py` への入口です。
- `complete_prompt.py` は完全な prompt の組み立て本体で、他の各ファイルはその構成要素となる断片や標準を提供します。
- この階層は、AI に渡す prompt の共通前提・アクセス規則・標準観点を分けて管理するための入口です。

## Read this when

- `complete_prompt.py` がどの prompt 断片を順に組み立てるか確認したいとき。
- ファイルアクセス規則、oracle / realization の基本概念、oracle 側標準、realization 側標準をまとめて把握したいとき。
- `prompt_parts/` 配下で新しい prompt 断片を追加・整理する前に、既存の構成と役割分担を確認したいとき。

## Do not read this when

- `complete_prompt.py`、`file_access_rule.py`、`oracle_and_realization_basic.py`、`oracle_standard.py`、`realization_standard.py` の目的がすでに分かっていて、対象ファイルを直接開くとき。
- `prompt_parts/` ではなく、`<cmoc-root>/oracle/src` 配下の別パッケージや別の入口を探しているとき。
- この階層の `INDEX.md` ではなく、個別の prompt 断片や補助コードだけを確認したいとき。

## hash

- 392379637f1534f47335313fba5b94a4d6315bbac1e2f9298fdb75d504686e61

# `utils`

## Summary

- この `utils` ディレクトリのルーティング文書で、`path_model.py`、`standard.py`、`struct_doc.py` への入口です。
- `path_model.py` は root token を含むパス表記と実パスの相互変換を扱い、`RootToken` と各種 `resolve_*` 関数をまとめます。
- `standard.py` は `Standard` / `Requirement` と `standard_to_struct_doc()` を、`struct_doc.py` は `StructDoc`、`render_as_markdown()`、`ntqs()` をまとめる共通基盤です。

## Read this when

- `<cmoc-root>/oracle/src/utils` 配下のどのユーティリティから読むべきか迷ったとき。
- `<cmoc-root>` / `<repo-root>` / `<run-root>` / `<work-root>` の解決規則を確認したいとき。
- `Standard` と `Requirement` の共通表現や、`StructDoc` への変換経路を把握したいとき。
- 階層化された文書の保持や markdown レンダリングの共通基盤を探したいとき。

## Do not read this when

- すでに読む対象が `path_model.py`、`standard.py`、`struct_doc.py` のいずれかに決まっていて、この階層の入口を経由する必要がないとき。
- パス解決だけ、標準表現だけ、`StructDoc` レンダリングだけを個別に確認したいとき。
- `oracle` 配下の個別仕様や開発規約を探していて、共通ユーティリティの目次は不要なとき。

## hash

- 7c4b7de450a02bac5e852eab54fb95bf9ce808e564fb840f4d87fec22e21151c
