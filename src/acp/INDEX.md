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
- ACP builder の realization adapter と互換 import 経路をまとめるディレクトリ。oracle 側の canonical builder への委譲、prompt の Markdown fence 保護、index・oracle・realization・session・TUI 各領域の builder 接続を扱う。下位項目から、対象機能の具体的な互換入口や処理実装へ進む。

## Read this when
- ACP builder の realization package 全体の責務や下位構成を確認するとき。
- 既存の acp.builder.* import 経路、canonical 実装への委譲、builder adapter の配置を調査・変更するとき。
- prompt 生成の動的 section 保護や、oracle・realization・session・index 関連 builder の対象を選ぶとき。

## Do not read this when
- canonical な oracle builder の仕様・実装そのものを確認したいときは、oracle 側の対応対象を直接読む。
- ACP builder の利用箇所や利用者向け公開面を調査するときは、各参照元を直接読む。
- 特定領域の具体的な実装詳細を確認するときは、このディレクトリ全体ではなく対応する下位項目を直接読む。

## hash
- e9f85fe4e2e462a0e3f5637971d03e25b28ddddc5783d38d2b63a2b3b31d1bad
