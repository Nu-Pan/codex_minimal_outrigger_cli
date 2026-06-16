# `complete_prompt.py`

## Summary

- `<cmoc-root>/oracle/src/prompt_parts/complete_prompt.py` は、AI エージェントへ渡す完全な prompt を `StructDoc` の列として組み立てる入口です。
- 必須要素として `role`、`summary`、`goal`、`file_access_rule` を含み、必要に応じて `oracle_and_realization_basic`、`oracle_standard`、`realization_standard` を追加します。
- `structured_output` が有効な場合は、指定された Structured Output schema に従うよう促す出力形式の指示を末尾に加えます。

## Read this when

- `build_complete_prompt()` がどの `StructDoc` 断片を順に結合するか確認したいとき。
- ファイルアクセス規則、oracle / realization の基本説明、各種 standard、Structured Output 指示のどれが最終 prompt に入るかを整理したいとき。
- `prompt_parts/` 配下で新しい prompt 断片を追加・整理する前に、この完全 prompt の組み立て方を把握したいとき。

## Do not read this when

- すでに `<cmoc-root>/oracle/src/prompt_parts/complete_prompt.py` の呼び出し先や構成が分かっていて、このファイル本体を直接確認するとき。
- `file_access_rule.py`、`oracle_and_realization_basic.py`、`oracle_standard.py`、`realization_standard.py` など、組み立て元の断片だけを個別に確認したいとき。
- `prompt_parts/` 配下のルーティングではなく、別の `<work-root>/oracle/src` サブディレクトリや別フローの入口を探しているとき。

## hash

- 19bfcc921faf8f1650be0c70dc3a7b74229e40a47b7bbb3fce20688f78087054

# `file_access_rule.py`

## Summary

- `<cmoc-root>/oracle/src/agent_call_parameter/prompt_builder/file_access_rule.py` は、AI エージェント向けのファイル読み書き規則を `StructDoc` として組み立てる入口です。
- 4 つの `FileAccessMode` ごとに、`<work-root>` 配下の読み書き可否と `memo` などの禁止条件を切り分けて定義します。
- 必要に応じて `aux_rules` を末尾に連結し、完全なアクセス規則文を返します。

## Read this when

- `build_file_access_rule()` がどのような読み書き制約を組み立てるか把握したいとき。
- `readonly`、`pure_oracle_read`、`realization_write`、`oracle_write` の各モードの差分や、`aux_rules` の付与方法を確認したいとき。
- prompt 生成の前提になるファイルアクセス規則を整理してから実装・修正したいとき。

## Do not read this when

- `build_file_access_rule()` の中身がすでに分かっていて、`<cmoc-root>/oracle/src/agent_call_parameter/prompt_builder/file_access_rule.py` 本体を直接確認したいとき。
- ファイル読み書き規則ではなく、`<cmoc-root>/oracle/src/utils/path_model.py` や `StructDoc` などの共通基盤だけを確認したいとき。
- `prompt_builder` 配下の別ファイルや、他の agent call parameter の入口を探しているとき。

## hash

- d49a60d40d2ca63385e4008dfc9b4ac9fc267dba6c4d08c5b9c45b1740b4a97f

# `oracle_and_realization_basic.py`

## Summary

- `<cmoc-root>/oracle/src/agent_call_parameter/prompt_builder/oracle_and_realization_basic.py` は、`oracle file` と `realization file` の基本概念を `StructDoc` としてまとめる入口です。
- このファイルは、両者の定義・役割・下位概念を整理し、`complete_prompt.py` が使う prompt 断片の基礎説明を提供します。
- `prompt_builder/` 配下の共通前提を確認したいときの、基本概念への入口です。

## Read this when

- `oracle file` と `realization file` の基本概念、役割、下位概念をまとめて把握したいとき。
- `build_oracle_and_realization_basic()` がどのような説明文を組み立てるか確認したいとき。
- `complete_prompt.py` に入る前に、prompt 生成で使う共通前提を整理したいとき。
- `oracle` ツリーとそれ以外のツリーをどう区別するか、基本定義を確認したいとき。

## Do not read this when

- すでに `<cmoc-root>/oracle/src/agent_call_parameter/prompt_builder/oracle_and_realization_basic.py` を直接確認する対象として把握できていて、この目次を経由する必要がないとき。
- `complete_prompt.py`、`file_access_rule.py`、`oracle_standard.py`、`realization_standard.py` など、同階層の別ファイルだけを確認したいとき。
- `agent_call_parameter` 全体の構成や、別サブコマンドの呼び出しパラメータを探しているとき。

## hash

- 5a815fcffb8e409653790fc71e3bf3bde6542114a865cea785ec8889210a0ad9

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

- fabd285b85fd2e315a7eebb34c1160253daeb5bd1e41ea6392b3d24083795479

# `realization_standard.py`

## Summary

- この `<cmoc-root>/oracle/src/agent_call_parameter/prompt_builder/realization_standard.py` は、realization file に対する標準的な観点を `StructDoc` として組み立てる入口です。
- `build_realization_standard()` は、最小化・高品質化・既存実装整理・抽象化抑制・公開面抑制といった realization 向けの standard をまとめ、`complete_prompt.py` から必要に応じて組み込まれます。
- realization file の実装・保守方針を、prompt 生成側から参照するための目次です。

## Read this when

- realization file に対してどのような標準が定義されているかを確認したいとき。
- `build_realization_standard()` がどの内容を `StructDoc` として返すかを追いたいとき。
- `complete_prompt.py` で realization 向け標準がどの条件で追加されるかを確認したいとき。
- realization file の最小化、重複排除、抽象化の抑制、公開面の増加抑制に関する方針をまとめて把握したいとき。

## Do not read this when

- すでに `build_realization_standard()` を読む目的が決まっていて、このファイル本体を直接確認するとき。
- realization 標準ではなく、`complete_prompt.py`、`oracle_standard.py`、`file_access_rule.py` など別の prompt_builder ファイルを確認したいとき。
- prompt_builder 全体の入口ではなく、個別の標準や補助関数だけを直接見たいとき。

## hash

- 0bf3d056ad8b651989d9df7d94ac46610e634c6e80fcd639976b6ce84015fb4b
