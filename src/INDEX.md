# `commons`

## Summary

- `src/commons` は cmoc 全体で共有する基盤処理をまとめた入口です。
- `__init__.py`、`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` への導線を整理します。
- 共通実行制御、エラー整形、Git リポジトリ判定、`INDEX.md` 維持、レポート保存、ログ、計時、タイムスタンプ生成の責務分担を把握するための目次です。

## Read this when

- `src/commons` 配下の共有ユーティリティ全体を俯瞰したいとき。
- 共通実行制御、Codex CLI 呼び出し、共通エラー、Git リポジトリ判定、`INDEX.md` 維持、レポート保存、サブコマンドログ、タイムスタンプ、計時の入口をまとめて確認したいとき。
- どの共通モジュールを読むべきかを素早く振り分けたいとき。
- 共有処理の責務分担を先に整理してから個別モジュールへ進みたいとき。

## Do not read this when

- 個別モジュールの実装詳細だけを確認したいときは、この目次ではなく各モジュールを直接読むべきです。
- `cmoc` のサブコマンド本体や CLI 引数の詳細だけを追いたいときは、この共通基盤の入口は優先度が低いです。
- `INDEX.md` の生成・維持ルールだけを確認したいときは、この入口ではなく `indexing.py` を読むべきです。
- `oracles` 側の仕様断片や `src/sub_commands` 側の実装だけを確認したいときは、このディレクトリではなく該当領域を読むべきです。

## hash

- e394b72f933e6a9076c5ddc12661ddc63b63c34e5f0bb1ef0215952dc88412a4
<!-- cmoc-index-kind: directory -->

# `main.py`

## Summary

- cmoc CLI のエントリーポイントで、Typer のルート `app` と `session` / `apply` / `review` の各サブアプリを組み立てるファイルです。
- `init`、`session`、`apply`、`review` の各コマンド登録に加えて、`eval-oracle` / `eval-oracles` の隠し別名や、`apply fork` の繰り返し回数・`scope`、`apply join` の `--force-resolve` などの既定値をまとめています。
- サブコマンド未指定時の `CmocError` 生成、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc CLI の起動点と、`session` / `apply` / `review` のサブアプリ構成を確認したいとき。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録名、エイリアス、既定オプションを確認したいとき。
- サブコマンド未指定時の利用者向けエラー、補完プローブの扱い、Click/Typer 例外の共通整形を追いたいとき。
- `python src/main.py` で直接起動する経路と、そのときの例外処理を確認したいとき。

## Do not read this when

- `src/sub_commands/` 配下の各サブコマンド本体の処理だけを確認したいとき。
- 共通エラー型や `format_error_report()` の整形仕様だけを確認したいとき。
- `INDEX.md` の生成ルールや `oracles` 側のルーティング方針だけを確認したいとき。

## hash

- 7eb6c6be9a4576cdc697c9a82f65de46450efcff9825b8fc064595ec07baf889
<!-- cmoc-index-kind: file -->

# `sub_commands`

## Summary

- `src/sub_commands/INDEX.md` は `cmoc` のサブコマンド実装全体への入口です。
- `__init__.py`、`apply`、`session`、`init.py`、`eval_oracles.py` へ案内し、各サブコマンドの役割分担を整理します。
- `cmoc` のサブコマンド実装を読む起点として、個別仕様に進む前の全体像を示します。

## Read this when

- `src/sub_commands` 配下のどのファイルを先に読むべきか確認したいとき。
- `cmoc apply`、`cmoc session`、`cmoc init`、`cmoc review oracles` の入口を一覧で把握したいとき。
- サブコマンド実装のパッケージ構成と責務分担を整理したいとき。

## Do not read this when

- 個別サブコマンドの引数、状態遷移、例外条件などの詳細仕様だけを確認したいとき。
- `oracles` 側の正本仕様断片や `INDEX.md` 生成ルールだけを確認したいとき。
- `src/sub_commands` のパッケージ宣言だけで足り、実装入口の整理が不要なとき。

## hash

- 4913b5c24cb830ed83db2e5dc037bf803a09c9086d42efcdd691569074edcda3
<!-- cmoc-index-kind: directory -->
