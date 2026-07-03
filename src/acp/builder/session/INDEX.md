# `__init__.py`

## Summary
- oracle.acp_builder.session との互換性を保つための package 初期化ファイル。既存の acp.builder.session.* import を維持するためだけに残されている。

## Read this when
- acp.builder.session.* import の互換維持経路を確認する。
- oracle.acp_builder.session 参照への移行や、互換 package を削除できる条件を確認する。

## Do not read this when
- session 実装の挙動や構成要素を確認したい場合。
- 新規機能の入口や通常の公開 API を探している場合。

## hash
- 1c24d1b1720d385b0f3388d0c70ebd4fa053c26df3a40f54e8cb91484c901dc8

# `join`

## Summary
- session join builder 配下の旧 import path 互換入口をまとめる領域。実装本体ではなく、既存の acp.builder.session.join.* 参照を canonical oracle 実装または互換 package 配置へ中継する薄い公開面維持層を扱う。

## Read this when
- session join builder の旧 acp.builder 配下 import path が、どの canonical 実装や互換入口へつながるかを確認したいとき。
- acp.builder.session.join 配下の互換 package や再公開モジュールを残す理由、公開面維持、削除条件を調べたいとき。
- build_session_join_conflict_resolution_parameter の旧公開元を追跡しているとき。

## Do not read this when
- session join の具体的な処理内容、制御フロー、builder 呼び出し順を確認したいときは、呼び出し元の session join 実装を読む。
- conflict resolution parameter builder の実装内容や仕様根拠を確認したいときは、canonical oracle 実装を読む。
- 互換 import の実際の利用箇所や、realization 側と利用者向け公開面から参照がなくなったかを判断したいときは、参照元を調査する。

## hash
- a15ba1cd6e0e08fbb876b209ed53bd6220137d51d7d7005d7c797e2610045d3c
