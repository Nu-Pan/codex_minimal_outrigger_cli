# `oracle_and_realization_basic.py`

## Summary
- oracle と realization の基本概念を説明するプロンプト断片を構築する関数。oracle file を人間所有の正本仕様、realization file をその具体化、uncategorised file を分類対象外として整理し、それぞれの役割・下位概念・分類条件を定義する。oracle と realization の説明文を組み立てる必要がある場合の入口となる。

## Read this when
- oracle と realization の役割や分類方法を説明するプロンプトを変更・確認するとき
- oracle doc・oracle src・oracle test、realization implementation・realization test・realization ancillary の定義を確認するとき
- oracle file、realization file、uncategorised file の分類条件を扱うとき

## Do not read this when
- oracle と realization の正本仕様そのものを確認する必要があるときは、参照先として示された oracle 文書を直接読む場合
- この関数が組み立てる説明内容ではなく、個別の prompt builder 部品や PlaceholderMap・SDHeader の実装を確認するときは、それぞれの対象を直接読む場合
- INDEX.md や AGENTS.md など分類対象外ファイルの扱いだけを確認するとき

## hash
- b9de13219cbc0a8734a98b60d82e1841da9c0d602bf9c108f8a8e800d003f7e6
