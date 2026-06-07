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

- `src/sub_commands/review/oracles.py` は `cmoc review oracles` の本体実装で、session branch の前提検証から review worktree の作成、oracle スナップショットの固定、所見の列挙・統合・検証・判定、レポート出力までを一連で担うモジュールです。
- Structured Output を使う所見パイプライン、`INDEX.md` を根拠にした対象 oracle の選定、`INDEX.md` コンフリクトの機械的解消、失敗時の error report 生成までをまとめています。
- 所見の集約、評価メタデータ更新、結果集計、Markdown レポート整形を支える helper 群もこのモジュールに含まれます。

## Read this when

- `src/sub_commands/review/oracles.py` の実装・修正・レビュー・テストを行うとき。
- `cmoc review oracles` の前提条件検証、review worktree の作成、oracle スナップショット固定、所見の列挙・統合・検証・判定、レポート出力までの流れを追いたいとき。
- Structured Output schema の読み込みや、所見パイプラインで使うヘルパー群の役割を確認したいとき。
- merge conflict 中の `INDEX.md` の扱い、評価結果やエラーレポートの生成条件を確認したいとき。

## Do not read this when

- `cmoc review oracles` の利用手順、引数、出力仕様だけを確認したいときは、[`oracles/docs/app_specs/sub_commands/review_oracles.md`](/home/happy/codex_minimal_outrigger_cli_stage1/.cmoc/worktrees/apply/2026-05-31_22-03-16_000000754/2026-06-07_10-40_51_000000114/oracles/docs/app_specs/sub_commands/review_oracles.md) を読むべきです。
- `src/sub_commands/review` のパッケージ宣言だけを確認したいときは、[`src/sub_commands/review/INDEX.md`](/home/happy/codex_minimal_outrigger_cli_stage1/.cmoc/worktrees/apply/2026-05-31_22-03-16_000000754/2026-06-07_10-40_51_000000114/src/sub_commands/review/INDEX.md) か [`src/sub_commands/review/__init__.py`](/home/happy/codex_minimal_outrigger_cli_stage1/.cmoc/worktrees/apply/2026-05-31_22-03-16_000000754/2026-06-07_10-40_51_000000114/src/sub_commands/review/__init__.py) を読むべきです。
- `cmoc review` の CLI 登録や hidden alias だけを確認したいときは、[`src/main.py`](/home/happy/codex_minimal_outrigger_cli_stage1/.cmoc/worktrees/apply/2026-05-31_22-03-16_000000754/2026-06-07_10-40_51_000000114/src/main.py) を読むべきです。
- `cmoc review oracles` の評価ロジックではなく、`oracles` 全体の共通仕様や別サブコマンドの入口を追いたいときは、このファイルではなく上位のルーティング文書を読むべきです。

## hash

- 22807b5ccafd7baea41f92a18b391e02270b5a22ff11be79c7a9bfa3651643f7
