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
- ACP builder の realization 側公開入口を束ねる領域。正本実装を oracle 側に置いたまま、既存の acp.builder 系 import path から apply、indexing、review、session、TUI などの builder へ到達できる互換境界を提供する。
- この階層の主な責務は、正本側 package 構造との対応維持、薄い再公開、最小限の適合処理、下位 builder 領域への入口整理であり、各 builder の本体仕様や具体的な処理ロジックは下位領域または oracle 側実装が担う。

## Read this when
- acp.builder 系の公開入口が oracle 側実装や下位 builder 領域へどのように接続されているかを確認したいとき。
- 既存の acp.builder.* 参照を残す理由、互換 import path の位置づけ、削除・移動・置換してよい条件を判断したいとき。
- apply、indexing、review、session、TUI のどの builder 領域へ進むべきかを、この階層の役割から切り分けたいとき。
- realization 側が正本側 builder を再公開するだけなのか、repo root 由来の oracle src import path 追加、戻り値の型適合、TUI 起動時の schema 除去、typo 補正などの最小調整を行うのかを確認したいとき。

## Do not read this when
- oracle.acp_builder 側の正本仕様、prompt 本文、structured output schema、具体的な agent call parameter 構築ロジックを理解したいとき。
- apply fork、review oracle、indexing、session join、TUI resolve parameter など個別 builder の詳細処理や入出力仕様を直接調べたいとき。
- ACP builder 以外の CLI 制御、fork 適用、git 操作、TUI 画面描画、状態管理、共通型定義、file access mode enum の意味を調べたいとき。
- 新規機能の実装場所やテスト対象を探しており、互換公開面や下位領域への入口ではなく処理本体を読むべきとき。

## hash
- 96826ba38afbb19521765a25eeea2eb69e690abc37f358504150320f4fef6669
