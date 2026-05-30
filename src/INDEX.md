# `commons`

## Summary

- `src/commons` は cmoc 全体で共有する基盤処理の集約先で、`__init__.py` と各種共通モジュールをまとめています。
- `codex.py` は `codex exec` の共通起動基盤、`command_runner.py` はサブコマンド共通実行、`repo.py` は git と cmoc 状態管理、`errors.py` は共通エラー整形を担当します。
- `subcommand_log.py`、`timing.py`、`timestamps.py`、`report_files.py`、`indexing.py` はそれぞれログ記録、経過時間計測、タイムスタンプ生成、レポート保存、`INDEX.md` 目次維持を扱います。
- このディレクトリの目次は、共通処理の役割を素早く切り分けて、必要な実装へ最短でたどるための入口です。

## Read this when

- cmoc 全体で使う共通基盤モジュールの役割分担を把握したいとき。
- `codex.py`、`command_runner.py`、`repo.py`、`errors.py`、`subcommand_log.py`、`timing.py`、`timestamps.py`、`report_files.py`、`indexing.py` のどれに何があるかを俯瞰したいとき。
- 共通処理の入口を確認してから、実装やテストの対象モジュールへ進みたいとき。

## Do not read this when

- `src/sub_commands` 側の個別サブコマンドの業務ロジックや CLI 引数だけを確認したいとき。
- `oracles` の正本仕様や `INDEX.md` の生成ルールだけを確認したいとき。
- 特定の共通モジュール 1 つだけの詳細実装を追いたいとき。

## hash

- e96c77a0a4f9c1684cb598a016371c6e97a12f05165463aed067a752844a737e

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

- `cmoc` の個別サブコマンド実装を集めるパッケージの入口です。
- `apply/` と `session/` に、`apply` 系と `session` 系の本体実装が分かれています。
- `src/main.py` から呼び出される CLI ルーティング先をたどる起点です。

## Read this when

- `cmoc` のサブコマンド本体がどこにあるか確認したいとき。
- `apply` 系と `session` 系の実装入口をまとめて把握したいとき。
- `src/main.py` から各サブコマンドへの対応関係を整理したいとき。
- `src/sub_commands` 配下を修正・レビュー・テストする前に入口を確認したいとき。

## Do not read this when

- 個別の `apply` / `session` コマンドの引数、状態遷移、終了条件だけを確認したいときは、該当サブディレクトリの仕様や実装を直接読むべきです。
- `cmoc` 全体の起動処理や共通エラーハンドリングだけを確認したいときは、`src/main.py` や共通モジュールを読むべきです。
- `INDEX.md` の生成ルールや `oracles` 側のルーティング方針だけを確認したいときは、このディレクトリを読む必要はありません。

## hash

- cf7f4287c853ec187a16380d5f11907995c4351163ca247c57444d583f5a862b
