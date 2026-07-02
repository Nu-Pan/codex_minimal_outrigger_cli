# `__init__.py`

## Summary
- oracle src 側の acp builder 実装を複製せず、既存の `acp.*` import 参照を維持するための互換入口。実体は別 module 側に置き、この対象は移行期間中の公開 import 面を保つ役割に限定される。

## Read this when
- `acp.*` 参照を `oracle.*` または実体 module へ移行する作業で、互換入口を残す理由や削除条件を確認したいとき。
- realization 側または利用者向け公開面に残る `acp.*` import の扱いを判断したいとき。
- oracle src 由来の acp builder 互換 import がどこで維持されているかを確認したいとき。

## Do not read this when
- acp builder の実装内容や生成処理そのものを調べたいとき。この対象は実体を持たない互換入口なので、実装本体へ進む。
- 新しい acp 機能や API 仕様を追加する場所を探しているとき。この対象は互換維持専用であり、機能追加の入口ではない。
- `acp.*` 参照がすでに全公開面と realization 側から消えていることだけを確認済みで、互換入口の詳細を読む必要がないとき。

## hash
- 9376c267fa8194d94f175e9895f353889128d4ce8fff592333bfe1d50f96077f

# `builder`

## Summary
- ACP の agent call parameter builder 群に対する realization 側の互換入口を集める階層。正本側 builder を既存の公開参照経路から利用できるようにし、実処理は主に oracle 側実装または下位の個別互換 wrapper に委ねる。
- apply、review、session、TUI、indexing、quota probe などの builder 領域について、旧来 import path の維持、正本側への委譲、realization 側 parameter 型への適合、互換コードの残置理由や削除条件を確認するための上位入口である。

## Read this when
- ACP builder 関連の公開 import path が正本側実装へどう接続されているかを、領域単位で切り分けたいとき。
- agent call parameter builder の変更で、どの下位領域が apply、review、session、TUI、indexing、quota probe などを担当するか判断したいとき。
- oracle 側へ実体を集約しつつ realization 側に残る互換 package、薄い wrapper、再公開境界の残置理由や削除条件を確認したいとき。
- 正本 builder の出力を realization 側の型や既存公開面へ適合させる経路を探しているとき。

## Do not read this when
- 個別 builder の正本仕様、prompt、出力条件、具体的な生成ロジックを確認したいときは、対応する oracle 側の本文または実装を読む。
- CLI コマンド全体の制御フロー、fork 作成、branch 操作、diff 生成、画面制御、状態管理など builder 互換入口以外の処理を調べたいときは、それぞれの実装領域へ進む。
- agent call parameter の共通データ構造、model、reasoning effort、file access mode などの基礎定義だけを調べたいときは、基礎定義側を読む。
- 新しい機能の実装場所やテスト対象を探しており、旧 import path の維持や正本側 builder への委譲と関係しないとき。

## hash
- 4713ed4a77a3cfb016121318ce6455d3cf080b543a1bc78c87ff7a6bbb8b751b
