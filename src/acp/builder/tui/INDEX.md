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
- TUI 起動パラメータ生成関数の実体を oracle 側に置いたまま、既存の公開 import path から同じ関数を参照できるようにする互換用モジュール。
- realization 側や利用者向け公開面に残っている既存参照を維持するための薄い再 export であり、TUI 起動パラメータの仕様や組み立てロジック自体は持たない。

## Read this when
- TUI 起動パラメータ生成関数の import 経路、公開面との互換性、または oracle 側実装への接続を確認したいとき。
- 既存の公開 import path を削除・移動・置換してよいか判断するために、互換コードを残す理由と削除条件を確認したいとき。
- TUI builder 周辺で、realization 側から oracle 側の TUI 起動パラメータ正本へどのように委譲しているかを確認したいとき。

## Do not read this when
- TUI 起動パラメータの具体的な構造、値、生成ロジックの正本を確認したいとき。この対象は再 export だけを担うため、oracle 側の実体を読む。
- TUI 画面の描画、イベント処理、ユーザー操作、または端末 UI の挙動を調べたいとき。
- 互換 import path ではなく、新しい起動仕様や利用者向け CLI 挙動そのものを設計・確認したいとき。

## hash
- 23d4d93c40bb8191cb1d3b58b15845e17afca479d63366ca50c92836df1b6091

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
