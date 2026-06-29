# `__init__.py`

## Summary
- oracle.acp_builder.review と互換の package であることだけを示す、review builder 領域の package 初期化用ファイル。実装ロジックや詳細な仕様ではなく、互換名前空間としての位置づけを確認する入口になる。

## Read this when
- review builder 領域で、oracle 側の同名 package と対応する realization package が存在するかを確認したいとき。
- package としての互換性や import 経路の成立だけを確認したいとき。

## Do not read this when
- review builder の具体的な処理、関数、クラス、出力、制御フローを調べたいとき。
- 正本仕様断片としての review builder の要求を調べたいとき。
- package 初期化以外の実装変更先を探しているとき。

## hash
- adf6124f1c3a49a136159186b6a58b39f4321e0113527b60e85d8b1e3205484e

# `oracle`

## Summary
- review oracle に関する realization 側の互換入口をまとめた階層。多くは正本側実装を再公開するだけで、finding の列挙・判定・challenger 検証の実体は持たない。
- 所見マージと所見擁護検証の agent call parameter 生成では、正本側 builder の戻り値を使い、実行前に prompt 内の oracle root token 表記だけを最小補正する。
- review oracle の処理本体や正本仕様ではなく、realization 側の import path から正本由来の review oracle 機能へ到達するための境界を扱う。

## Read this when
- realization 側から review oracle の finding 列挙・判定・検証・所見マージ機能が、どの正本側実装へ委譲されるか確認したいとき。
- review oracle 関連の import path を変更・削除してよいか判断するために、互換入口としての役割を確認したいとき。
- 所見マージまたは所見擁護検証の実行用 parameter 生成で、正本側 builder の戻り値に対してどの prompt token 補正が加わるか確認したいとき。
- この階層の module が独自の review ロジックを持つのか、正本側実装の再公開または最小補正に留まるのかを切り分けたいとき。

## Do not read this when
- finding 列挙・finding 判定・challenger 検証の具体的な処理内容、入出力、判定基準を理解したいとき。その場合は委譲先の正本側実装を読む。
- 所見マージや所見擁護検証の prompt 正本内容、structured output schema、review oracle の仕様断片を確認したいとき。正本側の対応する oracle src や関連 doc を読む。
- review 実行全体の制御フロー、CLI の入出力、agent call parameter の共通型定義や属性の意味を調べたいとき。より上位または共通定義の本文へ進む。
- oracle file の typo 修正提案や正本仕様の変更可否を判断したいとき。この階層は実行側の最小補正境界を示すだけで、正本変更の根拠を扱わない。

## hash
- 25f48ce6091efed3854a9d49eda78cc592ee9447656c567adaf9de8201bbf5ec
