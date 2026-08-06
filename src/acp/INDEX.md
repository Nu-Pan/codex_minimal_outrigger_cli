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
- ACP builder の realization package。正本側の builder 実装への互換入口・委譲 adapter をまとめ、apply、feedback、indexing、oracle、realization、session、TUI などの用途別 builder へ進む起点を提供する。

## Read this when
- ACP builder の realization package 全体の責務や、用途別 adapter の配置を確認するとき。
- 既存の acp.builder.* import 経路、正本 builder への委譲、builder 共通処理への入口を調査するとき。

## Do not read this when
- 特定用途の builder の具体的な生成ロジックを確認・変更するときは、対応する下位要素を直接読む。
- 正本側の canonical builder、CLI の実行処理、利用側の参照を調査するときは、それぞれの直接の対象を読む。

## hash
- 0b0f6f6b90ed811ba370d46c41d34f9f49a7e2eb199638d76766c11c21798789
