# `__init__.py`

## Summary
- `oracle.acp_builder.review.oracle` 互換名前空間を成立させるための package 初期化ファイル。本文は互換 package であることだけを示し、レビュー処理や oracle 内容そのものは持たない。

## Read this when
- 互換 import 経路として `oracle.acp_builder.review.oracle` 名前空間が存在する理由を確認したいとき。
- この階層が実処理を持つ module ではなく package 境界として置かれているかを確認したいとき。

## Do not read this when
- レビューの具体的な判定ロジック、builder 処理、oracle の仕様断片を調べたいとき。
- 公開 API、関数、クラス、定数、再 export の実装を探しているとき。

## hash
- af0101216671fb90a1b9f95b81758a8f49779d3a1830bc39993735590f29a60d

# `enumerate_finding.py`

## Summary
- review oracle の finding 列挙処理について、正本側の同名実装をそのまま公開する薄い realization implementation。実体は oracle 側にあり、この階層から review oracle の finding 列挙ロジックへ到達するための互換的な入口として機能する。

## Read this when
- realization implementation 側から review oracle の finding 列挙機能がどこへ委譲されているかを確認したいとき。
- この import 経路を使う呼び出し元で、正本側の finding 列挙実装との対応関係を確認したいとき。

## Do not read this when
- finding 列挙ロジックの具体的な仕様や処理内容を確認したいとき。その場合は正本側の対応する oracle src を読む。
- review oracle 全体の設計、CLI の入出力、または finding 以外の review 処理を調べたいとき。より上位または該当責務の本文を読む。

## hash
- 5171497ece3b245cc5c904cc424da7270138fb9696266e585f6b863709e102ca

# `judge_finding.py`

## Summary
- review oracle 領域の finding 判定実装を、正本側の実装から再公開する薄い互換モジュール。実体は別ツリーの同名責務にあり、この対象自体は判定ロジックを持たず、呼び出し側が realization 側の import path から正本由来の実装へ到達する入口になっている。

## Read this when
- review oracle の finding 判定を使う側で、realization 側の import path がどの実装へ委譲されているかを確認したいとき。
- 同階層の realization モジュール群が、正本側実装を再公開するだけなのか、独自実装を持つのかを切り分けたいとき。
- この import path を変更・削除してよいか判断するために、互換入口としての役割を確認したいとき。

## Do not read this when
- finding 判定ロジックそのもの、入力・出力・判定基準を理解したいとき。この対象ではなく、委譲先の正本側実装を読む。
- review oracle 全体の設計や他の判定処理を調べたいとき。より上位または該当責務の本文へ進む。
- 再公開ではない実装詳細、テスト観点、CLI 出力仕様を探しているとき。この対象にはそれらの情報は含まれていない。

## hash
- 2435689a0d7870d18e17827883aea06ae146b0db7a102b5881e4b2a8e877d524

# `merge_finding.py`

## Summary
- review oracle の finding 結合処理について、正本側実装を src 側へ公開する薄い再エクスポート実装。実体は正本側モジュールにあり、この対象自体は同階層からその実装を import して利用できる入口として機能する。

## Read this when
- src 側の review oracle builder から finding 結合処理を参照する import 経路を確認したいとき。
- 正本側にある同責務の実装が src 側でどのように公開されているかを確認したいとき。

## Do not read this when
- finding 結合処理そのもののアルゴリズム、入力、出力、失敗時挙動を確認したいとき。この対象ではなく正本側の実装を読む。
- review oracle builder 全体の責務分担や他処理との関係を調べたいとき。この対象だけでは判断材料にならないため、より上位または周辺の本文を読む。

## hash
- 50864ea5428b04c017eafeee21c4a87371e5b07a30b723d5af5eaa71e055e5c1

# `validate_finding_advocate.py`

## Summary
- realization 側で review oracle の finding advocate 検証パラメータ生成を公開し、oracle 側実装へ委譲したうえで prompt 内の oracle root 表記 typo だけを補正する薄い adapter。
- oracle src prompt の placeholder 表記差を、仕様で許容された realization-side patch として吸収するための入口。

## Read this when
- review oracle の finding advocate 検証パラメータ生成が、oracle 側実装と異なる prompt 文字列を返す理由を確認したいとき。
- `<oracle_root>` と `<oracle-root>` の表記補正がどこで行われているかを追うとき。
- review oracle validate finding advocate 用の realization 実装が、oracle 側パラメータ生成をどのように包んでいるか確認したいとき。

## Do not read this when
- finding advocate 検証 prompt の正本仕様や本来のパラメータ構成を確認したいだけなら、対応する oracle 側の実装または仕様文書を読む。
- review oracle 全般の設計、他の検証者、または review workflow の制御を調べるときは、より上位または該当 component の本文へ進む。
- 単に Structured Output schema、model class、reasoning effort、file access mode の定義を調べるときは、それらを定義する oracle 側または共通定義を読む。

## hash
- d64a075a6c1eec148438477316a1fedb9e53cdc8de0df390c33141b049e5ca04

# `validate_finding_challenger.py`

## Summary
- レビュー用 oracle 検証処理のうち、finding を challenger 観点で検証する実体を、realization 側の公開経路から再公開する薄い入口。
- 処理本体ではなく、実装側から oracle 由来の検証機能へ到達するための互換的な import 境界として位置づく。

## Read this when
- realization 側のレビュー検証コードから、challenger による finding 検証機能がどの公開経路で参照されるかを確認したいとき。
- レビュー用 oracle 検証モジュールの import 境界や再公開の有無を確認したいとき。

## Do not read this when
- challenger による finding 検証の具体的な判定ロジック、入出力、プロンプト構成を確認したいとき。
- oracle file と realization file の一般的な役割分担や編集責務を確認したいだけのとき。

## hash
- 5b902ceead10af43c7bf653959751fd8ca191352e4275fb80799a4ec71cc722c
