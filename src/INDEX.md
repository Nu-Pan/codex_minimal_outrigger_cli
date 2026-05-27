# `commons`

## Summary

- `src/commons` 配下の共有モジュールをまとめた入口で、`codex`、`command_runner`、`errors`、`indexing`、`repo`、`subcommand_log`、`timestamps`、`timing` への案内を提供します。
- 各サブコマンドで共通利用される実行制御、エラー整形、リポジトリ探索、ログ保存、タイムスタンプ生成、時間計測の担当範囲を整理するための目次です。
- 個別実装へ進む前に、どの共通機能がどのファイルにあるかを素早く判断するためのルーティング文書です。

## Read this when

- `src/commons` に置かれた共通ユーティリティの全体像を確認したいとき。
- 共有エラー処理、リポジトリ探索、ログ出力、タイムスタンプ生成、経過時間計測のどこへ進むべきか整理したいとき。
- 各サブコマンドで共通利用される機能の入口をまとめて把握したいとき。
- `src/commons` 配下の個別モジュールへたどる前に、役割分担を先に確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックだけを確認したいときは、`src/sub_commands` 側を直接読むべきです。
- `codex exec` や `apply` など、`src/commons` 以外の機能の仕様だけを確認したいときは、この目次を読む必要はありません。
- 特定の共有モジュールの実装詳細を知りたいときは、`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` を直接参照すべきです。
- `INDEX.md` の生成・更新ルールそのものだけを確認したいときは、`src/commons/indexing.py` を読むべきです。

## hash

- 2adb2bce9291af358a5cdecb51f152bf8de10f8c3aa468f1cb03120bedc6bfd1

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

- `src/sub_commands` は cmoc のサブコマンド実装群の入口です。`__init__.py` はパッケージ宣言のみで、`apply` と `session` は専用サブディレクトリに分かれています。
- `eval_oracles.py` は `cmoc eval-oracles` の本体、`init.py` は `cmoc init` の本体です。
- この目次から `apply/INDEX.md` と `session/INDEX.md` へ進み、各サブコマンドの詳細実装へたどれます。

## Read this when

- `src/sub_commands` 配下の実装入口をまとめて確認したいとき。
- `apply`、`session`、`eval-oracles`、`init` の実装ファイルがどこにあるか整理したいとき。
- 個別モジュールへ入る前に、サブコマンド群の役割分担と配置方針を把握したいとき。
- `apply/INDEX.md` や `session/INDEX.md` へ進むべきか判断したいとき。

## Do not read this when

- `cmoc apply` や `cmoc session` の個別処理だけを確認したいときは、この目次ではなく各下位 `INDEX.md` を直接読むべきです。
- `cmoc eval-oracles` や `cmoc init` の本体処理だけを確認したいときは、この目次ではなく `eval_oracles.py` や `init.py` を直接読むべきです。
- `src/sub_commands` が Python パッケージとして存在するかだけを確認したいときは、`__init__.py` だけで足ります。
- サブコマンドの仕様断片や利用手順だけを確認したいときは、`oracles/app_specs/sub_commands/` 側を読むべきです。

## hash

- c38b9eefb1ca26896d06bc808b4c27f0dec659f5d4fff50c7c5d7e7b591cab81
