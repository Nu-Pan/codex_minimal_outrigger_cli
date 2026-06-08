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

- c83df0f63c63b1a360c5760dc43e68cc8d494f7996479b6b40969ede0ee74f1b

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc のサブコマンド実装をまとめる入口ディレクトリです。
- 直下には `__init__.py`、`init.py`、`indexing.py` があり、配下の `apply/`、`review/`、`session/` には各サブコマンド群の本体実装が入ります。
- この階層は、各コマンドの実行ロジックへ進む前の最初の目次として、どのモジュールを開くべきかを切り分ける役割を持ちます。

## Read this when

- `src/sub_commands` 配下の入口構造をまとめて把握し、どの実装モジュールへ進むべきか整理したいとき。
- `cmoc init`、`cmoc indexing`、`cmoc apply`、`cmoc session`、`cmoc review` の各実装ファイルの配置と役割分担を確認したいとき。
- サブコマンド実装を追加・移動・分割する前に、この階層が持つパッケージ構成と案内先を確認したいとき。

## Do not read this when

- `cmoc` の CLI 登録やサブコマンドの接続関係だけを確認したいときは、このディレクトリではなく `src/main.py` を読むべきです。
- すでに読むべき個別モジュールが `init.py`、`indexing.py`、`apply/`、`review/`、`session/` のどれかに決まっているときは、この階層の目次は不要です。
- `cmoc apply`、`cmoc session`、`cmoc review` の正本仕様だけを確認したいときは、このディレクトリではなく `oracles/docs/app_specs/sub_commands/` 側を読むべきです。

## hash

- 92301bd3342e663208371fd3ab12ef03e6b48d9be24c7c035461cb5517de4e4b
