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
- TUI 起動時に使う AgentCallParameter を realization 側で組み立てる互換入口。oracle 側の prompt builder で complete prompt を作り、runtime の local 配下へ保存したうえで、その保存先を読む指示を agent call parameter に渡す。

## Read this when
- `cmoc tui` の起動時に渡す agent call parameter の内容、model class、reasoning effort、file access mode、prompt 保存先を確認する必要があるとき。
- TUI 起動用 complete prompt の生成フラグや original prompt の渡し方を変更するとき。
- oracle 側 prompt builder と realization 側 runtime path の接続箇所を確認するとき。

## Do not read this when
- complete prompt の本文構造や各 standard prompt の内容を確認したいだけのときは、oracle 側の prompt builder や関連する oracle file を読む。
- `.cmoc/local` 配下のディレクトリ規約や logs path の一般処理を確認したいだけのときは、runtime path を扱う共通実装を読む。
- TUI 起動後の UI 表示、入力処理、イベントループを調べるときは、TUI 本体の実装を読む。

## hash
- a594973bd10fe9f71f595f33097bacd11b21fa148eacb37af3c4e96d712805f5

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
