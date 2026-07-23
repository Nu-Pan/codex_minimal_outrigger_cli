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
- ACP 用の parameter builder adapter と互換 import 入口をまとめるディレクトリ。oracle.acp_builder の canonical builder への委譲、既存 acp.builder.* 参照の互換維持、TUI・session・indexing・quota probe・oracle・realization 各 builder の公開経路を扱う。詳細な処理は対応する下位パッケージまたは個別モジュールへの入口として利用する。

## Read this when
- acp.builder 配下の互換 import 経路、canonical builder への委譲、または builder adapter の配置を確認・変更するとき
- TUI、session、indexing、quota probe、oracle、realization のどの下位領域を読むべきか判断するとき

## Do not read this when
- canonical な oracle.acp_builder の実装仕様や prompt 内容を確認したいとき
- TUI 本体、CLI 処理、一般的な ACP parameter の仕様を調査したいときは、対応する canonical 実装または直接の利用側を読む

## hash
- 2127d28da7392d2428313686ecd44a8db0d6cebcb9c26d5cc1c0b6cc80b06c0f
