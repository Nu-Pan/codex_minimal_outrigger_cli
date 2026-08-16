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

# `policy_definitions.py`

## Summary
- `Policy` オブジェクトとして定義された、oracle と realization の扱い、仕様レビュー、検証、conflict 解消、editor handoff、INDEX.md ルーティングに関する全用途の規範を集約する。各 policy は識別子・題名に加え、要求・禁止・許可された判断境界を表し、関連する正本仕様や実装作業から参照するための共通入口となる。

## Read this when
- oracle file の権威性、仕様解釈、未定義事項、正本仕様間の整合性を確認するとき
- realization の実装・テスト・検証方針や、仕様適合性・レビュー所見の基準を確認するとき
- conflict marker の解消、editor handoff、または INDEX.md エントリー作成の規範を確認するとき

## Do not read this when
- 個別の oracle file や realization file の具体的な要求・挙動だけを確認する場合
- この定義を参照する必要がなく、対象作業が通常の実装詳細や単一のテストケースに限定される場合

## hash
- 4da502b2bb284ccd308837b5e56ceea067ecefff946d3240a92d7a377064d865
