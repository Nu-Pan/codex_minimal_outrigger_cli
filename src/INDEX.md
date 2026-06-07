# `commons`

## Summary

- この `src/commons` ディレクトリのルーティング文書で、cmoc 全体で共有する基盤モジュール群への入口です。
- `codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` をまとめて案内します。
- 個別サブコマンドの業務ロジックではなく、実行制御・エラー整形・リポジトリ操作・ログ・計測・レポート保存の共通部品をたどるための目次です。

## Read this when

- cmoc 全体で共通に使う基盤処理の入口を確認したいとき。
- `codex exec` 呼び出し、サブコマンド実行ラッパー、共通エラー、`INDEX.md` 生成、git/作業ツリー処理、ログ、タイムスタンプ、経過時間計測、レポート保存のどれを読むべきか切り分けたいとき。
- 各サブコマンドや自動メンテナンス処理が依存する共有モジュールを最初に整理したいとき。
- この階層の個別モジュールへ進む前に、どの機能がどのファイルにあるか俯瞰したいとき。

## Do not read this when

- 個別モジュールの実装詳細をすでに把握していて、`__init__.py` や各 `.py` へ直接進めるとき。
- `src/main.py` や `src/sub_commands/` の登録・配線だけを確認したいとき。
- `oracles` 側の正本仕様だけを確認したいとき。
- このディレクトリではなく、1 つの共通モジュールだけの挙動を確認したいとき。

## hash

- 04e470a2de168bc49328d34378fc67efa83b970e468471571c6f45aa451f6ad7

# `main.py`

## Summary

- cmoc CLI のエントリーポイントで、Typer のルート `app` と `session` / `apply` / `review` の各サブアプリを組み立てるファイルです。
- `init` や各サブコマンドの登録に加えて、`eval-oracle` / `eval-oracles` の隠し別名や既定オプションをまとめています。
- サブコマンド未指定時の `CmocError` 生成、自動補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc CLI の起点として、`app` と `session` / `apply` / `review` のサブアプリ構成を確認したいとき。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録名や隠し別名を確認したいとき。
- サブコマンド未指定時のエラー処理、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の経路を追いたいとき。

## Do not read this when

- `src/sub_commands/` 配下の各サブコマンド本体の処理や引数解釈を確認したいとき。
- `commons.errors` の例外型や `format_error_report()` の整形ロジックだけを確認したいとき。
- CLI の登録や補完分岐ではなく、各機能の業務ロジックそのものを追いたいとき。

## hash

- 6534c818d649a5bf27c91568e5d0f98ec2a3ca42c83e255968a94e7742459b54

# `sub_commands`

## Summary

- `src/sub_commands` は `cmoc` のサブコマンド実装をまとめる入口ディレクトリです。
- 直下には最小のパッケージ宣言 `__init__.py`、`cmoc init` 本体の `init.py`、および `apply/`、`session/`、`review/` の各サブパッケージがあります。
- 各下位ディレクトリはそれぞれ独自の `INDEX.md` を持ち、個別サブコマンド実装へ進むためのルーティング先になっています。

## Read this when

- `cmoc` のサブコマンド群全体の入口構造と、どの実装へ進むべきかを整理したいとき。
- `init.py` と `apply/`、`session/`、`review/` の責務分担を俯瞰して、修正・テスト・レビュー先を選びたいとき。
- CLI の配線や各サブコマンドの位置関係を把握してから、個別モジュールへ入る前の導線が欲しいとき。
- `src/sub_commands` 配下にある直接の子要素が何で、それぞれがどの系統の実装かを確認したいとき。

## Do not read this when

- 個別の `cmoc` サブコマンド 1 つだけの引数や終了条件を確認したいときは、この入口ではなく該当モジュールを直接読むべきです。
- `apply`、`session`、`review` のうち特定の系統だけを追いたいときは、このディレクトリ全体ではなく各下位ディレクトリの `INDEX.md` を読むべきです。
- `oracles` 側の正本仕様断片や利用手順だけを確認したいときは、実装側のこのディレクトリではなく該当する仕様文書を読むべきです。
- `src/sub_commands` のパッケージ宣言だけを確認したいときは、この目次ではなく `__init__.py` を見るだけで足ります。

## hash

- 72f144e6881fa6744f359c3baf99eb62acda7c47d1377f4dbf4d39ca051e821b
