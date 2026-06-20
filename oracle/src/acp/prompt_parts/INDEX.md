# `apply_review_standard.py`

## Summary

- `<cmoc-root>/oracle/src/acp/prompt_parts/apply_review_standard.py` は、`oracle file` の内容を `realization file` に適用する際のレビュー観点を `StructDoc` としてまとめる入口です。
- この断片は、`oracle file` と実装の明確な不整合と、実装上の明確な問題点を切り分ける前提を示し、仕様の隙間は原則として不整合扱いしない方針を含みます。
- あわせて、対象をバグ級の明確な問題に限定し、単なる品質改善案は含めない方針を案内します。

## Read this when

- `oracle file` を `realization file` に適用する際の、レビュー観点や所見の切り分け基準を確認したいとき。
- `oracle` と実装の明確な不整合と、実装上の明確な問題点をどう区別するか整理したいとき。
- 単なる改善提案ではなく、バグ級の要修正点だけを対象にする方針を確認したいとき。

## Do not read this when

- すでに `<cmoc-root>/oracle/src/acp/prompt_parts/apply_review_standard.py` を直接確認する対象が決まっていて、この目次を経由する必要がないとき。
- `apply_audit_finding.py` や `change_summary.py` など、`apply` 系の別段階の prompt 断片を探しているとき。
- `oracle` の正本仕様や開発規約だけを確認したいときで、この prompt 断片の入口が不要なとき。

## hash

- 9315a5b19019a7f90527480b702b4d1159ee66b62e7b6e5b6920ef1536893020

# `complete_prompt.py`

## Summary

- `<cmoc-root>/oracle/src/acp/prompt_parts/complete_prompt.py` は、AI エージェントへ渡す完全な prompt を `StructDoc` の列として組み立てる入口です。
- 必須要素として `role`、`summary`、`goal`、`file_access_rule` を含み、必要に応じて `oracle_and_realization_basic`、`oracle_standard`、`realization_standard`、`apply_review_standard`、`review_oracle_standard` を追加します。
- `structured_output` が有効な場合は、指定された Structured Output schema に従うよう促す出力形式の指示を末尾に追加します。

## Read this when

- 完全な prompt がどの `StructDoc` 断片で構成されるかを確認したいとき。
- `role`、`summary`、`goal`、`file_access_rule` に加えて、どの条件で oracle / realization の基本説明や標準が追加されるかを知りたいとき。
- `structured_output` が有効なときに、末尾へどの出力形式指示が付くかを把握したいとき。
- `prompt_parts/` 配下に新しい断片を追加・整理する前に、完全 prompt の組み立て順を押さえたいとき。

## Do not read this when

- すでに `<cmoc-root>/oracle/src/acp/prompt_parts/complete_prompt.py` を直接確認する対象が決まっていて、この目次を経由する必要がないとき。
- `file_access_rule.py`、`oracle_standard.py`、`realization_standard.py`、`oracle_and_realization_basic.py`、`apply_review_standard.py`、`oracle_review_standard.py` など、組み立て元の断片だけを個別に確認したいとき。
- `prompt_parts/` 全体ではなく、別の `<cmoc-root>/oracle/src` 配下や別フローの入口を探しているとき。

## hash

- adc28fd3f4a7423e9a8a836d2e4d31b0baaf24313dac7d6c8ad5d79588a562da

# `file_access_rule.py`

## Summary

- `<cmoc-root>/oracle/src/acp/prompt_parts/file_access_rule.py` は、`FileAccessMode` に応じたファイル読み書き制約を `StructDoc` として組み立てる入口です。
- `complete_prompt.py` から呼ばれ、`<work-root>` / `<work-root>/oracle` / `<work-root>/memo` の扱いをモードごとに切り替えます。
- 任意の `aux_rules` を末尾に追加できます。

## Read this when

- ファイル読み書き規則の具体的な制約内容を確認したいとき。
- `readonly` / `pure_oracle_read` / `realization_write` / `oracle_write` の違いを整理したいとき。
- `complete_prompt.py` がどのようにアクセス制約文を組み込むか確認したいとき。
- `aux_rules` の付加方法を把握したいとき。

## Do not read this when

- すでに `<cmoc-root>/oracle/src/acp/prompt_parts/file_access_rule.py` を直接確認する対象が決まっていて、この目次を経由する必要がないとき。
- `StructDoc`、`FileAccessMode`、`path_model.py` の定義だけを確認したいとき。
- ファイル読み書き規則ではなく、prompt 全体の構成や別の prompt 断片だけを探しているとき。

## hash

- 3009529bf6223bbaa7725345349674f88b58e0d9e37925c71f4dc6e10cc957d8

# `oracle_and_realization_basic.py`

## Summary

- `<cmoc-root>/oracle/src/acp/prompt_parts/oracle_and_realization_basic.py` は、`oracle file` と `realization file` の基本概念を `StructDoc` としてまとめる入口です。
- このファイルは、両者の定義・役割・下位概念を整理し、`complete_prompt.py` が使う prompt 断片の基礎説明を提供します。
- `prompt_parts/` 配下で、AI 呼び出し用プロンプトの共通前提を確認したいときの起点になります。

## Read this when

- `oracle file` と `realization file` の違い、定義、役割をまとめて把握したいとき。
- `build_oracle_and_realization_basic()` がどのような説明文を組み立てるか確認したいとき。
- `complete_prompt.py` に入る前に、prompt 生成で使う共通前提を整理したいとき。
- `oracle` ツリーとそれ以外のツリーをどう区別するか、基本定義を確認したいとき。

## Do not read this when

- すでに `oracle_and_realization_basic.py` の役割が分かっていて、この目次を経由せずに本体へ直接進むとき。
- `complete_prompt.py`、`file_access_rule.py`、`oracle_standard.py`、`realization_standard.py` など、同じ `prompt_parts` 配下の別ファイルだけを確認したいとき。
- `oracle` 全体の正本仕様や開発規約ではなく、別の階層や別フローの案内を探しているとき。

## hash

- fe33761da72ba70e8745a65b7ba3562e83c07ac65605f824a71f3fadb8996a03

# `oracle_standard.py`

## Summary

- `<cmoc-root>/oracle/src/acp/prompt_parts/oracle_standard.py` は、`oracle file` に対する標準的なレビュー観点を `StructDoc` として組み立てる入口です。
- `build_oracle_standard()` は、認知負荷の節約、正本仕様断片としての扱い、未定義部分の許容、総文字数の最小化、仕様断片間の整合、実装から仕様への逆流禁止、用語・命名の統一、ベストプラクティスより `oracle file` を優先すること、`goal` だけでなく `non-goal` も書くことの推奨をまとめます。
- このファイルは `complete_prompt.py` から `oracle_standard=True` のときに組み込まれ、`oracle` ツリーを根拠にした read-only な prompt の前提となります。

## Read this when

- `oracle file` に対する標準的なレビュー観点を、`StructDoc` としてまとめて把握したいとき。
- `build_oracle_standard()` に含まれる標準項目や、その優先順位・禁止事項を確認したいとき。
- `complete_prompt.py` で `oracle_standard=True` が有効になる前提や、`oracle_standard.py` を修正する前の関連文脈を整理したいとき。

## Do not read this when

- `build_oracle_standard()` の実装内容を、目次を経由せず直接確認したいとき。
- `complete_prompt.py` や `oracle_and_realization_basic.py` など、関連する別ファイルだけを個別に読みたいとき。
- `oracle` ツリー内の共通標準ではなく、個別の正本仕様断片そのものを確認したいとき。

## hash

- 8227d2300002501cc2aaacd55548b6d50d8ca9a960cc85004bd5bd311d8b674e

# `realization_standard.py`

## Summary

- この `realization_standard.py` は、realization file に対する標準的な観点を `StructDoc` として組み立てる入口です。
- `build_realization_standard()` は、総文字数の最小化、高品質化、既存 realization code の整理との一体化、実在する重複または明確な責務境界に基づく抽象化、公開面・設定面・状態の増加抑制といった観点をまとめます。
- このファイルは、`complete_prompt.py` から必要に応じて組み込まれる realization 向け標準の目次として機能します。

## Read this when

- realization file に対する標準的な実装・保守方針をまとめて把握したいとき。
- `build_realization_standard()` がどのような `StructDoc` を組み立てるか確認したいとき。
- `complete_prompt.py` で realization 向け標準がどの条件で追加されるかを確認したいとき。
- realization file の最小化、重複排除、既存実装整理、抽象化の抑制、公開面や状態の増加抑制に関する指針を確認したいとき。

## Do not read this when

- すでに `build_realization_standard()` の役割や返却内容が分かっていて、このファイル本体を直接確認するとき。
- `complete_prompt.py`、`oracle_standard.py`、`file_access_rule.py` など、別の prompt 断片や関連ヘルパーだけを確認したいとき。
- realization 標準そのものではなく、`Standard` や `Requirement` の共通定義、または `StructDoc` のレンダリング基盤だけを確認したいとき。
- `realization` 向けの方針ではなく、`oracle` 側の標準や別サブコマンドの呼び出し仕様を探しているとき。

## hash

- 138f10f02b35c5fcec377f6b663c09a2596beddffc01938231bbe2910d99a8f3

# `oracle_review_standard.py`

## Summary

- この `oracle_review_standard.py` のルーティング文書で、`build_review_oracle_standard()` への入口です。
- `cmoc review oracle` で使うレビュー観点の正本として、`fatal` と `minor` の判定基準、対象外の条件、汎用的なレビュー観点としての扱いを案内します。
- `codex exec` のプロンプトに注入する、リポジトリ固有の事情に依存しないレビュー観点の定義をまとめます。

## Read this when

- `cmoc review oracle` の所見分類基準や、`fatal` / `minor` の切り分けを確認したいとき。
- 仕様断片同士の明確な矛盾や、実装者の裁量で解消不能な問題をどう扱うか整理したいとき。
- 誤字・脱字・用語不統一・表記揺れなどの単純な問題を、レビュー対象に含めるか確認したいとき。
- `oracle file` だけでは問題と言い切れないものや、仕様から実装が一意に定まらないものを除外する条件を確認したいとき。

## Do not read this when

- すでに `build_review_oracle_standard()` を直接確認する対象が決まっていて、この目次を経由する必要がないとき。
- `enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py` など、別の review oracle を確認したいとき。
- `cmoc review oracle` の所見リストや Structured Output schema ではなく、別サブコマンドや別階層の仕様を探しているとき。

## hash

- ef82dafc4a59d85457c1f90e00878089b078449fcd6ed481e828b982594baa81
