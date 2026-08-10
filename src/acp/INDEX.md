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
- ACP builder の互換・委譲 adapter 群をまとめるパッケージ。basic、common、feedback、indexing、oracle、quota_probe、realization、session、tui など、正本実装への接続や既存 import 経路の維持、prompt の code fence 保護を扱う下位要素への入口となる。

## Read this when
- ACP builder の adapter 構成、正本 builder への委譲経路、既存 import 互換性を調査するとき。
- 特定の command、session、index、feedback、quota probe、TUI、realization builder の下位実装へ進む入口を選ぶとき。

## Do not read this when
- canonical な oracle 実装や正本仕様そのものを確認・変更するときは、対応する oracle 側対象を直接読む。
- ACP builder の特定機能の具体的な生成ロジックを調査するときは、該当する下位要素を直接読む。
- builder 以外の CLI 実行処理や利用箇所の公開面を調査するとき。

## hash
- 13aa1b37386b7e4ee9e652ae4c864846a5863d068a01df396970ef988807b7ad
