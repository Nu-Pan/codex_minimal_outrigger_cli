# `__init__.py`

## Summary
- oracle.acp_builder.session と同じ import 経路を実装側に用意するための互換 package 初期化ファイル。
- 実体の処理や公開オブジェクト定義は持たず、この階層を session package として成立させる入口に位置づけられる。

## Read this when
- acp builder の session package が oracle 側の package 構造とどう対応しているかを確認したいとき。
- この階層が import 可能な package として存在する理由だけを確認したいとき。

## Do not read this when
- session builder の具体的な処理、状態管理、入出力変換を調べたいとき。
- 公開 API、関数、クラス、定数の実装内容を探しているとき。
- oracle 側の正本仕様や互換対象そのものを確認したいとき。

## hash
- 7e4bc9c978926c93dcef2adf49463fd3703f72086d6dffc318e9381b610b5c88

# `join`

## Summary
- ACP builder の session join 領域における package 入口と、旧 import 経路を維持する互換入口を収める領域。
- この階層自体は session join の実処理を担う場所ではなく、oracle 側の対応構成との package 互換性と、正本側実装への再 export 境界を扱う。

## Read this when
- ACP builder の session join 配下が package として成立している理由や、oracle 側の対応構成との互換性を確認したいとき。
- session join conflict resolution について、旧 import 経路が残っている理由、移行用の互換入口、削除可否の前提を確認したいとき。
- session join 配下の実体を持つ実装へ進む前に、この階層が実処理ではなく互換境界として存在しているかを見分けたいとき。

## Do not read this when
- session join の具体的な処理内容、関数、クラス、入出力仕様、衝突解決の判定内容を調べたいときは、実体を持つ正本側実装へ進む。
- ACP builder 全体の設計や session join 以外の領域を調べたいときは、より上位または対象領域の入口から確認する。
- oracle 側の正本仕様そのものを確認したいときは、この互換領域ではなく oracle 側の該当本文を読む。

## hash
- 85933db87f4a855b5a4bdd80b5593fcd293c47c0e7c1c7fa2e11a1270fa78021
