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
- ACP builder に関する realization 側の互換入口を束ねる領域。正本側の builder 実装を既存の公開参照経路から利用できるようにし、apply、indexing、review、session、TUI などの下位領域へ進むための境界として位置づく。
- この領域自体は ACP builder の正本仕様や主要ロジックを所有せず、oracle 側実装への委譲、再公開、薄い適合、互換 import path の維持を扱う。

## Read this when
- realization 側の ACP builder 公開入口が、oracle 側 builder 実装へどのように接続されているかを確認したいとき。
- acp.builder 系の既存参照経路を残す理由、互換層の役割、削除条件を確認したいとき。
- apply、indexing、review、session、TUI の各 builder 領域のうち、どの互換入口または下位領域へ進むべきか切り分けたいとき。
- oracle 側の AgentCallParameter 構築結果を runtime 側へ渡す薄い adapter 層や、repo root 解決、oracle src import 準備などの境界処理を探しているとき。
- TUI 起動のように、正本側 builder へ委譲しつつ realization 側で最小限の差分や公開候補を扱う入口を確認したいとき。

## Do not read this when
- ACP builder の正本仕様、prompt 本文、model class、file access mode、Structured Output schema、AgentCallParameter 型そのものを確認したいとき。正本仕様断片または oracle 側の実装を読む。
- apply fork、review oracle、indexing、session join、TUI 本体などの具体的な処理ロジック、判定条件、入出力仕様を調べたいとき。該当する下位領域または正本側実装を読む。
- CLI 制御、git 操作、fork 適用、作業レポート生成、対話 UI の画面描画やキー操作など、builder の互換入口ではない実行フローを調べているとき。
- path model、ACP 共通型、enum 定義など、builder 領域が依存する外部定義そのものを確認したいとき。
- 新規機能の実装場所やテスト対象を探しており、互換 import path の維持や正本側への委譲境界が主題ではないとき。

## hash
- 4c927c8e7730f757825f365bcda38be08832bf513367278fd9b6f08869e31cd2
