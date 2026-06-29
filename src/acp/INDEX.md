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
- ACP builder の realization 側公開入口を束ねる階層。正本実装を oracle 側に置いたまま、既存の builder 参照経路を維持する互換 package と薄い adapter 群を配置している。
- 主な入口は、apply fork の agent call parameter 構築委譲、indexing 実装の再公開、review oracle 機能の再公開と一部 prompt placeholder 補正、session join への互換経路、TUI 起動・解決パラメータの再公開で構成される。
- この階層は builder 本体仕様を所有する場所ではなく、realization 側から oracle 側正本実装へ到達する import 境界と、既存参照を壊さないための互換面を確認するための入口である。

## Read this when
- ACP builder の既存公開参照が、oracle 側の正本実装へどのように接続されているかを確認したいとき。
- apply fork、review oracle、indexing、session join、TUI 関連の builder 入口が realization 側でどの領域に分かれているかを把握したいとき。
- builder 互換 import path を削除・移動・置換してよいか、残す理由や削除条件を確認したいとき。
- oracle 側 builder へ委譲する前後で、realization 側が行う最小限の調整や adapter 境界を探したいとき。

## Do not read this when
- builder の正本仕様、prompt 本文、Structured Output schema、モデル設定、file access mode などを確認したいとき。対応する oracle 側の本文や実装を読む。
- apply fork や review workflow の CLI 制御、git 操作、fork 作成、入出力処理など、builder 外の実行フローを調べたいとき。
- indexing、session join、TUI、review 判定などの具体的なアルゴリズムや入出力仕様そのものを理解したいとき。委譲先の oracle 側実装またはより直接の下位領域へ進む。
- 互換公開面ではなく、新しい機能の実装場所、公開 API の追加、または builder 以外の ACP 関連責務を探しているとき。

## hash
- 73e625154b662dd2592a44d610000f5654108ab1f4036fdf4e52eb18b5162050
