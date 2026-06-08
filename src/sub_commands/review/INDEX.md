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

- `src/sub_commands/review/oracles.py` は `cmoc review oracles` の本体実装で、session branch の前提確認、`.cmoc` の ignore 保証、review worktree の作成と merge をまとめて担います。
- oracle tree の snapshot 固定、`INDEX.md` を起点にした評価対象の選定、所見の列挙・統合・検証・判定のパイプラインを含みます。
- Structured Output schema の読込・検証、評価レポート / error report の生成、各種レイアウト用ヘルパーもこの 1 ファイルに集約されています。

## Read this when

- `cmoc review oracles` の実装・修正・レビュー・テストを行いたいとき。
- session branch 前提、clean worktree、review worktree 作成、merge の流れを追いたいとき。
- oracle ファイルの選定基準、所見処理パイプライン、Structured Output schema の扱いを確認したいとき。

## Do not read this when

- `cmoc review oracles` の利用手順や引数仕様だけを確認したいときは、`oracles/docs/app_specs/sub_commands/review_oracles.md` を読むべきです。
- `cmoc review` の CLI 登録や hidden alias だけを確認したいときは、`src/main.py` を読むべきです。
- `src/sub_commands/review` の入口構造だけを把握したいときは、`src/sub_commands/review/INDEX.md` で足ります。

## hash

- 43e3d6364ecc7f8d01e4f8608c3ab98dca17cfdc7615d8dc9fae5705b573bad5
