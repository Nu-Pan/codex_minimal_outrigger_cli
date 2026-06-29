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
- レビュー用 oracle merge finding パラメータ生成を、正本側の既存生成処理へ委譲しつつ、既知 finding 入力を含む prompt 内の oracle root プレースホルダー表記だけを最小修正する realization 実装。
- 正本仕様側の一時的な表記不整合に対して、生成済み AgentCallParameter の型・モデル・推論設定・アクセス設定・structured output schema 指定を保ったまま prompt だけを差し替える薄い互換層として機能する。

## Read this when
- レビュー oracle の merge finding 用 AgentCallParameter がどのように作られるか、または known findings が prompt へ渡った後にどの補正を受けるかを確認したいとき。
- oracle root プレースホルダー表記の `<<...>>` から `<...>` への補正が、どこで、どの範囲に限定して行われているかを調べるとき。
- 正本側の builder 実装を realization 側でラップしている箇所や、生成パラメータの一部だけを変更して他の設定を維持する実装を確認したいとき。

## Do not read this when
- レビュー finding の統合ロジックそのもの、finding の意味判定、重複判定、出力 schema の内容を調べたいとき。
- AgentCallParameter 型の定義、モデル選択、reasoning effort、file access mode の一般仕様を調べたいとき。
- oracle file と realization file の基本概念、または oracle root などのパスモデル全体を確認したいとき。

## hash
- c31535b2daad9099a12ca97622a917e1bbb7f3b5c1579039578d3e3753a3c8de

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
