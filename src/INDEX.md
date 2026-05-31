# `commons`

## Summary

- `src/commons` は cmoc の共通基盤をまとめるディレクトリで、CLI 実行制御、repo/worktree 操作、エラー整形、`INDEX.md` 生成、ログ、計測、タイムスタンプ、レポート保存を担います。
- `__init__.py` はパッケージ宣言のみで、実体は `codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` に分かれています。
- `codex.py` と `indexing.py` は共通処理の中核で、Codex CLI 呼び出しと `INDEX.md` の維持を扱います。
- `repo.py` は Git 状態や `session` / `apply` 管理、`errors.py` は共通エラー、`subcommand_log.py` / `timing.py` / `timestamps.py` / `report_files.py` は実行記録と時刻・レポート周辺を担当します。

## Read this when

- `src/commons` 全体の役割をまず把握したいとき。
- `codex.py`、`repo.py`、`indexing.py`、`errors.py` のどれに何があるか確認したいとき。
- CLI 実行制御、Git リポジトリ解析、`session` / `apply` 状態管理、ログ記録、時間計測、日時文字列生成の共通処理を探したいとき。
- 共通ユーティリティを新しく追加する前に、既存の責務分担を確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックだけを見たいときは、この目次ではなく `src/sub_commands` を読むべきです。
- 特定の関数やクラスの実装だけを追いたいときは、このディレクトリの目次ではなく該当モジュールを直接読むべきです。
- テスト仕様やユーザー向けワークフローだけを確認したいときは、この目次ではなく `tests` や `oracles` を参照すべきです。
- `__pycache__` のような生成物だけを確認したいときは、このディレクトリの対象外です。

## hash

- 15aaf4ea83494f154591cf9e25b0162eeef57feb2422b938c5259007c6a4db71

# `main.py`

## Summary

- cmoc CLI のエントリーポイントで、Typer のルート `app` と `session` / `apply` / `review` の各サブアプリを組み立てるファイルです。
- `init`、`session`、`apply`、`review` の各コマンド登録に加えて、`eval-oracle` / `eval-oracles` の隠し別名や、`apply fork` の繰り返し回数・`scope`、`apply join` の `--force-resolve` などの既定値をまとめています。
- サブコマンド未指定時の `CmocError` 生成、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc CLI の起動点と、`session` / `apply` / `review` のサブアプリ構成を確認したいとき。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録名、隠し別名、既定オプションを確認したいとき。
- サブコマンド未指定時の利用者向けエラー、補完プローブ時の分岐、Click/Typer 例外の共通整形を追いたいとき。
- `python src/main.py` で直接起動する経路と、そのときの例外処理を確認したいとき。

## Do not read this when

- `src/sub_commands/` 配下の各サブコマンド本体の実装だけを追いたいとき。
- `commons.errors` のエラー型や `format_error_report()` の整形ロジックだけを確認したいとき。
- `INDEX.md` の生成ルールや `oracles` 側のルーティング方針だけを確認したいとき。

## hash

- 34ab9fdae7d4622e261437958669dd52ce211f233a2300c1c7c831efc256c365

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc の各サブコマンド実装をまとめた Python パッケージのルートです。
- `apply`、`session`、`review` の各サブパッケージと、`cmoc init` 本体の `init.py`、パッケージ宣言の `__init__.py` を含みます。
- この配下から各サブコマンドの実装入口へ辿り、さらに下位の `INDEX.md` で個別実装へ進めます。

## Read this when

- cmoc のサブコマンド実装全体の配置や入口構成を確認したいとき。
- `cmoc init` の実装本体と、`apply` / `session` / `review` の各実装パッケージの関係を把握したいとき。
- どのサブコマンド実装ディレクトリへ進むべきかを判断したいとき。

## Do not read this when

- 特定のサブコマンドの手順や状態遷移だけを確認したいときは、対応する下位ディレクトリの `INDEX.md` や実装ファイルを直接読むべきです。
- `oracles` 配下の仕様断片や利用手順だけを確認したいときは、この実装ディレクトリではなく正本仕様を読むべきです。
- 共通の branch model、ログ、エラーハンドリングなどを確認したいときは、別の共通仕様へ進むべきです。

## hash

- a9212db7976d03742e8b1c1a2d27340388a325f255966f6fd16836a96b5772de
