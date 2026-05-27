# `commons`

## Summary

- `cmoc` の共通処理をまとめるディレクトリの入口です。
- `codex` 呼び出し、実行制御、リポジトリ探索と状態管理、共通エラー処理、`INDEX.md` 生成、サブコマンドログ、タイムスタンプ、経過時間計測を扱います。
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

- 0f7641a806f929f25ff8646c88b9de48ca9bc327e61aba29b460738447b1da8f

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

- `src/sub_commands` は `cmoc` のサブコマンド実装をまとめる入口ディレクトリです。
- `__init__.py` は `src.sub_commands` パッケージ宣言だけを担います。
- `apply/` は `cmoc apply` 系の実装入口で、`fork` / `join` / `abandon` をたどれます。
- `session/` は `cmoc session` 系の実装入口で、`fork` / `join` / `abandon` をたどれます。
- `init.py` は `cmoc init`、`eval_oracles.py` は `cmoc eval-oracles` の本体処理です。

## Read this when

- `src/sub_commands` 配下のどの実装モジュールへ進むべきか整理したいとき。
- `cmoc` のサブコマンド構成を俯瞰して、`apply` / `session` / `init` / `eval-oracles` の入口を確認したいとき。
- このディレクトリが Python パッケージとしてどう分かれているか把握したいとき。
- 個別サブコマンドの実装本文を読む前に、まずルーティング先を判断したいとき。

## Do not read this when

- `cmoc apply fork/join/abandon` の具体的な処理順や状態遷移だけを知りたいときは、`apply/` 配下の個別モジュールを直接読むべきです。
- `cmoc session fork/join/abandon` の個別処理だけを知りたいときは、`session/` 配下の個別モジュールを直接読むべきです。
- `cmoc init` や `cmoc eval-oracles` の実装詳細だけを知りたいときは、`init.py` や `eval_oracles.py` を直接読むべきです。
- パッケージ宣言の有無だけを確認したいときは、`__init__.py` だけを読めば足ります。

## hash

- 7f0f90de7defe594cf5b862cc9caf3eb22eefd083a148bfd4a876137087c73e0
