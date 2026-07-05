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
- acp builder 配下の互換入口と個別 builder 領域へのルーティングを担うディレクトリ。oracle 側実装を正本に保ちつつ、旧来の acp.builder import 経路を canonical 実装や realization 側の適応層へ接続する。
- apply fork、indexing、quota probe、review、session、TUI などの builder 入口があり、実処理本体ではなく import 互換、oracle builder 委譲、realization 公開型への最小変換、削除条件確認の入口として使う。

## Read this when
- acp.builder.* の旧 import 経路が、oracle 側 canonical 実装または realization 側 wrapper へどう接続されるかを調べたいとき。
- oracle 側 builder を正本としながら realization 側で AgentCallParameter への変換、module alias、package path 追加、既知 typo 補正などをどこで行うか確認したいとき。
- apply fork、quota probe、review、session、TUI、indexing の builder 互換入口や削除条件を確認し、個別領域へ進む入口を選びたいとき。
- 旧 acp.builder 参照を canonical import path へ移行する作業で、残すべき互換層、既存参照向け公開面、削除できる条件を調べたいとき。

## Do not read this when
- oracle 側 builder の正本仕様、prompt 本文、parameter 生成内容そのものを確認したい場合は、対応する oracle 側実装を直接読む。
- apply、review、session、TUI など各機能の実行フロー、画面挙動、branch 操作、finding 処理など builder 以外の実装詳細を調べたい場合は、該当機能の実装へ進む。
- AgentCallParameter の基本型、file access mode、path model、Structured Output schema などの共通基礎仕様だけを確認したい場合は、それぞれの共通定義を読む。
- 新しい公開 API や新規 import 経路を設計したい場合は、この互換領域ではなく正本仕様または新規機能の入口を確認する。

## hash
- ebd7c0a82c1bef7ff80f973308194949451ef3a138f2dbeb65af7707112da669
