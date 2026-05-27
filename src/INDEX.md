# `commons`

## Summary

- `src/commons` は、cmoc 全体で共有する基盤モジュール群の入口です。
- `codex` の呼び出し、サブコマンド共通実行制御、共通エラー、`INDEX.md` 管理、リポジトリ操作、サブコマンドログ、タイムスタンプ、経過時間計測をまとめて案内します。
- `__init__.py` も含めて、共有処理の配置先と各モジュールへの導線を整理するための目次です。

## Read this when

- cmoc の共通基盤として、`codex`、`command_runner`、`errors`、`indexing`、`repo`、`subcommand_log`、`timestamps`、`timing` の役割分担を横断的に確認したいとき。
- サブコマンド実行、エラー整形、ログ保存、経過時間計測、リポジトリ探索、`INDEX.md` 管理などの共有処理をどこへ置くべきか判断したいとき。
- `src/commons` 配下の共通モジュール群をまとめて把握し、どのファイルへ進むべきか整理したいとき。
- cmoc の実装やレビューで、共有ユーティリティ層の入口となる案内を確認したいとき。

## Do not read this when

- 個別のサブコマンド実装だけを確認したいときは、`src/sub_commands` 側を直接読むべきです。
- `src/commons` 配下のうち特定 1 モジュールだけが必要なときは、このディレクトリの案内ではなく該当ファイルを直接読むべきです。
- CLI の利用方法やユーザー向けコマンド仕様だけを追いたいときは、`oracles/app_specs` 側を読むべきです。
- `INDEX.md` の生成・更新ルールそのものだけを確認したいときは、`src/commons/indexing.py` や対応する正本仕様を直接読むべきです。

## hash

- fb2d35aca57aac47fa8276bd1a82372fb90e46310803768e89a66a2d0e3cdfd5

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

- `src/sub_commands` は cmoc のサブコマンド本体をまとめる入口です。`__init__.py`、`init.py`、`eval_oracles.py`、`apply/`、`session/` への案内をまとめます。
- `apply/INDEX.md` は `apply` 系の個別実装へ、`session/INDEX.md` は `session` 系の個別実装へ、それぞれ直接たどるための入口です。
- この INDEX は、サブコマンド本体の配置先と各ファイルへの導線を整理するための目次です。

## Read this when

- `cmoc apply` 系の本体処理と、その `fork/join/abandon` 実装の配置を確認したいとき。
- `cmoc session` 系の本体処理と、その `fork/join/abandon` 実装の配置を確認したいとき。
- `cmoc init` や `cmoc eval-oracles` の本体処理の置き場所を確認したいとき。
- このディレクトリ配下のどのモジュールを読むべきか、入口から判断したいとき。

## Do not read this when

- 共有ユーティリティや git 操作の共通処理だけを確認したいときは、`src/commons` を読むべきです。
- CLI のトップレベル登録やコマンドルーティング全体だけを確認したいときは、`src/main.py` を読むべきです。
- 個別のサブコマンド仕様断片だけを確認したいときは、`oracles/app_specs/sub_commands/` 側を読むべきです。
- `src/sub_commands` の個別実装ではなく、仕様文書だけを読みたいときは、対応する oracle 文書へ進むべきです。

## hash

- bc8f565ec785460cf8fd844be217b7e2e316270ab55a272bde6d2a07036153e5
