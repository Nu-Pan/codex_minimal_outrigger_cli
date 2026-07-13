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
- `src/acp/builder` は、`oracle.acp_builder` を `acp.builder` 互換の入口として見せるための公開層。正本側の実装へつなぐ初期化と、共通化された builder 群の受け口をまとめる。
- この階層は、旧来の `acp.builder.*` 参照を壊さずに正本側へ到達させたいときに読む。個別機能の本体ではなく、互換入口として何を公開し続けるかを確認するための場所である。
- 個別の builder 実装や正本仕様の詳細はここでは扱わない。実処理、出力条件、内部の parameter 生成は、対応する下位モジュールか `oracle.acp_builder` 側を読む。

## Read this when
- `acp.builder.*` の参照互換を維持したいとき。
- `oracle.acp_builder` へつながる入口として、この階層がどの公開面を残すか確認したいとき。
- この階層が共通 builder 群の受け口としてどう位置づくかを見たいとき。

## Do not read this when
- 正本の builder 実装そのものを確認したいときは、`oracle.acp_builder` 側を読む。
- 個別機能の実装や parameter 生成の詳細を見たいときは、この入口ではなく下位モジュールを読む。
- 互換入口ではなく、新規の公開 API や別の責務を持つ実装を探しているとき。

## hash
- 34427003fab66070874be4054703ae70d463a5f4f91210cf185bb82dc9a3a6b6
