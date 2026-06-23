# `apply_review_standard.py`

## Summary

- `<cmoc-root>/oracle/src/acp/prompt_parts/apply_review_standard.py` は、`oracle file` の内容を `realization file` に適用する場面で使うレビュー標準を `StructDoc` として組み立てる入口です。
- この断片は、明確な不整合を所見として扱うこと、仕様の隙間だけを根拠に過剰な指摘をしないこと、`realization file` だけから見て明らかな致命的問題を扱うことを整理します。
- `complete_prompt.py` では `apply_review_standard=True` のときに追加され、`cmoc apply fork` の所見列挙を支える前提になります。

## Read this when

- `cmoc apply fork` で、`oracle file` を `realization file` に適用する際のレビュー標準を確認したいとき。
- `oracle file` と `realization file` の不整合を、どこまで所見として扱うか整理したいとき。
- `complete_prompt.py` で `apply_review_standard=True` のときに追加される内容を把握したいとき。

## Do not read this when

- すでに `<cmoc-root>/oracle/src/acp/prompt_parts/apply_review_standard.py` を直接開いて、実装本体や規範文の詳細を確認するとき。
- `complete_prompt.py` への組み込み条件や `cmoc apply fork` での所見列挙の全体像を、この断片経由ではなく別の場所で追いたいとき。
- `oracle_review_standard.py` など、このファイル以外のレビュー標準を探しているとき。

## hash

- 8084bdb3ce48e798cad1515dc50a8d5c7d66c417ec7d2d32494a4d68d6b43799

# `complete_prompt.py`

## Summary

- `<cmoc-root>/oracle/src/acp/prompt_parts/complete_prompt.py` は、`build_complete_prompt()` で AI エージェントへ渡す完全な prompt を `StructDoc` の列として組み立てる入口です。
- 必須要素として `role`、`summary`、`goal`、`file_access_rule`、`routing_rule` を含み、必要に応じて `oracle_and_realization_basic`、`oracle_standard`、`realization_standard`、`review_oracle_standard`、`apply_review_standard`、`index_entry_standard` を追加します。
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

- 18efdddfcbec9b291f2ca8aac02f42177f6c4fe051e13b6d1953fd1ea9afcc9f

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

- この `index_entry_standard.py` は、`INDEX.md` の各エントリーが従うべきルーティング規範を `StructDoc` として組み立てる入口です。
- 対象を読むべき条件、対象の責務、同階層の別対象ではなくここへ進む理由を、最小限の意味情報でまとめます。
- 機械的に補える情報ではなく、対象を読む判断に必要な意味情報だけを扱います。

## Read this when

- `INDEX.md` の各エントリーに何を書くべきか、読む対象への導線の作り方を確認したいとき。
- `cmoc indexing` で使う目次文の規範や、`complete_prompt.py` がこの断片を組み込む条件を把握したいとき。
- 対象本文を読む前に、ルーティング情報としての役割だけを確認したいとき。

## Do not read this when

- すでにこのファイル本体を直接確認する対象が決まっていて、目次を経由する必要がないとき。
- Structured Output schema や生成結果の項目名・型・形式だけを確認したいとき。
- `INDEX.md` エントリーではなく、別の prompt 断片や別サブコマンドの仕様を探しているとき。

## hash

- 9948bdff6712106ea91119db4a9fbd06529bf36046318db4e3adb5863e9c5fb0

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

- `<cmoc-root>/oracle/src/acp/prompt_parts/oracle_review_standard.py` は、`build_review_oracle_standard()` を起点に `cmoc review oracle` 向けのレビュー標準を `StructDoc` として組み立てる入口です。
- 仕様断片同士の明確な矛盾や、実装者の裁量では解消できない問題を fatal 所見として扱い、誤字・脱字・用語不統一などの単純な問題を minor 所見として扱う方針をまとめます。
- 仕様の隙間や推測だけでは所見にしない、というレビューの境界条件を示します。

## Read this when

- `cmoc review oracle` の所見分類基準を確認したいとき。
- fatal と minor の切り分けや、レビュー対象外の条件を整理したいとき。
- `build_review_oracle_standard()` がどの観点を `StructDoc` にまとめるか把握したいとき。

## Do not read this when

- すでに `<cmoc-root>/oracle/src/acp/prompt_parts/oracle_review_standard.py` を直接確認する対象として決まっていて、目次を経由する必要がないとき。
- `enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py` など、別の review 断片を探しているとき。
- `cmoc review oracle` ではなく、別サブコマンドや別階層の仕様を確認したいとき。

## hash

- 1404f2566c5a97fa55822658a9003371e37b786d40ea67b3c81e64c0d013c436

# `oracle_standard.py`

## Summary

- `<cmoc-root>/oracle/src/acp/prompt_parts/oracle_standard.py` は、`oracle file` に対する標準的なレビュー観点を `StructDoc` として組み立てる入口です。
- `build_oracle_standard()` は、認知負荷の節約、正本仕様断片としての扱い、未定義部分の許容、総文字数の最小化、仕様断片間の整合、実装から仕様への逆流禁止、用語・命名の統一、ベストプラクティスより `oracle file` を優先すること、`goal` だけでなく `non-goal` も書くことの推奨をまとめます。
- このファイルは `complete_prompt.py` から `oracle_standard=True` のときに組み込まれ、`oracle` ツリーを根拠にした read-only な prompt の前提となります。

## Read this when

- `oracle file` に対する標準的なレビュー観点を、`StructDoc` としてまとめて把握したいとき。
- `build_oracle_standard()` に含まれる標準項目や、その優先順位・禁止事項を確認したいとき。
- `complete_prompt.py` で `oracle_standard=True` が有効になる前提や、この標準を修正する前の関連文脈を整理したいとき。

## Do not read this when

- すでに `<cmoc-root>/oracle/src/acp/prompt_parts/oracle_standard.py` を直接確認する目的が決まっていて、目次の案内が不要なとき。
- `complete_prompt.py` や `oracle_and_realization_basic.py` など、関連する別の prompt 断片だけを確認したいとき。
- `oracle` ツリー内の個別の正本仕様断片ではなく、`prompt_parts/` 全体の入口だけを探しているとき。

## hash

- 0a349edcd2226daeb977cfec784977f7ba675274ecc1267c01a68e304d36871a

# `realization_standard.py`

## Summary

- <cmoc-root>/oracle/src/acp/prompt_parts/realization_standard.py は、realization file に求める標準方針を StructDoc として組み立てる入口です。
- 総文字数の最小化、重複排除、既存実装の整理、明確な責務境界に基づく抽象化を中心に、実装・保守の判断基準をまとめます。
- 公開面・設定面・状態・テストの増加を抑えつつ、変更後に削除・統合・短縮できるものが残っていないかを確認する観点も含みます。

## Read this when

- realization file の削減すべき重複や、増やすべきでない公開面をまとめて把握したいとき。
- 新しい実装、抽象化、テスト、依存関係、状態追加の可否を判断したいとき。
- 変更後に削除・統合・短縮の余地があるかを確認したいとき。
- complete_prompt.py にこの標準が追加される前提を把握したいとき。

## Do not read this when

- すでに <cmoc-root>/oracle/src/acp/prompt_parts/realization_standard.py を直接開いて、本体の定義を確認するとき。
- 個別の helper、class、テストケース、import の整理だけを確認したいとき。
- oracle 側の正本仕様や別の標準、あるいはファイル読み書き規則を探しているとき。
- prompt_parts/ 全体ではなく、別のディレクトリや別フローの案内を探しているとき。

## hash

- 7b4ad34a5e4ad05a6dff26576b4398c32d5c504fb773c14299c0a5ef1b5be1a0

# `routing_rule.py`

## Summary

- `<cmoc-root>/oracle/src/acp/prompt_parts/routing_rule.py` は、AI エージェントが `INDEX.md` をヒントに必要な文章へ進むための固定規則を `StructDoc` として組み立てる入口です。
- `INDEX.md` を本文の代替ではなくルーティング情報として扱い、`Summary`、`Read this when`、`Do not read this when` から読む先を選ぶ方針をまとめます。
- `complete_prompt.py` では常に追加され、個別の標準フラグに依存せず agent 呼び出しの共通前提になります。

## Read this when

- agent prompt に固定挿入される `INDEX.md` の読み進め規則を確認したいとき。
- `build_complete_prompt()` がなぜ `routing_rule` を常に含めるか把握したいとき。
- `INDEX.md` エントリーの書き方ではなく、利用時にどう読むかの規則を確認したいとき。

## Do not read this when

- `INDEX.md` エントリー自体の生成規範を確認したいときは、`index_entry_standard.py` を読むべきとき。
- ファイル読み書き制約、oracle/realization の基本定義、レビュー標準など、別の prompt 断片だけを探しているとき。
- `INDEX.md` の配置対象や生成・更新手順を確認したいときは、app spec 側の indexing 仕様を読むべきとき。

## hash

- c3f89bf3c1b0ef3a19cfd0d7d7aee2e3b0ceb8314b7b32ca4551ec3977ecd2da
