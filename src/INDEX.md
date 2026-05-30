# `commons`

## Summary

- `src/commons` は cmoc 全体で共有する基盤処理の入口です。
- `command_runner.py`、`codex.py`、`repo.py`、`errors.py`、`indexing.py`、`report_files.py`、`subcommand_log.py`、`timing.py`、`timestamps.py`、`__init__.py` への導線をまとめます。
- 実行制御、Codex CLI 呼び出し、git リポジトリ検出、`INDEX.md` 生成・維持、レポート保存、サブコマンドログ、計時、タイムスタンプ生成の役割分担を整理するための目次です。

## Read this when

- 共通の実行制御、エラー整形、リポジトリ検出、ログ保存、計時の入口をまとめて把握したいとき。
- `codex exec` の呼び出し方、Structured Output の扱い、出力検証を確認したいとき。
- `INDEX.md` の生成・更新・再利用判定や、どの共通モジュールを読むべきかを振り分けたいとき。
- `src/commons` が Python パッケージとしてどう責務分割されているか確認したいとき。

## Do not read this when

- 個別サブコマンドの引数や業務ロジックだけを確認したいとき。
- `src/sub_commands` 側の実装や CLI のサブコマンド構成だけを追いたいとき。
- `INDEX.md` の生成ルールそのものや、`oracles` 側の仕様断片だけを確認したいとき。
- `src/commons` 以外の日時ユーティリティ、ログ表示、テスト観点だけを探したいとき。

## hash

- dc67ea824d511ed6f3286192649f913a0b5ce50cb92d54b50eb4c8dcd7635026
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

- `src/sub_commands` は cmoc のサブコマンド実装をまとめるディレクトリの入口です。
- 直下には `__init__.py`、`init.py`、`eval_oracles.py` と、`apply`・`session` の各パッケージがあり、それぞれのサブコマンド本体へ分岐します。
- この目次は、サブコマンド全体の役割分担と、各実装ファイルへの入り口を素早く振り分けるためのものです。

## Read this when

- `src/sub_commands` 全体の役割と、配下にどの実装入口があるかをまとめて把握したいとき。
- `cmoc init`、`cmoc review oracles`、`cmoc apply`、`cmoc session` のうち、どのファイルを読むべきか判断したいとき。
- `src.sub_commands` が Python パッケージとして成立していることや、配下の配置だけを確認したいとき。

## Do not read this when

- 個別サブコマンドの処理順、状態遷移、例外条件だけを確認したいとき。
- `cmoc apply` や `cmoc session` の詳細仕様を直接追いたいとき。
- `oracles` の仕様断片や `INDEX.md` 生成ルールだけを確認したいとき。

## hash

- 33f5bee825729d3ca2913d39b0490463fc0b3391eeb11f58c0c02261d687ef84
