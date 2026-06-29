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
- レビュー oracle 関連の AgentCallParameter builder と finding 判定・列挙・検証の互換 import 層をまとめる階層。多くは旧来の realization 側 import 経路から canonical oracle 側実装へ委譲するための薄い入口であり、一部は oracle src 由来 prompt の既知 placeholder 表記だけを限定的に補正する。
- 実処理本体や正本仕様を保持する場所ではなく、既存呼び出し元の移行中に必要な互換経路、削除条件、補正境界を確認するための入口として位置づけられる。

## Read this when
- レビュー oracle finding の列挙・判定・検証・統合 builder について、旧来の import 経路が canonical oracle 側へどう委譲されているか確認したいとき。
- 互換 import 層を削除できるか、または呼び出し元を canonical oracle path へ移行する必要があるか判断したいとき。
- oracle src 由来 prompt の placeholder 表記補正が、どの builder wrapper でどの範囲に限定されているか確認・変更したいとき。
- review oracle 用 AgentCallParameter 生成で、既知 finding や検証理由などの動的入力を保持しつつ静的 prompt だけを補正する境界を調べたいとき。

## Do not read this when
- レビュー finding の判定仕様、検出ロジック、正本 prompt、schema そのものを調べたいとき。この階層の多くは互換・補正層なので、canonical oracle 側または対応する oracle src を直接読む。
- AgentCallParameter の型、model、reasoning、profile、schema 指定の一般仕様を確認したいとき。基礎定義側を読む。
- 互換 import 経路や placeholder 補正と無関係な review 機能全般、CLI 表示、テスト方針を調べたいとき。より直接その責務を持つ対象へ進む。

## hash
- 845a81fc4c46c5f38c41cf6651df63e7ba22c7cfdf1d1afb4a0d6eb9f561899d
