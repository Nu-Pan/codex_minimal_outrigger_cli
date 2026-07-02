# `__init__.py`

## Summary
- oracle.acp_builder.session と互換性を持たせるための package 初期化部。互換 import 経路としての役割だけを示す入口であり、具体的な session 機能の実装本体ではない。

## Read this when
- oracle.acp_builder.session 互換の import 経路が必要か確認するとき。
- session 関連 package の初期化責務や互換 package としての位置づけを確認するとき。

## Do not read this when
- session の具体的な実装、制御フロー、状態管理を確認したいとき。
- oracle 側の正本仕様断片そのものを確認したいとき。

## hash
- 7e4bc9c978926c93dcef2adf49463fd3703f72086d6dffc318e9381b610b5c88

# `join`

## Summary
- `oracle.acp_builder.session.join` 互換の公開 import 経路を置く package。package 初期化対象と、conflict resolution の旧 import 経路を canonical oracle path へ再エクスポートする互換モジュールを含む。

## Read this when
- `oracle.acp_builder.session.join` 互換 package の存在や公開上の位置づけを確認する。
- セッション join の conflict resolution について、旧 import 経路から canonical oracle path への橋渡しや再エクスポートだけを確認する。
- 旧 import 経路との互換維持、canonical 側への移行状況、または互換モジュールを削除できる条件を判断する。

## Do not read this when
- join session や conflict resolution の具体的な仕様・実装内容・制御ロジックを確認したい場合は、canonical 側の実装を読む。
- 新しい conflict resolution の挙動を追加・変更したい場合は、この互換層ではなく実装本体を読む。
- 旧 import 経路の維持や削除条件に関係しない作業では読む必要はない。

## hash
- 59d7ecc61dd8c3f2b4c03a486af8a6ca24b6e81634a5befeb763c8f0086829cd
