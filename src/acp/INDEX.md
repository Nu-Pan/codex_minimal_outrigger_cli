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
- ACP builder 領域で、oracle 側 builder 実装を正本に保ちながら既存の realization 側 import 経路を成立させる互換層を束ねる階層。
- 各 subpackage や wrapper は、oracle 側 package への search path 接続、旧 import path から canonical 実装への再公開・委譲、oracle parameter から realization 側公開型への最小変換を担う。
- 実処理や正本仕様そのものではなく、apply、common、indexing、quota probe、review、session、TUI などの builder 互換入口と、移行中の公開面を残す理由・削除条件を確認するための入口になる。

## Read this when
- ACP builder 全体で、oracle 側実装を正本としつつ realization 側の既存 import surface をどう維持しているか確認したいとき。
- acp.builder 経由の旧参照、subpackage 互換入口、module alias、package path 接続、再公開先の対応関係を調べたいとき。
- oracle builder の戻り値を realization 側の AgentCallParameter や公開型へ適合させる wrapper の場所を探したいとき。
- apply、common、indexing、quota probe、review、session、TUI の各 builder 領域について、互換層を残す理由、移行状況、削除条件を確認したいとき。

## Do not read this when
- builder の prompt、parameter 生成内容、判定ロジック、変換処理本体などの正本仕様を確認したいときは、対応する oracle 側実装を読む。
- CLI コマンド全体の実行フロー、fork 作成、branch 操作、diff 生成、TUI 描画、状態管理など、builder 互換入口以外の実処理を調べたいときは、該当する実装領域を読む。
- AgentCallParameter の基礎構造、公開型、共通 model 設定、file access mode 全体の定義を確認したいときは、基本型定義や共通実装を読む。
- 個別 builder の具体的な関数、クラス、出力、制御フローを変更したいときは、この階層の入口ではなく、該当する個別 module または正本側実装を読む。

## hash
- ba9ad87e2f8de11a4449d9664f10683d35ffd21cc94bbac1b69a978f7b0f87d3
