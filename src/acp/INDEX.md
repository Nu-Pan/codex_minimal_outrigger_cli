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
- `acp.builder` 配下の互換入口と共通ビルダー群をまとめるルーティング対象。旧 `acp.builder.*` の参照を正本側へつなぐ薄い層と、quota / indexing / review / session / tui などの builder 入口を分けて案内する。
- この階層は、実処理の本体よりも「どの公開面を残すか」「どこから正本実装へ進むか」を判断するために読む。

## Read this when
- `acp.builder.*` の既存 import 互換を維持したい、または削除可否を判断したいとき。
- quota probe、indexing entry、review、session join、tui の各 builder 入口が正本側へどうつながるかを確認したいとき。
- 共通 builder の責務境界や、互換 wrapper と実体の切り分けを確認したいとき。

## Do not read this when
- 個別 builder の具体的な生成ロジックや出力仕様を確認したいときは、対応する正本実装側を読む。
- `acp.builder` 以外の公開面や別機能の実装方針を調べたいとき。
- 単に実装本体の詳細を追いたいだけなら、このルーティング層ではなく各サブモジュールへ直接進む。

## hash
- 62b85fcbf9d4c7d1b995384179bfff1694efb6b3337fe518f6e6760f85df9d72
