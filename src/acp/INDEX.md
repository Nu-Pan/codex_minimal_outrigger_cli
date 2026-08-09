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
- 対象ディレクトリの責務と、下位の builder adapter・共通処理・互換入口へのルーティングを簡潔に示すエントリーです。

## Read this when
- ACP builder の realization package 全体の構成、正本実装への委譲経路、prompt 生成用の共通処理、互換 import 入口を調査するとき。
- 特定の builder adapter の所属領域を判断し、下位ディレクトリまたは個別モジュールへ読み進めるとき。

## Do not read this when
- canonical な oracle builder の仕様や実装そのものを確認・変更するときは、oracle 側の対応対象を直接読む。
- ACP builder の利用箇所、CLI の実行処理、利用者向け公開面を調査するときは、各参照元や実行処理を直接読む。

## hash
- 1778b94e80a9ad9c0f19f7b69de33ad8e5d82447939508424fa137d249b5d63a
