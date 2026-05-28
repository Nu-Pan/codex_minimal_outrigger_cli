# `commons`

## Summary

- `cmoc` 全体で共有する基盤モジュール群の入口で、`codex` 呼び出し、`git` リポジトリ探索、共通エラー処理、サブコマンドログ、タイムスタンプ、経過時間計測、`INDEX.md` メンテナンスをまとめます。
- `__init__.py` はパッケージ宣言のみを担い、`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` へ案内します。
- サブコマンド本体ではなく、複数の機能から再利用される共通処理の参照先を整理するためのディレクトリ目です。

## Read this when

- `src/commons` にどの共通機能がまとまっているか、パッケージ全体の役割を確認したいとき。
- `codex exec` 呼び出し、`<repo-root>` 探索、共通エラー整形、サブコマンドログ、タイムスタンプ、経過時間表示、`INDEX.md` メンテナンスの関連先を整理したいとき。
- サブコマンド間で共有する基盤処理をどこに置くべきか、また既存の共通モジュールに何があるかを見直したいとき。
- `cmoc` の共通処理を実装・修正・レビューするときに、読むべき入口をまとめて把握したいとき。

## Do not read this when

- 個別サブコマンドの引数解析や業務ロジックだけを確認したいときは、この配下ではなく `src/sub_commands` を読むべきです。
- `codex exec` だけ、`git` だけ、ログだけ、タイムスタンプだけのように、特定の共通処理を単独で確認したいときは該当モジュールへ直接進むべきです。
- `INDEX.md` の生成・更新ルールそのものだけを確認したいときは、`oracles/app_specs/indexing.md` を読むべきです。
- 実装コードやテストコードだけで足りる場合は、このディレクトリの目次を読む必要はありません。

## hash

- 50545c0686b1d9da3efe4396141bc01f6cc3f44c54a8ad0b3d5119043555011c

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

- `cmoc` の個別サブコマンド実装群の入口で、`__init__.py`、`apply`、`session`、`eval_oracles.py`、`init.py` への案内をまとめるディレクトリです。
- `apply` と `session` はそれぞれ専用パッケージに分かれ、`eval-oracles` と `init` は単独モジュールとして置かれています。
- ここでは実装の役割分担と進み先だけを整理し、具体的な処理は各モジュールに委ねます。

## Read this when

- `src/sub_commands` 配下のどの実装を読むべきか切り分けたいとき。
- `cmoc apply`、`cmoc session`、`cmoc eval-oracles`、`cmoc init` の本体実装へ直接進みたいとき。
- サブコマンドごとの責務分担や入口を俯瞰したいとき。
- 新しい処理を追加・修正するときに配置先を確認したいとき。

## Do not read this when

- `apply`、`session`、`eval-oracles`、`init` のうち特定の 1 つだけの処理詳細を確認したいときは、該当モジュールを直接読むべきです。
- ユーザー向けの利用手順や正本仕様だけを見たいときは、`oracles/app_specs/sub_commands/` 側を読むべきです。
- CLI のエントリーポイントや引数定義だけを確認したいときは、`src/main.py` を読むべきです。
- 共通ユーティリティやエラーハンドリングだけを見たいときは、`src/commons/` を読むべきです。

## hash

- c370780a251e9beb8c8e963cea58f4aab3fbbcc4e6454737c18f9f2ab782514c
