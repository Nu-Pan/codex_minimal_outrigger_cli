# `oracle_and_realization_basic.py`

## Summary
- oracle と realization の分類境界、および両者の役割を定義する基本説明文を構築する。
- oracle 側では oracle doc・oracle src・oracle test、realization 側では realization code・implementation・test・ancillary の下位概念を整理する。
- call-scoped context から work-root の定義を取得し、説明文中のプレースホルダーへ渡す処理を含む。

## Read this when
- oracle file と realization file の分類規則や責務を確認するとき。
- oracle doc/src/test と realization implementation/test/ancillary の区分を確認するとき。
- oracle と realization に関する基本説明文の生成経路を変更・調査するとき。

## Do not read this when
- oracle と realization の分類や基本概念を扱わず、別の prompt_builder part を直接確認すべきとき。
- 具体的な分類アルゴリズムやテスト実装を確認する場合に、対応する実装・テスト対象へ直接進めるとき。

## hash
- 7d70bb60c470aff3275d9de18ec27d6b68d9da9fab51e7cf7a7608aa58964008
