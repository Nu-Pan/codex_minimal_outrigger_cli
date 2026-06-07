# `commons`

## Summary

- `src/commons` 配下の共通モジュール群へのルーティング文書で、`cmoc` の実行基盤や補助処理をまとめて案内します。
- `__init__.py` に加えて、`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` へ進むための入口です。
- まずこの目次で目的の共通処理を切り分け、必要に応じて個別モジュールへ進むための階層です。

## Read this when

- `src/commons` がどの共通モジュールをまとめているかを一覧したいとき。
- `codex` 実行、サブコマンド共通化、エラー整形、repo / worktree 管理、ログ、タイムスタンプ、時間計測の入口を切り分けたいとき。
- `INDEX.md` から `src/commons/*.py` のどれへ進むべきか迷ったとき。
- package 入口の `__init__.py` を含めて、commons 配下の役割分担を確認したいとき。

## Do not read this when

- 目的の共通モジュールがすでに分かっていて、`codex.py` や `repo.py` などの個別ファイルへ直接進めるとき。
- サブコマンド固有の手順や `src/sub_commands` 側の実装だけを確認したいとき。
- `oracles` 側の正本仕様や `docs/` のルーティングだけを確認したいとき。
- `README.md` や `AGENTS.md` など、リポジトリ運用ルールだけを確認したいとき。

## hash

- 76bb1584b6010eb3894af18dabed6f3a55d4bedbdc01c321c5a37ac12dfed172

# `main.py`

## Summary

- `src/main.py` は cmoc CLI のエントリーポイントで、Typer のルート `app` と `session` / `apply` / `review` の各サブアプリを組み立てるファイルです。
- `init`、`session`、`apply`、`review` の各コマンド登録に加えて、`eval-oracle` / `eval-oracles` の隠し別名や各コマンドの既定オプションをまとめています。
- サブコマンド未指定時の `CmocError` 生成、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc CLI の起点として、`session` / `apply` / `review` のサブアプリ構成を確認したいとき。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録名や隠し別名を確認したいとき。
- `apply fork` の既定反復回数や `scope`、`apply join` の `--force-resolve` などの既定オプションを確認したいとき。
- サブコマンド未指定時の利用者向けエラー、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の経路を確認したいとき。

## Do not read this when

- `src/sub_commands/` 配下の個別サブコマンド本体だけを確認したいとき。
- `commons.errors` や `format_error_report()` の例外整形だけを確認したいとき。
- `oracles` 側の正本仕様や `INDEX.md` 生成ルールだけを確認したいとき。
- `bin/cmoc` のシェル起動ラッパーだけを確認したいとき。

## hash

- 8e5c543120f5d8c879497bffa31a440854f689cb349abab0deb3f8a0cf8bf19e

# `sub_commands`

## Summary

- この `src/sub_commands` ディレクトリは、`cmoc` のサブコマンド実装をまとめる入口で、`__init__.py`、`init.py`、`indexing.py`、`apply/`、`session/`、`review/` への案内をまとめる場所です。
- `__init__.py` はパッケージ宣言のみ、`init.py` は `cmoc init`、`indexing.py` は `cmoc indexing` を担います。
- `apply/`、`session/`、`review/` はそれぞれ独立したサブコマンド系統の入口ディレクトリで、さらに下位の `INDEX.md` へ分岐します。
- この階層は、どのサブコマンド実装ファイルを読むべきかを最初に切り分けるための目次です。

## Read this when

- `cmoc init`、`cmoc indexing`、`cmoc apply`、`cmoc session`、`cmoc review` のうち、どの実装ファイルへ進むべきか整理したいとき。
- このディレクトリ配下のパッケージ構造と、各サブコマンド系統の役割分担を把握したいとき。
- サブコマンド実装の修正・レビュー・テストを始める前に、対象モジュールを絞り込みたいとき。
- `apply/`、`session/`、`review/` のどれかの下位実装へ進む前に、その入口だけ確認したいとき。

## Do not read this when

- 読むべき個別モジュールがすでに分かっていて、`init.py` や各下位ディレクトリの `INDEX.md` に直接進めるとき。
- `cmoc init` や `cmoc indexing` の実装詳細、状態遷移、エラーハンドリングだけを確認したいとき。
- `apply`、`session`、`review` の個別機能の仕様断片だけを確認したいときは、この階層ではなく各下位ディレクトリの文書を読むべきとき。
- リポジトリ全体の運用規則や `oracles` 側の正本仕様だけを確認したいとき。

## hash

- fcd22e8ea4d91263a4e1472a81d8d6509490baf31d0f8946b34e67fee766019a
