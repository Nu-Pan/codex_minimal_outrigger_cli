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
- ACP builder の互換入口と builder adapter 群をまとめるパッケージ。canonical な oracle 実装への接続、Markdown code fence 補正、indexing・session・TUI・realization・oracle 向け builder、quota probe の互換経路を扱う。各サブパッケージまたは関連モジュールへ進むためのルーティング起点。

## Read this when
- ACP builder のパッケージ構成、互換 import 経路、builder adapter の入口を確認するとき。
- prompt 生成時の code fence 補正や、oracle・realization・TUI など特定 builder 系統の下位要素を調査するとき。

## Do not read this when
- canonical な oracle builder の仕様や実装そのものを確認するときは、oracle 側の対象を直接読む。
- TUI、oracle、realization など各 builder の具体的な prompt 構築や処理本体を調査するときは、該当する下位要素を直接読む。
- ACP builder と無関係な CLI、TUI、agent call の利用箇所を調査するとき。

## hash
- 1bc257e908a7766b8a671a4d962e22ca2d20166ef02a2837d82be3c5f42a0055
