# `commons`

## Summary

- `src/commons` は、cmoc 全体で再利用する共通処理を集めたディレクトリです。`codex` 呼び出し、CLI サブコマンド共通の実行制御、エラー整形、リポジトリ探索、ログ、タイムスタンプ、経過時間、`INDEX.md` メンテナンスを扱います。
- `__init__.py` はパッケージ宣言だけを担い、他の各モジュールが実装本体です。
- このディレクトリは、個別機能よりも横断的な基盤処理を読む入口として使います。

## Read this when

- サブコマンド横断の実行制御や共通エラー報告の流れを確認したいとき。
- git リポジトリ探索、`cmoc/session/...` と `cmoc/apply/...` の branch 判定、session state path などを確認したいとき。
- tee ログ、タイムスタンプ、経過時間表示、`INDEX.md` 自動メンテナンスなどの共通基盤を見直したいとき。

## Do not read this when

- 特定のサブコマンドの引数や業務ロジックだけを見たいときは、`src/sub_commands` 側の該当モジュールを直接読むべきです。
- 単一の共通ヘルパーの実装だけが必要なときは、`codex.py` などの個別モジュールを直接読むべきで、このディレクトリ全体を読む必要はありません。
- `oracles` や `app_specs` の仕様断片、または利用手順だけを確認したいときは、このディレクトリではなく仕様側を読むべきです。

## hash

- 52ac3ce39e9cbed2091d85253e1f8c04faf8d89f808af7a4580b5d9a6942f3d4

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

- 個別の `cmoc apply` や `cmoc session` の処理内容だけを確認したいときは、それぞれの下位 INDEX や仕様文書を直接読むべきです。
- `cmoc eval-oracles` や `cmoc init` の本体処理だけを確認したいときは、この目次ではなく `eval_oracles.py` や `init.py` を直接読むべきです。
- `src/sub_commands` が Python パッケージとして存在するかだけを確認したいときは、`__init__.py` だけで足ります。
- サブコマンドの仕様断片や利用手順だけを確認したいときは、`oracles/app_specs/sub_commands/` 側を読むべきです。

## hash

- 3121ee5ec647fb9cd2603127bf038475e9ee6394dacf9b6d167fc43c1bd8803c
