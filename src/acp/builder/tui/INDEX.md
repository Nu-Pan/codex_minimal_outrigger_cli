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
- TUI 起動パラメータ生成関数の既存公開 import path を維持しつつ、完全 prompt の構築と `.cmoc/local/log/tui` への保存を realization runtime の path 配置に合わせて行う互換モジュール。
- prompt 本文の構成は oracle 側 helper を利用し、保存先や返却する prompt path など実行時配置に依存する部分だけを realization 側で適応する。

## Read this when
- TUI 起動パラメータ生成関数の import 経路、公開面との互換性、または oracle prompt helper と runtime path helper の接続を確認したいとき。
- TUI の完全 prompt 保存先、`AgentCallParameter.prompt` に含める prompt file path、または `.cmoc/local/log/tui` への追従を確認・変更したいとき。
- 既存の公開 import path を削除・移動・置換してよいか判断するために、互換コードを残す理由と削除条件を確認したいとき。

## Do not read this when
- TUI 起動パラメータの prompt 構成そのものの正本を確認したいとき。prompt 構築 helper や基礎型は oracle 側の実体を読む。
- TUI 画面の描画、イベント処理、ユーザー操作、または端末 UI の挙動を調べたいとき。
- 互換 import path ではなく、新しい起動仕様や利用者向け CLI 挙動そのものを設計・確認したいとき。

## hash
- bcc66a74e9ebc1259044e48efc1ced73240648b864dae22b997826dfea253f5f

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
