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
- ACP の agent call parameter builder 群を収める領域。正本側に実体を置く builder への互換入口、個別 builder への下位入口、quota probe 用 parameter 生成などを扱い、既存の acp.builder.* 参照から正本側実装や実装側 wrapper へ到達するための境界になる。
- apply、common、indexing、review、session、tui などの builder 系 package の分担を見分け、正本側への委譲、realization 側型への適合、旧 import 経路の維持や削除条件を確認するための上位入口。

## Read this when
- acp.builder.* の公開参照や互換 package が、正本側 builder 実装へどのように接続されているか確認したいとき。
- apply、common、review、session、tui、indexing など、ACP builder 配下のどの下位領域へ進むべきかを選びたいとき。
- 正本側 builder への委譲、realization 側 AgentCallParameter への変換、旧 import 経路の互換 wrapper、削除条件を調べる入口が必要なとき。
- Codex quota availability probe 用の AgentCallParameter 生成元や、probe が base parameter から引き継ぐ条件を確認したいとき。

## Do not read this when
- oracle 側 builder の正本仕様、prompt 本文、生成ロジックそのものを確認したいときは、対応する oracle file または正本側実装を読む。
- apply fork、review、TUI、session join などの具体的な処理内容を直接調べたいときは、該当する下位領域または実処理を持つ module を読む。
- AgentCallParameter 型、model、reasoning effort、file access mode などの基礎定義を確認したいだけのときは、基礎定義側を読む。
- ACP builder 以外の CLI 制御、fork 作成、branch 操作、diff 生成、TUI 描画、状態管理、ファイルアクセス規則の判定を調べたいときは、それぞれの責務を持つ対象へ進む。

## hash
- dc4a372a0843e54d5f1f7c5ba326d674e1f0d2a8415d3016ddcac98f4216995c
