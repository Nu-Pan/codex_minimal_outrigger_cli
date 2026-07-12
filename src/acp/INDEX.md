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
- `acp.builder` 互換の入口をまとめる階層。正本側 `oracle.acp_builder` へつなぐ再公開・委譲・互換維持の責務を持つため、この配下を読む。
- 個別のサブモジュールに進む前の案内役として、互換入口の有無や削除可否、どの公開面を残すかを判断するときに使う。

## Read this when
- `acp.builder` 経由の参照互換を維持したいとき。
- 旧公開名から正本側モジュールへつながる入口の振る舞いを確認したいとき。
- 互換入口を残すか削除するか、どの公開面を維持するかを判断したいとき。

## Do not read this when
- 正本側 `oracle.acp_builder` の実装そのものを変えたいときは、そちらの配下を読む。
- `acp.builder` 配下の個別機能の実装を確認したいときは、この入口ではなく各サブモジュールを読む。
- `acp.builder` 以外の公開面や別名互換の方針を確認したいとき。

## hash
- 1c95c0d73958cffa2a14bb1cf59cdff0ee15b1d04bd60fa3ca384519211ad091
