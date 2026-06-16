# `agent_call_parameter`

## Summary

- この `agent_call_parameter` ディレクトリのルーティング文書で、`base.py`、`prompt_builder/`、`apply/`、`review/`、`__init__py` への入口です。
- `base.py` は共通の呼び出しパラメータ型を定義し、`prompt_builder/` は prompt 組み立て、`apply/` と `review/` はそれぞれ `cmoc apply fork` と `cmoc review oracle` の入口をまとめます。
- `__init__py` はこのパッケージの Python モジュール入口として、他モジュールからの参照点になります。

## Read this when

- `AgentCallParameters`、`ModelClass`、`ReasoningEffort` の定義場所を確認したいとき。
- AI エージェント向け prompt の組み立てと、`apply` / `review` のどちらの入口を読むべきか迷ったとき。
- `agent_call_parameter` 配下で共有される呼び出しパラメータや、サブコマンド別の構成をまとめて把握したいとき。
- このパッケージ配下の `INDEX.md` を追加・修正する前に、全体の役割分担を整理したいとき。

## Do not read this when

- すでに `base.py`、`prompt_builder/complete_prompt.py`、`apply/fork/file_audit_finding.py`、`review/oracles/` など目的のファイルが分かっていて、直接開くとき。
- `cmoc apply fork` や `cmoc review oracle` の個別手順だけを確認したいとき。
- このパッケージではなく、`oracle` 全体の自然言語仕様や別系統の Structured Output schema を探しているとき。

## hash

- bb9c2c9b98cd6e731daa8e642639c597daf5704e9330038764a7ac863ab4012f

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

- dd3e17909e60de05ea96f1aed310c091efdc9ed9b5ef022f40a6844c2917478f
