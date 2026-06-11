# `__init__.py`

## Summary

- `<cmoc-root>/src/sub_commands/review/__init__.py` は `cmoc review` 系サブコマンドのパッケージ宣言だけを担う最小モジュールです。
- 公開 API、定数、実行ロジック、再エクスポートは持ちません。

## Read this when

- `<cmoc-root>/src/sub_commands/review` が Python パッケージとして宣言されていることを確認したいとき。
- `cmoc review` 系サブコマンドの入口となるパッケージ構造を把握したいとき。

## Do not read this when

- `cmoc review oracles` の実行フローや評価ロジックを確認したいときは、`<cmoc-root>/src/sub_commands/review/oracles.py` を読むべきです。
- `cmoc review oracles` の CLI 引数や hidden alias の登録だけを確認したいときは、`<cmoc-root>/src/main.py` を読むべきです。

## hash

- d432dc21ecc8d2cabf968eac490bb998f303e6d3e7411b90260759ccd587f07d

# `oracles.py`

## Summary

- `<work-root>/src/sub_commands/review/oracles.py` は `cmoc review oracles` の本体実装で、前提条件の検証、`.cmoc` の ignore 保証、review 用 worktree の作成と session への merge を担うモジュールです。
- oracle tree のスナップショット固定、`INDEX.md` を起点にした対象選定、所見の列挙・統合・検証・判定のパイプラインをまとめています。
- Structured Output schema の読み込み・検証、評価レポート / error report の生成、レイアウト用ヘルパー群もこのファイルに集約されています。

## Read this when

- `cmoc review oracles` の実装・修正・レビュー・テストを行いたいとき。
- session branch 前提の確認、clean worktree の検証、review worktree の作成と merge の流れを追いたいとき。
- oracle ファイルの選定や、所見の列挙・マージ・検証・判定、Structured Output schema の扱いを確認したいとき。

## Do not read this when

- `cmoc review oracles` の利用手順や引数仕様だけを確認したいときは、`<work-root>/oracles/docs/app_specs/sub_commands/review_oracles.md` を読むべきです。
- `cmoc review` の CLI 登録や hidden alias だけを確認したいときは、`<work-root>/src/main.py` を読むべきです。
- `<work-root>/src/sub_commands/review` の入口構造だけを把握したいときは、`<work-root>/src/sub_commands/review/INDEX.md` で足ります。

## hash

- 2c0882ad36fc7042d5717b9e2cbc4249615b2bf7b117da1b28cb8c2f344ba11c
