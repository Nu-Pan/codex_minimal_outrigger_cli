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
- ACP builder 領域の realization 側互換入口をまとめる階層。正本側 builder を既存の公開参照経路から利用できるようにし、必要に応じて正本側の agent call parameter を realization 側の公開型へ適合させる。
- 主な責務は、apply fork、review、quota availability probe、session、TUI、indexing、common などの builder 参照について、正本側実装への委譲、旧 import 経路の維持、互換 wrapper の残置理由と削除条件を切り分ける入口になることである。
- この階層は builder の正本仕様や実処理本体を集約する場所ではなく、正本側へ実体を置いたまま公開済み参照経路を壊さないための薄い互換境界として読む。

## Read this when
- ACP builder 系の既存公開参照が、正本側 builder や正本側 package 構造へどのように接続されているかを確認したいとき。
- agent call parameter 構築経路で、正本側 builder への委譲、realization 側公開型への変換、import 準備、互換 wrapper の役割を追いたいとき。
- apply fork、review、quota availability probe、session、TUI、indexing など、builder 種別ごとの互換入口や読むべき下位領域を選びたいとき。
- 旧来 import 経路や公開名を残す理由、削除条件、正本側 import path への移行可否を判断したいとき。
- 同名機能が realization 側にあるように見える場合に、実体が正本側実装なのか薄い互換入口なのかを切り分けたいとき。

## Do not read this when
- builder の prompt、parameter 生成内容、判定仕様、出力条件、人間意図などの正本仕様断片を確認したいときは、対応する oracle 側の本文を読む。
- apply fork コマンド全体、TUI の画面制御、review 機能全般、indexing の生成処理や探索処理など、builder 互換入口ではない実処理を調べたいときは、その責務を持つ実装へ直接進む。
- ACP parameter の基礎データ構造、model、reasoning effort、file access mode 全体、path model、汎用 helper などの共通定義を確認したいときは、該当する基礎定義を読む。
- 新規機能の実装場所やテスト対象を探しているだけで、既存公開参照の互換維持、正本側実装への委譲、削除条件の判断に関係しないとき。

## hash
- c66a8e96f54ea1372a2a8a11a1b30c0411fe3aa1e379478ce22a318623bb0f96
