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
- `apply`、`session`、`review` の各ディレクトリに、それぞれのサブコマンド群の実装入口があります。

## Read this when

- `src/sub_commands` 配下のサブコマンド実装全体の入口構造を把握したいとき。
- `cmoc init` の実装入口と、`apply`・`session`・`review` 系サブコマンドの配置を確認したいとき。
- `src/sub_commands` ディレクトリ内で、どのファイルや下位ディレクトリへ進むべきかを素早く判断したいとき。

## Do not read this when

- `cmoc init` の本体処理だけを確認したいときは、`src/sub_commands/init.py` を直接読むべきです。
- `cmoc apply`、`cmoc session`、`cmoc review` の個別実装だけを確認したいときは、それぞれの下位ディレクトリの `INDEX.md` や実装モジュールを読むべきです。
- `src/sub_commands` のパッケージ宣言だけを確認したいときは、この目次ではなく `src/sub_commands/__init__.py` を読むべきです。

## hash

- ef24cdc3808001e02d74a74a2579fd1a9db8548e5b7181dbbf470ea60f6f13e0
