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
- TUI 起動時に使用する AgentCallParameter を構築する realization adapter。oracle 側の parameter builder を呼び出しつつ、runtime 側の editor input directory を事前作成する。TUI 起動 parameter の生成処理を確認・変更するときの入口。

## Read this when
- `cmoc tui` の起動 parameter 構築を確認・変更するとき
- TUI 起動前の editor input directory 作成や runtime path 解決の挙動を確認するとき
- oracle builder と realization adapter の連携を調査するとき

## Do not read this when
- TUI 以外のサブコマンドの AgentCallParameter を調査するとき
- parameter の正本仕様や oracle 側の構築内容そのものを確認するときは、対応する oracle builder を直接読む
- runtime path や editor input directory の共通実装だけを調査するとき

## hash
- 645f234862e66ff62ad5e8eedf0db78ac5054fe882afeeeae48ff0cedcba243e

# `resolve_parameter.py`

## Summary
- TUI の resolve-parameter builder への互換 import 経路を提供する薄いラッパー。実装本体は持たず、canonical builder を再エクスポートする。

## Read this when
- `acp.builder.tui.resolve_parameter` からの既存 import 互換性や、TUI resolve-parameter builder の公開経路を確認するとき。

## Do not read this when
- builder の実装仕様や挙動を確認するときは、canonical builder である `oracle/src/oracle/acp_builder/tui/resolve_parameter.py` を直接読む。

## hash
- 5a1726a83d818e2933883355f8427c93a5e2456269cb4f1663cbd524552df945
