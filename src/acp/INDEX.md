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
- ACP builder 配下の realization 側互換入口をまとめる領域。oracle 側に置かれた正本 builder 実装を既存の acp.builder.* 参照から利用できるようにし、apply、common、indexing、review、session、tui、quota probe などの下位領域へ進むための上位入口となる。
- この階層は builder 本体仕様や各処理の正本ではなく、公開 import path の維持、oracle 側実装への委譲、realization 側 parameter への適応、互換 wrapper の残置理由と削除条件を見分けるために読む。

## Read this when
- acp.builder.* 参照が oracle 側 builder 実装へどの互換入口を経由して接続されているか確認したいとき。
- apply、common、indexing、review、session、tui、quota probe など、ACP builder 関連の読む先を上位階層から選びたいとき。
- realization 側に残る builder 互換 package、旧 import 経路、公開名、委譲先、削除条件を確認したいとき。
- oracle 側の正本 builder を利用しつつ、既存利用者や残存参照を壊さないための公開面を調べたいとき。

## Do not read this when
- 個別 builder の具体的な生成ロジック、repo root 解決、parameter 型変換、prompt 補正などを直接確認したいときは、該当する下位領域へ進む。
- builder の正本仕様、prompt 文面、出力条件、判定仕様、file access rule などを確認したいときは、対応する oracle file または正本側実装を読む。
- AgentCallParameter、FileAccessMode、model、reasoning effort などの基礎定義を調べたいときは、基礎定義側を読む。
- CLI コマンド全体の制御フロー、fork 作成、branch 操作、TUI 描画、runtime 実行処理など、ACP builder 互換入口ではない責務を調べたいときは、より直接の実装領域へ進む。

## hash
- 40926c0ca3cd569f9931362761ea2a508ebb48d2d3ddefc14a56b0b256b1e4f3
