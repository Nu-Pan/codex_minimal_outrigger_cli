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
- TUI 起動時に使う AgentCallParameter を realization 側で組み立てる互換入口。oracle 側の prompt builder で完全プロンプトを作り、realization runtime のローカルログ配置へ保存して、その保存先を読むよう agent call parameter に渡す。
- TUI 起動が codex exec と異なり Structured Output schema を要求しないこと、実行時保存先が oracle 側ではなく realization runtime の配置に従うことを扱う。

## Read this when
- TUI 起動用の AgentCallParameter の組み立て、モデル種別、reasoning effort、file access mode の受け渡しを確認または変更したいとき。
- TUI 起動時の complete prompt の生成、markdown 保存、保存先パス、agent へ渡す指示文の関係を確認したいとき。
- TUI 起動で Structured Output schema を渡すかどうか、または codex exec 向け parameter builder との差分を調べたいとき。

## Do not read this when
- TUI 画面そのものの表示、入力処理、イベントループ、端末 UI の挙動を調べたいとき。
- prompt builder の正本仕様や StructDoc の markdown rendering の詳細を調べたいとき。
- runtime のローカルディレクトリ配置や repo root 解決の一般仕様を調べたいとき。

## hash
- c4b75a4700fea11fb62ce4b085ae5a85ec716da8fc011235fd7c25e568fc8974

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
