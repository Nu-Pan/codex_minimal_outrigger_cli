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
- ACP builder 領域の realization 側入口をまとめる階層。正本側実装を既存の公開参照経路から利用するための互換入口と、apply・review・session・TUI・indexing などの下位 builder 領域への案内を担う。
- この階層は builder 本体の正本仕様や各処理の詳細を所有する場所ではなく、realization 側の import path を維持しながら oracle 側実装へ委譲する境界と、下位領域を選ぶための入口として位置づけられる。

## Read this when
- realization 側で ACP builder 関連の公開参照経路や package 構成が、正本側実装とどう接続されているか確認したいとき。
- apply、review、session、TUI、indexing のどの builder 領域へ進むべきかを大まかに切り分けたいとき。
- 旧来の acp.builder 系参照を残す理由、正本側実装への再公開関係、互換入口の削除条件を確認したいとき。
- builder の処理本体ではなく、realization 側から oracle 側 builder へ委譲する入口や互換名前空間を探しているとき。

## Do not read this when
- 各 builder の prompt 本文、structured output schema、モデル選択、file access mode、判定基準などの正本仕様を確認したいとき。対応する oracle 側の本文を読む。
- apply、review、session join、TUI、indexing の具体的な処理内容や入出力仕様をすでに調べる対象として特定しているとき。該当する下位領域または正本側実装へ直接進む。
- CLI 全体の制御フロー、fork 作成、git 操作、ユーザー向け挙動、TUI 画面やイベント処理を調べたいとき。builder 互換入口ではなく、それらを実装する対象を読む。
- AgentCallParameter、path model、基本 enum、共通型など、builder 領域に限らない基礎定義そのものを確認したいとき。

## hash
- 7ddfd871aad11ab69af2fec2a0597606862fec9d41c5fa92f22802580f6525c7
