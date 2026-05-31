# `commons`

## Summary

- `src/commons` は、cmoc 全体で共有する基盤モジュール群をまとめたパッケージです。
- repo root の解決、共通エラー整形、サブコマンド実行ラッパー、Codex CLI 呼び出し、`INDEX.md` 生成、サブコマンドログ、タイムスタンプ、経過時間計測、レポート保存を扱います。
- 個別サブコマンドの業務ロジックではなく、各機能が横断的に依存する共通部品の入口になっています。

## Read this when

- cmoc 全体で共通に使う基盤処理の入口を確認したいとき。
- repo root の解決、`CmocError`、`codex exec` 呼び出し、`INDEX.md` メンテナンス、ログ、計測、レポート保存の関係を把握したいとき。
- 各サブコマンドや自動メンテナンス処理が依存する共通部品をまとめて追いたいとき。
- どの共通モジュールに入るべきかを最初に切り分けたいとき。

## Do not read this when

- 個別サブコマンドの引数や業務ロジックだけを追いたいとき。
- `src/main.py` や `src/sub_commands/` 配下の登録・配線だけを確認したいとき。
- `oracles` 側の正本仕様だけを確認したいとき。
- このディレクトリのうち 1 つのモジュールだけの実装詳細を確認したいとき。

## hash

- 3a12b946b2ea21139ab98f385cea24130d63fd6e11337bbaa79c5e4a2f648d17

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
