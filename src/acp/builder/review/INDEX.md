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
- review oracle builder 周辺で、旧 import 経路の互換層と一部の agent call parameter 生成 wrapper をまとめる階層。多くは canonical oracle 側実装への再公開または委譲で、実体ロジックよりも移行中の import 互換性、暫定 prompt 補正、削除条件を扱う。

## Read this when
- review oracle builder の旧経路 import が canonical oracle 側へどう委譲されているか確認したいとき。
- review finding enumeration、judgment、validation、merge finding の互換 module や薄い wrapper の残存理由、移行状況、削除条件を調べたいとき。
- 正本側 builder の出力を realization 側で最小補正して agent call parameter を生成している箇所を探したいとき。

## Do not read this when
- review finding の判定仕様、検証ロジック、prompt 正本文面など、挙動本体や正本仕様を確認したいときは canonical oracle 側または対応する oracle file を読む。
- agent call parameter の基礎構造、共通 model 設定、file access mode などの一般仕様を確認したいときは基礎定義側を読む。
- review 全体の builder 構成や、この階層にない別種の review 処理を調べたいときは、より上位または該当する対象へ進む。

## hash
- af1dc93a74559b4fada9eb5a2266a8362f76b2ed3699b0d4239f039390a81b02
