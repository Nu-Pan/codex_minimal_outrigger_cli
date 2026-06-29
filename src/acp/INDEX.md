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
- ACP builder の realization 側互換境界を束ねる領域。正本実装を持つ oracle 側 builder 群を、既存の利用経路から参照できるようにする入口として機能する。
- この領域自体は builder 本体仕様や主要ロジックの置き場ではなく、apply fork、review oracle、session join、TUI パラメータ、indexing などの builder 関連下位領域へ進むための package 境界と再公開・薄い adapter を扱う。

## Read this when
- ACP builder に関する realization 側の import 経路が oracle 側実装とどう接続されているか確認したいとき。
- 既存の builder 参照経路を削除・移動・置換してよいか判断するため、互換入口として残されている範囲と削除条件を確認したいとき。
- apply fork の agent 呼び出しパラメータ生成、review oracle の finding 列挙・判定・統合・検証、session join、TUI 起動パラメータ、indexing など、builder 関連の下位領域へ進む入口を探しているとき。
- realization 側が独自の主要ロジックを持つのか、oracle 側実装への委譲・再公開・薄い補正に留まるのかを切り分けたいとき。

## Do not read this when
- builder の正本仕様、prompt 本文、Structured Output schema、モデル設定、file access mode、具体的な変換・判定・生成ロジックを確認したいとき。その場合は oracle 側の対応箇所へ進む。
- apply fork 全体の制御フロー、fork 作成、git 操作、実行 orchestration、CLI 入出力、TUI 画面やイベント処理など、builder 互換境界ではない実行本体を調べたいとき。
- repository root 解決、path model、AgentCallParameter、列挙値などの基本定義そのものを調べたいとき。
- ACP builder 以外の ACP 関連モジュール、または互換入口ではない新規機能の実装場所やテスト対象を探しているとき。

## hash
- 4d4500d717d7c2690d59a43a877d9b6e074e66edecef09b77203bc4b706505e9
