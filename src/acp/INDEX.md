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
- ACP builder の互換入口と realization adapter 群を収めるディレクトリ。canonical な oracle 実装への委譲、共通プロンプト整形、feedback・indexing・oracle・realization・session・TUI などの処理別 builder adapter の入口を提供する。

## Read this when
- 既存の `acp.builder` import 経路や canonical 実装への互換接続を確認するとき
- ACP builder 共通のプロンプト整形、feedback issue の正規化・検証、index-entry 生成、oracle command、realization workload、session join、TUI 起動などの adapter 構成を調査するとき
- 処理領域に対応する builder adapter の下位対象へ進む入口を探すとき

## Do not read this when
- canonical な oracle 実装、正本仕様、通常の利用側ロジックを調査・変更するときは、対応する正本実装や参照元を直接読む
- builder 共通処理や特定処理の詳細実装を確認したいときは、このディレクトリ全体ではなく該当する下位対象へ進む
- ACP builder と無関係な CLI 処理や実装を調査するとき

## hash
- 04a08f580be199d66ed178006449165f9c739f133e734641285d172efb41a49e
