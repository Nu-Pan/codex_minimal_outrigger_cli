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
- ACP の agent call parameter builder について、realization 側の公開 import 経路と oracle 側の正本実装を接続する互換・委譲層を扱う領域。多くは既存参照を壊さないための薄い再公開入口で、実装本体は oracle 側に置かれる。
- apply、review、session、TUI、indexing などの builder 名前空間ごとに、oracle 側 package 構造との対応、既存公開面の維持、削除条件、局所的な prompt 表記補正や parameter 変換境界を確認するための入口になる。
- quota availability probe については、現行 oracle 側に専用 builder がない制約を補う暫定 adapter を含み、runtime に prompt literal を置かず AgentCallParameter 構築境界へ揃える役割を持つ。

## Read this when
- ACP builder 系の古い公開 import 経路が、oracle 側の canonical 実装や package 構造へどう接続されているか確認したいとき。
- agent call parameter 生成について、realization 側でどこまでを互換層・委譲・変換・局所補正として扱っているか切り分けたいとき。
- apply fork、review oracle builder、session join、TUI 起動や resolve parameter、indexing 関連の builder 入口から、目的に合う下位領域を選びたいとき。
- 互換入口を残す理由、正本側実装への移行状況、既存参照がなくなった後の削除条件を確認したいとき。
- quota probe 用の暫定 parameter builder が存在する理由、引き継ぐ parameter 境界、oracle 側専用 builder が追加された場合の置換対象を確認したいとき。

## Do not read this when
- AgentCallParameter 型、FileAccessMode、path model、git helper などの共通型・共通処理そのものを調べたいときは、それぞれの基本実装へ進む。
- prompt の正本仕様、人間意図、builder の canonical な組み立て仕様を確認したいときは、対応する oracle 側の仕様断片または実装を読む。
- apply fork 全体の制御フロー、branch 操作、CLI 引数処理、diff 生成、quota 待機状態機械、resume token、call log などの利用側 runtime 挙動を追いたいときは、呼び出し元の実装へ進む。
- TUI の画面表示、イベント処理、入力操作、UI 構成など、parameter builder ではない UI 本体を調べたいとき。
- indexing や review finding の生成・探索・判定・検証ロジックそのものを変更したいときは、互換再公開層ではなく実処理を持つ正本側または対象実装を読む。

## hash
- 21b2c425b5fa37d72873f57fd9bae15ac676a8684bd5511ce6b9341ea7aaf7ea
