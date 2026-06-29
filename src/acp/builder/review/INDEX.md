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
- 対象階層は、review oracle builder 関連の realization 側互換 package であり、旧来 import 経路から正本側実装へ委譲する薄い module 群と、一部 prompt の oracle root 表記だけを補正する wrapper を収める。
- review finding の列挙・判定・challenger validation は実装本体を持たない再公開層として位置づけられ、呼び出し元が正本側経路へ移行した後に削除できる互換境界を示す。
- merge finding と finding advocate validation は、正本側 builder で生成した AgentCallParameter の他属性を維持しつつ、prompt 内の oracle root placeholder typo だけを補正する realization 側入口である。

## Read this when
- review oracle builder 周辺で、旧来の realization 側 import 経路が正本側実装へどう委譲されているかを確認したいとき。
- review finding の列挙・判定・challenger validation の互換 module が残っている理由や削除条件を確認したいとき。
- review oracle merge finding や finding advocate validation の AgentCallParameter 生成で、正本側 builder への委譲境界と prompt 内 oracle root 表記補正を確認したいとき。
- 同名機能の実装がこの階層にあるように見えるが、実体が正本側にあるのか realization 側 wrapper にあるのかを切り分けたいとき。

## Do not read this when
- review finding の列挙・判定・検証そのものの正本仕様、出力内容、検出ロジック、評価ロジックを調べたいとき。正本側の oracle 実装を読む。
- AgentCallParameter の共通型、model・reasoning・file access・structured output schema などの基礎定義を調べたいとき。
- review oracle 以外の builder、CLI 表示、テスト方針、または互換 import と prompt 表記補正に関係しない review 機能全般を調べたいとき。
- 新しい review 判定ロジックや検証処理を追加・変更したいとき。この階層の多くは委譲または最小補正だけを担うため、実装本体の対象へ進む。

## hash
- 970b5b4cebe0698ddd6ee2e13b4b8bbc5afab4ecd7fe0dc2d7d1b99292896ed7
