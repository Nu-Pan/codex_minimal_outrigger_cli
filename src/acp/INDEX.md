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
- ACP builder 領域における realization 側の互換入口群を束ねる階層。正本側に置かれた builder 実装への import 経路を維持し、既存の公開参照を壊さないための薄い再公開境界として機能する。
- 扱う対象は、apply fork 向け agent call parameter 構築入口、indexing 関連実装の互換公開、review oracle 関連 builder の委譲入口、session join 領域への境界、TUI 起動・resolve parameter 構築入口などである。
- この階層自体は各 builder の正本仕様や処理本体ではなく、realization 側から正本側実装へ到達するための package 境界、公開名の維持、局所的な互換補正、削除条件の確認に使う入口である。

## Read this when
- ACP builder 全体で、realization 側の公開 import path と正本側 builder 実装との対応関係を俯瞰したいとき。
- 既存利用者や残存参照を壊さずに、builder 関連の公開入口を維持・廃止・移動できるか判断したいとき。
- apply、indexing、review、session、TUI の各 builder 領域について、どの下位領域へ進むべきかを選びたいとき。
- 正本側 builder への委譲、正本側戻り値の realization 側型への適合、oracle import path の fallback、review prompt の局所的な互換補正など、互換境界の所在を探したいとき。

## Do not read this when
- agent call parameter の具体的な組み立て内容、プロンプト本文、出力条件、型定義、検証規則などの正本仕様を確認したいとき。その場合は委譲先の正本側本文や定義元を読む。
- indexing の生成処理・探索処理・データ構造、review finding の判定基準、session join の具体処理、TUI の画面制御やイベント処理を調べたいとき。各処理本体の領域へ直接進む。
- ACP builder 以外の ACP 関連モジュール、CLI 制御、git 操作、fork 適用処理、作業レポート生成フローを調べたいとき。
- 互換 package 境界や公開入口の維持・削除条件に関係しない新規機能の実装場所やテスト対象を探しているとき。

## hash
- 12275ff74918696d883a8d719eb8c1c93586105d58d269728fcb641a4cc1a686
