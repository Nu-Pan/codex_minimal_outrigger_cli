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

- `src/sub_commands` ディレクトリのルーティング文書で、`cmoc` の各サブコマンド実装への入口を整理する階層です。
- `__init__.py` はパッケージ宣言だけを担い、`init.py` と `indexing.py` は単独コマンド本体、`apply/`、`session/`、`review/` は各系統の入口です。
- この階層では、どのコマンド本体や下位 `INDEX.md` に進むべきかを切り分けます。

## Read this when

- `src/sub_commands` 配下で `cmoc` のどのサブコマンド実装へ進むべきか迷っているとき。
- `cmoc init`、`cmoc indexing`、`cmoc apply`、`cmoc session`、`cmoc review` の入口構造を把握したいとき。
- 下位ディレクトリの `INDEX.md` や個別実装ファイルを読む前に、全体の目次を確認したいとき。
- `src/sub_commands` が Python パッケージとして成立しているかを確認したいとき。

## Do not read this when

- 読む対象がすでに `__init__.py`、`init.py`、`indexing.py`、`apply/`、`session/`、`review/` のいずれかに決まっていて、この階層の案内が不要なとき。
- `cmoc` 全体の利用手順や共通仕様ではなく、個別のコマンド仕様断片だけを確認したいとき。
- `oracles` 側の正本仕様を直接たどる目的で、`src/sub_commands` の入口整理が不要なとき。
- 実装詳細ではなく CLI 登録や引数定義だけを確認したいとき。

## hash

- 05580656a91bdedb2492266393bbf9b47c4094d8ea23ea6e0b2c824aadc96f43
