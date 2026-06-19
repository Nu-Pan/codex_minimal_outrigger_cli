# `agent_call_parameter`

## Summary

- この `agent_call_parameter` ディレクトリのルーティング文書で、`base.py`、`builder/`、`prompt_parts/` への入口です。
- `base.py` は共通型、`builder/` はサブコマンド別の呼び出し仕様、`prompt_parts/` は prompt 断片と完全 prompt の組み立てをまとめます。
- この階層では、AI 呼び出しに共通する基盤と、用途別の入口を切り分けます。

## Read this when

- `AgentCallParameters`、`ModelClass`、`ReasoningEffort`、`FileAccessMode` の定義場所を確認したいとき。
- `builder/` 配下で `apply`、`indexing`、`review`、`session` のどれを読むか迷ったとき。
- `prompt_parts/` 配下で完全な prompt と各断片の役割を整理したいとき。
- `agent_call_parameter` 全体の共通基盤や入口をまとめて把握したいとき。

## Do not read this when

- すでに `base.py`、`builder/INDEX.md`、`prompt_parts/INDEX.md` のいずれかを読む対象として決まっていて、この階層の目次を経由する必要がないとき。
- `builder/` や `prompt_parts/` の下位ファイルへ直接進めるとき。
- この階層ではなく、`oracle` 全体の正本仕様や開発規約だけを確認したいとき。

## hash

- 7c28a7f1666d657a8febdea55b7302406816813cb86655648ef7a0e9afc2c24e

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
