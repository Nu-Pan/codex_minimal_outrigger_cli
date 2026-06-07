# `commons`

## Summary

- `src/commons` は、cmoc 全体で共有する基盤モジュール群をまとめたパッケージです。
- repo root の解決、共通エラー、サブコマンド実行ラッパー、Codex CLI 呼び出し、`INDEX.md` 生成、ログ、タイムスタンプ、経過時間計測、レポート保存を扱います。
- 個別サブコマンドの業務ロジックではなく、横断的に依存する共通部品の入口です。

## Read this when

- cmoc 全体で共有する基盤処理の入口を把握したいとき。
- repo root の解決、共通エラー整形、サブコマンド実行、`INDEX.md` 生成、ログ、計測、レポート保存の関係を整理したいとき。
- 各機能がどの共通モジュールに分かれているかを先に切り分けたいとき。
- 共通部品の修正やレビューの前に、どの責務をどのファイルで扱うか確認したいとき。

## Do not read this when

- 個別のサブコマンド本体や CLI 引数の挙動だけを追いたいとき。
- `src/sub_commands/` 側の業務ロジックや配線だけを確認したいとき。
- `oracles` 側の正本仕様断片だけを確認したいとき。
- このディレクトリのうち 1 つのモジュールだけの実装詳細を確認したいとき。

## hash

- 2d22f1c4ef91cb9f5a3b303efb8d821cc9a411f38f62a1b3cca92343302ca009

# `main.py`

## Summary

- `src/main.py` は cmoc CLI のエントリーポイントで、Typer のルート `app` と `session` / `apply` / `review` の各サブアプリを組み立てるファイルです。
- `init`、`session`、`apply`、`review` の各コマンド登録に加えて、`eval-oracle` / `eval-oracles` の隠し別名や各コマンドの既定オプションをまとめています。
- サブコマンド未指定時の `CmocError` 生成、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc CLI の起点として、`session` / `apply` / `review` のサブアプリ構成を確認したいとき。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録名や隠し別名を確認したいとき。
- `apply fork` の既定反復回数や `scope`、`apply join` の `--force-resolve` などの既定オプションを確認したいとき。
- サブコマンド未指定時の利用者向けエラー、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の経路を確認したいとき。

## Do not read this when

- `src/sub_commands/` 配下の個別サブコマンド本体だけを確認したいとき。
- `commons.errors` や `format_error_report()` の例外整形だけを確認したいとき。
- `oracles` 側の正本仕様や `INDEX.md` 生成ルールだけを確認したいとき。
- `bin/cmoc` のシェル起動ラッパーだけを確認したいとき。

## hash

- 8e5c543120f5d8c879497bffa31a440854f689cb349abab0deb3f8a0cf8bf19e

# `sub_commands`

## Summary

- この `src/sub_commands` ディレクトリのルーティング文書で、`__init__.py`、`indexing.py`、`init.py`、`apply/`、`review/`、`session/` への入口をまとめています。
- `__init__.py` はパッケージ宣言、`indexing.py` は `INDEX.md` 維持処理、`init.py` は初期化処理、`apply/`・`review/`・`session/` は各サブコマンド群の入口です。
- 個別実装へ入る前に、`cmoc` のサブコマンド実装をどの系統から読むかを切り分けるための目次です。

## Read this when

- `src/sub_commands` 配下の全体構造を把握して、次に開くべきファイルやディレクトリを選びたいとき。
- `cmoc` の `init`、`indexing`、`session`、`apply`、`review` の入口構造と役割分担を整理したいとき。
- サブコマンド実装の修正・レビュー・テストの前に、対象モジュールを絞り込みたいとき。
- `src/sub_commands` が Python パッケージとして成立していることを確認したいとき。

## Do not read this when

- すでに開くべき個別モジュールが決まっていて、この階層の目次を経由する必要がないとき。
- `cmoc` の利用手順や正本仕様だけを確認したいときで、実装の入口整理が不要なとき。
- `apply/`、`review/`、`session/` など下位ディレクトリの個別 `INDEX.md` を直接読みたいとき。

## hash

- 85480e738bea46670ab7a32d73e8efb72c9bddf05da07a00731cdfabc10a64fb
