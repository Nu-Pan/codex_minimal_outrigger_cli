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
- ACP builder 領域の realization 側入口を束ねる階層。公開済みの builder import 経路を維持しながら、正本側にある実装や定義へ薄く接続する互換境界として位置づけられる。
- 主な下位領域は、apply fork 用 agent call parameter 構築、indexing 互換入口、review oracle への再公開・薄い補正、session join への入口、TUI 起動パラメータ生成・解決への接続を扱う。
- この階層自体は ACP builder の正本仕様や主要アルゴリズムを持つ場所ではなく、realization 側から用途別 builder 領域へ進むためのルーティング起点である。

## Read this when
- ACP builder に関する realization 側の import 経路や互換 package 境界を確認したいとき。
- apply fork、indexing、review、session、TUI のどの builder 領域へ進むべきかを切り分けたいとき。
- 正本側 builder や基本定義を、既存の公開参照経路から利用できるようにする薄い adapter・再公開入口の位置づけを確認したいとき。
- 公開済みの ACP builder 参照経路を削除・移動・置換してよいか判断する前に、残す理由や接続先の種類を把握したいとき。

## Do not read this when
- ACP builder の prompt 本文、Structured Output schema、model 設定、file access mode などの正本仕様を確認したいとき。その場合は正本側の対応箇所へ進む。
- builder の具体的な変換処理、入出力仕様、判定条件、アルゴリズム、エラー処理を理解したいとき。その場合は用途別の実装本体または正本側実装を読む。
- CLI 全体の制御フロー、fork 作成、git 操作、TUI 画面処理、review workflow など、builder import 境界の外側にある実行側処理を調べたいとき。
- AgentCallParameter、path model、列挙値などの基本定義そのものを確認したいとき。その場合は basic 側の定義へ直接進む。

## hash
- c578835c0ab7f8f4bf14c5ad685c4b199763415246c4f8d6fe0f9b0686be08fd
