# `commons`

## Summary

- src/commons は cmoc 全体で共有する基盤処理をまとめた入口です。
- `command_runner.py`、`codex.py`、`repo.py`、`errors.py`、`indexing.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py`、`__init__.py` への導線を整理します。
- 共通実行制御、Codex CLI 呼び出し、エラー整形、Git リポジトリ判定、`INDEX.md` 維持、レポート保存、サブコマンドログ、計時、タイムスタンプ生成の責務分担を把握するための目次です。

## Read this when

- src/commons 配下の共有ユーティリティ全体を俯瞰したいとき。
- 共通実行制御、Codex CLI 呼び出し、エラー整形、Git リポジトリ判定、`INDEX.md` 維持、レポート保存、サブコマンドログ、タイムスタンプ、計時の入口をまとめて確認したいとき。
- どの共通モジュールを読むべきかを素早く振り分けたいとき。
- 共有処理の責務分担を先に整理してから個別モジュールへ進みたいとき。

## Do not read this when

- 個別モジュールの実装詳細だけを確認したいときは、この入口ではなく `src/commons` 配下の該当ファイルを直接読むべきです。
- サブコマンド本体や CLI 引数の詳細だけを追いたいときは、この共通基盤ではなく `src/sub_commands` 側を読むべきです。
- `INDEX.md` の生成・維持ルールだけを確認したいときは、この入口ではなく `indexing.py` を読むべきです。
- `oracles` 側の仕様断片やテスト観点だけを確認したいときは、この目次ではなく該当する仕様文書やテストを読むべきです。

## hash

- 3966b01882772166726f4d5175d3892424225a3acbce04ad8b2142967b7794ac
<!-- cmoc-index-kind: directory -->

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

- d03b4e0b3d0c12971884d8bc1e159f95c3f0efe50e8fca99dc96066066992456
<!-- cmoc-index-kind: file -->

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc のサブコマンド実装をまとめた入口です。
- 直下には `__init__.py`、`init.py`、`eval_oracles.py`、および `apply` / `session` の各パッケージがあり、CLI の主要な実行処理を分担しています。
- この `INDEX.md` は、各サブコマンドの実装や下位パッケージへ進むための案内役です。

## Read this when

- `src/sub_commands` 配下のサブコマンド実装全体の配置を把握したいとき。
- `init`、`review oracles`、`apply`、`session` のどこを読むべきかを判断したいとき。
- 新しいサブコマンド追加や既存入口の整理の前に、構成を確認したいとき。
- `src/sub_commands` が Python パッケージとして成立していることと、主要な実装入口がどこにあるかを素早く確認したいとき。

## Do not read this when

- 個別コマンドの引数、状態遷移、例外条件だけを確認したいときは、この目次ではなく各モジュールの仕様や実装を直接読むべきです。
- `cmoc apply` や `cmoc session` の詳細な実行フローだけを追いたいときは、このディレクトリ全体の目次ではなく `apply` / `session` 側を読むべきです。
- `oracles` 側の正本仕様や `INDEX.md` の生成ルールだけを確認したいときは、この目次ではなく該当する仕様文書を読むべきです。
- `src.sub_commands` のパッケージ宣言だけを確認したいときは、この目次を読む必要はありません。

## hash

- 462d1085dd7e8aee54053dda0d31c76d24015d6c81db7a3e253a8720724bb304
<!-- cmoc-index-kind: directory -->
