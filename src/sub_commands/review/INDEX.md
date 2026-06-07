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

- `/home/happy/codex_minimal_outrigger_cli_stage1/.cmoc/worktrees/apply/2026-05-31_22-03_16_000000754/2026-06-07_10-40_51_000000114/src/sub_commands/review/oracles.py` は `cmoc review oracles` の本体処理を担うモジュールです。
- `.cmoc` の ignore 保証、評価対象 oracle の選定、開始時点 snapshot の固定、`INDEX.md` のメンテナンス、oracle ファイルごとの並列評価、所見の整理、最終レポート保存までを一連で実行します。
- `--scope` と各種反復回数の上限を使いながら、fatal / minor の所見を列挙・検証・判定するための入口です。

## Read this when

- `cmoc review oracles` の実行フロー、開始時点 snapshot の固定、評価対象 oracle の選定を確認したいとき。
- `INDEX.md` メンテナンスを含む review の処理順と、oracle ファイルごとの並列評価・所見整理・レポート出力の流れを追いたいとき。
- `--scope`、`--enumerate-findings-loop`、`--merge-findings-loop`、`--refine-findings-loop` の処理位置や、どこで評価・検証ループに入るかを知りたいとき。
- `cmoc review oracles` が `.cmoc` の ignore 保証、評価対象の絞り込み、改善ループ、最終レポート保存をどうまとめて実行するかを把握したいとき。

## Do not read this when

- `cmoc review oracles` の利用手順や引数仕様だけを確認したいときは、`/home/happy/codex_minimal_outrigger_cli_stage1/.cmoc/worktrees/apply/2026-05-31_22-03_16_000000754/2026-06-07_10-40_51_000000114/oracles/docs/app_specs/sub_commands/review_oracles.md` を読むべきです。
- `cmoc review` の CLI 登録や hidden alias だけを確認したいときは、`/home/happy/codex_minimal_outrigger_cli_stage1/.cmoc/worktrees/apply/2026-05-31_22-03_16_000000754/2026-06-07_10-40_51_000000114/src/main.py` を読むべきです。
- `cmoc review` のパッケージ宣言だけを確認したいときは、`/home/happy/codex_minimal_outrigger_cli_stage1/.cmoc/worktrees/apply/2026-05-31_22-03_16_000000754/2026-06-07_10-40_51_000000114/src/sub_commands/review/__init__.py` を読むべきです。
- `oracles` の正本仕様そのものを確認したいときは、このファイルではなく `/home/happy/codex_minimal_outrigger_cli_stage1/.cmoc/worktrees/apply/2026-05-31_22-03_16_000000754/2026-06-07_10-40_51_000000114/oracles/` 配下の仕様断片を読むべきです。

## hash

- 013a8f829a216815e9394dc838185d059198cd501a0101c484852b5d1da537fe
