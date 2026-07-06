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
- agent call parameter builder の realization 側入口を束ねる階層。主に旧来の acp.builder 系 import 互換を維持し、oracle 側 canonical builder への委譲・再公開・薄い wrapper 境界を扱う。
- apply、review、session、tui、indexing、quota probe などの builder 領域について、既存参照を壊さず oracle 側実装へ接続するための package path、module alias、公開関数、削除条件を確認する入口になる。

## Read this when
- acp.builder 配下の旧 import path 互換が、oracle 側 canonical 実装または realization 側 wrapper へどう接続されるかを調べたいとき。
- apply、review、session、tui、indexing、quota probe の AgentCallParameter builder について、realization 側公開入口、委譲先、再公開境界、互換 shim の削除可否を確認したいとき。
- oracle 側 builder を正本に保ちながら、realization 側で package path、module alias、戻り値変換、限定補正、runtime 補助処理をどこまで担うかを追跡したいとき。

## Do not read this when
- AgentCallParameter の具体的な構築仕様、prompt、出力条件、人間意図を確認したい場合は、対応する oracle 側 canonical builder を読む。
- apply fork、review、session、TUI など各機能全体の実行フロー、CLI 引数処理、状態操作、画面構成、git 処理を調べたい場合は、それぞれの上位実装または直接の機能実装を読む。
- ACP parameter の公開型、汎用 path model、git helper、oracle file 定義、INDEX.md エントリー生成仕様など、builder import 互換以外の共通概念を調べたい場合は、それぞれの共通実装や正本仕様へ進む。

## hash
- 6bfbcfda2722a0c9c52e52da91435c4403b5fe256078eec2a2f60b0866ff5239
