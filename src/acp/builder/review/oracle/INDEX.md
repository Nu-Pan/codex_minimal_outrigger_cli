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
- review oracle の finding merge 呼び出し用 AgentCallParameter を、正本側の生成処理に委譲して作る realization 側の薄いアダプタ。
- 生成された prompt 内の oracle root プレースホルダー定義だけを最小補正し、正本側の不具合が解消されるまでの互換処理を担う。

## Read this when
- review oracle の finding merge 呼び出しで渡される AgentCallParameter の生成経路を確認したいとき。
- known findings を入力にした prompt が、実行前にどのように補正されるかを確認したいとき。
- oracle root プレースホルダー表記の一時的な互換補正や、その削除条件を調べたいとき。

## Do not read this when
- finding merge の本来の prompt 内容や structured output schema の正本定義を確認したいとき。
- review oracle 全体の設計意図、検出対象、出力仕様を確認したいとき。
- AgentCallParameter 型そのものの構造や共通仕様を調べたいとき。

## hash
- 391548e4fea16d20a1993058722af75334c480677e68a5911e83052504043623

# `validate_finding_advocate.py`

## Summary
- review oracle の finding advocate 検証用 AgentCallParameter を構築する薄い実装で、正本側の builder を呼び出した後、生成 prompt に含まれる既知の `<oracle_root>` 表記 typo だけを最小補正して返す。
- finding、既知の advocate 理由、既知の challenger 理由は正本側 builder にそのまま渡し、動的入力は byte-for-byte で維持しつつ、静的な goal 文言の表記補正だけを担う。
- 正本実装への追従用 wrapper として、正本側で `<oracle-root>` 表記が修正されるまで残す一時的な互換処理の入口になっている。

## Read this when
- review oracle の finding advocate 検証に渡す AgentCallParameter の構築経路を確認・変更したいとき。
- 生成 prompt 内の `<oracle_root>` と `<oracle-root>` の表記揺れ補正がどこで行われるかを調べるとき。
- 正本側 builder の返す parameter を保ったまま、prompt だけに局所的な補正をかける実装意図や削除条件を確認したいとき。
- finding や既知理由の動的入力を変更せず保持する必要がある変更・テストを扱うとき。

## Do not read this when
- review oracle の finding advocate 検証プロンプトそのものの正本仕様を確認したいだけなら、正本側の対応する oracle file を読む。
- review oracle の challenger 側や別種類の検証 parameter 構築を扱う場合は、その対象の実装へ進む。
- AgentCallParameter 型そのものの定義、model_class、reasoning_effort、file_access_mode などの共通仕様を調べる場合は、共通の parameter 定義を読む。
- INDEX.md 生成やルーティング文書全般の仕様を調べる場合は、この個別 wrapper ではなく INDEX.md エントリー仕様の正本を読む。

## hash
- 2b79e3665d77ceff0cd1636e2e772a5ab3a92e025778f47e83833b7105feca7c

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
