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
- レビュー指摘列挙機能について、旧来の実装側 import 経路を維持するための互換モジュール。実体は正本側の実装に委譲し、この経路を使う呼び出し元が残っている間だけ入口として機能する。
- この対象自体は列挙ロジックを定義せず、互換経路の維持理由と削除条件を示す薄い再公開層として位置づけられる。

## Read this when
- レビュー指摘列挙機能の import 経路を整理し、旧来の実装側経路をまだ残す必要があるか確認するとき。
- 正本側の実装へ呼び出し元を移行する作業で、互換モジュールの削除条件や残置理由を確認するとき。
- 互換 import 層が意図的な一時経路なのか、不要な重複実装なのかを判断するとき。

## Do not read this when
- レビュー指摘列挙そのものの仕様、出力内容、検出ロジックを確認したいとき。この対象ではなく正本側の実装を読む。
- 新しい列挙処理や判定ロジックを追加・変更したいとき。この対象は実装本体ではないため、委譲先を確認する。
- 互換経路と無関係なレビュー機能全般、CLI 表示、テスト方針を調べたいとき。より直接その責務を持つ対象へ進む。

## hash
- 0469200f883330879457152116ebf6fce239124db5e820f3bc7d0122adf3707b

# `judge_finding.py`

## Summary
- review finding judgment の実体を canonical oracle 側へ委譲するための互換 import module。既存 caller が旧来の realization 側 import path を使っている間だけ残され、実装本体は持たず wildcard import で canonical implementation を再公開する。
- 互換層を削除できる条件として、全 caller が canonical oracle path を直接使う状態になることを docstring で示す。

## Read this when
- review finding judgment の import 経路を調査していて、旧来の realization 側 path がまだ使われているか、canonical oracle 側への委譲だけをしているかを確認したいとき。
- 互換 import module の削除可否を判断するために、残している理由と削除条件を確認したいとき。
- 同名機能の実装が realization 側にあるように見えるが、実体がどこにあるかを切り分けたいとき。

## Do not read this when
- review finding judgment の判定仕様や具体的な実装内容を確認したいとき。この module は互換 import 層なので、canonical oracle 側の実装を直接読む方が適切。
- 新しい判定ロジック、データ構造、テスト観点を探しているとき。この module にはそれらの本文はない。
- 単に oracle file と realization file の一般的な責務境界を確認したいとき。この module 固有の情報は互換 import path の維持理由に限られる。

## hash
- 1af803594cd6409cf869f8b42cff07b9196e96439b57002bc1b935c328c1e069

# `merge_finding.py`

## Summary
- review oracle の finding 統合用 agent call parameter を、正本側 builder に委譲して生成する realization 実装。
- 正本側 prompt に含まれる oracle root placeholder 表記の既知不整合だけを、生成後に最小補正して返す薄い互換 wrapper。

## Read this when
- review oracle の finding 統合で使う agent call parameter の生成経路を確認・変更する場合。
- 正本側 builder から返る parameter を維持したまま prompt だけを補正する処理の意図や削除条件を確認する場合。
- oracle root placeholder 表記の補正が、known findings 入力や structured output schema path に影響しないことを確認する場合。

## Do not read this when
- 正本仕様断片そのものや正本側 builder の本来の prompt 生成仕様を確認したい場合。
- review oracle 以外の builder、または finding 統合以外の review flow を調べたい場合。
- 単に生成済み parameter の利用側挙動を追うだけで、prompt 補正 wrapper の有無が関係しない場合。

## hash
- 8addfc9fd89fb333e4f2f13cb17e2712431e694f2f070db859eb979463230303

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
- 既存呼び出し元向けに、古い import 経路から正本側の challenger finding validation 実装を再公開する互換モジュール。
- 実体の検証ロジックは持たず、全公開名を正本側実装へ委譲する入口としてだけ機能する。
- 呼び出し元が正本側の経路へ移行し終えた後に削除する前提の一時的な互換層である。

## Read this when
- 古い import 経路を使う呼び出し元が残っているか確認する。
- challenger finding validation の import 互換性や移行完了条件を調べる。
- 互換モジュールを削除できるか、または削除前に参照元を正本側へ移す必要があるか判断する。

## Do not read this when
- challenger finding validation の実際の判定仕様や検証ロジックを確認したい。その場合は正本側の実装を読む。
- 新しい検証処理を実装・変更したい。この対象は委譲だけであり、挙動本体の変更先ではない。
- 互換 import と無関係な review oracle 周辺の処理を調べている。

## hash
- 65259bcd79ca803eef7fc76ba4bbabf8267bb9b725e86300e20be0da2181ff24
