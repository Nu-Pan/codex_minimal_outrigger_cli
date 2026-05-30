# `commons`

## Summary

- `cmoc` の各サブコマンドから共通利用される基盤処理をまとめたディレクトリです。
- 実行ラッパー、Codex 呼び出し、Git リポジトリ操作、共通エラー、サブコマンドログ、時間計測、タイムスタンプ生成、レポート保存、`INDEX.md` 目次維持が入っています。
- サブコマンド実装の土台と、目次文書の自動維持を支える共通モジュール群の入口です。

## Read this when

- cmoc 全体で共有する実行制御、エラー整形、Git 操作、ログ記録の役割分担を把握したいとき。
- `codex exec` 呼び出し、`INDEX.md` 生成・維持、レポート保存、タイムスタンプ生成の共通処理を確認したいとき。
- サブコマンド本体の土台になるユーティリティ群の入口をまとめて見たいとき。

## Do not read this when

- 個別サブコマンドの引数解析や業務ロジックだけを確認したいとき。
- `src/sub_commands` 側の実装や各コマンドの実行フローだけを追いたいとき。
- `oracles` 配下の正本仕様や運用手順だけを確認したいとき。

## hash

- 33bc260786179e7413a3a0a6518523077f7f56ddc853bae1c0abc66fda74af27
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

- `cmoc` のサブコマンド実装をまとめるパッケージで、`__init__.py`、`init.py`、`eval_oracles.py` と `apply/`、`session/` の入口を持ちます。
- `cmoc init`、`cmoc review oracles`、`cmoc apply`、`cmoc session` の各実装を辿るときのルーティング起点です。
- 個別サブコマンドの実処理は各モジュール配下に分かれており、このディレクトリ自体は全体の入口として機能します。

## Read this when

- `cmoc` のサブコマンド実装全体の配置と役割分担を把握したいとき。
- `init`、`review oracles`、`apply`、`session` のどの実装ファイルへ進むべきか整理したいとき。
- 新しいサブコマンドを追加したり、既存サブコマンドの入口を確認したいとき。

## Do not read this when

- `commons` 配下の共通処理や Git・報告・計測の詳細だけを確認したいとき。
- `oracles` 配下の仕様断片そのものや、`INDEX.md` の生成ルールだけを確認したいとき。
- 対象モジュールが既に分かっていて、`init.py`、`eval_oracles.py`、`apply/`、`session/` の個別実装を直接読みたいとき。

## hash

- a04b55252d05e3b5d2dc808f226a956b1433be6da50c41a313ffd85c618382fb
<!-- cmoc-index-kind: directory -->
