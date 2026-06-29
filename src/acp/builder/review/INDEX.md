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
- レビュー用 oracle 機能を realization 側の互換 import 経路から参照するための薄い入口群をまとめる package。多くは正本側実装の再公開だけを担い、一部は AgentCallParameter 生成後の prompt に含まれる oracle root 表記だけを局所補正する。
- finding の列挙・判定・検証・merge について、realization 側コードが正本側の review oracle 実装へ到達する境界を確認するための起点になる。

## Read this when
- review oracle 関連処理を呼び出す realization 側 import 経路が、正本側実装へどう委譲されているかを俯瞰したいとき。
- finding の列挙、判定、検証、merge の入口が独自実装なのか再公開なのかを切り分けたいとき。
- review oracle 用 AgentCallParameter の生成後に、prompt 内の oracle root 表記を一時的に補正している箇所を探すとき。
- 正本側の typo や placeholder 表記不具合が解消された後に、互換補正 wrapper を削除できるか判断したいとき。

## Do not read this when
- finding の列挙条件、判定基準、検証プロンプト、merge prompt の正本内容を理解したいとき。その場合は委譲先の正本側実装や対応する oracle file を読む。
- AgentCallParameter 型の共通構造、model_class、reasoning_effort、file_access_mode、structured output schema の一般仕様を調べたいとき。
- review oracle 全体の設計意図、検出対象、出力仕様を確認したいとき。より上位の正本仕様または該当責務の本文へ進む。
- 再公開や局所的な prompt 補正ではない、レビュー処理本体や CLI 出力処理の実装を探しているとき。

## hash
- 07338706edd3154067d973bcd33cdb0317183771bab40f081e1f92ad539bf3b1
