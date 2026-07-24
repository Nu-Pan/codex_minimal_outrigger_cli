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
- ACP builder の互換入口と realization adapter をまとめるパッケージ。oracle.acp_builder への互換公開、prompt の code fence 補正、indexing・oracle・realization・session・tui 各 builder adapter、quota probe の fallback 入口を扱う。下位ディレクトリは用途別の builder 実装・互換経路を調査するための入口となる。

## Read this when
- acp.builder 配下の互換 import 経路、canonical な oracle builder への委譲、builder adapter の構成を調査・変更するとき。
- prompt の code fence 補正、indexing、oracle command、realization workload、quota probe、session、TUI builder のいずれかを調査するとき。
- 既存の acp.builder.* 参照や互換 package を削除・移行できる条件を確認するとき。

## Do not read this when
- canonical な oracle.acp_builder 実装や正本 prompt 仕様を確認したいときは、oracle 側の対象を直接読む。
- builder の利用箇所や利用者向け公開面を調査するときは、各参照元を直接読む。
- 特定の adapter の実装詳細を確認したいときは、このディレクトリ全体ではなく該当する下位対象を直接読む。

## hash
- f33397482198db01cb1d6d6833b80137743441bbf0353a4ed6378aab538d3603
