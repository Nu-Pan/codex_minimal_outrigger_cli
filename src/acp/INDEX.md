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
- ACP builder まわりの互換入口を集める領域。oracle 側の canonical builder を正本に保ちつつ、旧来の acp.builder 系 import 経路や既存 caller からの参照を成立させる薄い公開面を提供する。
- apply fork、review、session、TUI、quota probe、indexing などの builder について、oracle 側実装への委譲、realization 側公開型への最小適合、既存 import path 維持、削除条件確認の入口になる。

## Read this when
- acp.builder 系の旧 import 経路が oracle 側 canonical 実装や互換 wrapper へどう接続されるかを確認したいとき。
- ACP builder の互換層を削除・移行する作業で、既存 caller 向け公開面を残す理由や削除条件を調べたいとき。
- apply fork、review、session、TUI、quota probe、indexing の agent call parameter builder について、oracle builder への委譲境界や realization 側での最小補正・型適合を確認したいとき。
- 正本 prompt や canonical builder を realization 側へ複製しないための接続方法、package path、module alias、再 export の扱いを調べたいとき。

## Do not read this when
- oracle 側 builder の正本仕様、prompt 本文、canonical 実装内容を確認したいだけなら、oracle 側の該当実装を直接読む。
- apply、review、session、TUI、quota probe など各機能そのものの実行フロー、CLI 引数処理、UI 挙動、判定処理、状態操作を調べたい場合は、それぞれの機能実装へ進む。
- AgentCallParameter の基本構造、汎用 git helper、path model、file access mode、Structured Output schema など builder 互換入口以外の共通基盤を調べたい場合は、該当する共通実装を読む。
- 新しい公開 API や新規 import 経路を設計したいだけの場合は、既存互換維持を扱うこの領域ではなく、正本仕様や対象機能の入口を確認する。

## hash
- a04347ec13bca4d4f64c12283ccea2684da024db656cc373e875ae0e01af2b8c
