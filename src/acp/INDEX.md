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
- ACP builder の realization 側パッケージ入口。oracle 実装への互換委譲、共通 prompt 処理、index・feedback・session・TUI・quota probe・oracle・realization 用途別 adapter へのルーティングを担う。

## Read this when
- ACP builder の互換公開面、canonical oracle 実装への委譲経路、または配下 adapter の構成を確認するとき
- builder prompt の code fence 保護、quota availability probe、index・feedback・session・TUI・realization・oracle 関連の入口を選ぶとき

## Do not read this when
- canonical な oracle builder の仕様や prompt 本文を確認するときは oracle 側の対象を直接読む
- 特定の adapter の詳細実装、builder の利用箇所、または利用者向け公開面を調査するときは該当する下位要素や参照元を直接読む

## hash
- f5fb82debdac5bbadb0b96dd4ad0332e8156386c3f70e4123d0728b5291126f5
