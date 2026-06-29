# `__init__.py`

## Summary
- oracle src 側の basic パッケージと同じ import 入口を realization implementation 側に用意するためのパッケージ初期化ファイル。本文は互換 import 入口であることだけを示し、具体的な機能実装や公開名の定義は持たない。

## Read this when
- realization implementation 側の basic パッケージが、oracle src 側の basic パッケージと import 構造上どのように対応しているかを確認したいとき。
- basic 配下の個別モジュールではなく、パッケージ自体の import 入口としての意図だけを確認したいとき。

## Do not read this when
- basic 配下の具体的な関数、クラス、定数、CLI 挙動、path model などの実装内容を調べたいとき。その場合は対応する個別モジュールを読む。
- oracle file の正本仕様断片や basic の詳細仕様を確認したいとき。その場合は oracle src 側または oracle doc 側の該当本文を読む。

## hash
- e37f0c2c936022ed6a52cba2ff0c32ef5d7c162e9c1f5771050841cad1a50f4d

# `acp.py`

## Summary
- ACP 実行時に共有される呼び出しパラメータ型を、oracle src 側の正本定義から再公開する薄い realization implementation。
- モデル区分・推論努力・ファイルアクセスモード・AgentCallParameter の正本は oracle 側に置き、この入口は通常起動時に `basic.acp` から同じ型へ到達するための互換境界だけを持つ。

## Read this when
- realization implementation 側で `basic.acp` の import がどの oracle 側 ACP 型へ接続されているか確認したいとき。
- モデルクラス、reasoning effort、ファイルアクセスモード、AgentCallParameter を参照する実装の import 境界を確認したいとき。
- 正本側 ACP 型を realization 側にコピーせず再公開していることを確認したいとき。

## Do not read this when
- ACP 型のフィールド、enum 値、docstring など正本定義の内容を確認したいとき。その場合は oracle 側の対応本文を読む。
- ACP のパラメータ値を組み立てるロジックや選択規則を確認したいだけのとき。
- 実際のファイルアクセス制御、権限判定、書き込み可否の実装を確認したいとき。
- structured output schema の内容や検証処理そのものを確認したいとき。
- oracle file と realization file の一般定義や編集責任の境界を確認したいとき。

## hash
- b84e1780d9c60db454c59e876524e339f5cc22a0c0d6c59077d2a188e92a7f97

# `path_model.py`

## Summary
- realization implementation 側から、正本側で定義された path model の公開要素をそのまま再公開する薄い入口。実体は正本側の対応モジュールにあり、この対象自体には独自の path 定義・変換ロジック・補助処理を持たない。

## Read this when
- realization implementation から path model の定義がどこに接続されているかを確認したいとき。
- 正本側の path model を利用するための公開入口が、独自実装ではなく再公開になっていることを確認したいとき。

## Do not read this when
- path model の概念定義、各 root token の意味、path 変換の仕様や実装内容を確認したいとき。この対象ではなく、再公開元の正本側モジュールを読む。
- path model 以外の basic 領域の実装責務や、他の realization implementation の処理を調べたいとき。

## hash
- b906c53bea4ac1c03ad02aedac81b1ac738646dcadacf546a52fba636044e9eb

# `struct_doc.py`

## Summary
- 構造化ドキュメント本文を表す最小実装であり、正本側の同名概念実装をそのまま公開する転送口として機能する。
- この層自体には独自ロジックを持たず、実際の型・関数・挙動は正本側の構造化ドキュメント実装に委ねる。

## Read this when
- realization implementation 側から構造化ドキュメント関連の公開名がどこで提供されているかを確認したいとき。
- 正本側の構造化ドキュメント実装を src 配下から利用する import 経路を確認したいとき。
- このファイルに独自処理があるか、または正本側への再公開だけかを切り分けたいとき。

## Do not read this when
- 構造化ドキュメントの具体的な型、関数、変換規則、検証ロジックを調べたいとき。この対象ではなく、正本側の実装本文を読む。
- cmoc 全体の oracle file と realization file の基本概念や責務分担を調べたいとき。この対象ではなく、それらを定義する正本仕様断片を読む。
- INDEX.md エントリーの生成規則やルーティング文書の書き方を調べたいとき。この対象にはその説明は含まれていない。

## hash
- dbdafabe94f1382dd0ce411451a4192c12360db0220d57888e9f8510a811a91d
