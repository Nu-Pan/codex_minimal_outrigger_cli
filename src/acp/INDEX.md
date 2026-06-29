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
- realization 側の ACP builder 公開面を扱う領域。主な責務は、正本側に置かれた builder 実装を既存の公開 import 経路から利用できるようにする互換入口と、AgentCallParameter 生成の薄い委譲 wrapper を置くことである。
- apply fork、review oracle、indexing、session join、TUI 起動・parameter 解決などの builder 経路を正本側実装へ接続し、一部では repo root 解決、oracle src import 経路補正、生成済み prompt の最小補正、TUI 用 file access mode tuple の公開を担う。
- quota availability probe だけは、現行の正本側に専用 builder がないため、runtime 側に prompt literal を置かないための暫定 adapter として AgentCallParameter を組み立てる。

## Read this when
- 既存の ACP builder import 経路が正本側 builder へどのように接続されているか確認したいとき。
- apply fork、review oracle、indexing、session join、TUI 関連の AgentCallParameter 生成入口や互換公開面を探しているとき。
- 正本側 builder への委譲前後で、repo root 解決、oracle src import 経路補正、parameter 型の適合、prompt 内 placeholder 表記の局所補正があるか確認したいとき。
- quota availability probe の prompt と、元の parameter から引き継ぐ model、reasoning、file access の境界を確認したいとき。
- 互換入口や暫定 adapter を残す理由、または削除できる条件を判断したいとき。

## Do not read this when
- builder の prompt 仕様、出力 schema、判定基準、所見処理などの正本内容を確認したいときは、委譲先の正本側実装または正本仕様断片を読む。
- apply fork、review、session join、TUI、indexing の処理本体や制御フローを変更したいときは、この互換層ではなく実体を持つ実装側を読む。
- Codex exec の quota 待機状態機械、resume token、call log、subcommand event など runtime 側の制御を調べたいときは、runtime 実装を読む。
- TUI の画面表示、イベント処理、入力操作など UI 本体を調べたいときは、TUI 実装側を読む。
- AgentCallParameter、FileAccessMode、path placeholder などの共通型や基礎概念そのものを確認したいときは、基本モジュールや path model を読む。

## hash
- 241bdd22c5749dc57b2371dcb147636186cf73951a4aaa9628dd641c17c8afb2
