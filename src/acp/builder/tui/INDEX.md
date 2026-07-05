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
- TUI 起動用の AgentCallParameter を構築する realization 側の互換入口。oracle 側 builder を呼び出す前後で、TUI 用ログ配置の準備と structured output schema の無効化を補う。

## Read this when
- TUI 起動時に渡す AgentCallParameter の組み立て経路を確認・変更したいとき。
- oracle 側の TUI 起動 parameter builder と realization 側で補う互換処理の境界を確認したいとき。
- TUI 起動用ログディレクトリの作成条件、または TUI 起動で structured output schema を渡さない処理を確認したいとき。

## Do not read this when
- TUI 以外の subcommand の parameter builder を確認したいとき。
- AgentCallParameter や FileAccessMode 自体の定義を確認したいとき。
- runtime path 全般や logs directory の算出規則を確認したいとき。

## hash
- 32dc3dc10d188720fb3fe9ff8f7a9ec1d31f4c147bf9c19e444189f40a4f3bbd

# `resolve_parameter.py`

## Summary
- TUI 用 resolve parameter builder の旧 import surface を維持する互換モジュール。正本側 builder を再公開し、既存 TUI 呼び出し向けに NO_RULE を除いた file access mode 群を提供する。

## Read this when
- `acp.builder.tui.resolve_parameter` からの import 互換性、公開名、削除条件を確認する。
- TUI resolve parameter builder の呼び出し元を正本側 import path へ移行する作業を行う。
- 既存 TUI import surface が参照する file access mode の選択肢を確認する。

## Do not read this when
- 正本仕様としての TUI resolve parameter builder の内容を確認したい場合は、oracle 側の canonical builder を読む。
- TUI 以外の builder や file access mode 全体の定義を確認したい場合は、それぞれの定義元を読む。
- 互換 import path の維持や移行に関係しない resolve parameter 処理を調べる。

## hash
- cb619844023de6245704fce405a8473073988a8795d275f54d87a487d5750b70
