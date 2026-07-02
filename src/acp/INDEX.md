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
- ACP builder 領域の realization 側入口。正本側に置かれた builder 実装を既存の公開参照経路から利用するための互換層をまとめ、各 builder の戻り値を realization 側の公開型へ適合させる役割を持つ。
- apply、common、indexing、quota probe、review、session、TUI などの builder 互換領域へ進むための上位ルーティング対象であり、多くは実処理本体ではなく oracle 側実装への委譲、公開 import surface の維持、削除条件の確認を扱う。

## Read this when
- ACP builder 全体で、正本側 builder と realization 側公開 API の接続関係を俯瞰したいとき。
- 既存の acp.builder 系 import path が残っている理由、互換 wrapper の範囲、削除条件を確認したいとき。
- apply、common、indexing、quota probe、review、session、TUI のどの builder 互換領域へ進むべきかを選びたいとき。
- 正本側 builder への委譲、oracle src import 準備、realization 側 AgentCallParameter への変換に関わる入口を探しているとき。

## Do not read this when
- builder の正本仕様、prompt 文面、parameter 生成内容そのものを確認したいときは、対応する oracle 側の本文または実装を読む。
- ACP parameter の公開型、共通データ構造、汎用変換処理そのものを調べたいときは、基礎定義や共通 helper 側を読む。
- apply fork、review、TUI、session などの機能全体の実行フローや画面制御、状態管理を調べたいときは、それぞれの実処理を担う領域を読む。
- 互換 import path の維持や oracle 側 builder への委譲と無関係な新規機能の実装場所を探しているとき。

## hash
- aaab00c9ff486b50fcfdde4d30d71a4e0be0c07d1d0a536d679eaaf271ad08b6
