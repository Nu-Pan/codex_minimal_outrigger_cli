# `oracle_and_realization_basic.py`

## Summary
- oracle file と realization file の基本的な役割、分類方法、下位概念を定義する説明部品。oracle doc・oracle src・oracle test、realization code・implementation・test・ancillary への入口として機能する。
- oracle を正本として realization が生成される関係と、uncategorised file の分類対象外条件を確認するための基礎的なルーティング先。

## Read this when
- oracle file と realization file の責務や正本関係を確認するとき
- oracle doc・oracle src・oracle test の区分を判断するとき
- realization implementation・realization test・realization ancillary の範囲を判断するとき
- uncategorised file に該当するパス、ファイル名、git ignore、.git の分類条件を確認するとき

## Do not read this when
- 個別の oracle 文書・oracle 実装・oracle テストの内容を確認したいとき
- 個別の realization 実装・テスト・補助ファイルの具体的な挙動を確認したいとき
- prompt builder の他の部品の責務や、関数の呼び出し手順だけを確認したいとき

## hash
- d7a599e17eb8ec45d03ca644f887031ebca7488d5eca54e06433b4ed3600ee53
