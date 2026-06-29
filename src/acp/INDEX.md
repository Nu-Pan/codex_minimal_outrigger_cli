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
- ACP builder の realization 側公開入口を束ねる領域。正本側 builder 実装への委譲、既存 import path の互換維持、apply・indexing・review・session・TUI など用途別 builder 領域への入口を扱う。
- この階層の主な役割は、実処理本体を持つ場所ではなく、oracle 側へ集約された実装や下位 builder 領域を既存の acp.builder 系参照から利用できるようにする互換境界として機能すること。
- 具体的な agent call parameter 構築、prompt 補正、oracle src import path fallback、公開名の再エクスポートなどは下位領域ごとに分かれており、この対象はそれらへ進むための上位ルーティング入口である。

## Read this when
- acp.builder 系の公開参照が残っている理由や、oracle 側 builder 実装との互換関係を確認したいとき。
- ACP builder 全体のうち、apply・indexing・review・session・TUI のどの下位領域へ進むべきかを切り分けたいとき。
- realization 側 builder package が正本側 package 構造や既存 import path とどう対応しているかを把握したいとき。
- 互換入口、再公開、委譲境界、削除条件など、builder 領域の公開面維持に関わる変更を検討しているとき。
- apply fork、review oracle、session join、TUI 起動・resolve parameter、indexing 互換入口などの builder 関連入口を探しているとき。

## Do not read this when
- agent call parameter の具体的な構築ロジック、prompt 内容、出力条件、structured output schema、型定義、モデル設定などの詳細を直接確認したいとき。該当する下位実装または正本側実装を読む。
- oracle.acp_builder や各 builder の正本仕様そのものを確認したいとき。この領域は realization 側の互換・委譲入口であり、正本仕様本文ではない。
- ACP builder 以外の CLI 制御、git 操作、TUI 画面制御、レビュー基準、indexing の生成・探索処理、session 状態管理などを調べたいとき。
- 新規機能の本体実装場所やテスト対象を探しているとき。互換 package や公開入口ではなく、処理実体を持つ実装側へ進む。
- acp.builder 系参照の維持・廃止や下位 builder 領域の選択に関係しない ACP 全体の設計を調べたいとき。

## hash
- f4f2de9e5c20a64387105518cacdf920688f46bbf3a6051eeb941796283feb25
