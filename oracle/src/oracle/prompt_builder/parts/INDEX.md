# `oracle_and_realization_basic.py`

## Summary
- oracle と realization の基本概念を説明する prompt builder の定義。両者の役割、下位分類、分類条件、および uncategorised file の扱いを、call-scoped な work-root に基づく説明文として構築する。oracle/realization の区別や分類規則を含む動的プロンプトの生成元を確認する際の入口。

## Read this when
- oracle file、realization file、uncategorised file の役割・分類条件を説明するプロンプト生成を変更または調査するとき
- oracle と realization の配置先や正本仕様との関係を、call-scoped context から説明文へ反映する処理を確認するとき

## Do not read this when
- 個別の oracle doc・oracle src・oracle test の内容や仕様を確認するとき
- realization の実装・テストの具体的な挙動を確認するとき
- prompt builder の共通プレースホルダー定義だけを調査するとき

## hash
- 2484b310ef034cd6edba003ae57e1922b6bb1910300925d1afd090a50a54c2a2
