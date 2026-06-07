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

- `src/sub_commands/review/oracles.py` は `cmoc review oracles` の本体で、session branch 前提の検証、`.cmoc` の ignore / clean 状態確認、評価用 worktree 作成、oracle スナップショット固定、評価実行をまとめて担います。
- oracle ファイルの選定、`INDEX.md` のメンテナンス反映、並列評価、issue の改善ループ、結果レポート / エラーレポート保存までを一連の処理として実装しています。
- Structured Output の検証、参照可能な oracle / `INDEX.md` パスの妥当性確認、review branch と session branch の merge conflict 解消もこのモジュールの役割です。

## Read this when

- `cmoc review oracles` の実装・修正・レビュー・テストを行いたいとき。
- 開始時点の oracle 内容を固定した snapshot 評価、`INDEX.md` メンテナンスの反映、評価対象ファイルの選定方法を追いたいとき。
- `--scope` / 旧 `--full`、各種 loop 回数、issue payload の検証、レポート出力の流れを確認したいとき。

## Do not read this when

- `cmoc review oracles` の利用手順や引数仕様だけを確認したいときは、`oracles/docs/app_specs/sub_commands/review_oracles.md` を読むべきです。
- `cmoc review` の CLI 登録や hidden alias だけを確認したいときは、`src/main.py` を読むべきです。
- `src/sub_commands/review` のパッケージ宣言だけを確認したいときは、`src/sub_commands/review/__init__.py` を読むべきです。
- oracles 側の正本仕様そのものを確認したいときは、`oracles/INDEX.md` から仕様断片をたどるべきです。

## hash

- 684e5cf865198dc9b8cade8433b461e70e27a17fda99b282bd82506be249995e
