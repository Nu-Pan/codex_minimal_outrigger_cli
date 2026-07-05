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
- acp builder 領域の互換入口をまとめ、既存の acp.builder 系 import path を oracle 側 canonical 実装や realization 側の最小補正層へ接続する。
- 主に apply、review、session、tui、indexing、quota probe などの builder 互換経路、oracle builder への委譲、旧公開面維持、削除条件確認の入口になる。
- builder 本体の正本仕様ではなく、oracle 側実装を正本に保ちながら既存参照を成立させる package path、module alias、再 export、薄い fallback/補正を扱う。

## Read this when
- acp.builder 経由の旧 import path 互換が、oracle 側 canonical 実装や realization 側 wrapper へどう接続されるか確認したいとき。
- apply fork、review、session、tui、indexing、quota probe などの agent call parameter builder 互換入口、委譲境界、最小補正、fallback の所在を探すとき。
- 既存 caller を canonical path へ移行する作業で、互換 package や再公開 module を残す理由、削除条件、残存参照への影響を判断したいとき。
- oracle 側 builder を正本としつつ、realization 側公開型への適合、module alias、package search path、file access mode 再公開、structured output schema 抑制などの互換処理を調べるとき。

## Do not read this when
- agent prompt、出力条件、parameter 生成内容、builder 本体の正本仕様や人間意図を確認したいだけなら、対応する oracle 側 builder を読む。
- apply、review、session、tui など各機能そのものの実行フロー、UI、branch 操作、finding 処理、quota 管理ロジックを調べる場合は、それぞれの実装領域へ進む。
- AgentCallParameter、FileAccessMode、path model、git helper、構造化出力 schema などの基礎型や共通実装を確認したいだけなら、該当する共通定義を直接読む。
- 新しい公開 API や新規 import 経路を設計したい場合は、この互換領域を入口にせず、現行の canonical 実装または対象機能の公開面を確認する。

## hash
- 24cab1f619625b7b6c17d0a86558d404f9c72d9351af6acca6869c2d3941f528
