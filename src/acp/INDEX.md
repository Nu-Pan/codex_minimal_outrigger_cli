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
- ACP builder の旧 import 経路を oracle 側の正本実装へ接続する互換層をまとめる領域。realization 側では package path、module alias、再 export、最小限の出力適合を担い、builder の仕様本体や生成ロジックは oracle 側に置く。
- apply fork、review、session、TUI、indexing、quota probe、common recovery など、既存参照を壊さず正本側 builder を利用するための入口を切り分ける。互換層を残す理由、削除条件、正本側実装との対応関係を確認するための上位入口になる。

## Read this when
- ACP builder 周辺の旧 import 互換性、再 export、module alias、oracle 側実装への委譲境界を確認したいとき。
- 正本側 builder の生成結果を realization 側の agent call parameter 型や既存公開面へどう適合させているかを調べたいとき。
- apply fork、review、session、TUI、indexing、quota probe、common recovery などの builder 互換入口のうち、どの下位領域へ進むべきか判断したいとき。
- 互換 wrapper や一時補正を残す理由、削除条件、旧参照から canonical oracle 実装への移行可否を検討するとき。

## Do not read this when
- agent prompt、parameter 生成内容、判定仕様、builder 本体などの正本仕様を確認したい場合は、対応する oracle 側の本文または実装を読む。
- apply の実行フロー、fork 作成、branch 操作、diff 生成、CLI 引数処理など、builder 互換層以外の機能実装を調べたい場合は、その機能本体へ進む。
- agent call parameter の基礎データ構造、汎用変換 helper、repo root 解決、git helper、path model だけを調べたい場合は、それぞれの共通実装を読む。
- TUI 画面、session 挙動、review 判定、indexing 生成処理など、個別機能の実処理やデータ構造を変更したい場合は、互換入口ではなく実体を持つ対象を読む。

## hash
- 6d2d2cd4f62f90144129d2842351186dac529aa02513d4638da681ace1a029e8
