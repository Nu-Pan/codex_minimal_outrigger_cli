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
- `acp.builder` 配下の互換入口と薄い実装層をまとめる上位ディレクトリ。正本側の `oracle.acp_builder` へつなぐ公開面維持と、各 builder 領域への振り分けの起点になる。
- この配下は、個別機能そのものよりも、既存 import 経路を壊さずに正本実装へ到達させる役割が中心で、互換公開面を残すかどうかの判断に向く。
- 同じ名前空間の中でも、apply・indexing・review・session・tui・quota_probe などの責務が分かれており、具体仕様は各下位対象を読む。

## Read this when
- `acp.builder.*` の既存参照互換を維持したいとき。
- 正本側の builder 実装へ到達する互換入口の振る舞いを確認したいとき。
- この名前空間にどの薄い公開面を残し、どれを削除できるか判断したいとき。
- 配下の builder 領域を横断して、互換層と正本側実装の境界を確認したいとき。

## Do not read this when
- 個別の builder の具体仕様や生成ロジックを確認したいときは、対応する下位対象を読む。
- 正本側の `oracle.acp_builder` そのものを変更したいときは、そちらを読む。
- `acp.builder` 以外の公開面や別名互換の方針を確認したいとき。
- 新規機能の実装場所を探しているだけで、既存互換層に関係しないとき。

## hash
- c1969d7cacc0d0229d9b80214e3521ae86d68e465f5b9a340233ae7652726ab9
