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
- agent call parameter builder 群の realization 側領域。oracle 側 builder を正本に保ちながら旧 import 経路を維持する互換入口と、quota probe・TUI・apply fork など一部呼び出し用途向けの最小適応層をまとめる。
- 主な責務は、canonical oracle 実装への中継、既存参照を壊さない再公開、oracle builder 戻り値を realization 側公開型や runtime path へ接続する境界の提供であり、prompt 本文や正本仕様そのものは扱わない。

## Read this when
- agent call parameter builder 周辺で、旧 import 経路がどの canonical 実装や互換入口へつながるかを確認したいとき。
- oracle 側 builder を正本に保ちつつ、realization 側で package path、module alias、公開型変換、runtime path 接続をどう補っているかを調べるとき。
- apply fork、quota availability probe、review、session、TUI などの agent call parameter 構築入口や互換層の残存理由・削除条件を確認したいとき。
- 既存 caller を canonical path へ移行する作業で、互換 package や再公開 module の影響範囲を絞りたいとき。

## Do not read this when
- agent prompt、出力条件、parameter 生成内容の正本仕様や人間意図を確認したい場合は、対応する oracle 側 builder や oracle file を読む。
- agent call parameter の基本型、enum、構造化出力 schema、汎用 git helper、path model などの共通定義を調べたい場合は、それぞれの定義元へ進む。
- apply、review、session、TUI など各機能の実行フロー、UI、branch 操作、結果判定、外部コマンド実行を調べたい場合は、機能本体の実装を読む。
- 互換 import 経路ではなく新規公開 API や新機能の設計だけを検討している場合は、利用すべき canonical 実装または設計対象を直接読む。

## hash
- dc27cd3715146b39aafcc4d982c3e5a76c5341802dbddbca0b9cfe6a38385831
