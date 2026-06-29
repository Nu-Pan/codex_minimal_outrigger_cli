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
- ACP builder の realization 側互換入口を束ねる領域。正本側 builder 実装への再公開・委譲、既存 import 経路の維持、局所的な adapter や prompt 表記補正を扱い、実処理本体は多くの場合正本側または下位領域に置かれる。
- apply fork、review oracle、session join、TUI 起動、indexing、quota availability probe など、agent call parameter 構築に関わる公開参照面と正本側実装との接続関係を確認するための入口になる。

## Read this when
- ACP builder に関する既存の公開 import 経路が、正本側 builder 実装または下位の realization 側 adapter へどう接続されているかを確認したいとき。
- 正本側へ実装を集約しつつ、利用者向けまたは realization 側に残る古い参照を壊さないための互換層を調べたいとき。
- apply fork、review oracle、TUI、session、indexing、quota probe のどの builder 領域へ進むべきかを切り分けたいとき。
- 互換入口や暫定 adapter を残す理由、削除条件、正本側 builder への委譲関係を確認したいとき。
- oracle 側戻り値を realization 側の AgentCallParameter として扱う適合処理、または生成済み prompt への限定的な補正の所在を探したいとき。

## Do not read this when
- builder の正本仕様、prompt 内容、AgentCallParameter の組み立て規則そのものを確認したいとき。正本側の対応する実装や仕様断片を読む。
- ACP 型、FileAccessMode、repo root 解決、oracle src import path などの共通定義や検証規則を確認したいとき。それぞれの定義元を読む。
- CLI 制御、fork 適用処理、git 操作、quota 待機の状態機械、TUI 画面処理など、生成済み parameter の利用側挙動を追いたいとき。
- 新しい builder ロジック、判定処理、探索処理、UI 処理を実装したいとき。互換再公開や薄い adapter ではなく、実体を持つ実装先を読む。
- 特定領域の具体的な関数・クラス・入出力だけを調べたいとき。まず該当する下位領域または正本側本文へ直接進む。

## hash
- 509972bda8d4182bf1dcebeccf844685b6cd780d372d62eb92eb21cd66e47fb8
