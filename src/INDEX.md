# `commons`

## Summary

- `src/commons` は、cmoc 全体で共有する基盤モジュールをまとめたパッケージです。
- `codex.py`、`repo.py`、`errors.py`、`indexing.py`、`subcommand_log.py`、`timing.py`、`timestamps.py`、`report_files.py`、`command_runner.py` など、CLI 実行・ログ・エラー・リポジトリ操作・`INDEX.md` 維持に必要な共通処理が入っています。
- サブコマンド固有の処理ではなく、複数機能から再利用される横断的な処理を読む入口として使います。

## Read this when

- `codex exec` の共通呼び出し、Structured Output 検証、oracle 保護、`INDEX.md` 維持の流れを確認したいとき。
- repo root 探索、`.cmoc` 配下の状態管理、git 共通処理、変更検出を確認したいとき。
- サブコマンド実行の共通制御、エラー整形、JSONL ログ、時間計測、タイムスタンプ生成などの共通基盤を探したいとき。

## Do not read this when

- 個別サブコマンドの引数解析や業務ロジックだけを確認したいとき。
- `INDEX.md` の生成ルールそのものや、`oracles` 側の正本仕様だけを確認したいとき。
- `src/commons` ではなく、CLI の各コマンド実装やテストを直接追いたいとき。

## hash

- d7632a466fc918dfa350c7b8034af05858721e91210bf92020ddcd6565e4c650

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

- a756de7b8e379a66e5e1bdfc4aa80c43d910a513c480de908c6d46a9f1196f81

# `sub_commands`

## Summary

- `src/sub_commands` ディレクトリ全体のルーティング文書で、`cmoc` のサブコマンド実装へ案内する入口です。
- この階層では、`__init__.py` のパッケージ宣言、`init.py` の `cmoc init`、`indexing.py` の `cmoc indexing` を起点に、`apply/`、`session/`、`review/` の各系統へ分岐します。
- 個別の実装や仕様に進む前に、どの下位ディレクトリを読むべきかを切り分けるための目次です。

## Read this when

- `src/sub_commands` 配下の入口構造をまとめて把握し、どのモジュールや下位ディレクトリへ進むべきか整理したいとき。
- `src/sub_commands/__init__.py`、`init.py`、`indexing.py` の役割分担を確認したいとき。
- `apply`、`session`、`review` の各サブコマンド群へ分岐する前に、この階層のルーティングだけを押さえたいとき。
- `cmoc init` と `cmoc indexing` の実装入口、および各サブコマンド系ディレクトリの案内を一括で見たいとき。

## Do not read this when

- `src/sub_commands` 配下の入口構造ではなく、すでに対象の個別モジュールやサブコマンドが決まっているとき。
- `cmoc init` や `cmoc indexing` などの本体実装を直接読みたいときは、この目次ではなく各 `.py` を読むべきとき。
- `cmoc apply` / `cmoc session` / `cmoc review` の個別仕様だけを確認したいときは、この階層ではなく各下位ディレクトリの `INDEX.md` や `oracles` 側を読むべきとき。
- CLI 登録や起動点だけを確認したいときは、この目次ではなく `src/main.py` を読むべきとき。

## hash

- 695744e4fa1b38cc2a709486dcc5e98b9aa4ebf087484a444080279e25047734
