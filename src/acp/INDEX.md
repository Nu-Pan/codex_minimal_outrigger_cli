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
- ACP builder 領域の realization 側入口。正本側に実体を置く builder 群について、既存の公開参照経路を維持する互換 package 群と、quota availability probe 用の最小 parameter builder をまとめる。
- apply、review、session、TUI、indexing、file access recovery などの下位領域へ進む前に、実処理本体ではなく互換層・委譲境界・probe parameter 生成のどれを読むべきかを切り分けるための階層。

## Read this when
- ACP builder の realization 側公開入口が、正本側 builder や旧 import 経路とどう対応しているかを確認したいとき。
- apply fork、review oracle、session join、TUI、indexing、file access recovery などの builder 関連作業で、まず下位領域の分担を選びたいとき。
- 正本側実装への委譲、realization 側 parameter 型への適応、互換 wrapper の残置理由や削除条件を確認したいとき。
- Codex quota availability probe 用に、既存 parameter から動作確認用 parameter を組み立てる処理を確認・変更したいとき。

## Do not read this when
- 各 builder の正本仕様、prompt 正本文面、出力条件、判定仕様そのものを確認したいときは、対応する oracle file または正本側実装を読む。
- apply fork の制御フロー、branch 操作、diff 生成、CLI 引数処理、TUI の描画やイベント処理など、builder 入口ではない実行処理を調べたいとき。
- AgentCallParameter、FileAccessMode、model、reasoning effort などの基礎データ構造を調べたいときは、基礎定義側を読む。
- 互換 import 経路や quota probe parameter 生成に関係しない新規機能の実装場所やテスト対象を探しているとき。

## hash
- f71ed6f2f66d30c5e3a816090e2206dc3d311607064cf488f717172c102a9317
