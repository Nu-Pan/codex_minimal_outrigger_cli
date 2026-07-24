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
- ACP builder の互換公開・共通処理・各 workload 向け builder adapter をまとめる realization package。旧 `acp.builder.*` import 経路から canonical builder へ委譲する入口と、TUI・session・oracle・realization・indexing などの下位要素を案内する。

## Read this when
- ACP builder の互換 import 経路、canonical builder への委譲、または各 builder adapter の構成を確認するとき。
- TUI、session、oracle、realization、indexing など特定の builder adapter の入口を探すとき。
- 動的 prompt の code fence 保護や quota probe の互換 fallback を含む builder 周辺の公開経路を調査するとき。

## Do not read this when
- canonical builder の正本仕様や具体的な prompt 構築内容を確認したいとき。
- ACP builder 以外の CLI 処理、TUI 実装本体、または各 adapter 内部の具体的な生成ロジックだけを調査するとき。

## hash
- 00b954537d026cd830582858005ad12b91e2bc63486bc17455bb07defa2ba398
