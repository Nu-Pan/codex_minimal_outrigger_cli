# `oracle_and_realization_basic.py`

## Summary
- oracle file、realization file、uncategorised file の基本概念と分類規則を説明する prompt 構造を構築する関数。
- oracle doc・oracle src・oracle test と realization implementation・realization test・realization ancillary の役割、配置、正本責務、委譲、優先関係を下位要素としてまとめる。
- path_context から work-root を取得し、説明文中のプレースホルダーを埋めるための PlaceholderMap と、階層化された SDHeader を返す。
- 個別の仕様本文ではなく、oracle と realization の一般的な関係およびファイル分類を参照する入口にあたる。

## Read this when
- oracle と realization の基本的な役割や正本関係を確認したいとき
- oracle doc・oracle src・oracle test、realization implementation・realization test・realization ancillary の分類や配置を確認したいとき
- oracle file から realization file が生成される関係、委譲された詳細の優先関係を確認したいとき
- uncategorised file の分類条件を確認したいとき
- oracle と realization の基本説明を prompt builder で構築する処理を変更・調査するとき

## Do not read this when
- 個別の意味仕様を確認したいときは、対応する oracle doc を直接読む
- oracle src に委譲された正確な実装・定義を確認したいときは、その oracle src を直接読む
- PlaceholderMap や SDHeader の共通仕様・実装だけを確認したいときは、対応する共通部品を直接読む
- prompt 全体の組み立て順序や、この関数以外の prompt 部品を確認したいときは、該当する prompt builder の対象を直接読む

## hash
- a8f01202b02f0358bc605299721a4f5d3ef0dc40bcdd6492a3fe50932ca828bb
