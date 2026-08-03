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
- ACP builder の互換入口と各種 builder adapter をまとめるディレクトリ。oracle 側の canonical 実装への委譲、prompt の code fence 保護、index・quota probe・session・TUI・realization 関連 builder の既存 import 経路維持を扱う。
- 下位の common、indexing、oracle、realization、session、tui などへ進むための入口であり、処理領域や互換 import 経路が特定できた場合は対応する下位要素を直接確認する。

## Read this when
- ACP builder の realization 構成、互換 import 経路、canonical 実装への委譲先を調査するとき
- builder の prompt 生成における動的 section の code fence 保護や、index・quota probe・session・TUI・realization 関連 adapter の入口を判断するとき
- 対象機能の下位 package が不明で、ACP builder 内の処理領域を特定するとき

## Do not read this when
- oracle 側の canonical builder 実装や正本 prompt 仕様そのものを確認・変更するとき
- 具体的な builder adapter の実装詳細や利用箇所を調査するときは、対応する下位要素または参照元を直接読む
- ACP builder と無関係な TUI 本体、CLI 処理、正本仕様を調査するとき

## hash
- 04eed9f1742b2d626a70047db9e635fe3d355b94074c2203875f12e50f8f26fe
