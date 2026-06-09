# `commons`

## Summary

- cmoc の共通基盤をまとめた `src/commons` パッケージで、repo/root 解決、エラー整形、Codex 呼び出し、ログ、タイムスタンプ、所要時間計測、`INDEX.md` 生成を担うモジュール群です。
- 個別サブコマンドの本体ではなく、複数コマンドから再利用される横断処理を集約しています。
- `__init__.py` を含む各モジュールへの入口で、必要に応じて `codex.py`、`repo.py`、`indexing.py`、`subcommand_log.py` などへ分岐します。

## Read this when

- cmoc 全体で共有する基盤処理の役割分担を把握したいとき。
- `codex exec` 呼び出し、サブコマンド実行制御、repo/worktree 解決、状態保存、ログ出力のどれを読むべきか判断したいとき。
- `INDEX.md` の生成・整合性検査、タイムスタンプ、経過時間表示、エラーレポートの共通仕様を追いたいとき。

## Do not read this when

- 個別サブコマンドの引数解析や業務ロジックだけを確認したいとき。
- `oracles` 配下の正本仕様や、`tests` の回帰条件だけを確認したいとき。
- 対象の役割がすでに `codex.py` や `repo.py` などの個別モジュールで分かっているとき。

## hash

- 401396c424b539e69a3a46f6cf2a7a0216050bab7fe35e5d6fd78224e0203965

# `main.py`

## Summary

- `src/main.py` は cmoc CLI のエントリーポイントで、Typer のルート `app` と `session` / `apply` / `review` の各サブアプリを組み立てるファイルです。
- `init`、`indexing`、各サブコマンドの登録に加えて、`eval-oracle` / `eval-oracles` の隠し別名や各コマンドの既定オプションをまとめています。
- サブコマンド未指定時の `CmocError` 生成、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc CLI のルート構成と、`session` / `apply` / `review` のサブアプリを確認したいとき。
- `init`、`indexing`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録名や既定引数を確認したいとき。
- サブコマンド未指定時のエラー生成、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の経路を確認したいとき。

## Do not read this when

- 個別サブコマンドの実装本体だけを確認したいとき。
- `commons.errors` や `commons.command_runner` など、共通基盤の詳細だけを追いたいとき。
- CLI 入口ではなく、`oracles` 側の正本仕様や利用手順だけを確認したいとき。

## hash

- ee925dc07d26b235724d5d792adb638166ae640a05e4b1f6ca38f773e8c24834

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc のサブコマンド実装群のルーティング目次です。
- ここから `__init__.py`、`indexing.py`、`init.py`、および `apply/`、`review/`、`session/` へ分岐します。
- この階層は、個別実装へ進む前にサブコマンド群の入口を整理するための案内役です。

## Read this when

- `src/sub_commands` 配下で、どの実装モジュールや下位ディレクトリを読むべきか迷ったとき。
- `cmoc init` と `cmoc indexing` の本体実装、または `apply` / `review` / `session` 系の入口を一覧で把握したいとき。
- `src/sub_commands` の構成をレビュー、修正、テストの前に整理したいとき。
- パッケージ宣言と実装モジュール、下位サブコマンド群の役割分担を確認したいとき。

## Do not read this when

- すでに `src/sub_commands/__init__.py`、`src/sub_commands/indexing.py`、`src/sub_commands/init.py`、`src/sub_commands/apply/`、`src/sub_commands/review/`、`src/sub_commands/session/` の読み先が決まっていて、この階層の目次が不要なとき。
- `cmoc init` や `cmoc indexing` の利用手順だけを確認したいとき。
- この階層ではなく、上位の `src/` 全体や下位ディレクトリの個別 `INDEX.md` だけを確認したいとき。
- CLI 登録や実装詳細ではなく、リポジトリ運用ルールだけを確認したいとき。

## hash

- bbb1d33940e7e13c0cae366c996484877ed3216d2fb509cd9c20f7a4184d1b85
