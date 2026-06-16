# `complete_prompt.py`

## Summary

- `<cmoc-root>/oracle/src/agent_call_parameter/prompt_builder/complete_prompt.py` は、AI エージェントへ渡す完全な prompt を `StructDoc` の列として組み立てる入口です。
- 同ディレクトリの `file_access_rule.py`、`oracle_and_realization_basic.py`、`oracle_standard.py`、`realization_standard.py` を組み合わせて、役割・要約・目標・ファイルアクセス規則・補助標準をまとめます。
- `structured_output` の有無に応じて出力形式の指示を追加し、呼び出し側がそのまま利用できる prompt 構造を返します。

## Read this when

- `build_complete_prompt()` の構成や、どの prompt 断片が最終的に入るか確認したいとき。
- `<cmoc-root>/oracle/src/agent_call_parameter/prompt_builder/` 配下で、ファイルアクセス規則や oracle / realization の基本説明、標準文をどこから参照するか迷ったとき。
- 新しい agent call parameter の prompt 断片を追加・整理する前に、このディレクトリの役割を把握したいとき。

## Do not read this when

- すでに `build_complete_prompt()` の呼び出し先や構成が分かっていて、直接 `<cmoc-root>/oracle/src/agent_call_parameter/prompt_builder/complete_prompt.py` を確認するとき。
- ファイルアクセス規則だけ、または `oracle_standard.py` / `realization_standard.py` だけを個別に確認したいとき。
- `<cmoc-root>/oracle/src/agent_call_parameter/` 全体の他サブディレクトリや review / apply の別フローを探しているとき。

## hash

- 7061fadd439e527e5a8f8f9960b28858245d9bec3ba77655078c28059db3670f

# `file_access_rule.py`

## Summary

- このファイルは、AI エージェント向けのファイル読み書き規則を `StructDoc` として組み立てる入口です。
- 4 つの `FileAccessMode` ごとに、`<work-root>` 配下の読み書き可否と `memo` などの禁止条件を切り分けて定義します。
- 必要に応じて追加の `aux_rules` を末尾に連結し、完全なアクセス規則文を返します。

## Read this when

- `build_file_access_rule` がどのファイルアクセス規則を組み立てるか確認したいとき。
- `readonly`、`pure_oracle_read`、`realization_write`、`oracle_write` の各モードの差分や `aux_rules` の付与方法を見たいとき。
- プロンプト生成の前提になる読み書き制約を整理してから実装・修正したいとき。

## Do not read this when

- `file_access_rule.py` のモードや禁止条件がすでに分かっていて、直接コードを確認するとき。
- ファイル読み書き規則ではなく、`<work-root>/oracle/src/utils/path_model.py` や `<work-root>/oracle/src/utils/struct_doc.py` の共通基盤だけを確認したいとき。
- `prompt_builder` 配下の他のプロンプト生成処理だけを追いたいとき。

## hash

- c705662e63287a85526056e81e624d6bdfb9fb3853a246c3013ab4b71656b0f1

# `oracle_and_realization_basic.py`

## Summary

- この `prompt_builder` ディレクトリのルーティング文書で、`cmoc` の prompt 生成まわりの入口です。
- `oracle_and_realization_basic.py` は oracle file と realization file の基本概念を定義し、`file_access_rule.py` は読み書き規則を定義します。
- `oracle_standard.py` と `realization_standard.py` はそれぞれ oracle / realization の標準観点をまとめ、`complete_prompt.py` はそれらを束ねた完全な prompt を構築します。

## Read this when

- `cmoc` のプロンプト生成に関わる共通部品の入口をまとめて把握したいとき。
- `complete_prompt.py`、`file_access_rule.py`、`oracle_and_realization_basic.py`、`oracle_standard.py`、`realization_standard.py` のどれを読むべきか迷ったとき。
- oracle file と realization file の基本概念、読み書き規則、各種標準文書、最終的な完全プロンプトの組み立てを順にたどりたいとき。
- このディレクトリ配下のルーティング文書を追加・修正するとき。

## Do not read this when

- `<cmoc-root>/oracle/src/agent_call_parameter/prompt_builder/` 配下の読み先がすでに分かっていて、`complete_prompt.py`、`file_access_rule.py`、`oracle_and_realization_basic.py`、`oracle_standard.py`、`realization_standard.py` のいずれかを直接読むとき。
- この階層ではなく、`agent_call_parameter` の他のディレクトリや別サブコマンドの呼び出しパラメータだけを確認したいとき。
- `INDEX.md` の更新方針や `oracle` 全体のルーティング規則だけを確認したいとき。

## hash

- 5d92b23a7707603a18385e66f1a99c30c90a16949e31799a3bbb5f91753472b8

# `oracle_standard.py`

## Summary

- `<cmoc-root>/oracle/src/agent_call_parameter/prompt_builder/` 配下で、`oracle file` に対する標準的なレビュー観点を組み立てる `oracle_standard.py` への入口です。
- `build_oracle_standard()` は `oracle file` の標準を `StructDoc` として定義し、`complete_prompt.py` から `oracle_standard` フラグ経由で組み込まれます。
- `oracle_and_realization_basic.py` や `realization_standard.py` と合わせて、AI 呼び出し用プロンプトの文脈を切り分けるための目次です。

## Read this when

- `oracle file` の標準的なレビュー観点をまとめて確認したいとき。
- `build_oracle_standard()` がどの文脈で呼ばれ、`complete_prompt.py` のどこから組み込まれるかを確認したいとき。
- `oracle_and_realization_basic.py` や `realization_standard.py` との役割分担を整理したいとき。
- `oracle_standard.py` を修正する前に、同階層の関連ファイルの入口をたどりたいとき。

## Do not read this when

- `build_oracle_standard()` がすでに目的の対象で、このファイル本体を直接読むとき。
- `oracle file` ではなく、`realization file` や別フローの agent call parameter を確認したいとき。
- `prompt_builder` 全体の組み立てではなく、すでに個別の prompt 文書だけを特定しているとき。
- ルーティング文書ではなく、`oracle` 配下の正本仕様や開発規約そのものを確認したいとき。

## hash

- 0bbdc467692e517465e42377f0eabad9235582e6f3986e8a8333724c640cd100

# `realization_standard.py`

## Summary

- `<cmoc-root>/oracle/src/agent_call_parameter/prompt_builder/` 配下の prompt 組み立て用モジュールへの入口です。
- `complete_prompt.py` は role / summary / goal / file access rule を束ね、必要に応じて `oracle_and_realization_basic.py`、`oracle_standard.py`、`realization_standard.py`、`file_access_rule.py` を追加します。
- `realization_standard.py` は realization file の最小化・高品質化・既存実装整理・抽象化抑制・公開面抑制といった標準を定義します。

## Read this when

- `<cmoc-root>/oracle/src/agent_call_parameter/prompt_builder/` 配下で、AI エージェント向けプロンプトの構成方法をまとめて把握したいとき。
- `complete_prompt.py` で全体プロンプトを組み立てる前に、ファイルアクセス規則や oracle / realization の基本定義、各種標準の役割分担を確認したいとき。
- `realization_standard.py` を含む各ビルダーの責務を整理し、どのヘルパーを読むべきか迷ったとき。

## Do not read this when

- `<cmoc-root>/oracle/src/agent_call_parameter/prompt_builder/` 配下の個別ビルダーがすでに特定できており、`complete_prompt.py`、`file_access_rule.py`、`oracle_and_realization_basic.py`、`oracle_standard.py`、`realization_standard.py` のいずれかを直接開くとき。
- `agent_call_parameter` の prompt_builder 群ではなく、`<work-root>/oracle/doc` や `<work-root>/oracle/src` の別系統の仕様・実装を確認したいとき。
- この階層のルーティングではなく、単一関数や単一定義の実装内容だけを見たいとき。

## hash

- f4b15e7217ca0311f3a217b422a616e7b04aa1a24ae8d3f40e0f80616f1a928d
