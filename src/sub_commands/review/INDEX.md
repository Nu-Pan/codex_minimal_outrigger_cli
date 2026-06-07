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

- `src/sub_commands/review/oracles.py` は `cmoc review oracles` の本体で、前提検証から review worktree / branch の作成、oracle スナップショットの固定、所見の列挙・統合・検証・判定、レポート出力までをまとめて担う実装です。
- 正本の Structured Output schema を読み込み、所見リストや評価メタデータを処理する helper 群もこのモジュールに含まれます。
- `INDEX.md` を根拠に対象 oracle を選び、失敗時の error report 生成まで含めてレビュー実行の中核を構成します。

## Read this when

- `src/sub_commands/review/oracles.py` の実装・修正・レビュー・テストを行うとき。
- `cmoc review oracles` の前提条件検証、worktree / branch 作成、oracle 固定、所見の列挙・統合・検証・判定、レポート出力の流れを追いたいとき。
- Structured Output schema の読み込みや、所見パイプラインで使う helper 群の役割を確認したいとき。
- `INDEX.md` を根拠にした対象 oracle の選定や、失敗時の error report 生成条件を確認したいとき。

## Do not read this when

- `cmoc review oracles` の利用手順、引数、出力仕様だけを確認したいときは `oracles/docs/app_specs/sub_commands/review_oracles.md` を直接読むべきです。
- `src/sub_commands/review` 全体の入口構造だけを確認したいときは `src/sub_commands/review/INDEX.md` を読むべきです。
- `cmoc review` の CLI 登録や hidden alias だけを確認したいときは `src/main.py` を読むべきです。
- `review` ではなく `apply` や `session` の実装を追いたいときは、このファイルではなく各サブコマンド側を読むべきです。

## hash

- 68bcf0b80ea1c118bed5ec96ff65cdfb554246c0090bbe6590ba26b20dc5f0f4
