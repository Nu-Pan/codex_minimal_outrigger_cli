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
- ACP builder の realization 実装をまとめるディレクトリ。`acp.builder` の互換入口、apply・indexing・session・TUI の互換層、oracle command builder の adapter、quota probe の fallback 入口を含む。各下位要素から、対応する builder の具体的な互換経路や委譲処理へ進む。

## Read this when
- `acp.builder` 配下の互換 import 経路、canonical builder への委譲、builder adapter、または quota probe builder の fallback を調査・変更するとき。
- apply、indexing、session、TUI、oracle command builder の realization 側入口を横断して構成や責務の境界を確認するとき。

## Do not read this when
- canonical な builder の正本仕様や具体的な実装内容を確認したいときは、対応する `oracle` 側の実装を直接読む。
- apply fork や session join のループ制御・state 遷移、TUI の画面実装、builder 以外の CLI 処理を調査するときは、対応するサブコマンドや実装を直接読む。
- 生成済み Python キャッシュの内容だけを調査する場合を除き、review 配下へ進む必要はない。

## hash
- d927f586d0f9f5776d1f5b193e02c67fab386c1bdd3334862151cf65221e809e
