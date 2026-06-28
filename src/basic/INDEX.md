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
- ACP 関連の basic 実装を、正本側の実装からそのまま公開する薄い中継モジュール。実体の責務や挙動はこの対象内では定義せず、正本側の basic 実装に委ねる。

## Read this when
- realization 側で ACP basic API がどこから公開されているかを確認したいとき。
- この階層の ACP 関連実装が独自実装を持つのか、正本側実装の再公開なのかを切り分けたいとき。

## Do not read this when
- ACP の具体的な型、関数、挙動、生成ロジックを確認したいとき。この対象は中継だけなので、正本側の対応実装を読む方が直接的である。
- realization 側で独自に実装された ACP 処理を探しているとき。この対象には独自ロジックはない。

## hash
- 4420dd500ac5254358305547d9e45cdc143f1ab0ffcc641e909f2ce7fa04ad92

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
