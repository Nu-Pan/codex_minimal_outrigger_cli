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
- ACP builder の互換入口と、oracle 実装へ委譲する処理別 builder adapter を収めるディレクトリ。共通のプロンプト整形、feedback・indexing・quota probe・realization・session・TUI など、acp.builder 配下の公開経路や adapter 構成を確認する際の上位入口。

## Read this when
- acp.builder 名前空間の構成、互換 import 経路、または配下の builder adapter の入口を調査するとき
- 共通 builder 処理と、feedback・indexing・quota probe・realization・session・TUI など処理別 adapter の配置関係を確認するとき

## Do not read this when
- 特定の builder の正本実装、仕様、入出力、または利用箇所を調査するときは、対応する oracle 実装や参照元を直接読む
- ACP builder と無関係な CLI 処理や、個別 adapter の詳細実装だけを確認したいとき

## hash
- a519de07934c5eabd2bf47db7c7e3c3eaa8b66eca0edf52285e0d7f41a0491fe
