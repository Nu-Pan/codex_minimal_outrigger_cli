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
- ACP builder の互換入口と各種 builder adapter をまとめるパッケージ。canonical な oracle 実装の再公開、prompt の code fence 補正、indexing・session・TUI・oracle・realization 向け adapter、quota probe の fallback を扱う。下位の機能領域を調査する際の入口となる。

## Read this when
- ACP builder のパッケージ構成、互換 import 経路、各 builder adapter の責務を確認するとき。
- prompt 境界補正、quota probe、oracle・realization workload、session、TUI builder のいずれかを調査・変更するとき。

## Do not read this when
- canonical な oracle 実装や具体的な prompt 仕様を確認するときは、対応する oracle 側の対象を直接読む。
- 個別 adapter の詳細や利用箇所を調査するときは、該当する下位パッケージまたは参照元を直接読む。

## hash
- 2d1f876760bac4f3dfa0362671394effa9ac94d979b485094fec5e01177914a9
