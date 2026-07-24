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
- ACP builder の互換入口・共通処理・oracle command builder・realization workload builder adapter・TUI/session 関連 adapter をまとめたパッケージ。既存の `acp.builder.*` import 経路を維持しつつ、canonical な oracle 実装への委譲や prompt の code fence 保護を提供する。各機能の詳細調査は対応する下位ディレクトリまたは canonical 実装へ進む。

## Read this when
- `acp.builder` 配下の互換公開経路、builder adapter の構成、共通 prompt 処理の入口を確認するとき
- oracle command、realization workload、TUI、session、indexing などの builder adapter の下位実装へ進むべき対象を判断するとき

## Do not read this when
- canonical な oracle builder の具体的な prompt 生成仕様や実装挙動を確認したいとき
- TUI、session、realization apply/refactor、indexing など特定機能の詳細だけを調査・変更するときは、対応する下位実装を直接読む
- `acp.builder` と無関係な CLI、TUI 本体、一般的な ACP parameter 処理を調査するとき

## hash
- 9e8de6fa702b5042204eed7aca5e18ee675efbf3fa52ce226bd8c22cc8bfc4af
