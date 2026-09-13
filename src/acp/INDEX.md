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
- oracle.acp_builder を acp.builder として公開する互換入口。canonical 実装を参照し、既存の acp.builder.* import 経路を維持する。
- feedback、indexing、oracle、realization、session、tui など目的別 builder adapter へ進むための上位パッケージ入口。

## Read this when
- acp.builder 配下の構成、公開入口、互換 import 経路を確認するとき
- 目的別 builder adapter の下位入口や oracle 実装への委譲関係を調査するとき
- 既存の acp.builder.* 参照を削除・移行できる条件を判断するとき

## Do not read this when
- 特定 builder の実装仕様や挙動を確認・変更するときは、対応する下位対象または oracle の正本実装を直接読む
- builder 共通処理の詳細を調査するときは、common などの共通処理対象を直接読む
- acp.builder の利用箇所や利用者向け公開面を調査するときは、各参照元を直接読む

## hash
- 29f5fc681339276305cbb34e003cc06ed4eb507b13dc60f0b579bc3c25a40e0c
