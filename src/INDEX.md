# `commons`

## Summary

- `src/commons` 配下の共通モジュール群へのルーティング文書で、cmoc の実行基盤や補助処理をまとめて案内する階層です。
- `__init__.py` に加えて、`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` へ進むための入口です。
- CLI 実行、共通エラー整形、repo / worktree 操作、`INDEX.md` 維持、サブコマンドログ、時間計測、タイムスタンプ、レポート保存を切り分けるための目次です。

## Read this when

- `src/commons` 配下でどの共通モジュールがどの役割を担うかを一覧したいとき。
- `codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` のどれへ進むべきか迷ったとき。
- CLI 実行基盤、共通エラー整形、repo / worktree 操作、`INDEX.md` 維持、ログ、時刻、経過時間、レポート保存の入口を切り分けたいとき。
- package 入口の `__init__.py` を含めて、commons 配下の役割分担を把握したいとき。

## Do not read this when

- 個別の共通モジュールの実装へすでに進む先が決まっていて、この階層の目次を読む必要がないとき。
- `src/sub_commands` や各サブコマンドの業務ロジックだけを確認したいとき。
- `oracles` 側の正本仕様や、`README.md`・`AGENTS.md` などのリポジトリ運用ルールだけを確認したいとき。

## hash

- 7ad2328e1fc72cf01d836a423cd9cb9c95f29c8be5240bb2149280220ec99c8c

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

- `src/sub_commands` は cmoc の各サブコマンド実装への入口をまとめる階層です。
- `__init__.py` はパッケージ宣言のみを担い、`init.py` は `cmoc init`、`indexing.py` は `cmoc indexing` の本体実装です。
- `apply/`、`session/`、`review/` の各下位ディレクトリは、それぞれのサブコマンド群への案内入口です。

## Read this when

- `src/sub_commands` 配下の入口ファイルと下位ディレクトリの役割分担を確認したいとき。
- `__init__.py`、`init.py`、`indexing.py`、および `apply/`、`session/`、`review/` への導線を把握したいとき。
- `cmoc` のサブコマンド実装群の全体像を最初に整理したいとき。

## Do not read this when

- 目的のモジュールや下位ディレクトリがすでに分かっていて、`src/sub_commands/apply/`、`src/sub_commands/session/`、`src/sub_commands/review/`、`init.py`、`indexing.py` の個別ファイルへ直接進めるとき。
- `cmoc init`、`cmoc indexing`、`cmoc apply`、`cmoc session`、`cmoc review` の詳細な実行フローだけを確認したいとき。
- この階層の案内ではなく、各モジュール本体のコードや `oracles` 側の正本仕様を直接確認したいとき。

## hash

- 1374245397d23df3f5c3fb683ae3dc3aa5222a067f6f633e0454d9a556bd8017
