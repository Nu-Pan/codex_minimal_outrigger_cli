# `__init__.py`

## Summary
- `acp` 互換の公開入口を扱う。`acp.*` を利用している既存参照を、`oracle.*` または実体モジュールへ移す必要があるときに読む。

## Read this when
- `acp` という公開名を残すべきか、削除できるかを判断したいとき。
- 既存の利用者向け参照を壊さずに、`oracle` 側の実体へ切り替える導線を確認したいとき。

## Do not read this when
- `acp` 配下の具体的な実装内容や移行先の詳細を知りたいだけなら、直接その実体モジュールを読む。
- 互換入口の存廃ではなく、`acp.*` の内部挙動そのものを変えたいだけならここではない。

## hash
- fe0939ab61e919bfb5ae35264e02859ee36efb102a15498d95fcbd45f9670e76

# `builder`

## Summary
- `acp.builder` の realization package。oracle.acp_builder を旧 import 経路から利用する互換入口を提供し、quota probe、共通 Markdown section 処理、indexing、oracle command、realization、session、TUI などの builder adapter 群へ進む起点となる。

## Read this when
- acp.builder 配下の互換 import 経路、canonical oracle builder への委譲、または builder adapter の責務と構成を確認・変更するとき。
- quota probe、prompt の code fence 保護、indexing、oracle command、realization、session、TUI の各 builder 領域へ進む対象を選ぶとき。

## Do not read this when
- canonical な oracle builder の仕様・実装そのものを確認または変更するときは、oracle 側の対応対象を直接読む。
- TUI、CLI、session などの利用側実装や、各 builder の具体的な処理詳細を調査するときは、対応する下位対象または参照元を直接読む。

## hash
- cdc72845231c6a64ed6db1ee9f4ceafdfa22347e30b4f26b49a54b096873c648
