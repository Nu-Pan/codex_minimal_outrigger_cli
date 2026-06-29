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
- レビュー用 oracle merge finding の AgentCallParameter 生成を、正本側の生成処理に委譲しつつ、prompt 内の oracle root プレースホルダー表記だけを最小補正する実装。
- 正本側がまだ誤ったプレースホルダー表記を出す場合に限り、既知 findings を入力として生成された parameter の prompt を差し替え、他の parameter 属性は維持する。

## Read this when
- review oracle merge finding 用の AgentCallParameter を realization 側でどう組み立てているか確認したいとき。
- 正本側の prompt 生成結果に含まれる oracle root プレースホルダー表記の互換補正を調査・修正したいとき。
- known findings を入力にした review oracle merge finding prompt の生成経路や、正本実装への委譲境界を確認したいとき。

## Do not read this when
- review oracle merge finding の正本仕様や本来の prompt 内容を確認したいだけなら、対応する oracle 側の本文を読む。
- AgentCallParameter の型や共通属性の定義を確認したいだけなら、その基礎定義を読む。
- review oracle merge finding 以外の review builder や oracle prompt 生成処理を調査しているなら、対象となる別モジュールを読む。

## hash
- 30f34cf41e060b2567a79f4e46fafe181afdd10fd79a1a7be75807ec8320b973

# `validate_finding_advocate.py`

## Summary
- review oracle の finding advocate 検証用 AgentCallParameter を、正本側 builder に委譲して生成する realization 実装。
- 正本側 prompt に含まれる `<oracle_root>` 表記の typo だけを `<oracle-root>` に補正する薄い wrapper であり、finding と既知理由の動的入力は改変せず、元の parameter の model・reasoning・file access・structured output schema 指定を維持して返す。

## Read this when
- review oracle の finding advocate 検証呼び出しで、realization 側が正本側 builder をどのように包んでいるか確認したいとき。
- 生成される prompt の `<oracle-root>` 表記補正、またはその補正が動的入力へ影響しないことを確認・変更したいとき。
- AgentCallParameter の各フィールドを保持したまま prompt だけを最小補正する実装意図を確認したいとき。

## Do not read this when
- review oracle の finding advocate 検証そのものの正本仕様や元 prompt の全体内容を確認したいとき。
- finding、advocate reasons、challenger reasons の内容生成や評価ロジックを調べたいとき。
- review oracle 以外の builder、または typo 補正を含まない通常の parameter 生成経路を調べたいとき。

## hash
- 31b050587e1d463e96b41b466bf5c79a8f3e17f87aa8c35847045f73823e5d2a

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
