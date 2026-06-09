# `commons`

## Summary

- cmoc の共通基盤をまとめた `src/commons` パッケージで、repo/worktree 解決、Codex 呼び出し、エラー整形、ログ、タイムスタンプ、経過時間計測、レポート保存、`INDEX.md` 生成を担うモジュール群です。
- 個別サブコマンドの本体ではなく、複数コマンドから再利用される横断処理を集約しています。
- この階層は、`__init__.py` を含む各モジュールへの入口として、必要に応じて `codex.py`、`repo.py`、`indexing.py`、`subcommand_log.py` などへ分岐します。

## Read this when

- cmoc 全体で共有する基盤処理の役割分担を把握したいとき。
- `codex exec` 呼び出し、`INDEX.md` 生成・整合性検査、repo/worktree 解決、エラー整形、サブコマンドログ、レポート保存、タイムスタンプ、経過時間表示のどれを読むべきか判断したいとき。
- `src/commons` 配下の個別モジュールへ進む前に入口を整理したいとき。

## Do not read this when

- 個別サブコマンドの引数解析や業務ロジックだけを確認したいとき。
- すでに `codex.py`、`repo.py`、`indexing.py` などの個別モジュールの読み先が決まっているとき。
- `oracles` 側の正本仕様や `tests` の回帰条件だけを確認したいとき。

## hash

- 4d1c5258c179522400d107914b29db66a91a0aff2b99db7337fac905770a0816

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

- `src/sub_commands` ディレクトリのルーティング文書で、`__init__.py`、`init.py`、`indexing.py`、`apply/`、`session/`、`review/` への入口です。
- この階層では、パッケージ宣言だけの最小モジュールと、各サブコマンド本体または下位パッケージへ進む分岐を整理します。
- 個別実装に進む前に、どのモジュールがどの責務を持つかを切り分けるための目次です。

## Read this when

- `src/sub_commands` 配下の入口構造を把握し、どの実装ファイルや下位ディレクトリへ進むべきかを判断したいとき。
- `cmoc init` や `cmoc indexing` の本体実装を確認したいとき。
- `cmoc apply`、`cmoc session`、`cmoc review` の各パッケージへ分岐する前に、まずこの階層の役割を整理したいとき。

## Do not read this when

- すでに読む対象の `init.py`、`indexing.py`、`apply/`、`session/`、`review/` が分かっていて、直接その先へ進めるとき。
- `src/sub_commands` 全体ではなく、個別のサブコマンド実装やその下位ディレクトリの `INDEX.md` だけを確認したいとき。
- CLI 登録や起動経路ではなく、`oracles` 側の正本仕様断片だけを確認したいとき。

## hash

- 16b84a5af55772e6375e0c36a3d354fc8ac4c9802afb80901d710c4fceead53b
