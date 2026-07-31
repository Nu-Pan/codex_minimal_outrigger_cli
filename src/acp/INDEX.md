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
- ACP builder realization のパッケージ。oracle 実装への互換入口、builder 共通処理、oracle・realization・session・TUI・indexing 向け adapter をまとめ、quota probe の fallback も提供する。各サブディレクトリは対応する builder adapter や共通処理を調査するための下位入口である。

## Read this when
- ACP builder realization の構成や、互換入口から各 builder adapter へ進む経路を確認するとき。
- 既存の acp.builder import 互換性、oracle 実装への委譲、builder 共通の Markdown code fence 保護を調査するとき。
- cmoc oracle・realization・session・TUI・indexing builder、または quota probe の adapter の入口を探すとき。

## Do not read this when
- canonical な oracle builder の仕様や実装そのものを確認・変更するときは、oracle 側の対象を直接読む。
- TUI、CLI、session など利用側の挙動や公開面を調査するときは、各利用側の実装・参照元を直接読む。
- 特定の adapter の実装詳細を確認するときは、このディレクトリ全体ではなく該当する下位要素を直接読む。

## hash
- 67ed1cfe49653c5efe8729fdab97581587611d7b1321a6815c0fd8b81cff5be4
