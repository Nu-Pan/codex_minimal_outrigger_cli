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
- ACP builder 配下の realization 側入口をまとめる領域。oracle 側 builder を正本に保ちながら、旧来の `acp.builder` import 経路、apply/review/session/tui/indexing などの互換 package、quota probe 用の軽量 builder へ進むためのルーティング起点になる。
- 主な責務は、canonical oracle 実装への中継、既存参照を壊さない再 export、必要最小限の realization 側適応、各 builder 領域の削除条件や互換維持理由の確認入口を分けることにある。

## Read this when
- ACP builder 全体で、旧 import path 互換、oracle 側 canonical builder への委譲、realization 側公開型への適応境界のどこを読むべきか選びたいとき。
- apply fork、review oracle、session、TUI、indexing、quota probe などの agent call parameter builder 領域を横断して、該当する下位 package または module への入口を探すとき。
- `acp.builder.*` 参照の移行・削除・互換維持を検討しており、どの互換入口がどの責務を持つか切り分けたいとき。

## Do not read this when
- oracle 側 builder の正本 prompt、canonical 実装、生成内容そのものを確認したい場合は、対応する oracle 側の実装や doc を直接読む。
- ACP parameter の共通型、汎用 git helper、path model、CLI 実行フロー、TUI 描画、apply/review/session の本体挙動など、builder 入口や import 互換と無関係な詳細を調べたい場合は、それぞれの実装領域へ進む。
- 個別 builder の変換処理、wrapper の詳細、quota probe の呼び出し制御など読む対象が既に特定できている場合は、この階層ではなく該当する下位 module または呼び出し元を直接読む。

## hash
- cb74f5bae750efd7e34355906d2dbf73619b6c92f710c13d85f84d87e1ecdf03
