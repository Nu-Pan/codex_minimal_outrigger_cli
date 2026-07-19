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
- `acp.builder` の互換ビルダー入口をまとめるディレクトリ。`oracle.acp_builder` への委譲、既存 import 経路の維持、quota probe・realization・session・TUI などの builder adapter 公開を扱う。各サブディレクトリやファイルは、対応する互換層・adapter の詳細へ進むための入口である。

## Read this when
- `acp.builder` の互換 import 経路、パッケージ構成、builder adapter の配置を確認・変更するとき。
- quota probe、realization workload、session、TUI などの互換入口から対応する builder 実装を辿るとき。

## Do not read this when
- canonical な builder の仕様や実装内容を確認したいときは、対応する `oracle.acp_builder` 側または下位の直接実装を読む。
- builder 以外の処理や、互換入口を経由しない利用側の挙動だけを調査するとき。

## hash
- 838f5bbc8e0bb34bba80f3c04f958f980fed535ed5176b17d62e70197895c17c
