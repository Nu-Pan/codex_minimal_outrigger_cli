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

- `src/sub_commands` は cmoc のサブコマンド実装をまとめたパッケージの入口です。
- 配下には `cmoc init` と `cmoc review oracles` の実装モジュール、および `cmoc apply` / `cmoc session` 系のサブパッケージが入っています。
- このディレクトリの `INDEX.md` は、各サブコマンドの実装へ進むための目次として使います。

## Read this when

- cmoc のサブコマンド実装全体の配置を把握したいとき。
- `cmoc init` や `cmoc review oracles`、`cmoc apply`、`cmoc session` のどれを読むべきか判断したいとき。
- 新しいサブコマンド追加や、既存サブコマンドの入口整理を行う前に構成を確認したいとき。

## Do not read this when

- 特定のサブコマンドの詳細仕様や状態遷移だけを確認したいときは、このディレクトリではなく該当モジュールやその下位の `INDEX.md` を読むべきです。
- CLI の利用手順や人間向けの開発フローだけを確認したいときは、`oracles/app_specs/` 側を読むべきです。
- Python パッケージ宣言だけを確認したいときは、`src/sub_commands/__init__.py` を直接見れば足ります。

## hash

- 8839c1fe561f32882aab762e5ed3c9b48c86218e6791c6d0f9af161d196751e1
<!-- cmoc-index-kind: directory -->
