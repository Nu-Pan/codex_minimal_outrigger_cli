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

- `src/sub_commands/review/oracles.py` は `cmoc review oracles` の本体実装です。
- review 実行前提の検証、review branch / worktree の準備、oracle snapshot の固定、所見パイプライン、レポート出力をまとめて担います。
- Structured Output schema の読み込みと検証ヘルパー群を含み、`INDEX.md` を手がかりに評価対象を選び、エラー時の report 生成まで扱います。

## Read this when

- `src/sub_commands/review/oracles.py` の実装・修正・レビュー・テストを行いたいとき。
- session branch 前提の検証、clean worktree の確認、review branch / worktree の作成手順を追いたいとき。
- oracle snapshot の固定、`INDEX.md` を基準にした対象 oracle の選定、所見の列挙・統合・検証・判定の流れを確認したいとき。
- Structured Output schema の読み込みと payload 検証、ならびに失敗時の Markdown レポート生成までを把握したいとき。

## Do not read this when

- `src/sub_commands/review` 配下全体の入口構造だけを確認したいときは、親ディレクトリの `INDEX.md` を読むべきです。
- `cmoc review oracles` の利用手順、引数、出力仕様だけを確認したいときは、`oracles/docs/app_specs/sub_commands/review_oracles.md` を直接読むべきです。
- `cmoc review` の CLI 登録や hidden alias だけを確認したいときは、`src/main.py` を読むべきです。
- `review` ではなく `apply` や `session` の実装を追いたいときは、それぞれのサブコマンド側を読むべきです。

## hash

- 70f72fff118ed37f0b7882fd23959eb07e1d2533feed0e6fab5aaaae24842556
