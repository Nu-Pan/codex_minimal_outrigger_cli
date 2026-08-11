# `conflict_resolution.py`

## Summary
- `cmoc session join` における merge conflict marker 解消用のエージェント呼び出しパラメータを構築する。対象パスを解決し、conflict 解消専用の prompt、最高品質モデル設定、リポジトリ書き込み権限、作業ディレクトリなどをまとめて返す。

## Read this when
- `session join` の conflict 解消エージェント呼び出し条件や prompt 構築を変更・確認するとき。
- conflicted paths の解決方法、agent call のモデル・推論設定、conflict 解消時の indexing preflight 制御を確認するとき。

## Do not read this when
- 通常の `session join` 処理や conflict 検出ロジックだけを確認するときは、まずその処理の実装へ進む。
- 共通の prompt 構築仕様や agent call パラメータ型の詳細を確認する場合は、それぞれの共通実装を直接読む。

## hash
- b2f2b3f50bbd3d97d30643cb225bc0c5e5f0f36af7c72a4874be233eaf4df05f
