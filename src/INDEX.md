# `commons`

## Summary

- `src/commons` は `cmoc` 全体で共有する基盤モジュール群をまとめるディレクトリです。
- `codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` が主要な構成要素です。
- この目次は、実行制御、共通エラー、リポジトリ操作、目次維持、ログ、時間表示、レポート保存のどこへ進むかを素早く判断するための入口です。

## Read this when

- `cmoc` 全体で使う共通基盤の役割分担を把握したいとき。
- CLI 実行、エラー整形、ログ、時間計測、タイムスタンプ、レポート保存の共通処理を確認したいとき。
- repo root や `.cmoc` の管理、`INDEX.md` 生成・維持の流れを追いたいとき。
- `src/commons` 配下のどのモジュールを読むべきか切り分けたいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや引数解析だけを追いたいとき。
- `src/sub_commands/` 側の実装や CLI の振る舞いだけを確認したいとき。
- `oracles` 配下の正本仕様断片を直接たどりたいとき。
- テストケースの期待値だけを確認したいとき。

## hash

- ca47d61b847f9e0afe7c517c6caceab4b6a115f63b01c06a4089e8a71d926cc3

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

- 34ab9fdae7d4622e261437958669dd52ce211f233a2300c1c7c831efc256c365

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc の各サブコマンド実装をまとめる入口ディレクトリです。
- `__init__.py` はパッケージ宣言のみを担い、`init.py` は `cmoc init` の本体です。
- `apply`、`session`、`review` はそれぞれ対応サブコマンドの実装ディレクトリで、個別の `INDEX.md` に詳細があります。
- この目次は、`src/sub_commands` 配下のどこから読み始めるべきかを素早く判断するための案内です。

## Read this when

- `src/sub_commands` 配下で、どのサブコマンド実装を読むべきか整理したいとき。
- `cmoc init`、`cmoc apply`、`cmoc session`、`cmoc review` の入口構造を俯瞰したいとき。
- パッケージ宣言だけのモジュールと、本体実装のあるモジュールを切り分けたいとき。
- サブコマンド群の責務分担と、下位ディレクトリへのルーティング先を確認したいとき。

## Do not read this when

- `cmoc` の CLI 登録や引数パースだけを確認したいとき。
- `apply`、`session`、`review` の個別実装の詳細を追いたいときは、この目次ではなく各サブディレクトリの `INDEX.md` を読むべきです。
- `init.py` など個別モジュールの実装詳細だけを確認したいとき。
- `oracles` 配下の仕様断片そのものを直接確認したいとき。

## hash

- d7287ae93f4288b05f967d5d4b6abe6fd713ad83eb450404ff1c869b1dedebe7
