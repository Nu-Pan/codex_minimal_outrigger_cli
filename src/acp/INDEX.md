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
- ACP builder の realization adapter と互換 import 経路をまとめるディレクトリ。canonical な oracle builder への委譲、prompt の code fence 保護、index・oracle・realization・session・TUI builder のコマンド別入口を扱う。
- 特定の builder や共通処理を調査・変更する際は、該当する下位パッケージまたはモジュールへ進むための起点となる。

## Read this when
- ACP builder 全体の構成や realization adapter の責務範囲を確認するとき。
- 特定の command builder、互換 import 経路、prompt fence 共通処理の入口を切り分けるとき。

## Do not read this when
- canonical な oracle builder の仕様や実装そのものを確認するとき。
- CLI 実装、ACP builder の利用箇所、または特定 builder の詳細挙動を直接調査するときは、対応する下位要素や参照元を直接読む。

## hash
- 8895f03be1a35e171ae6139ff1eef41fb1d9ca2805cefefffbf3a280f75bd826
