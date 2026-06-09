# `commons`

## Summary

- `src/commons` は、cmoc 全体で共有する共通基盤モジュール群のルーティング目次です。
- ここから `__init__.py`、`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timing.py`、`timestamps.py` へ分岐します。
- CLI 実行や共通処理の入口をまとめ、個別モジュールへ進む前の案内役を担います。

## Read this when

- `src/commons` 配下で、どの共通モジュールがどの責務を持つかをまとめて把握したいとき。
- `codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timing.py`、`timestamps.py` のどれを読むべきか整理したいとき。
- CLI 実行、ログ、時間計測、エラー整形、Git 操作、`INDEX.md` 維持、タイムスタンプ、レポート保存の入口を確認したいとき。
- このディレクトリの下位ファイルへ進む前に、共通基盤の役割分担を整理したいとき。

## Do not read this when

- すでに読む対象が `src/commons/codex.py` など個別モジュールに決まっていて、この階層の案内が不要なとき。
- 個別サブコマンドの引数解析や業務ロジックだけを確認したいとき。
- `src/main.py` や `src/sub_commands/` など、CLI の入口や各コマンド本体を直接追いたいとき。
- `oracles` 側の正本仕様や `INDEX.md` の生成ルールだけを確認したいとき。

## hash

- 442b2d5d9053c1ae1f6c1dd7c95e986e4f8a43daeda1d55055532b47703fd9b9

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

- `src/sub_commands` ディレクトリのルーティング文書で、`__init__.py`、`indexing.py`、`init.py` と、`apply/`、`review/`、`session/` へ案内する入口です。
- `__init__.py` はパッケージ宣言のみ、`indexing.py` は `cmoc indexing`、`init.py` は `cmoc init` の本体実装です。
- `apply/`、`review/`、`session/` はそれぞれ配下の `INDEX.md` を起点に、個別サブコマンド実装へ進みます。

## Read this when

- `src/sub_commands` 配下で、どの実装モジュールや下位ディレクトリを開くべきか迷ったとき。
- `cmoc init` や `cmoc indexing` の本体実装、または `apply` / `review` / `session` 系の入口を一覧で把握したいとき。
- `src/sub_commands` の構成をレビュー・修正・テスト前に整理したいとき。
- パッケージ宣言と実装モジュール、下位サブコマンド群の役割分担を確認したいとき。

## Do not read this when

- すでに `__init__.py`、`indexing.py`、`init.py`、`apply/`、`review/`、`session/` の読み先が決まっていて、直接そちらへ進むとき。
- `cmoc init` や `cmoc indexing` の利用手順や正本仕様だけを確認したいとき。
- この階層ではなく、上位の `src/` や下位の各ディレクトリの `INDEX.md` だけを確認したいとき。
- CLI 登録やコマンド実行の細部ではなく、リポジトリ運用ルールだけを確認したいとき。

## hash

- f29b425aca19ce6cc71f0f543358644e8b4368f9e0853390efeaa917f93aa449
