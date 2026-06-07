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

- `src/sub_commands` は cmoc のサブコマンド実装を束ねる入口ディレクトリです。
- `__init__.py` は `src.sub_commands` パッケージを宣言するだけの最小モジュールです。
- `init.py` は `cmoc init` の本体処理を担います。
- `apply`、`review`、`session` はそれぞれ `cmoc apply` / `cmoc review` / `cmoc session` 系の入口ディレクトリで、配下の個別実装をまとめます。

## Read this when

- `src/sub_commands` 配下でどの実装を開くべきか整理したいとき。
- `cmoc init` / `apply` / `review` / `session` の責務分担と入口構造を確認したいとき。
- `cmoc` の CLI サブコマンド実装の導線をたどりたいとき。

## Do not read this when

- 個別モジュールの実装詳細や状態遷移だけを確認したいとき。
- `cmoc` の利用手順や正本仕様だけを確認したいとき。
- `src/main.py` の CLI 登録だけを追いたいとき。

## hash

- 20af897d05758a65d383d7812c03f7146157bde32ab53da60c0afa96b40b7a4d
