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
- ACP builder 群の公開入口を扱う領域。oracle 側 builder を正本に保ちながら、旧来の acp.builder import 経路を canonical 実装や realization 側の最小適応層へ接続する。
- apply fork、quota probe、review、session、TUI、indexing などの agent call parameter builder 互換入口と、個別 builder 領域へ進むためのルーティング起点になる。
- 主な責務は、oracle builder への委譲、既存 import 互換、module alias、package path 接続、必要最小限の realization 側変換境界の確認であり、prompt 正本や各機能本体の実行処理は扱わない。

## Read this when
- acp.builder 経由の import 互換性や、旧公開名前空間から oracle 側または canonical 実装へ到達する経路を確認したいとき。
- agent call parameter builder のうち、apply fork、quota probe、review、session、TUI、indexing のどの領域へ進むべきかを判断したいとき。
- oracle 側 builder を正本としつつ、realization 側で package path、module alias、戻り値変換、既知表記補正などをどこで扱うか調べたいとき。
- 既存 caller を canonical path へ移行する作業で、互換 package や再公開モジュールを残す理由、削除条件、残存参照の確認入口を探しているとき。

## Do not read this when
- agent prompt、出力条件、parameter 生成内容の正本仕様や人間意図を確認したい場合は、対応する oracle 側 builder や oracle file を読む。
- apply、review、session、TUI など各機能そのものの実行フロー、UI、branch 操作、diff 生成、CLI 引数処理を調べたい場合は、その機能本体の実装へ進む。
- AgentCallParameter の型定義、構造化出力 schema、path model、汎用 git helper、runtime path など共通基盤を確認したいだけの場合は、それぞれの定義元を読む。
- 新規公開 API や新規 import 経路を設計したいだけの場合は、この互換領域ではなく、利用者向け公開面や設計対象の定義元を確認する。

## hash
- 5e5a44ec80b92a675a1e2b3be41555d9951673d48755266da2028992d4d7fc06
