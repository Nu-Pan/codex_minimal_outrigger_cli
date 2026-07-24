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
- ACP builder の互換 adapter と補助 builder をまとめるパッケージ領域。oracle 実装の互換入口、prompt の code fence 補正、oracle・realization・indexing・session・TUI 向け builder adapter、quota probe fallback への入口を提供する。
- 下位の `common`、`indexing`、`oracle`、`realization`、`session`、`tui` から、共通 prompt 補正、各 command builder adapter、session 互換経路、TUI parameter builder などの詳細実装へ進める。

## Read this when
- ACP builder の互換 import 経路、adapter 構成、canonical oracle builder への委譲を調査・変更するとき。
- prompt の code fence 保護や quota probe fallback を含む builder 共通入口の責務を確認するとき。
- oracle command、realization workload、indexing、session、TUI の各 builder adapter の担当領域を判断するとき。

## Do not read this when
- canonical な oracle builder の仕様・実装そのものを調査するときは、oracle 側の対象を直接読む。
- 個別 adapter の具体的な挙動を調査するときは、該当する下位ディレクトリまたはファイルを直接読む。
- builder を利用する CLI・TUI の利用箇所や利用者向け公開面を調査するときは、各参照元を直接読む。

## hash
- 414ae1b7e8532e0e0a76692d9987a7541dfd5e16d229ae7ca75ca7c373eb40c3
