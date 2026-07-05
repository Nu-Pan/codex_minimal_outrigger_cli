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
- ACP builder 領域の入口。oracle 側 builder を正本として扱いながら、旧来の公開名前空間や既存 import 経路を維持する互換層と、quota probe・apply fork・TUI など一部の realization 側 AgentCallParameter 構築境界をまとめる。
- 主な責務は、canonical oracle 実装への委譲・再公開、旧 import 互換の削除条件確認、oracle builder 戻り値を realization 側公開型や runtime 要件へ最小限適合させる境界の把握である。

## Read this when
- ACP builder 全体で、oracle 側正本実装と realization 側互換入口の接続方針を確認したいとき。
- 旧来の acp.builder 系 import path を canonical 実装へ移行する作業で、互換 package や再公開モジュールを残す理由・削除条件を調べたいとき。
- apply fork、quota probe、review、session、TUI、indexing などの builder 領域のうち、どの下位対象へ進むべきかを判断したいとき。
- oracle builder の生成結果を realization 側 AgentCallParameter、公開型、runtime 保存、既知表記補正へ適合させる境界を探しているとき。

## Do not read this when
- agent prompt、出力条件、parameter 生成内容の正本仕様や人間意図を確認したいだけなら、対応する oracle 側 builder を読む。
- apply、review、session、TUI など各機能そのものの実行フロー、CLI 引数処理、状態操作、UI 挙動を調べたいなら、それぞれの機能実装へ進む。
- ACP parameter の公開型、汎用 git helper、path model、file access mode、Structured Output schema など builder 互換層と無関係な基礎実装を確認したいなら、該当する共通実装を直接読む。
- 新しい公開 API や新規 import 経路を設計したいだけなら、既存互換層ではなく正本仕様と利用者向け公開面の方針を確認する。

## hash
- fcc671a2003cd9edba9f36d1a2592ac512b9ff9c97b3c8f9795c5777a9bb558a
