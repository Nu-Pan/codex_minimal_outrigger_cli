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
- ACP builder における session join 領域の realization 側入口。package 階層の互換境界と、セッション join 時の競合解決機能を正本側実装へ委譲する入口をまとめて扱う。
- この階層自体は join 処理の実体を持たず、realization 側から正本側の対応実装へ接続するための薄い境界として位置づく。

## Read this when
- ACP builder の session join 領域で、realization 側の package 構成や import 経路が正本側と対応しているか確認したいとき。
- セッション join 時の競合解決機能について、realization 側の入口がどの正本実装へ接続されているか確認したいとき。
- join 配下の具体的な実装へ進む前に、この階層が処理実体ではなく互換境界・委譲入口として成立していることを確認したいとき。

## Do not read this when
- セッション join の具体的な判定条件、分岐、データ構造、入出力仕様を調べたいとき。この階層は実体を持たないため、正本側の対応実装を読む。
- ACP builder 全体の設計や session join 以外の領域を調べたいとき。より上位または該当領域の対象を読む。
- oracle 側の正本仕様そのものを確認したいとき。この階層は realization 側の入口であり、正本仕様の本文ではない。

## hash
- 72d257157db7c1849431e74bb0de90b9b8d3bce2ea95c90b4dbfeb06b20730e4
