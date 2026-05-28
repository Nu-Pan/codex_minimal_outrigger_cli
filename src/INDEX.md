# `commons`

## Summary

- cmoc の共通処理をまとめる `src/commons` 配下の入口で、`codex` 呼び出し、サブコマンド実行制御、共通エラー、git リポジトリ操作、サブコマンドログ、タイムスタンプ、経過時間計測、`INDEX.md` 生成補助を案内します。
- このディレクトリからは `codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`subcommand_log.py`、`timestamps.py`、`timing.py`、`__init__.py` へたどれます。

## Read this when

- cmoc の共通実行基盤や、複数のサブコマンドにまたがる処理の置き場所を確認したいとき。
- codex exec の呼び出し、repo root 解決、共通エラー整形、ログ記録、タイムスタンプ、時間計測のどこへ進むべきか整理したいとき。
- このディレクトリ配下の個別モジュールを横断して、共通ユーティリティの役割分担を把握したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数だけを確認したいときは、`src/sub_commands` 側を読むべきです。
- `INDEX.md` の生成・更新ルールだけを確認したいときは、`src/commons/indexing.py` ではなく `oracles/app_specs/indexing.md` を読むべきです。
- このディレクトリのうち特定の 1 ファイルだけを確認したいときは、ここではなく該当するモジュールを直接参照すべきです。

## hash

- 15688b3b0b4503d7b246bb989eb7ec6967ff863ba9ac28ec4e4f2a43bb69cb25

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

- `src/sub_commands` は cmoc のサブコマンド実装の入口で、`apply` と `session` の各パッケージ、`init.py`、`eval_oracles.py`、`__init__.py` への案内をまとめる。
- `apply` と `session` はそれぞれ独立したサブコマンド群として、配下の `INDEX.md` から個別実装へたどれる。
- `init.py` と `eval_oracles.py` は単体モジュールとして、初期化処理と oracle 評価処理の入口を担う。

## Read this when

- `cmoc` のサブコマンド実装全体の入口を確認したいとき。
- `apply` や `session` のような複数ファイルの実装群と、`init.py` / `eval_oracles.py` の単体モジュールを見分けたいとき。
- どのサブコマンド実装へ進むべきか、このディレクトリの目次から判断したいとき。
- `src/sub_commands` 配下の個別 `INDEX.md` や実装ファイルの入口を探したいとき。

## Do not read this when

- 個別サブコマンドの実装や手順だけを確認したいときは、対応する配下の `INDEX.md` や実装ファイルを直接読むべきです。
- `cmoc` の共通処理や `commons` 側の仕様だけを確認したいときは、このディレクトリではなく該当する案内を読むべきです。
- サブコマンドの利用手順そのものではなく、実装やテストの詳細を追いたいときは、より下位の文書を読むべきです。
- このディレクトリの役割確認だけで足りるときに、個別モジュールまで読み進める必要はありません。

## hash

- 1bff4db46839c7837f563219170fac803f6a78105e1aa58e283e7367c13a34f0
