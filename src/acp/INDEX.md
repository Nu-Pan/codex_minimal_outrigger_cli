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
- ACP builder の互換入口と realization adapter 群を収めるディレクトリ。canonical な oracle 実装への接続、prompt の code fence 補正、indexing・session・TUI・realization などの builder adapter、quota probe の fallback を扱う。各下位領域の実装や互換 import 経路を調査するための入口。

## Read this when
- ACP builder の互換公開面、canonical 実装への委譲経路、builder adapter の構成を確認するとき。
- prompt の code fence 保護、index エントリー生成、session join、TUI parameter、realization workload、quota probe に関する builder 処理を調査・変更するとき。

## Do not read this when
- canonical な oracle builder の仕様や実装そのものを確認・変更するとき。
- TUI 本体、fork 適用処理、builder の利用箇所、利用者向け公開面を調査するときは、それぞれの直接の対象を読む。
- このディレクトリ内の特定の adapter の詳細だけを確認する場合は、該当する下位パッケージや実装ファイルへ直接進む。

## hash
- 7f022fac292799b6c93be958426d09aac7151979c9ba3f188d73b9fe82ffff5e
