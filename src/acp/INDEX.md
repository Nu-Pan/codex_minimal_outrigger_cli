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
- ACP の agent call parameter builder 群に対する realization 側の公開入口と互換境界を束ねる領域。正本側実装を本体としつつ、既存の公開参照経路から apply、indexing、review、session、TUI 関連の builder 機能へ到達できるようにする。
- この階層は主に package 境界、再公開、委譲、互換維持、削除条件の確認に使う入口であり、各 builder の正本仕様や具体的な構築ロジックそのものは下位領域または正本側実装に置かれる。

## Read this when
- ACP builder 領域で、realization 側の公開 import path と正本側 builder 実装との対応関係を把握したいとき。
- 既存の acp.builder 系参照を残す理由、互換入口の役割、削除してよい条件を確認したいとき。
- apply、indexing、review、session、TUI のどの builder 領域へ進むべきかを、この階層の責務境界から切り分けたいとき。
- 正本側 builder への委譲、再公開、戻り値や import path の互換調整など、realization 側に残された薄い境界処理の所在を探しているとき。

## Do not read this when
- ACP builder の具体的な parameter 構築処理、プロンプト本文、出力 schema、判定意味論などの正本仕様を確認したいとき。対応する正本側本文または下位実装を読む。
- apply fork、review、session join、TUI など個別機能の詳細な制御フロー、入出力変換、git 操作、画面挙動を調べたいとき。より直接の機能実装へ進む。
- AgentCallParameter 型、model class、reasoning effort、file access mode、repo root 解決などの共通定義や一般仕様を調べたいとき。定義元の共通領域を読む。
- 新しい builder 機能の本体実装や仕様追加先を探しているとき。この階層は互換公開面と委譲入口が中心であり、処理本体の追加場所ではない。

## hash
- d2e3501d55dd034c5beb16f1948eea45e75562f13e455f187bc04f958e95572b
