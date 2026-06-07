# `commons`

## Summary

- この `src/commons` ディレクトリのルーティング文書で、cmoc 全体で共有する基盤モジュールへの入口です。
- `codex.py`、`command_runner.py`、`errors.py`、`repo.py`、`subcommand_log.py`、`timing.py`、`timestamps.py`、`report_files.py`、`indexing.py` を、用途ごとにたどるための目次です。
- CLI 起動、エラー整形、リポジトリ操作、ログ保存、時間計測、`INDEX.md` 維持のどこを読むべきかを切り分けます。

## Read this when

- cmoc の共通処理の入口を探していて、どのモジュールを読むべきか整理したいとき。
- Codex 実行制御、サブコマンド実行ラッパー、エラー表示、repo 判定、ログ、時間計測、レポート保存、`INDEX.md` 維持のいずれかを追いたいとき。
- 個別サブコマンドの前に、共有基盤の責務分担を把握したいとき。
- 実装やテストで、共通モジュール同士の依存関係を確認したいとき。

## Do not read this when

- 個別サブコマンドの引数解析や業務ロジックだけを確認したいときは、`src/sub_commands` 側を読むべきです。
- この階層ではなく、特定モジュールの詳細実装だけを確認したいときは、該当する `*.py` を直接読むべきです。
- `oracles` の正本仕様だけを確認したいときは、この階層ではなく `oracles` 側の文書を読むべきです。
- `README.md` や `AGENTS.md` など、リポジトリ運用ルールだけを確認したいときは、この目次ではなく該当文書を参照するべきです。

## hash

- 55ca5d64c5669a4aeed0145a2818ff70696bfd169de3bca1ff33d5b61af90981

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

- 9280406a283e336539f66984c0562dc6293de863c243121df1eb1f33874ee15e

# `sub_commands`

## Summary

- `src/sub_commands` のルーティング文書で、配下の入口モジュールと各サブコマンド系ディレクトリへ案内するための目次です。
- `__init__.py` はパッケージ宣言のみ、`indexing.py` は `cmoc indexing`、`init.py` は `cmoc init` の実装入口です。
- `apply/`、`session/`、`review/` はそれぞれ `cmoc apply`、`cmoc session`、`cmoc review` 系の入口ディレクトリです。

## Read this when

- `src/sub_commands` ディレクトリ全体の入口構造と、どのモジュールへ進むべきかを整理したいとき。
- `cmoc init`、`cmoc indexing`、`cmoc apply`、`cmoc session`、`cmoc review` の実装・修正・レビュー・テストに入る前に、参照先を切り分けたいとき。
- `src/sub_commands` 配下のパッケージ宣言、共通処理、各サブコマンド系ディレクトリの役割分担を把握したいとき。
- 個別モジュールに入る前のルーティング文書として、まず全体の目次を確認したいとき。

## Do not read this when

- `src/sub_commands/__init__.py` だけを確認したいとき。
- `cmoc init`、`cmoc indexing`、`cmoc apply`、`cmoc session`、`cmoc review` のうち、すでに対象モジュールが分かっていて直接そちらへ進むとき。
- `apply/`、`session/`、`review/` の個別実装や、さらに下位のモジュールだけを追いたいとき。
- `src/sub_commands` の入口構造ではなく、`oracles` 側の正本仕様や別階層の文書だけを確認したいとき。

## hash

- ff10d734c6532b18493da4dc023b8620e34f6e95a324c1a21ff26f3ba64f9fdd
