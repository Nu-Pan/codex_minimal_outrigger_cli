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
- ACP builder 群の旧公開 import 経路と互換入口を集約する領域。oracle 側の canonical builder を正本に保ちつつ、既存の `acp.builder.*` 参照を成立させる薄い再 export、module alias、package path 接続、realization 側公開型への最小変換を扱う。
- apply fork、quota probe、review oracle finding、session、TUI、indexing、common recovery などの builder 入口を含み、builder 本体の正本仕様ではなく、oracle 側実装と realization 側公開面の接続境界を調べるための入口になる。

## Read this when
- `acp.builder.*` 配下の既存 import 互換性、互換 package の残存理由、削除条件、oracle 側 canonical 実装への委譲経路を確認したいとき。
- oracle 側 builder 出力を realization 側の `AgentCallParameter` や既存公開型へどう適合させているかを確認・変更したいとき。
- apply fork、quota probe、review、session、TUI、indexing、common recovery など、特定用途の agent call parameter builder 入口を探したいとき。
- oracle 側 acp builder package を正本に保ちながら、realization 側 package path、module alias、再 export、薄い wrapper をどう配置しているか調べたいとき。

## Do not read this when
- agent prompt、parameter 生成内容、review 判定、TUI 起動パラメータなどの正本仕様や人間意図を確認したいだけなら、対応する oracle 側 builder または oracle doc を読む。
- apply、review、session、TUI など各機能そのものの実行フロー、CLI 引数処理、画面描画、branch 操作、エラー処理を調べたいときは、それぞれの機能実装や呼び出し元へ進む。
- `AgentCallParameter` の基礎構造、model、reasoning effort、file access mode、path model、汎用 git helper などの共通定義を確認したいだけなら、該当する共通実装を直接読む。
- builder の個別変換処理や wrapper の詳細挙動だけを調べる場合は、この領域の入口ではなく、その処理を持つ個別 module または subpackage を読む。

## hash
- 6a3ae3c9cd6c1b99ed5e1afd07b34cb44bdd8c4a81179bd0d37e3d50582c2510
