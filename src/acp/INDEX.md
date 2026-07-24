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
- acp.builder 配下の互換入口と builder adapter をまとめる realization package。既存の acp.builder.* import 経路を維持し、indexing・oracle・realization・session・TUI・quota probe などの下位要素へ案内する。

## Read this when
- acp.builder の互換 import 経路やパッケージ構成を確認するとき
- 配下の builder adapter、indexing、session、TUI、quota probe の接続先を調査・変更するとき

## Do not read this when
- canonical な oracle builder の具体的な実装内容を確認したいとき
- TUI 本体、realization workload、または個別 builder の詳細挙動だけを調査するときは、対応する下位要素を直接読む

## hash
- 88db9974dfc4f688d283b3c3e55aece54d4172ec982ca6ee835a0a7a9dace0a8
