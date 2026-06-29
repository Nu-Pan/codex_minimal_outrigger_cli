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
- レビュー用の oracle 所見列挙プロンプトを組み立てる実装。既存の oracle 側パラメータ生成を呼び出したうえで、レビュー基準、対象 oracle file 本文、所見配列を返すための出力指示を追加する。
- 対象 oracle file の実パス解決、本文の fenced code 化、出力指示の追記を担う補助処理を含む。

## Read this when
- oracle file をレビューして新規所見を列挙する agent call parameter の生成経路を確認・変更したいとき。
- レビュー所見列挙プロンプトへ、レビュー基準や対象 oracle file 本文がどのように追加されるかを確認したいとき。
- 対象 oracle path の解決失敗時の扱い、対象ファイルが存在しない場合の本文扱い、markdown code fence のエスケープ処理を確認したいとき。

## Do not read this when
- レビュー所見の判定基準そのものを確認したいとき。対象はこの実装ではなくレビュー基準を構築する側である。
- agent call parameter の基本構造やモデル選択、file access mode などの共通仕様を確認したいとき。対象はこの実装ではなく共通のパラメータ定義側である。
- oracle file の正本仕様本文を確認したいとき。この実装は本文をプロンプトへ埋め込むだけで、仕様内容の入口ではない。

## hash
- 5bbb0b5fd23d7a486c112b33307f5b4097df1bde83c443f7e24a3000ab4a1beb

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
- review oracle の finding advocate 検証用 AgentCallParameter を、正本側 builder の結果を基に生成する realization 実装。
- 正本側 API を再公開しつつ、生成済み prompt に含まれる静的な oracle root 表記 typo だけを最小修正して返す入口。
- finding と既知理由の入力値はそのまま正本側 builder に渡し、動的入力を byte-for-byte で変更しない制約を担う。

## Read this when
- review oracle の finding advocate 検証呼び出しで使う AgentCallParameter の組み立て経路を確認したいとき。
- 正本側 builder の返却値に対して realization 側でどの補正を加えているかを確認したいとき。
- prompt 内の oracle root 表記 typo 補正が、静的な goal 文だけに限定されているかを調べるとき。
- finding、既知 advocate 理由、既知 challenger 理由などの動的入力を改変していないことを確認したいとき。

## Do not read this when
- review oracle 全体の判定仕様や finding advocate の正本プロンプト本文を確認したいだけのとき。
- AgentCallParameter 型そのものの定義、model class、reasoning effort、file access mode の一般仕様を確認したいとき。
- review oracle 以外の builder や、advocate ではない検証ロールの実装経路を調べているとき。
- INDEX.md 生成やルーティング文書の一般規則を確認したいだけのとき。

## hash
- 1ccc000be2eabbaf35cd53d1a83e2e1f45e77126fb7d54ec57eb38f9917139b9

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
