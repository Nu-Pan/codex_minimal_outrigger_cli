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
- ACP builder 領域の realization 側入口。正本側 builder 実装を既存の公開参照経路から利用するための互換 package 群と、quota availability probe 用 parameter builder を扱う。
- 主な責務は、正本側実装への薄い委譲、旧来 import 経路の維持、互換層の残置理由と削除条件の確認、apply・review・session・TUI・indexing など下位 builder 領域へのルーティングである。
- この領域自体は多くの builder 本体仕様を持たず、具体的な処理内容は下位の個別 builder、正本側実装、または実行側 module へ進んで確認する。

## Read this when
- ACP builder 全体で、realization 側の公開 import surface と正本側 builder 実装の対応関係を確認したいとき。
- 既存の acp.builder 系参照が残っている理由、互換入口を残す条件、削除できる条件を判断したいとき。
- apply、review、session、TUI、indexing、common などの builder 関連領域について、どの下位領域へ進むべきかを選びたいとき。
- Codex quota availability probe に渡す最小限の AgentCallParameter の生成内容を確認・変更したいとき。
- 正本側へ実装を集約しつつ、realization 側で旧来参照を壊さないための wrapper や package 初期化境界を調べたいとき。

## Do not read this when
- 各 builder の正本仕様断片、prompt の正本文面、出力条件、判定仕様そのものを確認したいときは、対応する oracle 側の本文を読む。
- apply fork、review oracle、session join、TUI 起動 parameter、indexing 生成処理などの具体的な実装を直接調べたいときは、該当する下位領域または正本側実装を読む。
- AgentCallParameter 型、model、reasoning effort、file access mode などの基礎定義を確認したいときは、基礎定義側を読む。
- Codex CLI の実行規則、quota probe parameter 生成後の runtime 処理、CLI コマンド全体の制御フローを調べたいときは、実行側またはコマンド実装側を読む。
- 互換 import 経路の維持や削除判断と関係しない新規機能の実装場所、画面制御、状態管理、ユーザー向け挙動を探しているときは、より直接その責務を持つ対象へ進む。

## hash
- 677081123f5a0fe4ce05f57b3b2626dbc216883df46012db0d251f3273fd50ab
