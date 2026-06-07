# `commons`

## Summary

- この `src/commons` ディレクトリのルーティング文書で、cmoc 全体で共有する基盤モジュールへの入口です。
- `codex.py`、`command_runner.py`、`errors.py`、`repo.py`、`subcommand_log.py`、`timing.py`、`timestamps.py`、`report_files.py`、`indexing.py` を、用途ごとにたどるための目次です。
- CLI 起動、共通エラー整形、リポジトリ操作、ログ保存、時間計測、レポート保存、`INDEX.md` 維持のどこを読むべきかを切り分けます。

## Read this when

- cmoc の共通処理の入口を探していて、どのモジュールを読むべきか整理したいとき。
- Codex 実行制御、サブコマンド実行ラッパー、エラー表示、repo 判定、ログ、時間計測、レポート保存、`INDEX.md` 維持のいずれかを追いたいとき。
- 個別サブコマンドの前に、共有基盤の責務分担を把握したいとき。
- 実装やテストで、共通モジュール同士の依存関係を確認したいとき。

## Do not read this when

- 個別モジュールの実装詳細だけを確認したいときは、このディレクトリではなく該当する `*.py` を直接読むべきとき。
- `src/sub_commands` 側の引数解析や業務ロジックだけを追いたいとき。
- `oracles` の正本仕様だけを確認したいとき。
- `README.md` や `AGENTS.md` など、リポジトリ運用ルールだけを確認したいとき。

## hash

- 59104107970b9b9547c1d104dba8cf5e0a769149fea8fbabad0b851a0b4531da

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

- `src/sub_commands` ディレクトリのルーティング文書で、配下の入口モジュールと各サブコマンド系ディレクトリへ案内するための目次です。
- `__init__.py` はパッケージ宣言のみ、`indexing.py` は `cmoc indexing`、`init.py` は `cmoc init` の実装入口です。
- `apply/`、`session/`、`review/` はそれぞれ `cmoc apply`、`cmoc session`、`cmoc review` 系の入口ディレクトリです。
- `src/sub_commands` 全体を読む前に、どのモジュールへ進むべきかを用途別に切り分けるための入口です。

## Read this when

- `src/sub_commands` 配下の全体構造と、どの入口モジュールへ進むべきかを整理したいとき。
- `cmoc init`、`cmoc indexing`、`cmoc apply`、`cmoc session`、`cmoc review` の実装・修正・レビュー・テストに入る前に、参照先を切り分けたいとき。
- `__init__.py`、`indexing.py`、`init.py`、`apply/`、`session/`、`review/` の役割分担を把握したいとき。

## Do not read this when

- `src/sub_commands` の入口構造は把握済みで、`init.py` や `indexing.py`、各系統ディレクトリへ直接進むとき。
- `apply/`、`session/`、`review/` の個別実装だけを確認したいとき。
- `oracles/` 側の正本仕様やリポジトリ運用ルールだけを確認したいとき。

## hash

- 5a93b5f4ed194d5fbdc02783e52d86a74cdc56bb4ce2c620a3bc2589f5b2d77d
