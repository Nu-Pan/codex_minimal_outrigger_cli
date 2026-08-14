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
- `oracle.acp_builder` の正本実装を `acp.builder` として公開する互換 builder adapter 群の入口。
- feedback、indexing、quota probe、session join、TUI、oracle command、realization workload に関する旧 import 経路を維持し、必要な場合は正本 builder の呼び出しや実行前準備へ接続する。
- 各 adapter の実装本体は oracle 側にあり、この対象は互換 API と realization 側の接続構成を確認するための入口である。

## Read this when
- `acp.builder.*` から `oracle.acp_builder.*` への互換 import 経路や削除条件を調査するとき
- feedback issue、index entry、quota availability probe、session join、TUI 起動、oracle edit・investigation・review、realization apply・refactor の builder adapter の構成や委譲経路を確認するとき
- oracle 正本 builder を呼び出す前のリポジトリパス解決、editor input directory 準備、既存 API のパラメータ適合を調査するとき

## Do not read this when
- oracle 側の canonical builder の prompt、仕様、入出力、処理ロジックそのものを確認・変更するときは、対応する oracle 実装を直接読む
- `acp.builder.*` の利用箇所、利用者向け公開面、または互換 import の削除可否を確認するときは、各参照元を直接読む
- builder と無関係な CLI 処理、workload の本体実装、正本仕様やテストを調査するとき

## hash
- 22b620f26f2c9e38bb708b730acaadd5731e1b4eaafda05500ea6cc24dd58db0
