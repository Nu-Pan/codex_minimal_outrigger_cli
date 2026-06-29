# `__init__.py`

## Summary
- oracle src 側の basic 互換 import を realization 側で受けるための入口。ACP 基本型などを複製せず、既存の `basic.*` 参照を維持する互換層として位置づけられる。
- 互換目的で残されており、削除可否は realization 側と利用者向け公開面から `basic.*` 参照がなくなり、正本側または実体 module への移行が済んでいるかで判断する。

## Read this when
- `basic.*` 参照の互換維持、移行、削除条件を確認したいとき。
- oracle src 側の basic 互換 import 入口と、realization 側または利用者向け公開面との関係を確認したいとき。
- ACP 基本型や関連する基本 module を複製せず既存参照を保つ理由を確認したいとき。

## Do not read this when
- 個別の ACP 基本型や実体 module の定義・挙動を確認したいとき。
- 正本仕様断片そのものや oracle src 配下の具体的な実装内容を確認したいとき。
- `basic.*` 互換参照の有無や削除条件ではなく、一般的な path model、CLI 挙動、テスト挙動を調べたいとき。

## hash
- bd7e89dfb56983290190c9facb93f671f397b370fc9ea0fb32052b0bc819b591

# `acp.py`

## Summary
- 正本側で定義された ACP 関連型を realization 側の既存公開面へ再公開する互換用モジュール。
- 正本型を複製せず、既存の参照を維持するための薄い入口であり、利用者向け公開面や realization 側からその参照がなくなれば削除可能な位置づけを持つ。

## Read this when
- 既存コードや利用者が参照している ACP 関連型の import 経路を維持・整理する必要があるとき。
- realization 側で ACP 型を独自定義せず、正本側の型を再公開している互換境界を確認したいとき。
- この互換入口を削除できるか判断するために、残す理由と削除条件を確認したいとき。

## Do not read this when
- ACP 関連型そのものの定義内容、列挙値、データ構造を確認したいとき。その場合は正本側の型定義を直接読む。
- ACP の生成ロジック、変換処理、CLI 挙動、テスト観点を調べたいとき。この対象は再公開だけを担い、それらの実装責務を持たない。
- 新しい ACP 型や挙動を追加する場所を探しているとき。この対象は互換用の公開入口であり、正本型の追加・変更場所ではない。

## hash
- de511dc6ae0bf66bbe04c2916d62b5268565b3e4ecdd7da73137fc3bb6174faa

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
