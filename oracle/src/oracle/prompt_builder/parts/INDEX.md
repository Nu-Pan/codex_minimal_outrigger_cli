# `oracle_and_realization_basic.py`

## Summary
- agent向けプロンプトに、oracle file・realization file・uncategorised file の役割、下位区分、基本的な分類方法を渡す文面を組み立てる。root の work-root 定義を使ったパス上の区分も含む。
- これらの概念をプロンプトで確認する入口。各ファイル種別の作業判断基準や、列挙処理の詳細を定めるものではない。

## Read this when
- agent向けの説明における oracle・realization・uncategorised file の役割や分類境界を調べる、またはその説明文面を変更するとき。
- プロンプトに渡される基本説明と、正本の意味仕様との対応を確認するとき。

## Do not read this when
- 分類の意味仕様そのものや、実際の列挙・git ignore 判定の詳細を確認するときは、対応する oracle 文書を読む。
- oracle file や realization file を扱う作業上の判断基準を確認するときは、それぞれの判断方針を読む。
- プロンプト全体の組み立て順序や共通構造だけを調べるときは、全体を組み立てる側を読む。

## hash
- b51458d36449660e20004b1a282e16ccf5417f7ae3bfda9449b75899e6513d97
