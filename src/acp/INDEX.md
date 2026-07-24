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
- ACP builder の互換入口を提供するパッケージ領域。oracle.acp_builder の canonical 実装を参照しつつ、既存の acp.builder.* import 経路を維持する初期化、共通 prompt 補正、indexing・oracle・realization・session・tui 向け adapter、quota probe builder を含む。

## Read this when
- acp.builder 配下の互換 import 経路、builder adapter の構成、canonical 実装との接続を調査・変更するとき
- ACP builder の prompt code fence 補正、quota probe、oracle command、realization workload、session、TUI builder の入口を確認するとき

## Do not read this when
- canonical な oracle.acp_builder 実装や正本仕様そのものを調査・変更するとき
- 各 builder の具体的な挙動、利用箇所、TUI 実装本体を確認するときは、該当する下位要素や参照元を直接読む

## hash
- 5c4aaf084d3c945587d6f0e3b929dd1ad7180bc3ea8e6fca20342e77fc9311d4
