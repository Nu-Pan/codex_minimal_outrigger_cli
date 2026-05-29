# `commons`

## Summary

- cmoc 全体で再利用する共通ユーティリティ群をまとめたディレクトリです。
- `codex.py` は Codex CLI 呼び出しの共通処理、`command_runner.py` はサブコマンド実行ラッパーを扱います。
- `errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` は、それぞれ共通例外、INDEX.md 生成、git/セッション状態、レポート保存、ログ記録、タイムスタンプ生成、時間計測を担当します。
- `__init__.py` は `src.commons` パッケージを定義するだけの最小モジュールです。

## Read this when

- cmoc の共通処理をどのモジュールに置くか判断したいとき。
- Codex CLI 呼び出し、リポジトリ探索、共通例外、ログ、タイムスタンプ、経過時間計測、レポート保存の実装を確認したいとき。
- 新しいサブコマンドや共通ユーティリティを追加するときに、既存の共通部品の役割分担を把握したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや引数定義だけを確認したいとき。
- `src/commons` 全体ではなく、`errors.py` や `repo.py` など特定の共通モジュールだけを追いたいとき。
- `src/commons` の実装変更ではなく、テストや他ディレクトリの仕様だけを確認したいとき。

## hash

- 38e6f8f3c72c63d08f8603249c7df21733024f939672ddce3643a485c0cc2974

# `main.py`

## Summary

- cmoc CLI のエントリーポイントで、Typer のルート app と `session` / `apply` / `review` のサブアプリを組み立てます。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録と、それぞれのオプション既定値やエイリアスをまとめます。
- サブコマンド未指定時の利用者向けエラー、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc の起動点やサブコマンド登録を修正・レビューしたいとき。
- `init` / `session` / `apply` / `review` のコマンド名、エイリアス、オプション既定値を確認したいとき。
- サブコマンドなし起動時の利用者向けエラー、終了コード、`--help` への誘導を確認したいとき。
- `python src/main.py` で直接起動する経路と、その例外ハンドリングを確認したいとき。

## Do not read this when

- 各サブコマンドの本体ロジックや `src/sub_commands/` 配下の処理だけを確認したいとき。
- 共通エラー型や `format_error_report` の整形仕様だけを確認したいとき。
- `INDEX.md` の生成ルールや共通ユーティリティの設計だけを追いたいとき。

## hash

- 725244cd04649c14efdc472340862818b2eabfb76416af919258408edf3121cc

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc のサブコマンド実装の入口で、`__init__.py`、`init.py`、`eval_oracles.py`、`apply/`、`session/` を含みます。
- `init.py` は `cmoc init`、`eval_oracles.py` は `cmoc review oracles` を担当します。
- `apply/` と `session/` は、それぞれ apply 系・session 系サブパッケージです。

## Read this when

- `src/sub_commands` 配下にどのサブコマンド実装が置かれているかを俯瞰したいとき。
- `cmoc init`、`cmoc review oracles`、`cmoc apply`、`cmoc session` の入口を素早く見分けたいとき。
- このディレクトリが Python パッケージとして宣言され、個別コマンド実装とサブパッケージに分かれていることを確認したいとき。

## Do not read this when

- 個別サブコマンドの詳細仕様だけを確認したいときは、各モジュールを直接読むべきです。
- `cmoc apply` や `cmoc session` 配下の詳細だけを確認したいときは、それぞれの子ディレクトリの `INDEX.md` を読むべきです。
- `src/sub_commands` のパッケージ宣言だけを確認したいときは、`__init__.py` を直接見れば足ります。

## hash

- eb599cb48d326c6a3a9d236be3cd568a9d42c56614e3f8bcb80b57a8aa3c8b21
