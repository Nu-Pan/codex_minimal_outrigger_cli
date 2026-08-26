# `oracle_and_realization_basic.py`

## Summary
- oracle と realization の基本概念を説明する文章を構築する関数。oracle file、realization file、uncategorised file の役割・下位概念・分類条件をまとめ、パス文脈から得た work-root をプレースホルダーへ渡す。
- oracle と realization に関する基本説明の入口であり、プロンプト生成時にこれらのファイル分類や責務を説明する必要がある場合に参照する。

## Read this when
- oracle file と realization file の責務や正本性をプロンプトへ組み込むとき
- oracle doc・oracle src・oracle test、realization implementation・realization test・realization ancillary の分類を説明するとき
- uncategorised file のパス、git ignore、.git に基づく分類条件を扱うとき
- AgentCallPathContext から work-root を取得し、PlaceholderMap と SDHeader を構築する処理を変更・確認するとき

## Do not read this when
- 特定の oracle または realization ファイルの具体的な仕様・実装内容を確認したいとき
- 基本説明ではなく、oracle と realization の詳細な意味仕様を確認したいときは、本文で参照されている oracle 文書を直接読むとき
- プロンプト構築の別パーツが担う説明だけを変更・確認するとき

## hash
- 511d8460a33e4fdbaee6974af70d500edbc0dd6bf84cca43999301746368ebf4
