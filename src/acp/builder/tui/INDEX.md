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
- `cmoc tui` の起動パラメータを組み立てる互換入口。実体の生成は oracle 側に委譲し、この層では実行時に必要な `tui` 保存先だけ先に用意する。

## Read this when
- TUI 起動時の `AgentCallParameter` の作り方と、実行前に必要な保存先の準備を確認したいとき。
- realization 側の入口が oracle 側の builder をどう包んでいるかを見たいとき。

## Do not read this when
- `cmoc tui` の引数解釈や出力内容そのものを知りたいときは、委譲先の oracle 側 builder を読む。
- TUI 以外のコマンドの起動パラメータを調べたいとき。

## hash
- 544414fb16a433336a20d2d8feb385b3b15697d08a23768a5aa47fafd3bcc734

# `resolve_parameter.py`

## Summary
- TUI の resolve-parameter builder への互換 import 経路を提供する。canonical builder を再公開し、既存 TUI caller 向けに NO_RULE を除く FileAccessMode の選択肢も公開する。caller が canonical import に移行して mode tuple が不要になった時点で削除対象となる。

## Read this when
- TUI の resolve-parameter builder の import 経路や既存 TUI import surface を確認するとき
- TUI 用 FileAccessMode 選択肢の公開箇所や互換維持条件を調査するとき

## Do not read this when
- canonical な resolve-parameter builder の実装詳細を確認したいとき
- TUI 以外の builder や FileAccessMode の定義自体を確認したいとき

## hash
- 9347dc57eb25cd9e5a9725889c3ae19467589d68da4e34e96de68205e7c2fee9
