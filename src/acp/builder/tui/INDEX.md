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
- TUI 起動用 AgentCallParameter を構築する realization adapter。oracle builder に処理を委譲する前に、runtime 側の editor input directory を作成する。

## Read this when
- cmoc tui の起動 parameter 構築や editor input directory の準備処理を確認・変更するとき。

## Do not read this when
- oracle 側の TUI launch parameter 仕様や builder 本体の実装を確認するとき。
- TUI 以外の parameter builder や、起動後の TUI 処理を確認するとき。

## hash
- 3502d9873b62abbf0ec153c7df8ea429ef1077ec35f72fec75785f7748c2dac5

# `resolve_parameter.py`

## Summary
- TUI の resolve-parameter builder に対する互換 import shim。既存の `acp.builder.tui.resolve_parameter` caller 向けに canonical builder と TUI 用の FileAccessMode 選択肢を再公開する。

## Read this when
- 既存 TUI import surface の互換性を確認・変更するとき
- 互換 shim の削除条件や `TUI_FILE_ACCESS_MODES` の利用箇所を調べるとき

## Do not read this when
- resolve-parameter builder 本体を実装・変更するときは canonical oracle path を読む
- 互換 import 経路に関係しない TUI builder の処理を調べるとき

## hash
- ecaa0fc136f723fdcd9ead1add141c738130ab8500136c11f8290979d1721879
