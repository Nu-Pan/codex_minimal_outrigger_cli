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

- `src/sub_commands/review/oracles.py` は `cmoc review oracles` の本体実装で、oracles スナップショット固定、`INDEX.md` メンテナンス、oracle ファイルごとの並列評価、所見改善、レポート保存までを一括して担います。
- `--scope` と旧 `--full` の互換、各種反復回数の検証、issue payload の検証、エラー時のレポート生成もまとめて扱います。
- `cmoc review oracles` の実行フローと、評価対象ファイルの選定・検証・出力のどこを読むべきかを切り分けるための目次です。

## Read this when

- `cmoc review oracles` の実装・修正・レビュー・テストを行いたいとき。
- 開始時点の oracles スナップショット固定、`.cmoc` の ignore 確認、`INDEX.md` メンテナンス反映後の評価対象スナップショットの扱いを追いたいとき。
- oracle ファイルの並列評価、問題点リストの改善、レポート保存や error report の分岐を確認したいとき。
- `--scope` / 旧 `--full` の互換、`--enumerate-findings-loop`、`--merge-findings-loop`、`--refine-findings-loop` の制御点を確認したいとき。

## Do not read this when

- `cmoc review oracles` の利用手順や引数仕様だけを確認したいときは、`oracles/docs/app_specs/sub_commands/review_oracles.md` を読むべきです。
- `cmoc review` の CLI 登録や hidden alias だけを確認したいときは、`src/main.py` を読むべきです。
- `src/sub_commands/review` のパッケージ宣言だけを確認したいときは、`src/sub_commands/review/__init__.py` を読むべきです。
- `oracles` 側の正本仕様そのものを確認したいときは、この実装ではなく `oracles/` 配下の仕様断片とその `INDEX.md` を読むべきです。

## hash

- f623f708d09b0f1b8b646c1e9ec492394ee76bce441811b0c7202da7ee61acfe
