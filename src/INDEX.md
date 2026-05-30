# `commons`

## Summary

- `src/commons` は cmoc 全体で共有する基盤処理の入口です。
- `command_runner.py`、`codex.py`、`repo.py`、`errors.py`、`indexing.py`、`report_files.py`、`subcommand_log.py`、`timing.py`、`timestamps.py`、`__init__.py` への導線をまとめます。
- 実行制御、Codex CLI 呼び出し、git リポジトリ検出、`INDEX.md` 生成・維持、レポート保存、サブコマンドログ、計時、タイムスタンプ生成の役割分担を整理するための目次です。

## Read this when

- 共通の実行制御、エラー整形、リポジトリ検出、ログ保存、計時の入口をまとめて把握したいとき。
- `codex exec` の呼び出し方、Structured Output の扱い、出力検証を確認したいとき。
- `INDEX.md` の生成・更新・再利用判定や、どの共通モジュールを読むべきかを振り分けたいとき。
- `src/commons` が Python パッケージとしてどう責務分割されているか確認したいとき。

## Do not read this when

- 個別サブコマンドの引数や業務ロジックだけを確認したいとき。
- `src/sub_commands` 側の実装や CLI のサブコマンド構成だけを追いたいとき。
- `INDEX.md` の生成ルールそのものや、`oracles` 側の仕様断片だけを確認したいとき。
- `src/commons` 以外の日時ユーティリティ、ログ表示、レポート保存だけを探したいとき。

## hash

- 4f9681f625184a1b9499863ab38ca820d39f82c5017e276fa64f5f559639502a
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

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc の個別サブコマンド仕様への入口で、`apply`、`session`、`review oracles`、`init` の各正本仕様へ案内します。
- `apply_abandon.md`、`apply_fork.md`、`apply_join.md`、`session_abandon.md`、`session_fork.md`、`session_join.md`、`review_oracles.md`、`init.md` に分かれた手順・前提条件・状態遷移・終了条件をまとめます。
- この目次は、サブコマンドごとの目的や読むべき詳細仕様を素早く選べるようにするための入口です。

## Read this when

- cmoc の個別サブコマンドの入口をまとめて確認したいとき。
- `apply`、`session`、`review oracles`、`init` のどの仕様断片へ進むべきか整理したいとき。
- サブコマンドごとの目的、入力条件、実行手順、状態遷移、終了条件を俯瞰したいとき。

## Do not read this when

- 個別のサブコマンド仕様だけを確認したいときは、この目次ではなく該当する `apply_*`、`session_*`、`review_oracles.md`、`init.md` を直接読むべきです。
- 実装コードやテストコードの作業だけで足りるときは、この目次を読む必要はありません。
- `branch_model`、`codex_call`、ログ、エラーハンドリング、`oracles` 全体の扱いなど、他の共通仕様を確認したいときは別の入口文書を読むべきです。

## hash

- 0c07dd24e14b12d607ca1b2fbf332a5d640627679b59e67559e13db9e2a98f6e
<!-- cmoc-index-kind: directory -->
