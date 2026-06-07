# `commons`

## Summary

- `src/commons` 配下の共通モジュール群へのルーティング文書で、cmoc の実行基盤と補助処理をまとめて案内する階層です。
- `__init__.py`、`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` へ進むための入口です。
- CLI 実行、エラー整形、repo / worktree 操作、`INDEX.md` 維持、サブコマンドログ、時間計測、タイムスタンプ、レポート保存の役割を切り分けるための目次です。

## Read this when

- `src/commons` 配下でどの共通モジュールがどの役割を担うかを一覧したいとき。
- `codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` のどれへ進むべきか迷ったとき。
- CLI 実行基盤、共通エラー整形、repo / worktree 操作、`INDEX.md` 維持、ログ、時刻、経過時間、レポート保存の入口を切り分けたいとき。
- package 入口の `__init__.py` を含めて、commons 配下の役割分担を把握したいとき。

## Do not read this when

- 個別の共通モジュールの実装へすでに進む先が決まっていて、この階層の目次を読む必要がないとき。
- `src/sub_commands` や各サブコマンドの業務ロジックだけを確認したいとき。
- `oracles` 側の正本仕様や、`README.md`・`AGENTS.md` などのリポジトリ運用ルールだけを確認したいとき。
- `__pycache__` などの生成物ではなく、ソースコードの個別実装だけを確認したいとき。

## hash

- dd0a9fdc440e8c7f63da9a2d64ec372e1d8a06a0ccd5b7f1ec08706793d614e5

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

- `src/sub_commands` 配下のルーティング文書で、`cmoc` のサブコマンド群へ進むための入口です。
- `__init__.py` はパッケージ宣言、`init.py` は `cmoc init`、`indexing.py` は `cmoc indexing` の本体実装を案内します。
- `apply/`、`review/`、`session/` はそれぞれ専用の下位ルーティングを持ち、個別サブコマンドの実装へ分岐するための目次です。

## Read this when

- `src/sub_commands` 配下の入口構造をまとめて把握し、どの実装ファイルや下位ディレクトリへ進むべきか迷っているとき。
- `__init__.py`、`init.py`、`indexing.py` と、`apply/`、`review/`、`session/` の各サブコマンド群の役割分担を整理したいとき。
- `cmoc` のサブコマンド実装やテストに入る前に、この階層の目次としてどの文書を読むべきか確認したいとき。
- `src/sub_commands` を起点に、個別サブコマンドの実装・仕様・ルーティングをたどり始めたいとき。

## Do not read this when

- `src/sub_commands` 配下の個別モジュールや下位ディレクトリへ直接進む対象がすでに決まっているとき。
- `cmoc init` や `cmoc indexing` など、個別サブコマンドの詳細仕様だけを確認したいとき。
- `apply/`、`review/`、`session/` の各入口ではなく、別のディレクトリのルーティング文書を見たいとき。
- `src/sub_commands` 全体ではなく、CLI 登録や別層の共通処理だけを確認したいとき。

## hash

- f603137b619d6e3f10b9458b365c562d46b60955f6c5050bb9fec25a07e74791
