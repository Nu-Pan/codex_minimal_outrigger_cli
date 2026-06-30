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
- review oracle 周辺の agent call parameter builder と、旧来 import 経路を保つ互換層をまとめる階層。正本側 builder への委譲、prompt placeholder の暫定補正、互換 module の残置理由と削除条件を扱う。
- レビュー指摘の列挙・判定・検証・merge finding に関する実装入口があるが、多くは実装本体ではなく canonical oracle 側への再公開または薄い wrapper として位置づけられる。

## Read this when
- review oracle 系の agent call parameter 生成処理を調査・変更したいとき。
- 正本側 builder の出力を realization 側でどのように補正しているか、特に oracle root placeholder 表記の暫定補正を確認したいとき。
- レビュー指摘の列挙・判定・検証に関する旧来 import 経路が残っている理由、委譲先、削除条件を確認したいとき。
- 同名機能の実装が realization 側にあるように見えるが、実体が canonical oracle 側か薄い wrapper かを切り分けたいとき。

## Do not read this when
- review oracle の正本仕様断片そのもの、prompt の正本文面、判定仕様、検出ロジックを確認したいときは、対応する oracle file または canonical 実装を読む。
- agent call parameter の基礎データ構造、model、reasoning effort、file access mode などの共通仕様を調べたいときは、基礎定義側を読む。
- 互換 import 経路や review oracle builder と無関係な CLI 表示、テスト方針、review 機能全般を調べたいときは、より直接その責務を持つ対象へ進む。

## hash
- 970b5b4cebe0698ddd6ee2e13b4b8bbc5afab4ecd7fe0dc2d7d1b99292896ed7
