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
- 所見マージ用の agent call parameter を oracle src 実装から取り込み、実行側で必要な最小限の prompt 補正を加える realization implementation。oracle src 側の既存ビルダーを正としつつ、生成された parameter の prompt 内に残る oracle root トークン表記の typo だけを実行前に置換して返す入口である。

## Read this when
- 所見マージ prompt の実行用 parameter がどの oracle src 実装を呼び出しているか確認したいとき。
- 所見マージ prompt に含まれる oracle root トークン表記の補正理由や補正範囲を確認したいとき。
- oracle src 由来の parameter を realization 側でどこまで変更してよいか、最小補正の実装境界を確認したいとき。

## Do not read this when
- 所見マージ prompt の正本内容そのもの、structured output schema、または review oracle の仕様断片を確認したいとき。
- 所見マージ以外の review builder parameter 生成や、review 実行全体の制御フローを調べたいとき。
- oracle file の typo を修正する提案や正本仕様の変更可否を判断したいとき。

## hash
- 9480575f8b473f6392c067c70449375146ec969882cb148940af310af578751a

# `validate_finding_advocate.py`

## Summary
- 所見擁護検証用の agent call parameter を実行側で組み立てる薄いラッパー。正本側の同名 builder を呼び出し、prompt 内の path token typo だけを最小補正して返す。
- 正本仕様断片から生成された parameter をそのまま使うのではなく、realization 側で許容された `<oracle_root>` から `<oracle-root>` への補正を挟む入口として位置づく。

## Read this when
- 所見擁護検証 prompt の実行用 parameter 生成経路を確認したいとき。
- 正本側 builder の戻り値に対して realization 側でどの最小補正を加えているかを確認したいとき。
- `<oracle_root>` と `<oracle-root>` の表記差が、所見擁護検証 prompt でどこで補正されるかを調べるとき。

## Do not read this when
- 所見擁護検証 prompt の正本内容や schema 自体を確認したいときは、正本側の対応する oracle src や関連 doc を読む。
- 所見擁護ではない review oracle prompt の parameter 生成経路を調べるときは、対象 prompt に対応する別の builder を読む。
- agent call parameter の型定義や共通属性の意味を調べるときは、共通の parameter 定義を読む。

## hash
- 4d0405bdc8dff07f326fbe150096936fc60459e6f4f820c5ed1daa079c0311a6

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
