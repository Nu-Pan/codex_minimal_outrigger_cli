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
- review oracle builder の realization 側入口をまとめる package。finding の列挙・判定・challenger 検証は正本側実装の薄い再公開として扱い、merge finding と advocate 検証は正本側 builder の生成結果を保ったまま prompt 内の oracle root 表記だけを最小補正する互換層を含む。

## Read this when
- レビュー用 oracle builder のうち、finding の列挙・判定・統合・検証に関する realization 側の import 経路を探すとき。
- 正本側 review oracle 実装を src 側から再公開しているだけの入口と、生成済み AgentCallParameter の一部だけを補正する実装を切り分けたいとき。
- merge finding または advocate 検証で、known findings や finding 入力を保ったまま prompt 内の oracle root 表記補正がどこで行われるか確認したいとき。

## Do not read this when
- finding の列挙条件、判定基準、統合ロジック、検証ルール、出力 schema など review oracle の正本仕様そのものを理解したいとき。
- AgentCallParameter の型定義、モデル選択、reasoning effort、file access mode など共通基盤を調べたいとき。
- レビュー builder 全体、CLI 出力仕様、oracle file と realization file の一般的な役割分担を確認したいとき。

## hash
- 9c81504b436a0ef3e65f8973c77f8d4393f3bdc1f5599e8fe92e96b7d1a59ac5
