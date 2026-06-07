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

- `src/sub_commands/review/oracles.py` は `cmoc review oracles` の本体実装で、session branch の前提検証から review worktree の作成、oracle スナップショット固定、所見パイプラインの実行、review branch の merge、Markdown レポート出力までを一連で担います。
- 所見の列挙・統合・検証・判定を Structured Output 付きで進め、scope に応じた対象 oracle の選定、`INDEX.md` メンテナンスの反映、失敗時の error report 生成までをまとめて扱います。
- レビュー対象の oracle 選定や部分評価 / 全体評価の切り替え、merge conflict 中の `INDEX.md` 自動解消、レポート補助処理や payload 検証の helper 群もこのモジュールの責務です。

## Read this when

- `src/sub_commands/review/oracles.py` の実装・修正・レビュー・テストを行いたいとき。
- session branch 前提の検証、`.cmoc` の ignore / clean 状態確認、review worktree 作成から review branch の merge までの流れを追いたいとき。
- oracle スナップショット固定、`INDEX.md` メンテナンス反映、所見の列挙・統合・検証・判定の Structured Output パイプラインを確認したいとき。
- review レポートや error report の生成、保存、表示、そして merge conflict 中の `INDEX.md` 自動解消仕様を確認したいとき。

## Do not read this when

- `cmoc review oracles` の利用手順、引数、出力仕様だけを確認したいときは、実装ではなく `oracles/docs/app_specs/sub_commands/review_oracles.md` を読むべきです。
- `src/sub_commands/review` のパッケージ宣言だけを確認したいときは、`src/sub_commands/review/__init__.py` を読むべきです。
- `cmoc review oracles` の CLI 登録や hidden alias だけを確認したいときは、`src/main.py` を読むべきです。
- `INDEX.md` の生成・更新ルールや、`oracles` 全体のルーティング方針だけを確認したいときは、`oracles/docs/app_specs/indexing.md` を読むべきです。

## hash

- 3e0299bcbb8c345b09ce1b6c4618f3d83f0857b0745f6b6007baf20ae57a393b
