# `commons`

## Summary

- cmoc で共通利用する基盤モジュール群の集約先です。`codex.py`、`command_runner.py`、`repo.py`、`errors.py`、`subcommand_log.py`、`timing.py`、`timestamps.py`、`report_files.py`、`indexing.py` など、CLI 実行・リポジトリ操作・ログ・時間計測・レポート保存・`INDEX.md` メンテナンスを支える処理が入っています。
- `__init__.py` はパッケージ宣言のみで、公開 API の本体は個別モジュールに分かれています。

## Read this when

- cmoc 全体で使う共通処理の役割分担や、どのモジュールに何があるかを把握したいとき。
- Codex CLI 呼び出し、サブコマンド実行制御、Git リポジトリ探索、共通エラー整形、サブコマンドログ、タイムスタンプ、経過時間計測、レポート保存、`INDEX.md` メンテナンスの実装や修正に入る前に入口を確認したいとき。
- `src.commons` が Python パッケージであることを確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや `src/commands` 側の振る舞いを確認したいときは、この共通モジュール群ではなく該当コマンド側を読むべきです。
- `oracles` の正本仕様や `INDEX.md` 生成ルールの詳細だけを確認したいときは、このディレクトリではなく `oracles/app_specs/indexing.md` を読むべきです。
- 特定の共通処理だけを追いたいときは、`codex.py`、`repo.py`、`errors.py` など該当モジュールへ直接進めば足ります。

## hash

- d6674278d3c0b39f52c2f3bfa2c07c42ccd8e122a333fe3bc1fafd40582f69af
<!-- cmoc-index-kind: directory -->

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

- d03b4e0b3d0c12971884d8bc1e159f95c3f0efe50e8fca99dc96066066992456

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc の個別サブコマンド実装の入口です。
- 直下の `__init__.py`、`apply`、`session`、`eval_oracles.py`、`init.py` に分かれた責務を案内します。
- この目次は、どのサブコマンド本体やパッケージ入口へ進むべきかを素早く振り分けるためのものです。

## Read this when

- cmoc の個別サブコマンド実装の入口をまとめて確認したいとき。
- `apply`、`session`、`review oracles`、`init` のどの実装ファイルへ進むべきか整理したいとき。
- パッケージ入口とコマンド本体の対応関係を俯瞰したいとき。

## Do not read this when

- `src/sub_commands` 配下の個別サブコマンドの処理順、前提条件、状態遷移だけを確認したいときは、該当モジュールや正本仕様を直接読むべきです。
- パッケージ宣言だけを確認したいときは、`__init__.py` を直接見れば足ります。
- `branch_model`、`codex_call`、`indexing`、`error_handling` など、別の共通仕様だけを確認したいときは、他の入口文書を読むべきです。

## hash

- 03ddb0a912f05fca82efe7b37afcf333228f298c95db02e80dcd2dab18a720a9
<!-- cmoc-index-kind: directory -->
