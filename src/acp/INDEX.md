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
- ACP builder の互換入口と builder adapter をまとめるパッケージ。oracle 側の canonical 実装への接続を維持し、quota probe、session、TUI、realization、review、feedback など処理領域別の下位 builder と、動的 Markdown section の code fence 保護用共通処理への routing 起点を提供する。

## Read this when
- ACP builder の互換 import 経路、oracle 実装への委譲、または builder adapter の構成を調査・変更するとき
- quota probe、session join、TUI 起動、realization apply/refactor、review finding、feedback issue のいずれかに関係する builder の入口を探すとき
- 動的 prompt section の code fence 保護や section 実体位置特定を扱う共通処理へ進むとき

## Do not read this when
- canonical な oracle builder の仕様・prompt 内容・本体ロジックを確認するときは、対応する oracle 側の対象を直接読む
- 個別 builder の具体的な処理や利用箇所を調査するときは、このパッケージの入口ではなく該当する下位実装または参照元を直接読む
- INDEX エントリーの routing 規則や生成内容だけを確認するときは、builder 実装の対象へ進まない

## hash
- d20654f8e0be0d31cf01c5ca0999ea0971674a510050a57668a6911a55cbbf64
