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
- ACP の agent call parameter builder に関する realization 側の互換入口をまとめる領域。正本側に置かれた builder 実装へ既存の公開参照や import 経路から到達できるようにし、主に再公開・委譲・最小 wrapper によって公開面の互換性を保つ。
- apply、indexing、review、session、TUI などの builder 系領域へ進むための上位入口であり、各領域が実処理本体なのか、正本側実装への互換境界なのかを切り分けるための案内点になる。
- この領域自体は builder の正本仕様や主要ロジックを集約する場所ではなく、正本側実装との対応、旧 import 経路の維持、互換層を残す理由や削除条件を確認するための階層である。

## Read this when
- ACP builder 関連の既存公開参照や旧 import 経路が、正本側 builder 実装へどのように接続されているかを確認したいとき。
- agent call parameter builder のうち、apply、indexing、review、session、TUI のどの下位領域へ進むべきかを上位で切り分けたいとき。
- realization 側に残る builder 互換層について、再公開・委譲・最小 wrapper の範囲、残す理由、削除条件を確認したいとき。
- 正本側へ実装を集約しながら、既存利用者向けの公開 import surface を維持している境界を調べたいとき。

## Do not read this when
- 各 builder の具体的な生成処理、prompt 構築、parameter 型変換、入出力仕様、判定ロジックを直接確認したいときは、正本側の実装または該当する下位領域へ進む。
- ACP 全体の型定義、AgentCallParameter、file access、model、reasoning、structured output schema などの基礎定義を調べたいときは、基本モジュール側を読む。
- CLI コマンド全体の制御フロー、branch 操作、diff 生成、TUI 画面処理など、builder 互換入口ではない機能本体を調べたいとき。
- 新しい builder ロジックや正本仕様を追加・変更する場所を探しているときは、この互換境界ではなく正本側の本文や実体を持つ実装領域を読む。

## hash
- b2dead17d1385da16b0c86e4a9ac2a492b249f55b5896727c83b1bc956b76ad6
