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
- ACP の agent call parameter builder 群について、realization 側に残る公開 import path と oracle 側 canonical 実装への互換境界をまとめる領域。多くは正本側実装の薄い再公開・委譲入口であり、実処理本体ではなく、既存参照を壊さずに正本側へ接続する役割を持つ。
- apply fork、review oracle、session、TUI、indexing などの builder 系入口へ進むための上位境界であり、どの系統が互換 package、再公開層、委譲層、一時補正層のどれに当たるかを切り分ける入口になる。

## Read this when
- ACP builder 系の既存公開参照が oracle 側実装へどう接続されているかを、上位から切り分けたいとき。
- agent call parameter builder のうち、apply fork、review oracle、session join、TUI 起動・resolve、indexing 関連のどの入口へ進むべきか判断したいとき。
- realization 側に残る互換 import path、再公開層、委譲層を残す理由や削除条件を確認したいとき。
- oracle 側 package 構造に合わせて realization 側 package が存在している理由を確認したいとき。
- 正本側 builder の戻り値や公開面を realization 側で扱うための適合処理、import path fallback、一時的な互換補正の所在を探し始めるとき。

## Do not read this when
- builder の具体的な prompt、出力条件、structured output schema、正本仕様そのものを確認したいとき。正本側の対応する本文を読む。
- agent call parameter の型定義、file access mode、model class、repo root 解決などの共通構造を確認したいとき。共通定義のある領域へ進む。
- apply fork 全体の CLI 制御、fork 適用処理、git 操作、作業レポート生成フローを調べたいとき。ここは parameter 構築入口と互換境界に限られる。
- TUI の画面表示、イベント処理、入力操作など UI 本体の実装を調べたいとき。TUI 本体の領域へ進む。
- indexing の生成処理、探索処理、データ構造、入出力仕様を調べたいとき。互換入口ではなく実体を持つ正本側実装を読む。

## hash
- a05c840cbeae069b5a217e3011efb80b6404b8ce94f28ae846fffe57203ae605
