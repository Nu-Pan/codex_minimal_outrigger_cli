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
- ACP builder の互換入口と各種 parameter builder adapter をまとめるパッケージ。canonical な oracle 実装を再公開し、indexing、quota probe、oracle、realization、session、TUI 系の下位要素へ案内する。

## Read this when
- acp.builder 配下の builder 互換 import 経路や parameter 構築処理の配置を確認するとき
- indexing、quota probe、oracle、realization、session、TUI の builder adapter を横断して調査するとき

## Do not read this when
- canonical な builder の具体的な仕様や実装内容だけを確認したいとき
- builder 以外の ACP 実装や、個別 adapter の詳細だけを調査するときは、対応する下位要素へ直接進む

## hash
- 78a8f8b12e449663d7407468e2c89089ee63c60e75710b318b779a8b89c3b23c
