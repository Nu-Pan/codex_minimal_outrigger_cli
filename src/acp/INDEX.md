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
- `src/acp/builder` 配下の互換入口と canonical 実装への橋渡しをまとめる階層。`oracle.acp_builder` 側の正本 builder を既存の `acp.builder.*` 参照から到達できるようにし、必要に応じて薄い互換層だけを残す。
- この階層で扱うのは、apply / indexing / review / session / tui の各 builder 系入口と、quota 判定の互換呼び出し、および共通処理の置き場である `common`。個別の実処理本体ではなく、どの公開経路を維持するかの判断が主目的になる。
- `__init__.py` は `acp.builder` 互換の入口、各サブディレクトリは旧 import path 互換や正本実装への再公開を担う。実装詳細を追うより、どの名前空間を残すべきか、どの入口が正本へ委譲するかを確認するための層である。

## Read this when
- `acp.builder.*` の既存参照を壊さずに、どの互換入口を維持・削除できるか判断したいとき。
- apply / indexing / review / session / tui の builder 系で、正本実装への委譲経路や薄い互換 wrapper の有無を確認したいとき。
- quota 判定や共通 builder 処理のように、複数の builder 入口から使われる補助的な経路を確認したいとき。
- 旧公開名前空間から canonical 実装へどうつながるか、またはどの公開面を残すべきかを決めたいとき.

## Do not read this when
- 各 builder の具体的な生成ロジック、入出力仕様、エラー条件そのものを追いたいときは、対応する正本実装側を読む。
- `acp.builder` 以外の公開 API や新規機能の追加先を探しているだけなら、この互換階層は優先しない。
- 個別の CLI フロー、fork/session の実行手順、TUI 画面構成など、より上位の機能仕様を知りたいときは別の対象を読む。

## hash
- bc29784563a5175bfb57e516fcd7c95ab9cedc44609043ca97f928f533d3485e
