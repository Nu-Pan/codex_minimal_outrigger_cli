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
- レビュー用 oracle 所見処理の realization 側入口をまとめる package。所見列挙、統合、判定、advocate/challenger 検証に使う agent call parameter 生成または再公開の経路を扱う。
- 正本側 builder の返却値を基本的に維持しつつ、レビュー基準や対象 oracle file 本文の追記、静的な oracle root 表記の最小補正など、prompt まわりの互換調整を行う実装が含まれる。
- 多くの対象は正本側実装への薄い再公開または wrapper であり、この階層自体はレビュー基準や finding 判定意味論の正本ではなく、realization 側から正本由来機能へ到達するための境界として位置づく。

## Read this when
- レビュー用 oracle 所見の列挙・統合・判定・検証で、realization 側の import path からどの正本側 builder や検証機能へ到達するかを確認したいとき。
- 正本側 agent call parameter の model、reasoning、file access、structured output 指定などを保ったまま、prompt だけをどのように補正または追記しているかを調べたいとき。
- 対象 oracle file 本文やレビュー基準が、所見列挙用 prompt にどのように付加されるかを確認したいとき。
- oracle root 表記 typo や placeholder 表記の補正が、静的文面だけに限定され、finding や既知理由などの動的入力を改変しないことを確認したいとき。
- レビュー用 oracle builder まわりの互換 import 境界を変更・削除してよいか判断するために、この階層が独自実装を持つのか再公開だけなのかを切り分けたいとき。

## Do not read this when
- レビュー基準そのもの、finding の意味判定、重複判定、advocate/challenger 検証の正本プロンプト本文を理解したいとき。委譲先の正本側本文を読む。
- AgentCallParameter 型、model class、reasoning effort、file access mode、structured output schema の一般仕様を確認したいとき。共通定義側を読む。
- oracle file と realization file の基本概念、oracle root などのパスモデル全体、または正本仕様断片そのものを確認したいとき。該当する基本仕様や path model 側へ進む。
- レビュー処理全体の CLI 出力仕様、テスト観点、またはこの階層以外の builder 責務を調べたいとき。より上位のレビュー実装または該当責務の本文へ進む。
- 互換 package の存在理由だけを確認したい場合を除き、公開 API を持たない package 境界そのものを詳細に読む必要はない。

## hash
- 45ee102ec468e32188e0f64dd6b873272f43d0f7a28fb2f45b4c393f875a89b5
