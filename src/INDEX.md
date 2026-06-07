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

- 6534c818d649a5bf27c91568e5d0f98ec2a3ca42c83e255968a94e7742459b54

# `sub_commands`

## Summary

- `src/sub_commands` ディレクトリのルーティング文書で、`apply/`、`session/`、`review/`、`init.py`、`__init__.py` へ案内する入口です。
- `cmoc` の各サブコマンド実装のどこへ進むべきかを切り分けるための目次です。
- この階層では、実装本体よりも入口構造と参照先の案内を優先します。

## Read this when

- `src/sub_commands` 配下の入口構造と、どのサブコマンド実装へ進むべきかを整理したいとき。
- `cmoc apply`、`cmoc session`、`cmoc review`、`cmoc init` の責務分担をまとめて把握したいとき。
- `src/sub_commands/__init__.py` のパッケージ宣言と、各サブディレクトリ・モジュールの役割を確認したいとき。
- この階層のルーティング文書として、次に読むべき下位ファイルを切り分けたいとき。

## Do not read this when

- すでに目的のサブコマンド実装が分かっていて、`apply/`、`session/`、`review/`、`init.py` の該当ファイルへ直接進めるとき。
- `src/sub_commands` ではなく、個別モジュールの実装やテストだけを確認したいとき。
- `oracles` 側の正本仕様や、リポジトリ全体の運用ルールだけを確認したいとき。

## hash

- 1b3600f86b236e6ddae1e7a0f6394fab267d8b1901a6f11a34f4f5ab087b56b6
