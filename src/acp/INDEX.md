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
- ACP builder 関連の既存公開参照を、正本側 builder 実装へつなぐ互換入口をまとめる領域。apply、review、session、TUI、indexing、quota probe などの agent call parameter 生成周辺について、実体が正本側にあるのか、realization 側の薄い wrapper なのかを切り分けるための上位入口である。
- この領域の主な責務は、公開済み import 経路の維持、正本側 builder への委譲、realization 側 parameter 型への適合、互換コードの残置理由と削除条件の確認である。各 builder の正本仕様や詳細ロジックそのものは、下位の個別領域または正本側実装に委ねられる。

## Read this when
- ACP builder 周辺で、既存公開参照が正本側実装へどのように接続されているかを確認したいとき。
- agent call parameter builder の領域分担を見分け、apply、review、session、TUI、indexing、quota probe などのどの下位領域へ進むべきか判断したいとき。
- realization 側に残る互換 package、再公開 module、wrapper、暫定補正について、残す理由や削除条件を確認したいとき。
- 正本側 builder の出力を realization 側で利用する際の委譲関係、型適合、公開 import 経路維持の境界を調べたいとき。
- 同名機能が realization 側にあるように見える場合に、実処理の所在が正本側か互換入口かを切り分けたいとき。

## Do not read this when
- 個別 builder の具体的な生成ロジック、repo root 解決、prompt 文面、出力条件、判定仕様を直接確認したいときは、下位の個別領域または正本側実装を読む。
- CLI コマンド全体の制御フロー、branch 操作、diff 生成、TUI 描画、イベント処理、Codex CLI 実行など、parameter builder 以外の処理を調べたいときは、その責務を持つ実装へ進む。
- agent call parameter の共通データ構造、model、reasoning effort、file access mode などの基礎定義を確認したいときは、基礎定義側を読む。
- 正本仕様断片そのものや oracle 側の実装内容を確認したいときは、互換入口ではなく対応する正本側本文を読む。
- 新しい機能の実装場所やテスト対象を探しているだけで、既存 import 経路の互換維持や正本側 builder への委譲関係を確認する必要がないとき。

## hash
- 8c0a8c3e4b5c601a729618217ed20f80faba0a561f372b10988bddcda449cb59
