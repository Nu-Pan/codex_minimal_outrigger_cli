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
- ACP builder 領域で、oracle 側 builder 実装を正本に保ちながら、既存の realization 側 import 経路を維持する互換入口を束ねる階層。
- apply、common、indexing、quota probe、review、session、TUI などの builder 互換 package や wrapper へ進むための入口であり、実処理や正本仕様そのものではなく、oracle 側実体への委譲、再公開、型適合、削除条件の確認に使う。

## Read this when
- ACP builder 配下で、既存 import path と oracle 側 builder 実装の接続関係を確認したいとき。
- oracle 側 builder を正本に保ちつつ、realization 側で package path、module alias、薄い wrapper、公開型への変換をどう維持しているか調べたいとき。
- apply、common、indexing、quota probe、review、session、TUI など、特定 builder 領域の互換入口や削除条件へ進む対象を選びたいとき。
- 正本側実装への移行中に残された旧 import 経路、再公開、暫定補正、互換 layer の残存理由を確認したいとき。

## Do not read this when
- builder の prompt、parameter 内容、判定仕様、生成ロジックなどの正本仕様を確認したいだけなら、対応する oracle 側実装を直接読む。
- ACP parameter の基礎データ構造、共通変換処理、repo root 解決、oracle src import 準備の詳細を調べたい場合は、該当する共通 helper や型定義へ進む。
- apply fork、review、TUI、session join などの具体的な実行フロー、状態管理、UI 制御、判定処理を変更したい場合は、互換入口ではなく実処理を持つ個別 module を読む。
- 新しい公開 API や import 経路を追加する場所を探しているだけのとき。

## hash
- 63022a3aec2f6a77c84b0455fe08cb7b91fd891359d35ec9d2544f14ccde1998
