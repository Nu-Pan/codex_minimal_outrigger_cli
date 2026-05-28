# `commons`

## Summary

- `src/commons` は cmoc の共有基盤をまとめるディレクトリの入口で、Codex CLI 呼び出し、サブコマンド実行制御、エラー整形、リポジトリ操作、ログ、タイムスタンプ、経過時間計測を案内します。
- `codex.py`、`indexing.py`、`repo.py` は実行フローとメンテナンス処理の中核で、`INDEX.md` の生成・維持や git ルート、branch、session state の管理も扱います。
- `command_runner.py`、`errors.py`、`subcommand_log.py`、`timing.py`、`timestamps.py` はサブコマンドの共通実行基盤を支える補助群です。

## Read this when

- `src/commons` 配下の共有処理の役割分担を把握したいときに読むべきです。
- `codex exec`、Structured Output、`INDEX.md` メンテナンス、`.cmoc` 管理の関連を横断して確認したいときに読むべきです。
- サブコマンド本体から再利用すべき共通関数の置き場所を探したいときに読むべきです。
- 共有ユーティリティの一覧から目的のモジュールへ進みたいときに読むべきです。

## Do not read this when

- 個別サブコマンドの仕様や CLI 引数を確認したいときは、このディレクトリではなく `src/sub_commands` を読むべきです。
- `INDEX.md` の自動生成ルールだけを確認したいときは、このディレクトリではなく `src/commons/indexing.py` を直接読むべきです。
- 共通エラーの整形だけを確認したいときは、このディレクトリではなく `src/commons/errors.py` を直接読むべきです。
- タイムスタンプ生成、ログ、経過時間計測のうち特定 1 つだけを確認したいときは、対応する個別ファイルを直接読むべきです。

## hash

- 1728f9a6a6b99b9bae07b413f81c2272fc03c9a7eaee6b0e982b6800ee18b83d

# `main.py`

## Summary

- `cmoc` CLI のエントリーポイントで、Typer アプリ本体と `session` / `apply` のサブアプリを組み立てています。
- `init`、`session`、`apply`、`eval-oracles` の各コマンドを定義し、実処理は `src/sub_commands/` 側の実装へ委譲しています。
- Typer / Click の例外処理をまとめて受け、`NoArgsIsHelpError` を含むエラーを `format_error_report()` で整形して終了コード付きで終了します。

## Read this when

- `cmoc` のエントリーポイント、Typer アプリの構成、サブコマンド登録を修正・レビューしたいとき。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`eval-oracles` とその引数定義を確認したいとき。
- サブコマンドなし起動時の `NoArgsIsHelpError` の扱い、`--help` 相当の挙動、終了コードの伝播を確認したいとき。
- Typer / Click の例外を `CmocError` と共通エラーレポートへ変換する起動経路を確認したいとき。
- `python src/main.py` で直接起動する経路の振る舞いを確認したいとき。

## Do not read this when

- 各サブコマンド本体の処理内容だけを確認したいときは、このファイルではなく `src/sub_commands/` 配下の実装を見るべきです。
- 共通エラー型やエラーレポートの整形だけを確認したいときは、このファイルではなく `src/commons/errors.py` を見るべきです。
- CLI の設計ルールや配置方針だけを確認したいときは、このファイルではなく `oracles/dev_rules/design_rules.md` を見るべきです。
- サブコマンドごとの仕様断片だけを確認したいときは、このファイルではなく `oracles/app_specs/sub_commands/` 配下の文書を見るべきです。

## hash

- fd4b3fe58ddc1bb32e637e83cc5ddca509458ade3b15a69c1c5d5bc677ba138b

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc のサブコマンド実装の入口で、`apply` と `session` の各パッケージ、`init.py`、`eval_oracles.py`、`__init__.py` への案内をまとめます。
- `apply` と `session` はそれぞれ独立したサブコマンド群として、配下の `INDEX.md` から個別実装へたどれます。
- `init.py` と `eval_oracles.py` は単体モジュールとして、初期化処理と oracle 評価処理の入口を担います。
- `__init__.py` は `src.sub_commands` パッケージを宣言するだけの最小モジュールです。

## Read this when

- `cmoc` のサブコマンド実装全体の入口を確認したいときに読むべきです。
- `apply` や `session` のような複数ファイルの実装群と、`init.py` / `eval_oracles.py` の単体モジュールを見分けたいときに読むべきです。
- どのサブコマンド実装へ進むべきか、このディレクトリの目次から判断したいときに読むべきです。
- `src/sub_commands` 配下の個別 `INDEX.md` や実装ファイルの入口を探したいときに読むべきです。

## Do not read this when

- `src/sub_commands` 配下のどの実装へ進むべきかではなく、CLI の起動口やコマンド登録全体を確認したいときは `src/main.py` を読むべきです。
- 個別サブコマンドの利用手順や正本仕様だけを確認したいときは、`oracles/app_specs/sub_commands/` 側の文書を直接読むべきです。
- 共通処理やリポジトリ操作、エラー整形などの横断的な仕組みを確認したいときは、`src/commons/` 側を読むべきです。
- `apply`、`session`、`init.py`、`eval_oracles.py` のうち特定の 1 つだけを深く追いたいときは、この目次ではなく該当する配下の `INDEX.md` やモジュールを直接読むべきです。

## hash

- 0553470bbdbf893543c16374e33fe53b6281294c9f04662f43680ff05a751d57
