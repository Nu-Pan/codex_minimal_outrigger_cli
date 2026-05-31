# `commons`

## Summary

- `src/commons` は cmoc 全体で共有する基盤処理の集約先で、`__init__.py` と共通モジュールをまとめています。
- `codex.py`、`command_runner.py`、`errors.py` は Codex CLI 呼び出し、共通実行制御、共通例外とエラー表示を担当します。
- `repo.py`、`subcommand_log.py`、`timing.py`、`timestamps.py`、`report_files.py`、`indexing.py` は repo root と状態管理、ログ、経過時間、タイムスタンプ、レポート保存、`INDEX.md` メンテナンスを扱います。

## Read this when

- cmoc 全体で使う共通基盤の役割分担を把握したいとき。
- `codex.py`、`command_runner.py`、`repo.py`、`errors.py`、`subcommand_log.py`、`timing.py`、`timestamps.py`、`report_files.py`、`indexing.py` のどれに何があるかを整理したいとき。
- 共通処理の入口を確認してから、実装やテストの対象モジュールへ進みたいとき。

## Do not read this when

- `src/sub_commands` 側の個別サブコマンドの業務ロジックや CLI 引数だけを確認したいとき。
- `oracles` の正本仕様や `INDEX.md` の生成ルールだけを確認したいとき。
- 特定の共通モジュール 1 つだけの詳細実装を追いたいとき。

## hash

- 1ba1fce91f8152e96eb3b0bb4bcebbefe6d76b064655ee562d9a5cf3fd96d81c

# `main.py`

## Summary

- cmoc CLI のエントリーポイントで、Typer のルート `app` と `session` / `apply` / `review` の各サブアプリを組み立てるファイルです。
- `init`、`session`、`apply`、`review` の各コマンド登録に加えて、`eval-oracle` / `eval-oracles` の隠し別名や、`apply fork` の繰り返し回数・`scope`、`apply join` の `--force-resolve` などの既定値をまとめています。
- サブコマンド未指定時の `CmocError` 生成、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc CLI の起動点と、`session` / `apply` / `review` のサブアプリ構成を確認したいとき。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録名、隠し別名、既定オプションを確認したいとき。
- サブコマンド未指定時の利用者向けエラー、補完プローブ時の分岐、Click/Typer 例外の共通整形を追いたいとき。
- `python src/main.py` で直接起動する経路と、そのときの例外処理を確認したいとき。

## Do not read this when

- `src/sub_commands/` 配下の各サブコマンド本体の実装だけを追いたいとき。
- `commons.errors` のエラー型や `format_error_report()` の整形ロジックだけを確認したいとき。
- `INDEX.md` の生成ルールや `oracles` 側のルーティング方針だけを確認したいとき。

## hash

- 34ab9fdae7d4622e261437958669dd52ce211f233a2300c1c7c831efc256c365

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc のサブコマンド実装を束ねる入口ディレクトリです。
- `__init__.py` は `src.sub_commands` パッケージを宣言するだけの最小モジュールです。
- `init.py` は `cmoc init` の本体実装です。
- `apply`、`review`、`session` はそれぞれ `cmoc apply`、`cmoc review`、`cmoc session` 系の実装入口をまとめるサブディレクトリです。

## Read this when

- `src/sub_commands` 配下で、どのファイルがどの `cmoc` コマンドを担当しているかを素早く整理したいとき。
- `cmoc init`、`cmoc apply`、`cmoc review`、`cmoc session` の入口をどこから読むべきか判断したいとき。
- `src/sub_commands` の入口として、`__init__.py`・`init.py`・`apply`・`review`・`session` の役割分担を把握したいとき。
- サブコマンド実装の修正やレビューに入る前に、関連するモジュールの配置を確認したいとき。

## Do not read this when

- `src/sub_commands` 配下の個別実装や処理分岐だけを確認したいときは、この目次ではなく各モジュールや各サブディレクトリの `INDEX.md` を直接読むべきです。
- `cmoc` の利用手順や仕様断片だけを確認したいときは、実装ではなく `oracles/app_specs/sub_commands/` 側を読むべきです。
- `src/sub_commands` のパッケージ宣言だけを確認したいときは、この目次ではなく `src/sub_commands/__init__.py` を直接読むべきです。
- `cmoc` の CLI 全体構成や共通基盤だけを追いたいときは、このディレクトリではなく `src/main.py` や `src/commons` を読むべきです。

## hash

- d91c91c243612d8b0bd857f16e994b2ed602eec5cf80fa975a4cb53e3c470dc0
