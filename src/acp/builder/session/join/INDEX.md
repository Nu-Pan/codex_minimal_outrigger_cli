# `__init__.py`

## Summary
- oracle.acp_builder.session.join 互換の package 初期化ファイル。既存の acp.builder.session.join.* import を維持するためだけに残る互換入口であり、実装本体は持たない。

## Read this when
- acp.builder.session.join 配下の import 互換性や公開面維持のために、この package が存在する理由を確認したいとき。
- oracle.acp_builder.session.join から realization 側への互換 package 配置を調べているとき。

## Do not read this when
- session join の具体的な処理内容や振る舞いを確認したいとき。
- 互換 import の利用箇所を探したいとき。
- realization 側と利用者向け公開面から参照がなくなったかを判断するために、実際の参照元を調査したいとき。

## hash
- 072255c777a758fe7fa412dab9c417d50fc420b5871fae782e550e97a8c1b483

# `conflict_resolution.py`

## Summary
- session join の conflict resolution parameter builder について、旧 import path から canonical oracle 実装へ中継する互換モジュール。呼び出し元が直接 oracle 側の実装を import するまで残す薄い再公開層であり、実装本体ではない。

## Read this when
- session join の conflict resolution builder が、旧 acp.builder 配下の import path からどの実装へ委譲されるかを確認したいとき。
- 旧 import path の互換維持や削除条件を確認したいとき。
- build_session_join_conflict_resolution_parameter の公開元を追跡しているとき。

## Do not read this when
- conflict resolution parameter builder の実装内容や仕様根拠を確認したいときは、canonical oracle 実装を読む。
- session join 全体の制御フローや builder 呼び出し順を確認したいときは、呼び出し元の session join 実装を読む。
- 新しい conflict resolution ロジックを追加・変更したいときは、この互換 import 層ではなく canonical 実装側を確認する。

## hash
- 303afc45719ee75cf972f2b71e716ce3622227e39c5211b7a2e7b2d4077095d3
