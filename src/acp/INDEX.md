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
- ACP builder の互換入口と realization adapter を収めるディレクトリ。既存の `acp.builder.*` import 経路を維持し、canonical な oracle 実装への接続、prompt のコードフェンス補正、各 workload・command・TUI・session 向け builder adapter を提供する。
- 下位要素には、共通 fence 補正、indexing・oracle・realization・TUI・session の互換入口、quota probe の fallback builder、review 関連の実行時キャッシュが含まれる。

## Read this when
- ACP builder 全体の互換構成、canonical 実装への接続、または下位 builder adapter の担当領域を確認するとき。
- `acp.builder.*` の import 経路、prompt のコードフェンス補正、oracle・realization workload の builder 連携を調査・変更するとき。

## Do not read this when
- canonical な oracle builder の仕様・実装や prompt 内容を確認するときは、対応する oracle 側の対象を直接読む。
- TUI、session、apply、refactor などの具体的な処理本体を調査するときは、各実装対象を直接読む。
- 利用側の参照や利用者向け公開面だけを調査するときは、各参照元を直接読む。

## hash
- 2cd81d3c3857b31236876b72266825683fdea0d531e09a079e4d6a1daba2c609
