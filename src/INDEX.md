# `commons`

## Summary

- `src/commons` 配下の共通モジュール群へ案内するルーティング文書です。
- `__init__.py`、`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` をまとめて案内します。
- CLI 実行制御、エラー整形、repo / worktree 操作、`INDEX.md` 維持、ログ、時刻、経過時間、レポート保存の役割分担を確認する入口です。

## Read this when

- `src/commons` のどのモジュールがどの役割かを一覧したいとき。
- `codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` のどれを読むべきか迷ったとき。
- CLI 実行基盤、共通エラー、repo / worktree 操作、`INDEX.md` 維持、サブコマンドログ、時間計測、タイムスタンプ、レポート保存の入口を切り分けたいとき。
- package 入口の `__init__.py` を含めて commons 配下の役割分担を把握したいとき。

## Do not read this when

- すでに読む先の共通モジュールが決まっていて、この階層の目次を確認する必要がないとき。
- `src/sub_commands` や個別サブコマンドの業務ロジックだけを確認したいとき。
- `oracles` 側の正本仕様や、`README.md`・`AGENTS.md` などのリポジトリ運用ルールだけを確認したいとき。
- 生成物や `__pycache__` ではなく、個別実装だけを確認したいとき。

## hash

- d6beff3aa9f8416d0473c32d8582edf729746bb95102fc095753417096350669

# `main.py`

## Summary

- `src/main.py` は cmoc CLI のエントリーポイントで、Typer のルート `app` と `session` / `apply` / `review` の各サブアプリを組み立てるファイルです。
- `init`、`indexing`、`session`、`apply`、`review` の各コマンド登録に加えて、`eval-oracle` / `eval-oracles` の隠し別名や各コマンドの既定オプションをまとめています。
- サブコマンド未指定時の `CmocError` 生成、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc CLI の起点として、`session` / `apply` / `review` のサブアプリ構成を確認したいとき。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録名や隠し別名を確認したいとき。
- `apply fork` の既定反復回数や `scope`、`apply join` の `--force-resolve` などの既定オプションを確認したいとき。
- サブコマンド未指定時の利用者向けエラー、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の経路を確認したいとき。

## Do not read this when

- `session`、`apply`、`review` など個別サブコマンドの本体実装だけを確認したいとき。
- `commons.errors` や `format_error_report()` の共通エラー整形だけを確認したいとき。
- `bin/cmoc` のシェル起動ラッパーだけを確認したいとき。

## hash

- a756de7b8e379a66e5e1bdfc4aa80c43d910a513c480de908c6d46a9f1196f81

# `sub_commands`

## Summary

- この `src/sub_commands` ディレクトリのルーティング文書で、`cmoc` のサブコマンド実装へ進むための入口です。
- `__init__.py`、`init.py`、`indexing.py` と、`apply/`、`review/`、`session/` の各下位ディレクトリへ案内します。
- 個別サブコマンドの本体実装と、階層化された入口を切り分けるための目次です。

## Read this when

- `src/sub_commands` 配下の入口構造をまとめて把握し、どの実装ファイルへ進むべきか整理したいとき。
- `__init__.py`、`init.py`、`indexing.py`、`apply/`、`review/`、`session/` の役割分担を確認したいとき。
- `cmoc init` や `cmoc indexing` を含むサブコマンド実装の起点を確認したいとき。
- この階層から個別実装や下位の `INDEX.md` に分岐し始めたいとき。

## Do not read this when

- すでに読む先の個別モジュールや下位ディレクトリが決まっていて、この階層の目次を確認する必要がないとき。
- `cmoc init`、`cmoc indexing`、`cmoc apply`、`cmoc review` のいずれかの実装本体だけを直接確認したいとき。
- `oracles` 側の正本仕様や、生成物・`__pycache__` のような対象外ファイルだけを確認したいとき。

## hash

- 938729801e184f56c7e3dc081278a4c4df328c4138ba68d89db61cc413ecd18d
