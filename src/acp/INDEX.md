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
- acp builder 配下で、oracle 側 builder 実装を正本に保ちながら旧来の acp.builder 系 import 経路を成立させる realization 側互換入口を束ねる階層。
- apply、review、session、tui、indexing などの builder 群について、canonical oracle 実装への中継、再公開、薄い wrapper、削除条件を確認するための入口になる。
- quota 回復確認用の最小 agent call parameter builder など、通常 builder とは異なる限定用途の実装も含む。

## Read this when
- acp.builder.* の旧 import 互換性や、既存参照を oracle 側実装へ接続する仕組みを確認したいとき。
- apply、review、session、tui、indexing の agent call parameter builder について、realization 側の互換入口、再公開、wrapper、削除可否を調べたいとき。
- oracle 側 builder を呼び出した結果を realization 側公開型や既存公開名へどう適合させるかを確認したいとき。
- quota wait 中の回復確認で使う低コストな probe 用 agent call parameter の構築内容を確認・変更したいとき。

## Do not read this when
- 各 builder の正本仕様、prompt、生成内容、人間意図を確認したい場合は、対応する oracle 側 builder を読む。
- apply fork、review、session、TUI など各機能全体の実行フローや CLI 制御を調べたい場合は、それぞれの上位実装や呼び出し元を読む。
- ACP parameter の公開型、path model、汎用 git helper、index entry 生成仕様など、builder 互換入口以外の共通実装を調べたい場合は該当対象を読む。
- 新規機能の実装場所を探しているだけで、既存 acp.builder import 互換や quota probe に関係しない場合。

## hash
- 110915aad540f1dfc04662648e2159e9f044eabe48fc1f5e3bb982a5458e0fcb
