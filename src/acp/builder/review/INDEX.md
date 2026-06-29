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
- レビュー oracle 領域の realization 側互換入口をまとめる package。多くの対象は正本側実装の再公開や薄い委譲であり、finding の列挙・判定・検証、merge finding や所見擁護検証の agent call parameter 生成経路へ、実装側 import path から到達するための境界として機能する。
- 一部の builder は正本側の生成結果を保ったまま prompt 内の path token や oracle root 表記だけを最小補正するため、review oracle の実行用 parameter 生成で realization 側補正の有無と範囲を確認する入口になる。

## Read this when
- realization 側から review oracle の finding 列挙・判定・検証機能がどの正本側実装または公開経路へ委譲されるかを確認したいとき。
- review oracle 用の merge finding や所見擁護検証の AgentCallParameter 生成で、正本側 builder の戻り値に対して prompt だけを補正する箇所を探したいとき。
- この階層の module が独自ロジックを持つのか、互換 import 境界として正本側実装を再公開するだけなのかを切り分けたいとき。
- oracle root プレースホルダーや path token の表記差が、review oracle の実行経路でどこまで補正されるかを確認したいとき。

## Do not read this when
- finding の列挙・判定・検証ロジックそのもの、入力・出力・判定基準、prompt 本文、structured output schema の正本内容を理解したいとき。その場合は委譲先の正本側 oracle src や関連 doc を読む。
- AgentCallParameter 型、モデル選択、reasoning effort、file access mode などの共通仕様を調べたいとき。その場合は共通 parameter 定義へ進む。
- review oracle 全体の設計、CLI の入出力、oracle file と realization file の基本概念、またはパスモデル全体を確認したいとき。より上位または該当責務の本文を読む。
- 公開 API の詳細な関数・クラス実装や、finding 以外の review 処理を探しているとき。この階層は主に互換入口と限定的な prompt 補正を扱う。

## hash
- 7c819a224c762eea3c1a2f9a0faa3b0f86ae1de8a9e49d79560bedbbecf0098a
