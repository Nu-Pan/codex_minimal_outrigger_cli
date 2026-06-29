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
- review oracle の finding 列挙ロジックを、正本側の実装からそのまま公開する薄い再エクスポートファイル。実際の責務や判定内容は正本側にあり、このファイル自体は realization 側の import 経路を保つ入口として位置づけられる。

## Read this when
- realization 側から review oracle の finding 列挙機能を import する経路を確認したいとき。
- 正本側の review oracle 実装が、src 側のどの入口から参照されているかを追跡したいとき。

## Do not read this when
- finding の列挙条件、出力内容、判定ロジックそのものを確認したいとき。その場合は再エクスポート先の正本側実装を読む。
- review oracle 全体の仕様意図やルールを確認したいとき。その場合は対応する oracle file や上位の正本仕様を読む。

## hash
- eac5a4d9395959e1b8fe4f22e02a3e127b1517fdfe317b3197f9ae19ac149a93

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
- review oracle の finding 検証で advocate 側を呼び出す AgentCallParameter を組み立てるための realization implementation。正本側の builder から生成した parameter をほぼそのまま返しつつ、静的 prompt 内に残る oracle root 表記の typo だけを最小限に補正する薄い互換層として機能する。
- 動的入力である finding と既知理由は改変せず、正本由来 prompt の固定文言だけを 1 箇所置換する責務を持つ。

## Read this when
- review oracle の finding 検証における advocate 側 AgentCallParameter の生成経路を確認・変更するとき。
- 正本側 builder の出力を realization 側でどの程度補正しているかを調べるとき。
- prompt 内の `<oracle-root>` 表記補正、または dynamic input を byte-for-byte に保つ制約に関わる変更を行うとき。
- oracle src に残る静的 typo と realization 側の最小補正の関係を確認するとき。

## Do not read this when
- review oracle の challenger 側、別の review builder、または finding 検証以外の AgentCallParameter 生成を調べるとき。
- 正本仕様そのものの文言や prompt 標準を確認・変更したいとき。この対象は realization 側の補正実装であり、正本仕様の代替ではない。
- finding 本文や既知理由の生成・解釈・検証ロジックを調べたいとき。この対象はそれらを加工せず parameter へ渡すだけである。
- 単に AgentCallParameter の型定義、モデル設定、structured output schema の内容を調べたいとき。

## hash
- 7a11d132eebabaa517f49ce2d7551b2adc0098d73ea6027f8e93fa605d9ad858

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
