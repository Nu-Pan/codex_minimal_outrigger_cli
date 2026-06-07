# `commons`

## Summary

- `src/commons` にある cmoc 共通モジュール群のルーティング入口です。
- repo 管理、サブコマンド実行ラッパー、共通エラー、INDEX.md 生成、ログ、時刻処理などの基盤処理をまとめています。
- 個別サブコマンドの実装ではなく、複数機能から再利用される共通部品を案内するための目次です。

## Read this when

- `cmoc` 全体で使う共通処理の入口を把握したいとき。
- repo root の探索、コマンド実行、エラー整形、ログ、時刻、インデクシングなどの共通基盤を確認したいとき。
- `src` や `tests` の実装前に、共通ユーティリティ群の役割分担を整理したいとき。

## Do not read this when

- 個別サブコマンドの引数解析や業務ロジックだけを追いたいとき。
- `README.md` や `AGENTS.md` など、リポジトリ運用ルールだけを確認したいとき。
- `src/commons` の特定モジュールがすでに分かっていて、そのファイルへ直接進めるとき。

## hash

- 41231a9af0487dabc4c76d01f61930a619e60c4443d583539889b8739f42305f

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
