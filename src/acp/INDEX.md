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
- `acp.builder` 系の互換入口をまとめる上位ディレクトリ。正本側 `oracle.acp_builder` への転送や再公開を担う入口と、apply・review・session・indexing・tui・quota_probe の各配下をここから振り分ける。
- この階層は実処理本体ではなく、旧 `acp.builder.*` 参照をどこへつなぐか、どの互換面を残すかを判断するための案内点として読む。

## Read this when
- `acp.builder.*` の旧 import 互換を維持したい、または削除できるか判断したいとき。
- `oracle.acp_builder` を正本に保ちながら、この階層がどのサブ領域を公開しているか確認したいとき。
- 互換入口の削除条件や、apply・review・session・indexing・tui・quota_probe のどこへ進むべきかを選びたいとき。

## Do not read this when
- `oracle.acp_builder` 側の正本実装そのものを変更したいときは、そちらの配下を読む。
- apply・review・session・indexing・tui の個別挙動や builder 本体を確認したいときは、この上位入口ではなく各サブモジュールを読む。
- quota probe の実装詳細や最小 fallback の内容を確認したいときは、この階層ではなく `quota_probe.py` を読む。

## hash
- 28cfc0ab2dcf9899e47631a1bc14a9e0336969323e4aba9e1db9744698d7ce10
