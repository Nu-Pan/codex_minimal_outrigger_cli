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
- oracle 側の canonical ACP builder を正本に保ちながら、realization 側の既存公開 import 経路を維持する互換層をまとめる領域。
- apply fork、review、session、TUI、indexing、quota probe などの agent call parameter builder について、oracle 実装への委譲、再公開、module alias、package path 接続、必要最小限の出力適合を扱う。
- builder 本体の正本仕様や個別処理ではなく、旧参照を壊さず canonical 実装へ到達させる入口と、その互換経路の残存理由・削除条件を確認するための入口になる。

## Read this when
- ACP builder 周辺の旧 import 経路、再 export、module alias、package path 接続が oracle 側 canonical 実装へどうつながるかを確認したいとき。
- 既存参照を保つための互換 package や shim を残す理由、公開面維持、削除条件、移行可否を判断したいとき。
- apply fork、review、session、TUI、indexing、quota probe の agent call parameter builder 入口を探し、realization 側公開型への変換境界や限定的な wrapper 挙動を確認したいとき。
- oracle 側 builder の生成結果を realization 側の AgentCallParameter や既存利用者向け公開面へ適合させる経路を追いたいとき。

## Do not read this when
- agent prompt、structured output、parameter 生成内容、canonical builder 実装などの正本仕様断片を確認したいだけなら、対応する oracle 側実装や oracle doc を読む。
- apply、review、session、TUI など各機能の実行フロー、CLI 引数処理、永続状態、git 操作、画面描画、イベント処理を調べたい場合は、それぞれの機能実装へ進む。
- AgentCallParameter 型、共通 enum、汎用 git helper、path model、file access rule 検出、ログ収集など builder 互換層以外の共通基盤を調べたい場合は、該当する共通実装を読む。
- 旧 import 互換ではなく個別 builder の変換処理、wrapper の詳細挙動、または新規公開 API の設計をしたい場合は、実体を持つ個別 module や正本側を直接読む。

## hash
- b9b36554de8e04e7c973c12e97027a1c899e2d8049ce3e5f1d51a28bf1d7c05f
