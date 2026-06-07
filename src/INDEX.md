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

- `src/sub_commands` は `cmoc` の各サブコマンド実装をまとめるパッケージです。
- `init.py` と `indexing.py` に加えて、`apply`・`review`・`session` の各サブパッケージを含みます。
- 各サブコマンドの入口から実装本体へ案内するルーティング起点になります。

## Read this when

- `cmoc` のサブコマンド実装の全体構造を把握したいとき。
- `cmoc init`、`cmoc indexing`、`cmoc apply`、`cmoc review`、`cmoc session` のどこへ進むべきか判断したいとき。
- サブコマンド追加・整理・再配置に伴って、入口ディレクトリの目次を確認したいとき。

## Do not read this when

- 個別の `cmoc apply` / `cmoc review` / `cmoc session` の処理順や状態遷移だけを確認したいときは、このディレクトリではなく各サブパッケージの `INDEX.md` や実装ファイルを読むべきです。
- `oracles` 側の正本仕様や利用手順だけを確認したいときは、このディレクトリではなく `oracles/docs/app_specs/sub_commands/` を読むべきです。
- `cmoc` 全体のブランチモデルや repo 初期化の仕様だけを確認したいときは、ここではなく該当する専用モジュールを読むべきです。

## hash

- 15d0829d9a8ce21e33a438ef42ad2bdf40c39b7ac9e62183aaa923f7737e3657
