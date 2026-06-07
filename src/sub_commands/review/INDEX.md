# `__init__.py`

## Summary

- `src/sub_commands/review/__init__.py` は `cmoc review` 系サブコマンドのパッケージ宣言だけを担う最小モジュールです。
- 公開 API、定数、実行ロジック、再エクスポートは持ちません。

## Read this when

- `src/sub_commands/review` が Python パッケージとして宣言されていることを確認したいとき。
- `cmoc review` 系サブコマンドの入口となるパッケージ構造を把握したいとき。

## Do not read this when

- `cmoc review oracles` の実行フローや評価ロジックを確認したいときは、このファイルではなく `oracles.py` を読むべきです。
- `cmoc review oracles` の CLI 引数や hidden alias 登録だけを確認したいときは、`src/main.py` を読むべきです。

## hash

- d432dc21ecc8d2cabf968eac490bb998f303e6d3e7411b90260759ccd587f07d

# `oracles.py`

## Summary

- `src/sub_commands/review/oracles.py` は `cmoc review oracles` の実装本体で、事前条件検証、レビュー用 worktree / branch の準備、oracle スナップショットの固定、所見パイプライン、レポート出力をまとめて担います。
- Structured Output schema の読み込みと、所見の列挙・統合・検証・判定に使う helper 群を含みます。
- `INDEX.md` を手がかりにレビュー対象 oracle を選び、失敗時の error report 生成まで含めて実行全体を束ねます。

## Read this when

- `cmoc review oracles` の実装・修正・レビュー・テストを行いたいとき。
- review branch / worktree の作成、oracle snapshot の固定、`--scope` や反復回数オプションの処理順を確認したいとき。
- 所見の列挙・マージ・検証・判定や、Structured Output schema の読み込みと payload 検証の流れを追いたいとき。
- レポート生成、error report、`INDEX.md` を基準にした対象 oracle 選定の仕組みを把握したいとき。

## Do not read this when

- `src/sub_commands/review` 全体の入口構造だけを確認したいときは、親ディレクトリの `INDEX.md` を読むべきです。
- `cmoc review oracles` の利用手順、引数、出力仕様だけを確認したいときは、`oracles/docs/app_specs/sub_commands/review_oracles.md` を直接読むべきです。
- `src/main.py` の CLI 登録や hidden alias だけを確認したいときは、このファイルではなく `src/main.py` を読むべきです。
- `review` ではなく `apply` や `session` の実装を追いたいときは、このファイルではなく各サブコマンド側を読むべきです。

## hash

- 6e5dd54a09dd7b26302ee67eedc5972c6c159863d77c62011a6720cec88ed919
