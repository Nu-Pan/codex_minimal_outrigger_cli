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
- `acp.builder` 配下の ACP parameter builder 群を束ねるルーティング層。各サブ領域の互換入口と正本実装への案内を集約し、どの builder 系を読むべきかを切り分ける。
- ここでは個別 builder の実処理本体ではなく、`apply`、`indexing`、`review`、`session`、`tui`、`quota_probe.py` などの役割境界と参照先の選び分けを確認する。

## Read this when
- `acp.builder` 配下で、どのサブ領域に進むべきかを判断したいとき。
- 旧来の import 互換を残す入口と、正本実装への委譲先を見分けたいとき。
- ACP parameter builder 群のうち、共通部品と個別 builder の境界を確認したいとき。

## Do not read this when
- 個別 builder の生成ロジックや仕様本体を知りたいときは、この階層ではなく該当サブモジュールを読む。
- `oracle` 側の正本仕様断片そのものを確認したいときは、対応する oracle 配下を読む。
- 単に別の公開名前空間や上位 CLI の振る舞いを調べたいときは、`acp.builder` ではなくその入口を読む。

## hash
- c3795a10e3cf9af6625be5356f5b711a5acafdb9b972dfe5270874b58562d3c9
