# `agent_call_parameter`

## Summary

- この `<cmoc-root>/oracle/src/agent_call_parameter` ディレクトリのルーティング文書で、`__init__py`、`base.py`、`prompt_builder/`、`apply/`、`review/` への入口です。
- `__init__py` はパッケージの Python モジュール入口、`base.py` は共有の呼び出しパラメータ型、`prompt_builder/` は prompt 組み立て、`apply/` と `review/` は各サブコマンド系の入口をまとめます。
- この階層で、AI エージェント呼び出しに関わる共通基盤と用途別の分岐先を整理するための目次です。

## Read this when

- `AgentCallParameters`、`ModelClass`、`ReasoningEffort` の定義場所を把握したいとき。
- `prompt_builder/` の断片、`apply/` の監査フロー、`review/` の Structured Output schema をどこから読むべきか迷ったとき。
- `agent_call_parameter` 配下で共有される呼び出しパラメータ基盤と、サブディレクトリごとの役割分担をまとめて確認したいとき。
- この階層の `INDEX.md` を追加・修正する前に、配下の入口を整理したいとき。

## Do not read this when

- 目的のファイルがすでに分かっていて、`base.py`、`prompt_builder/` 配下、`apply/`、`review/` を直接開くとき。
- `cmoc apply fork` や `cmoc review oracle` の個別手順だけを確認したいとき。
- `oracle` 全体の自然言語仕様や `doc/` 側の運用文書を探しているとき。

## hash

- 698bae45af2b7fa00d00d52ce6901ec8eb6f5586e6e3b5866c9093e1233c3745

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
