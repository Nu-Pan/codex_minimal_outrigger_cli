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
- acp builder 配下の旧 import path 互換入口をまとめるディレクトリ。oracle 側 builder を正本に保ちながら、既存の acp.builder.* 参照を canonical 実装や realization 側 adapter へ中継する。
- apply、review、session、tui、indexing、quota probe などの builder 互換層と、oracle 実装の再公開・alias・fallback・削除条件を確認する入口になる。

## Read this when
- acp.builder.* の旧 import 経路互換、canonical oracle builder への接続、module alias、再公開 shim の残存理由を確認したいとき。
- apply fork、review oracle、session、TUI、indexing、quota probe の agent call parameter builder について、realization 側の互換境界や oracle 側への委譲関係を調べるとき。
- 正本 builder 追加後または旧参照移行後に、互換入口・fallback・wrapper を削除できる条件を確認したいとき。

## Do not read this when
- agent prompt、parameter 生成内容、builder 本体の正本仕様や canonical 実装を確認したい場合は、oracle 側の該当 builder を直接読む。
- apply、review、session、TUI など各機能の実行フロー、CLI 引数処理、状態操作、画面構成を調べたい場合は、それぞれの機能実装へ進む。
- acp.builder 以外の acp package 公開面、汎用 AgentCallParameter 型、git helper、path model、quota 判定ロジックそのものを調べたい場合は、対象の共通実装や上位 package を読む。

## hash
- d28a2d91e0a968f86c5ac7803651bc80785347f956d9f9e51a0672e60d285af8
