# `__init__.py`

## Summary
- 既存の `acp.builder.tui.*` import を維持するためだけに残された、`oracle.acp_builder.tui` 互換 package の入口。
- realization 側と利用者向け公開面からこの参照が消えた後に削除できる互換層として位置づけられる。

## Read this when
- 既存 import 経路 `acp.builder.tui.*` の互換維持や削除可否を確認する。
- `oracle.acp_builder.tui` との互換 package がなぜ残っているかを確認する。

## Do not read this when
- TUI 実装本体の挙動や画面構成を確認したい場合。
- 新しい公開 API や新規 import 経路を設計したい場合。

## hash
- 9e5ae7e28c1e80b5ffa414ac5eea7dd08927b7977f87292b3afa9b714a894d0a

# `launch_tui.py`

## Summary
- TUI 起動 parameter builder の互換 import 経路を提供する薄いモジュール。実体の実装や正本仕様は持たず、正本側で定義された builder を再公開する。

## Read this when
- TUI 起動 parameter builder の import 経路や互換性を確認するとき。
- TUI 起動 parameter builder の公開名を参照するコードの入口を確認するとき。

## Do not read this when
- builder の具体的な生成ロジックや仕様を確認したいときは、正本として示された oracle 側の実装を直接読む。
- TUI 起動処理全体や別の parameter builder を調査するとき。

## hash
- 6e9784f7e8505819488f5b54a774a719a4f662ab87693b9fbecc5a080f79477a

# `resolve_parameter.py`

## Summary
- TUI の resolve-parameter builder への互換 import 経路を提供する薄いラッパー。実装本体は持たず、canonical builder を再エクスポートする。

## Read this when
- `acp.builder.tui.resolve_parameter` からの既存 import 互換性や、TUI resolve-parameter builder の公開経路を確認するとき。

## Do not read this when
- builder の実装仕様や挙動を確認するときは、canonical builder である `oracle/src/oracle/acp_builder/tui/resolve_parameter.py` を直接読む。

## hash
- 5a1726a83d818e2933883355f8427c93a5e2456269cb4f1663cbd524552df945
