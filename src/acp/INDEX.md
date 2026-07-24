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
- ACP builder の互換・委譲層をまとめるパッケージ。既存の `acp.builder.*` import 経路を維持し、oracle 側の canonical builder、共通 prompt 補正、indexing、session、TUI、realization などへの入口を提供する。下位ディレクトリは各 builder 領域の互換 adapter として案内される。

## Read this when
- ACP builder の互換 import 経路、canonical builder への委譲、または builder adapter の構成を調査・変更するとき。
- prompt の code fence 保護、quota probe、oracle・realization・session・TUI builder の接続先を確認するとき。

## Do not read this when
- oracle 側の canonical builder の正本仕様や具体的な実装内容だけを確認したいとき。
- TUI 本体、fork 適用処理、または ACP builder と無関係な実装を調査するとき。

## hash
- 859cb07cdefc8d0d38acf78c1798b8f31fc7657b091cf110ff77ca2ccb5dde39
