# `commons`

## Summary

- `cmoc` の共有基盤モジュール群をまとめたディレクトリです。`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`subcommand_log.py`、`timestamps.py`、`timing.py`、`__init__.py` を含みます。
- Codex CLI 呼び出し、共通エラー、git リポジトリ操作、サブコマンドログ、経過時間計測、タイムスタンプ生成、`INDEX.md` 自動更新を支えます。
- サブコマンド実行の土台となる横断的な処理をここに集約しています。

## Read this when

- `codex exec` 呼び出しや Structured Output 検証を追いたいとき。
- CLI 共通の実行ラッパー、エラー整形、終了コード、ログ、計測、repo 探索を確認したいとき。
- `INDEX.md` の生成・更新ルールや除外条件を確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや引数定義だけを確認したいとき。
- `oracles` の仕様断片やユーザー向け手順だけを追いたいとき。
- 共有処理ではなく、特定機能の実装詳細だけが必要なとき。

## hash

- 8966e867ef9449b1b2c3ce2356ed66e759d3b2d6a1384403ad4fc15f2f299eda

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

- `src/sub_commands` は `cmoc` のサブコマンド実装群の入口です。
- `__init__.py` はパッケージ宣言のみを担い、`apply` と `session` はそれぞれ専用のサブディレクトリに分かれています。
- `eval_oracles.py` は `cmoc eval-oracles` の本体、`init.py` は `cmoc init` の本体です。
- この目次から、`apply/INDEX.md` と `session/INDEX.md` へ進んで、それぞれの詳細実装へたどれます。

## Read this when

- `src/sub_commands` 配下のサブコマンド実装全体を、どのファイルに何があるかという観点で把握したいとき。
- `apply`、`session`、`eval-oracles`、`init` の実装入口をまとめて整理したいとき。
- 各サブコマンドの個別モジュールへ進む前に、役割分担と配置方針を確認したいとき。
- `src/sub_commands` 以下の入口案内として、どの INDEX や実装ファイルへ進むべきかを判断したいとき。

## Do not read this when

- 個別の `cmoc apply` 実装だけを確認したいときは、この目次ではなく `apply/INDEX.md` を直接読むべきです。
- 個別の `cmoc session` 実装だけを確認したいときは、この目次ではなく `session/INDEX.md` を直接読むべきです。
- `cmoc eval-oracles` や `cmoc init` の処理内容だけを確認したいときは、この目次ではなく `eval_oracles.py` や `init.py` を直接読むべきです。
- `src/sub_commands` が Python パッケージとして宣言されているかだけを確認したいときは、`__init__.py` だけで足ります。

## hash

- 9a0d7d5af087c5fc768acb3eb8b4da92f8ed61023ed700b0b122876c877e170c
