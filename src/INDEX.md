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
