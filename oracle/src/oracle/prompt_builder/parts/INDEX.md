# `oracle_and_realization_basic.py`

## Summary
- oracle と realization の基本概念を説明する prompt builder の構成部品。両者の役割、下位分類、分類条件、および uncategorised file の定義を、call-scoped な work-root を埋め込んだ構造化文書ヘッダーとして生成する。oracle/realization の責務境界やファイル分類に関するプロンプト生成経路を確認するときの入口となる。

## Read this when
- oracle と realization の基本説明を含むプロンプト部分の生成・変更を調べるとき
- oracle file、realization file、uncategorised file の分類規則や下位概念の説明元を確認するとき
- path context から work-root を取得して構造化文書へ渡す処理を確認するとき

## Do not read this when
- oracle または realization の具体的な仕様本文・実装・テストそのものを確認したいとき
- prompt builder の別の説明部品や、基本知識以外のプロンプト構築処理を直接調べるとき
- 既に生成済みのプロンプト文面だけを確認すれば足り、生成元の構造化ヘッダーを調べる必要がないとき

## hash
- bac939e8e47bd31e60228450037f2f42375d84a52c0c674afe14c8d773a35594
