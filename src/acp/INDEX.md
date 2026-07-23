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
- ACP builder 関連の realization adapter と互換入口をまとめるパッケージ。oracle.acp_builder の canonical 実装を旧 acp.builder 系の import 経路から利用可能にし、oracle・realization・TUI・session・indexing・quota probe の builder 連携を下位要素へ振り分ける。

## Read this when
- acp.builder 系の互換 import、builder adapter、または canonical builder への委譲経路を調査・変更するとき
- oracle command、realization workload、TUI、session、indexing、quota probe の builder 入口を探すとき

## Do not read this when
- canonical な builder 実装や正本仕様の詳細を確認するとき
- builder と無関係な CLI、ACP runtime、一般的な処理を調査するとき

## hash
- 59a4e20c6fd7f6b672192896491568912cf688216c2feda42d292e1e685d5618
