# `commons`

## Summary

- `src/commons` にある cmoc 共通モジュール群のルーティング入口です。
- `codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` などの基盤処理をまとめています。
- 個別サブコマンドの実装ではなく、複数機能から再利用される共通部品を案内するための目次です。

## Read this when

- `src/commons` 配下の共通基盤モジュールの入口を把握したいとき。
- repo 管理、コマンド実行ラッパー、共通エラー、INDEX.md 生成、ログ、時刻、時間計測の役割分担を確認したいとき。
- `src/commons/__init__.py` と各モジュールの位置関係を整理してから、個別ファイルへ進みたいとき。

## Do not read this when

- `src/commons` の目的のモジュールがすでに分かっていて、`codex.py` や `repo.py` などへ直接進めるとき。
- `src/commons` ではなく、個別サブコマンドの実装や `src/sub_commands/` 側だけを確認したいとき。
- `README.md` や `AGENTS.md` など、リポジトリ運用ルールだけを確認したいとき。

## hash

- 241d72d59800142f6b1de16b6e77fc5bf594139a1682589d563ef9a536a7bb54

# `main.py`

## Summary

- cmoc CLI のエントリーポイントで、Typer のルート `app` と `session` / `apply` / `review` の各サブアプリを組み立てるファイルです。
- `init` や各サブコマンドの登録に加えて、`eval-oracle` / `eval-oracles` の隠し別名や既定オプションをまとめています。
- サブコマンド未指定時の `CmocError` 生成、自動補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc CLI の起点として、`app` と `session` / `apply` / `review` のサブアプリ構成を確認したいとき。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録名や隠し別名を確認したいとき。
- サブコマンド未指定時のエラー処理、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の経路を追いたいとき。

## Do not read this when

- `src/sub_commands/` 配下の各サブコマンド本体の処理や引数解釈を確認したいとき。
- `commons.errors` の例外型や `format_error_report()` の整形ロジックだけを確認したいとき。
- CLI の登録や補完分岐ではなく、各機能の業務ロジックそのものを追いたいとき。

## hash

- 8fc9b7c2c0694a002ed3129ad239c90bfa7fba52cbed104640d431f03365aa70

# `sub_commands`

## Summary

- `src/sub_commands` パッケージ配下の実装入口をまとめたルーティング文書です。
- `__init__.py`、`init.py`、`apply/`、`review/`、`session/` へ進むための目次です。
- 各サブコマンドの実装ファイルを読む前に、どの系統へ分岐するかを整理します。

## Read this when

- `src/sub_commands` 配下のどのモジュールを開くべきか確認したいとき。
- `cmoc init` / `apply` / `review` / `session` の実装入口を俯瞰したいとき。
- サブコマンド実装やレビューの前に、パッケージ全体の配置を把握したいとき。

## Do not read this when

- 目的のファイルがすでに分かっていて、該当モジュールへ直接進むとき。
- 各サブコマンドの詳細仕様や実装フローだけを確認したいとき。
- この階層ではなく、上位の CLI 登録や `oracles` 側の仕様だけを見たいとき。

## hash

- 07a9c7b7e427032d494f337f8a31c9c22c57b4a9c1aa5fe891b83612308214d1
