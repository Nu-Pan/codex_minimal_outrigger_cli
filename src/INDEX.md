# `commons`

## Summary

- この `src/commons` ディレクトリのルーティング文書で、cmoc 全体で共有する基盤モジュールへの入口です。
- `__init__.py`、`codex.py`、`command_runner.py`、`errors.py`、`repo.py`、`subcommand_log.py`、`timing.py`、`timestamps.py`、`report_files.py`、`indexing.py` を、用途ごとにたどるための目次です。
- CLI 起動、共通エラー整形、リポジトリ操作、サブコマンドログ、時間計測、レポート保存、`INDEX.md` 維持のどこを読むべきかを切り分けます。

## Read this when

- cmoc の共通処理の入口を探していて、どの基盤モジュールを読むべきか整理したいとき。
- Codex 実行制御、サブコマンド実行ラッパー、エラー表示、git / worktree 操作、ログ保存、時間計測、タイムスタンプ生成、レポート保存、`INDEX.md` 維持のいずれかを追いたいとき。
- 個別サブコマンドの前に、`src/commons` の責務分担と依存関係を把握したいとき。
- 実装やテストで、共通モジュール同士の役割分担を確認したいとき。

## Do not read this when

- 個別モジュールの実装詳細だけを確認したいときは、このディレクトリではなく該当する `*.py` を直接読むべきです。
- `src/sub_commands` 側の引数解析や業務ロジックだけを追いたいときは、この目次ではなくサブコマンド側の文書を読むべきです。
- `oracles` の正本仕様だけを確認したいときや、`README.md`・`AGENTS.md` などの運用ルールだけを確認したいときは、このディレクトリを読む必要はありません。

## hash

- bbb87d1ac16d8bd68899318b9fd93b2385d1ff0c8fc409131dd18adc07b5bae1

# `main.py`

## Summary

- `src/main.py` は cmoc CLI のエントリーポイントで、Typer のルート `app` と `session` / `apply` / `review` の各サブアプリを組み立てるファイルです。
- `init`、`session`、`apply`、`review` の各コマンド登録に加えて、`eval-oracle` / `eval-oracles` の隠し別名や各コマンドの既定オプションをまとめています。
- サブコマンド未指定時の `CmocError` 生成、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc CLI の起点として、`session` / `apply` / `review` のサブアプリ構成を確認したいとき。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録名や隠し別名を確認したいとき。
- `apply fork` の既定反復回数や `scope`、`apply join` の `--force-resolve` などの既定オプションを確認したいとき。
- サブコマンド未指定時の利用者向けエラー、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の経路を確認したいとき。

## Do not read this when

- `src/sub_commands/` 配下の個別サブコマンド本体だけを確認したいとき。
- `commons.errors` や `format_error_report()` の例外整形だけを確認したいとき。
- `oracles` 側の正本仕様や `INDEX.md` 生成ルールだけを確認したいとき。
- `bin/cmoc` のシェル起動ラッパーだけを確認したいとき。

## hash

- 8e5c543120f5d8c879497bffa31a440854f689cb349abab0deb3f8a0cf8bf19e

# `sub_commands`

## Summary

- この `src/sub_commands` ディレクトリのルーティング文書で、`__init__.py`、`indexing.py`、`init.py`、`apply/`、`review/`、`session/` への入口をまとめています。
- `__init__.py` はパッケージ宣言、`indexing.py` は INDEX.md 維持処理、`init.py` は初期化処理、`apply/`・`review/`・`session/` は各サブコマンド群の入口です。
- 個別実装へ入る前に、`cmoc` のサブコマンド実装をどの系統から読むかを切り分けるための目次です。

## Read this when

- `src/sub_commands` 配下の全体構造を把握して、次に開くべきファイルやディレクトリを選びたいとき。
- `cmoc` の `init`、`indexing`、`session`、`apply`、`review` の入口構造と役割分担を整理したいとき。
- サブコマンド実装の修正・レビュー・テストの前に、対象モジュールを絞り込みたいとき。
- `src/sub_commands` が Python パッケージとして成立していることを確認したいとき。

## Do not read this when

- すでに開くべき個別モジュールが決まっていて、この階層の目次を経由する必要がないとき。
- `cmoc` の利用手順や正本仕様だけを確認したいときで、実装の入口整理が不要なとき。
- `apply/`、`review/`、`session/` など下位ディレクトリの個別 `INDEX.md` を直接読みたいとき。

## hash

- dbfde66384f701f483024f4618a7918c67cb9121e147ef2a1ecb96dc9fe909d2
