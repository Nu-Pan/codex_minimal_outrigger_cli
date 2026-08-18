# `oracle_and_realization_basic.py`

## Summary
- oracle と realization の基本概念を構築する prompt-builder 部品。両者の役割、下位分類、配置、分類条件に加え、uncategorised file の分類規則をまとめた説明文を生成し、呼び出し側の work-root 定義を埋め込むための入口。

## Read this when
- oracle file と realization file の責務境界や正本関係を確認するとき
- oracle doc・oracle src・oracle test、または realization implementation・realization test・realization ancillary の分類を確認するとき
- uncategorised file のパス、git ignore、.git による分類規則を確認するとき
- work-root を参照する oracle/realization 説明文の生成処理を変更・調査するとき

## Do not read this when
- 個別の oracle 文書・実装・テストの内容そのものを確認したいとき
- realization の具体的な実装責務やテスト実行方法だけを確認したいとき
- INDEX.md や AGENTS.md の分類対象外規則だけを確認したいとき

## hash
- b238ab4dbc923ab8eff0e55865c0538ea751e1d4f50b35dd9c57deefa0472081
