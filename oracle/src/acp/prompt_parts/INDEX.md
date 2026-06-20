# `apply_review_standard.py`

## Summary

- `<cmoc-root>/oracle/src/acp/prompt_parts/apply_review_standard.py` は、`oracle file` の内容を `realization file` に適用する場面で使うレビュー標準を `StructDoc` として組み立てる入口です。
- この断片は、明確な不整合の指摘、仕様の隙間だけを根拠にした過剰な指摘の禁止、`realization file` だけから見たバグ級の明確な問題の扱いを整理します。
- `complete_prompt.py` では `apply_review_standard=True` のときに追加され、`cmoc apply fork` の所見列挙を支える前提になります。

## Read this when

- `cmoc apply fork` で `oracle file` を `realization file` に適用する際のレビュー観点を確認したいとき。
- `oracle file` と `realization file` の不整合を、どこまで要修正点として扱うか整理したいとき。
- 単なる改善提案ではなく、バグ級の明確な問題だけをレビュー対象にしたいとき。
- この断片を `complete_prompt.py` へ組み込む前に、役割を把握したいとき。

## Do not read this when

- すでに `<cmoc-root>/oracle/src/acp/prompt_parts/apply_review_standard.py` を直接確認する目的が決まっていて、目次の案内が不要なとき。
- `change_summary.py`、`file_audit_finding.py`、`refine_fixing_point.py` など、`apply` 系の別断片を探しているとき。
- `oracle` の正本仕様や `review_oracle_standard.py` だけを確認したいときで、この適用レビュー標準が不要なとき。

## hash

- 620ee33defb76cfcf77a1c369188426e09cf7193c0cf46e2d7d3b7e3650f6309

# `complete_prompt.py`

## Summary

- `<cmoc-root>/oracle/src/acp/prompt_parts/complete_prompt.py` は、`build_complete_prompt()` で AI エージェントへ渡す完全な prompt を `StructDoc` の列として組み立てる入口です。
- 必須要素として `role`、`summary`、`goal`、`file_access_rule` を含み、必要に応じて `oracle_and_realization_basic`、`oracle_standard`、`realization_standard`、`review_oracle_standard`、`apply_review_standard`、`index_entry_standard` を追加します。
- `structured_output` が有効な場合は、指定された Structured Output schema に従うよう促す出力形式の指示を末尾に追加します。

## Read this when

- 完全な prompt がどの `StructDoc` 断片で構成されるかを把握したいとき。
- `role`、`summary`、`goal`、`file_access_rule` に加えて、どの条件で `oracle` / `realization` の基本説明や標準、レビュー観点が追加されるか確認したいとき。
- `structured_output` が有効なときに、末尾へどの出力形式指示が付くかを確認したいとき。
- `INDEX.md` 目次を追加・整理する前に、`build_complete_prompt()` の組み立て順と依存関係を押さえたいとき。

## Do not read this when

- すでに `<cmoc-root>/oracle/src/acp/prompt_parts/complete_prompt.py` を直接確認する対象が決まっていて、目次を経由せず本体へ進むとき。
- `file_access_rule.py` や `oracle_standard.py` など、個別の prompt 断片だけを確認したいとき。
- `prompt_parts/` 全体ではなく、別の `src` 配下や別フローの入口を探しているとき。

## hash

- f8fbbc947eb7ac120513580612636fd8f155ed1113c57dc98d717814ead98a2c

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

# `index_entry_standard.py`

## Summary

- `<cmoc-root>/oracle/src/acp/prompt_parts/index_entry_standard.py` は、`INDEX.md` のエントリーが従うべき規範文を `StructDoc` としてまとめる入口です。
- この断片は、`INDEX.md` エントリーを読むべき対象へのルーティング情報として扱い、`summary`、`read_this_when`、`do_not_read_this_when` に何を書くかの方針を示します。
- `complete_prompt.py` から `index_entry_standard=True` のときに組み込まれ、`cmoc indexing` の目次情報生成を支える前提になります。

## Read this when

- `INDEX.md` の各エントリーに何を書けばよいか、要約・読む条件・読まなくてよい条件の書き方を確認したいとき。
- `cmoc indexing` で生成する目次情報のルーティング方針を把握したいとき。
- `complete_prompt.py` で `index_entry_standard=True` のときにどの規範が追加されるか確認したいとき。

## Do not read this when

- すでに `<cmoc-root>/oracle/src/acp/prompt_parts/index_entry_standard.py` 自体を直接確認する対象が決まっていて、この目次を経由する必要がないとき。
- `cmoc indexing` の出力 JSON 形式や Structured Output schema だけを確認したいとき。
- `complete_prompt.py` や他の prompt 断片の役割ではなく、別のサブコマンドや別階層の案内を探しているとき。

## hash

- b686cf3efbae97576f9d9511869eaf6ade20633a3fa9390705c69c498dc3f02e

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

# `oracle_review_standard.py`

## Summary

- `<cmoc-root>/oracle/src/acp/prompt_parts/oracle_review_standard.py` は、`build_review_oracle_standard()` を起点に `cmoc review oracle` 向けのレビュー観点を `StructDoc` としてまとめる入口です。
- 仕様断片同士の明確な矛盾や、実装者の裁量では解消できない問題を fatal 所見として扱う方針を案内します。
- 誤字・脱字・用語不統一などの単純な問題を minor 所見として扱い、仕様の隙間や推測だけでは所見にしない方針を示します。

## Read this when

- `cmoc review oracle` の所見分類基準を確認したいとき。
- fatal と minor の切り分けや、レビュー対象外の条件を整理したいとき。
- `build_review_oracle_standard()` がどの観点を `StructDoc` にまとめるか把握したいとき。

## Do not read this when

- すでに `<cmoc-root>/oracle/src/acp/prompt_parts/oracle_review_standard.py` を直接読む対象として決めていて、目次を経由する必要がないとき。
- `enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py` など、別の review 断片を探しているとき。
- `cmoc review oracle` ではなく、別サブコマンドや別階層の仕様を確認したいとき。

## hash

- 62c948874b421e1bb2e35dfd2c116f1855d6b94114001a16b8e616fafae9044b

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

- 実装系の標準的な方針をまとめ、読むべき観点の入口になる。
- 総文字数の最小化、重複排除、既存実装の整理、明確な責務境界に基づく抽象化を案内する。
- 公開面・設定面・状態の増加、テストの肥大化、依存関係や補助生成物の増加を抑える方針を含む。
- 変更完了時に削除・統合・短縮できるものが残っていないかを確認する観点も扱う。

## Read this when

- 実装・保守の指針として、削減すべき重複や増やすべきでない公開面をまとめて把握したいとき。
- 新しい実装、抽象化、テスト、依存関係、状態追加の可否を判断したいとき。
- 変更後に削除・統合・短縮の余地があるかを確認したいとき。
- 完全な prompt にこの標準を含める条件を確認したいとき。

## Do not read this when

- すでにこの標準の役割が分かっていて、本文を直接確認したいとき。
- 個別の helper、クラス、テストケースだけを確認したいとき。
- 標準ではなく、共通型やレンダリング基盤の定義を探しているとき。
- 別の標準やファイル読み書き規則を確認したいとき。

## hash

- 50527499f8c0d6014d6ddff4b9304061725fba0e147c176b033a9e7e7d2728d7
