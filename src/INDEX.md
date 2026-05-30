# `commons`

## Summary

- `src/commons` は、cmoc 全体で共有する基盤処理を集めたディレクトリの入口です。
- `__init__.py`、`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` へのルーティングをまとめます。
- 個別モジュールへ進む前に、共通実行制御、Git リポジトリ判定、ログ、計時、タイムスタンプ、レポート保存、`INDEX.md` 維持の責務分担を把握するための目次です。

## Read this when

- `src/commons` 配下の共有ユーティリティ全体を俯瞰したいとき。
- Codex CLI 呼び出し、共通実行制御、共通エラー、Git リポジトリ判定、INDEX.md 維持、レポート保存、サブコマンドログ、タイムスタンプ、計時の入口をまとめて確認したいとき。
- どの共通モジュールを読むべきかを素早く振り分けたいとき。
- 共有処理の責務分担を把握してから個別モジュールに進みたいとき。

## Do not read this when

- 個別モジュールの実装詳細だけを確認したいときは、この目次ではなく `__init__.py`、`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` を直接読むべきです。
- `cmoc` のサブコマンド本体や CLI 引数の詳細だけを追いたいときは、この共通基盤の入口は優先度が低いです。
- `INDEX.md` の生成・維持ルールだけを確認したいときは、この入口ではなく `indexing.py` を読むべきです。
- `oracles` 側の仕様断片や `src/sub_commands` 側の実装だけを確認したいときは、このディレクトリではなく該当領域を読むべきです。

## hash

- 0f11418c658502b88f8940ea38e85539125e6369d77304ccc9baf220862964d2
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

- `src/sub_commands` は `cmoc` の個別サブコマンド実装への入口です。
- `apply/` と `session/` の各パッケージ、`init.py`、`eval_oracles.py`、`__init__.py` へのルーティングをまとめます。
- どのモジュールがどのコマンドを担当するかを素早く振り分けるための目次です。

## Read this when

- `src/sub_commands` 配下で、どのモジュールがどのサブコマンドを担当しているか整理したいとき。
- `apply/`、`session/`、`init.py`、`eval_oracles.py`、`__init__.py` の役割と配置を一覧したいとき。
- `cmoc apply`、`cmoc session`、`cmoc init`、`cmoc review oracles` の実装入口を素早くたどりたいとき。
- サブコマンド本体の詳細仕様へ進む前に、まず入口を把握したいとき。

## Do not read this when

- 個別の `cmoc apply fork/join/abandon` や `cmoc session fork/join/abandon` の詳細仕様、状態遷移、例外条件だけを確認したいとき。
- `cmoc review oracles` の評価条件、Structured Output の検証、レポート保存などの詳細だけを追いたいとき。
- `cmoc init` の `.cmoc` 追跡解除や `cmoc` 全体の起動経路だけを確認したいとき。
- 共通処理や `oracles` 側の正本仕様だけを確認したいときは、この配下ではなく該当領域を読むべきです。

## hash

- 3c24b2def2ffd864018bced6f2492a317f6955098b85ebf61677af7e64f9310c
<!-- cmoc-index-kind: directory -->
