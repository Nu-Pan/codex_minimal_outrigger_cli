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
- ACP builder 領域全体の入口。oracle 側 builder を正本に保つための import path 接続、旧 acp.builder 系公開面の互換維持、各サブコマンド向け builder package へのルーティングを扱う。
- apply、review、session、tui、indexing、quota probe などの builder 互換層や個別 builder 入口を下位に持ち、実処理本体よりも canonical oracle 実装への委譲・再公開・最小補正の境界を確認する起点になる。

## Read this when
- acp.builder 配下の旧 import 経路互換、oracle 側 builder への接続、module alias、package path の扱いを広く確認したいとき。
- apply fork、review、session、tui、indexing、quota probe のどの builder 領域へ進むべきか判断したいとき。
- oracle 側 builder を正本としつつ realization 側で公開型への適合、既存 caller 向け再公開、互換入口の削除条件を調べたいとき。
- acp.builder 配下の互換 package や薄い wrapper を削除・移行する作業で、対象となる下位領域を選びたいとき。

## Do not read this when
- agent call parameter の型定義、path model、file access mode、git helper など builder 以外の共通基盤を調べたいときは、それぞれの定義元を読む。
- prompt、出力条件、parameter 生成内容の正本仕様や人間意図を確認したいだけなら、対応する oracle 側 builder または oracle document を直接読む。
- apply、review、session、tui など各機能本体の実行フロー、CLI 引数処理、状態操作、画面構成を調べたいときは、対象機能の実装へ進む。
- 特定 builder の個別変換処理、fallback、再公開、補正挙動が分かっている場合は、この階層全体ではなく該当する下位 package または module を読む。

## hash
- 651246c3a0407f43a09b25729e30829c6b095bf74ce930fbbce04067e94d0de4
