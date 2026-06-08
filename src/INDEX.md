# `commons`

## Summary

- `src/commons` は、cmoc 全体で共有する共通基盤モジュール群のルーティング目次です。
- ここから `__init__.py`、`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timing.py`、`timestamps.py` へ分岐します。
- CLI 実行や共通処理の入口をまとめ、個別モジュールへ進む前の案内役を担います。

## Read this when

- `src/commons` 配下で、どの共通モジュールがどの責務を持つかをまとめて把握したいとき。
- `codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timing.py`、`timestamps.py` のどれを読むべきか整理したいとき。
- CLI 実行、ログ、時間計測、エラー整形、Git 操作、`INDEX.md` 維持、タイムスタンプ、レポート保存の入口を確認したいとき。
- このディレクトリの下位ファイルへ進む前に、共通基盤の役割分担を整理したいとき。

## Do not read this when

- すでに読む対象が `src/commons/codex.py` など個別モジュールに決まっていて、この階層の案内が不要なとき。
- 個別サブコマンドの引数解析や業務ロジックだけを確認したいとき。
- `src/main.py` や `src/sub_commands/` など、CLI の入口や各コマンド本体を直接追いたいとき。
- `oracles` 側の正本仕様や `INDEX.md` の生成ルールだけを確認したいとき。

## hash

- 442b2d5d9053c1ae1f6c1dd7c95e986e4f8a43daeda1d55055532b47703fd9b9

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

- `src/sub_commands` は cmoc のサブコマンド実装群の入口目次です。
- 直下の `__init__.py`、`init.py`、`indexing.py` と、配下の `apply/`、`review/`、`session/` へ案内します。
- 個別コマンド本体へ進む前に、どの実装モジュールを開くかを切り分ける役割を持ちます。

## Read this when

- `src/sub_commands` 配下の全体構成と、次に読むべきモジュールを整理したいとき。
- `cmoc init`、`cmoc indexing`、`cmoc apply`、`cmoc review`、`cmoc session` の実装位置を確認したいとき。
- サブコマンドの追加・移動・分割を行う前に、この階層の案内先を確認したいとき。

## Do not read this when

- すでに読む対象が `src/sub_commands/__init__.py`、`src/sub_commands/init.py`、`src/sub_commands/indexing.py`、`src/sub_commands/apply/`、`src/sub_commands/review/`、`src/sub_commands/session/` のいずれかに決まっていて、この階層の目次が不要なとき。
- `cmoc` の CLI 登録やサブコマンド接続だけを追いたいときは `src/main.py` を読むべきとき。
- `cmoc apply`、`cmoc review`、`cmoc session` など個別サブコマンドの正本仕様だけを確認したいときは `oracles/docs/app_specs/sub_commands/` 側を読むべきとき。

## hash

- 0d86eb0ca2224f2bc3de87976f3f831a5b1a8f92ac31db2db30a346ecb2a7529
