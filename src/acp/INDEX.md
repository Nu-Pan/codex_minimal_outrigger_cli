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
- ACP builder の互換・委譲層をまとめるパッケージ。acp.builder 名前空間から basic、feedback、indexing、session、tui、quota probe、realization、oracle などの builder adapter へ進む入口を提供し、canonical 実装への接続や旧 import 経路の維持を扱う。

## Read this when
- acp.builder 配下の builder adapter の構成、互換 import 経路、canonical 実装への委譲先を確認するとき
- ACP builder の共通処理、quota probe、feedback、indexing、session、TUI、realization、oracle command builder の各領域へ進む入口を探すとき

## Do not read this when
- canonical な oracle 実装、prompt 仕様、または各 builder の具体的な処理内容を確認・変更するときは、対応する正本または下位対象を直接読む
- ACP builder と無関係な CLI、ACP 本体、または利用箇所の公開 API を調査するときは、それぞれの対象を直接読む

## hash
- b62c65e899c98d552d5fe295f3495b536d45a09c03d4c61114b1e394d79076ee
