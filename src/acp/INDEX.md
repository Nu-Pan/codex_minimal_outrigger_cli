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
- AgentCallParameter builder 群の realization 側入口を束ねる領域。多くは正本側実装への委譲・再公開・互換 import path 維持を担い、既存参照を壊さずに正本側 builder を利用できる境界として位置づく。
- apply fork、review、session、TUI、indexing、quota probe など用途別の builder 入口へ進むための上位ルーティング対象。prompt や parameter の正本仕様そのものではなく、realization 側公開面と正本側実装の接続関係を切り分けるために読む。
- 一部には正本側 builder が未整備な用途の暫定 adapter や、正本側 builder の生成結果に対する局所的な補正 wrapper が含まれるため、互換層を残す理由、削除条件、委譲先との対応を確認する入口になる。

## Read this when
- ACP builder の realization 側公開入口が、正本側 builder や既存 import path とどう対応しているかを用途別に確認したいとき。
- apply fork、review、session、TUI、indexing、quota probe などの agent call parameter 構築入口を探し、どの下位領域へ進むべきか判断したいとき。
- 互換再公開、薄い委譲 wrapper、暫定 adapter、prompt 表記補正など、builder 周辺の realization 側境界を残す理由や削除条件を確認したいとき。
- 公開済み参照経路の維持・廃止、正本側 import path への移行、残存参照の整理に関わる変更を検討しているとき。

## Do not read this when
- AgentCallParameter の prompt 内容、出力条件、型定義、正本仕様そのものを確認したいとき。正本側の対応する仕様断片または実装を読む。
- 各用途の処理本体、CLI 制御、git 操作、TUI 画面処理、session join の衝突解決、indexing の生成・探索処理などを調べたいとき。ここは主に builder 入口と互換境界を扱う。
- 新しい機能の実装場所やテスト対象を探しており、既存 builder の公開面・委譲関係・互換層が関係しないとき。より直接の実装領域またはテスト領域へ進む。
- 生成済み parameter の利用側挙動だけを追う作業で、builder の import 経路、正本側への委譲、暫定 adapter、局所補正の有無が判断材料にならないとき。

## hash
- 241bdd22c5749dc57b2371dcb147636186cf73951a4aaa9628dd641c17c8afb2
