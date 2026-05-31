# `commons`

## Summary

- `src/commons` は、cmoc 全体で共有する基盤処理をまとめたディレクトリです。
- ここには `codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` があり、Codex 呼び出し、リポジトリ操作、エラー整形、`INDEX.md` 管理、ログ保存、時間表示を担当します。
- 個別のサブコマンドよりも先に、共通処理の入口と責務分担を確認したいときに読むディレクトリです。

## Read this when

- cmoc の共通基盤として、このディレクトリに何がまとまっているかを把握したいとき。
- リポジトリ検出、session / apply 管理、共通例外、ログ、計測、タイムスタンプの入口を探したいとき。
- `INDEX.md` のメンテナンスや、`src/commons` 配下の各モジュールへどう案内するかを確認したいとき。

## Do not read this when

- `src/commons` 全体ではなく、個別モジュールの実装や挙動だけを追いたいとき。
- `codex exec` の起動制御や Structured Output の詳細だけを確認したいとき。
- `src/commons` 以外のサブコマンド本体、引数解釈、業務ロジックを追いたいとき。

## hash

- 0cf71011795da352f88ebd84b46e50ce96193c287c5e7782178eee33e2b6602c

# `main.py`

## Summary

- cmoc CLI のエントリーポイントで、Typer のルート `app` と `session` / `apply` / `review` の各サブアプリを組み立てるファイルです。
- `init`、`session`、`apply`、`review` の各コマンド登録に加えて、`eval-oracle` / `eval-oracles` の隠し別名や各コマンドの既定オプションをまとめています。
- サブコマンド未指定時の `CmocError` 生成、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc CLI の起点と、`session` / `apply` / `review` のサブアプリ構成を確認したいとき。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録名や隠し別名を確認したいとき。
- `apply fork` の繰り返し回数や `scope`、`apply join` の `--force-resolve` など既定オプションを確認したいとき。
- サブコマンド未指定時の利用者向けエラー、補完プローブ時の分岐、Click/Typer 例外の共通整形を追いたいとき。
- `python src/main.py` で直接起動する経路と、そのときの例外処理を確認したいとき。

## Do not read this when

- `src/sub_commands/` 配下の個別サブコマンド本体だけを確認したいとき。
- `commons.errors` の例外型や `format_error_report()` の整形ロジックだけを確認したいとき。
- CLI 登録や補完、例外変換ではなく、各機能の業務ロジックそのものを追いたいとき。
- `INDEX.md` の生成ルールや `oracles` 側の正本仕様だけを確認したいとき。

## hash

- 1a1bb5753238e77dc6df1252d876b3fc6c7cc1706bd8b8499554963755c0a4d7

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc のサブコマンド実装をまとめる入口ディレクトリです。
- `__init__.py` はパッケージ宣言のみを担い、`init.py` は `cmoc init` の本体処理を持ちます。
- `apply`、`review`、`session` の各サブディレクトリが、それぞれのサブコマンド群の実装入口になっています。

## Read this when

- `src/sub_commands` 配下にどのサブコマンド実装があるかを俯瞰し、どのモジュールへ進むべきか整理したいとき。
- `cmoc init`、`cmoc apply`、`cmoc review`、`cmoc session` の入口構造と役割分担を確認したいとき。
- このディレクトリの `__init__.py`、`init.py`、`apply`、`review`、`session` の位置づけを把握したいとき。

## Do not read this when

- 個別のサブコマンド実装や引数・状態遷移を確認したいときは、対応する `apply`、`review`、`session`、`init.py` を直接読むべきです。
- `src/commons` の共通基盤や `src/main.py` の CLI 登録だけを確認したいときは、このディレクトリではなく該当箇所を読むべきです。
- `INDEX.md` の生成・更新ルールや、`oracles` 側の正本仕様だけを確認したいときは、このディレクトリではなく別の仕様文書を参照すべきです.

## hash

- 5407c1e97ae6cd2e085bdc381aed7e547e441ac0734e4c8186dc2c1eafbfdf3e
