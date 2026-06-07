# `commons`

## Summary

- `src/commons` は、cmoc 全体で再利用する共通基盤モジュールをまとめたパッケージです。
- `codex.py`、`repo.py`、`errors.py`、`indexing.py`、`subcommand_log.py`、`timing.py`、`timestamps.py`、`report_files.py`、`command_runner.py` など、CLI 実行やログ、エラー、リポジトリ操作、`INDEX.md` 維持に関わる処理が入っています。
- サブコマンド固有の処理ではなく、複数の機能から横断的に使う共通処理の入口として使います。

## Read this when

- `cmoc` 全体で共有する基盤モジュールの役割分担を把握したいとき。
- `codex` 呼び出し、repo 操作、エラー整形、ログ、時間計測、タイムスタンプ、レポート保存、共通コマンド実行のどれを読むべきか迷ったとき。
- `src/commons` 配下の各モジュールへ進む前に、このディレクトリ全体の入口を整理したいとき。

## Do not read this when

- 個別サブコマンドの引数解析や業務ロジックだけを確認したいとき。
- `src/main.py` や `src/sub_commands/` など、CLI の入口や各コマンド本体を直接追いたいとき。
- `INDEX.md` の生成ルールそのものや `oracles` 側の正本仕様だけを確認したいとき。

## hash

- 37c70754ad4c088b5516a594242afbefdb20778b999243daf90ac93ba5e72d7b

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

- `src/sub_commands` は `cmoc` の各サブコマンド実装をまとめるルーティング用パッケージです。
- `__init__.py`、`init.py`、`indexing.py` に加えて、`apply`・`review`・`session` の各パッケージへの入口を含みます。
- 個別実装に入る前の案内として、どのモジュールを読むべきかを整理する目次の役割を持ちます。

## Read this when

- `src/sub_commands` 配下の入口構造をまとめて把握したいとき。
- `cmoc init` と `cmoc indexing` の実装入口、ならびに `apply`・`review`・`session` の各パッケージのどこへ進むべきか整理したいとき。
- サブコマンドの追加、整理、再配置に伴って、この階層の目次を確認したいとき。
- 個別実装に入る前に、どのモジュールを読むべきかを切り分けたいとき。

## Do not read this when

- すでに読む対象が `cmoc init`、`cmoc indexing`、`cmoc apply`、`cmoc review`、`cmoc session` のいずれかに決まっていて、この階層の案内が不要なとき。
- 個別サブコマンドの引数仕様や処理本体だけを直接確認したいとき。
- `oracles` 側の正本仕様や利用手順だけを確認したいとき。

## hash

- 0feb9f6aec6689ed8d9d603d415e09262c6027834948e52a4c09d2662bd2e6d3
