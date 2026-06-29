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
- ACP の agent call parameter builder 群に対する realization 側の入口を束ねる領域。正本側実装への委譲、既存公開 import path の互換維持、TUI・apply・review・session・indexing など用途別 builder 境界への案内を担う。
- この階層の多くは処理本体ではなく薄い互換・再公開・補正層であり、具体的な構築ロジックや正本仕様は下位領域または対応する oracle 側実装へ進んで確認する。

## Read this when
- ACP builder 全体の realization 側入口から、apply、review、session、TUI、indexing など用途別の読む先を選びたいとき。
- 既存の acp.builder.* 参照や公開 import path が、oracle 側 builder 実装へどう接続されているかを確認したいとき。
- 正本側へ実装を集約しつつ realization 側に互換入口を残している理由、削除条件、再公開先との対応関係を確認したいとき。
- AgentCallParameter 構築に関する realization 側の薄い委譲層、補正層、公開境界の所在を切り分けたいとき。
- TUI 起動、apply fork、review oracle、session join、indexing 互換入口のどの下位領域へ進むべきか判断したいとき。

## Do not read this when
- AgentCallParameter の型定義、モデル設定、reasoning effort、file access mode、structured output schema など共通仕様そのものを調べたいとき。
- oracle 側 builder の正本仕様、プロンプト内容、具体的な引数組み立て、検証処理の本体を確認したいとき。
- apply fork 全体の CLI 制御、git 操作、作業レポート生成、TUI 画面描画、キー操作など builder 境界外の挙動を調べたいとき。
- indexing の生成処理・探索処理・データ構造、review finding の判定基準や統合方針、session join の具体的な分岐を直接確認したいとき。
- 互換入口ではなく新規機能の実装場所、正本仕様本文、または下位 builder の具体的な処理本体を読む対象が既に分かっているとき。

## hash
- eff139d3af5f23e608bde57bec637a21de0206b9f1098191371687d1f5b46b44
