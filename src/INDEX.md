# `commons`

## Summary

- `cmoc` の共通処理をまとめるディレクトリの入口です。
- `codex` 呼び出し、コマンド実行制御、リポジトリ探索と状態管理、共通エラー処理、`INDEX.md` 生成、サブコマンドログ、タイムスタンプ、経過時間計測を扱います。
- 各サブコマンドから再利用される機能を、目的ごとに個別モジュールへ分けて案内します。

## Read this when

- `src/commons` にある共通処理の役割分担を把握したいとき。
- `codex` 呼び出し、実行制御、リポジトリ操作、エラー処理、ログ、タイムスタンプ、経過時間計測のどこへ進むべきか整理したいとき。
- `INDEX.md` の生成・更新やサブコマンド実行まわりの共通基盤を確認したいとき。
- 複数のサブコマンドで共有する処理をどのモジュールに置くべきか判断したいとき。

## Do not read this when

- 個別の共通モジュールだけを確認したいときは、このディレクトリの目次ではなく該当する `*.py` を直接読むべきです。
- サブコマンド固有の業務ロジックや CLI 引数だけを確認したいときは、`src/sub_commands` 側を読むべきです。
- `oracles` の仕様断片やユーザー向け手順だけを追いたいときは、このディレクトリではなく `oracles` 側を読むべきです。
- `INDEX.md` の生成・更新ルールそのものだけを確認したいときは、`src/commons/indexing.py` を読むべきです。

## hash

- 5fa52d10d1d5aaa65a8c347b3d9c4f66a0ef424dff9f1158a06656a20a7cfc56

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

- `src/sub_commands` は `cmoc` のサブコマンド実装群の入口です。`__init__.py` がパッケージ宣言を担い、`init.py` と `eval_oracles.py` が単体コマンド本体、`apply/` と `session/` がそれぞれのサブコマンド群をまとめます。
- このディレクトリは、`cmoc init`、`cmoc eval-oracles`、`cmoc apply` 系、`cmoc session` 系の実装ファイルや下位パッケージへ進むための目次です。

## Read this when

- `cmoc` のサブコマンド実装全体の配置と役割分担をまとめて確認したいとき。
- `init.py`、`eval_oracles.py`、`apply/`、`session/` のどこへ進むべきか判断したいとき。
- `src/sub_commands` が Python パッケージとしてどう構成されているかを入口から把握したいとき。
- `apply` や `session` の下位ディレクトリへさらにルーティングしたいとき。

## Do not read this when

- 特定のサブコマンド 1 つの実装や挙動だけを確認したいときは、この目次ではなく該当モジュールを直接読むべきです。
- `cmoc apply` や `cmoc session` の仕様断片だけを確認したいときは、`oracles/app_specs/sub_commands/` 側を読むべきです。
- パッケージ宣言だけを確認したいときは、`__init__.py` を直接見れば足ります。
- `init` や `eval-oracles` の処理順だけを知りたいときは、ここではなく各 `*.py` を読むべきです。

## hash

- ea8309cf02a0e1ed560207da952387c7b00ab02835cf74ac09afb7d90d4d6dd3
