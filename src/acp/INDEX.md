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
- ACP の agent call parameter builder 群への上位入口。正本側 builder を既存の実装側参照経路から利用するための互換 package 群と、quota probe など実装側で持つ builder を含む。
- apply、review、session、TUI、indexing、file access recovery などの builder 領域へ進む前に、各下位領域が互換入口なのか具体的な parameter 生成実装なのかを見分けるための階層。

## Read this when
- ACP builder 全体で、目的の agent call parameter 生成処理や互換入口がどの下位領域にあるかを選びたいとき。
- 正本側 builder を実装側の既存 import path から参照するための互換層、公開参照経路、削除条件を確認したいとき。
- apply fork、review oracle、session join、TUI 起動、file access recovery、indexing、quota probe などの builder 関連処理の入口を探しているとき。
- builder 領域に見える実装が、正本側への薄い委譲・再公開なのか、実装側で parameter を組み立てる処理なのかを切り分けたいとき。

## Do not read this when
- 個別 builder の具体的な関数、型変換、prompt 補正、import 経路補正、schema fallback などを直接確認したいときは、該当する下位領域を読む。
- agent call parameter の基礎型、model、reasoning effort、file access mode の定義を調べたいときは、基礎定義側を読む。
- CLI コマンドの制御フロー、branch 操作、diff 生成、Codex CLI 実行、TUI 描画など、parameter builder 以外の実処理を調べたいときは、それぞれの実行側を読む。
- 正本仕様断片、prompt の正本文面、oracle 側 builder 本体、indexing や review の仕様そのものを確認したいときは、対応する oracle 側の本文を読む。

## hash
- fb147b6aed1448b03b9b4c86ee7c9d25d77e9075c5cd6dae3faf8efe8d4b6f7d
