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
- ACP builder 領域で、正本側 builder を既存の realization 側公開 import path から利用できるようにする互換入口を束ねる階層。
- 主な責務は、oracle 側実装への委譲、realization 側公開型への適合、旧 import 経路の維持、互換コードの残存理由と削除条件の確認入口を提供することである。
- apply、common、indexing、quota probe、review、session、TUI などの builder 系互換領域へ進むための上位ルーティング位置にある。

## Read this when
- ACP builder 全体で、oracle 側 builder と realization 側の既存公開 import path の対応関係を確認したいとき。
- 正本側へ実装を置いたまま、acp.builder 配下の旧参照経路や公開入口を維持している理由を確認したいとき。
- builder が oracle 側へ委譲し、戻り値を realization 側の公開型や AgentCallParameter へ適合させる経路を探したいとき。
- apply、common、indexing、quota probe、review、session、TUI のどの builder 互換領域へ進むべきか切り分けたいとき。
- acp.builder 配下の互換入口を削除・移動・置換してよいか、残存参照や削除条件を確認したいとき。

## Do not read this when
- agent prompt、出力条件、parameter 生成内容、人間意図などの正本仕様を確認したいときは、対応する oracle 側 builder を読む。
- ACP parameter の基礎構造、公開型、共通 model 設定、file access mode 全体の定義を確認したいときは、それぞれの基本型定義や共通実装を読む。
- apply fork、review、TUI、session join など各機能の具体的な制御フローや実処理を調べたいときは、対象機能の本体実装へ直接進む。
- indexing の生成処理・探索処理・データ構造など、互換入口ではなく処理本体を確認したいときは、正本側の実体を持つ実装を読む。
- 新規 builder 機能の仕様や実装場所を探しているだけで、既存 import path の互換維持や oracle 側委譲に関係しないとき。

## hash
- 599ddc5f706184846308c0f1331b24291dcc772ad0954d7748c74a31c207928a
