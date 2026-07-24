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
- ACP builder の互換入口と realization adapter 群をまとめるディレクトリ。`acp.builder` 名前空間の公開、共通 prompt 処理、indexing・oracle・realization・session・TUI 向け adapter、quota probe の互換経路を確認するための入口。

## Read this when
- 既存の `acp.builder.*` import 互換性や、canonical 実装への委譲経路を調査するとき
- ACP builder の prompt code fence 保護、quota probe、oracle command builder、realization workload builder の構成を確認・変更するとき
- このディレクトリ直下の builder adapter の責務や下位パッケージへの進み先を判断するとき

## Do not read this when
- canonical な oracle builder・session・TUI 実装や prompt 正本仕様の詳細を確認したいとき
- builder 以外の CLI 処理、TUI 本体、fork 適用処理を調査するとき
- 新しい公開 API や新規 import 経路を設計するときは、互換入口ではなく対応する正本実装と仕様を直接確認する

## hash
- dd721281b03bcca2d678370cd224e67a947046e79060fbf2f1e3d8680c31b2ae
