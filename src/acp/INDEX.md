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
- ACP builder 関連の互換入口・共通処理・indexing、oracle/realization workload、session、TUI、quota probe builder をまとめるパッケージディレクトリ。旧 `acp.builder.*` import 経路から canonical builder へ委譲する adapter 群への入口となる。

## Read this when
- ACP builder のパッケージ構成、互換 import 経路、canonical builder への委譲を調査・変更するとき
- builder 共通処理、index entry 生成、oracle/realization workload、session、TUI、quota probe の adapter を扱うとき

## Do not read this when
- canonical builder の正本仕様や具体的な実装内容だけを確認したいとき
- TUI 実装本体、fork 適用処理、一般的な prompt 仕様を直接調査するとき

## hash
- 49d85cc4c087b683a79cb812cffaa0a3339aad35618c98fbb2d734d30ecf893c
