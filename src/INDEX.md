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

- `cmoc` の個別サブコマンド実装への入口です。
- `apply/`、`session/`、`review/`、`init.py` と `__init__.py` をまとめ、どの実装を読むべきかを素早く選べるようにします。
- このディレクトリを起点に、`apply` 系、`session` 系、`review oracles`、`init` の各詳細仕様へ分岐します。

## Read this when

- `cmoc` の個別サブコマンド実装の入口をまとめて確認したいとき。
- `apply`、`session`、`review oracles`、`init` のどの実装ディレクトリやファイルへ進むべきか整理したいとき。
- サブコマンドごとの役割分担、入口構造、関連ファイルの位置関係を俯瞰したいとき。
- `src/sub_commands` 直下の新しいサブコマンド実装や入口ファイルを追加・再配置するとき。

## Do not read this when

- 個別のサブコマンド実装を深く追いたいだけのときは、この目次ではなく `apply/`、`session/`、`review/`、`init.py` を直接読むと早いです。
- `src/sub_commands` のパッケージ宣言だけを確認したいときは、`__init__.py` を直接読めば十分です。
- `cmoc` 全体の共通仕様や `oracles` 側の正本を確認したいときは、このディレクトリではなく該当する上位の仕様文書を読むべきです。
- サブコマンド本体ではなく、CLI 起動点や共通処理だけを見たいときは `src/main.py` や `src/commons/` を読むべきです。

## hash

- 9cf3b99f2698fab153ea86201969c52916d218b7b4d53538768832cbe9619c8f
