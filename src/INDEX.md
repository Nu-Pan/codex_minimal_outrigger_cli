# `commons`

## Summary

- `cmoc` のサブコマンド群で共通利用する基盤モジュールをまとめたディレクトリです。
- `__init__.py` は `src.commons` パッケージ宣言だけを行う最小モジュールです。
- `codex.py` が `codex exec` の起動、Structured Output 検証、再試行、quota 待機、INDEX メンテナンス連携を担当します。
- `command_runner.py`、`errors.py`、`subcommand_log.py`、`timing.py`、`timestamps.py`、`report_files.py` が実行制御、エラー整形、ログ、計測、時刻、レポート保存を支えます。
- `indexing.py` が `INDEX.md` の自動維持と再生成を担います。
- `repo.py` が repo root 探索、branch / state 判定、`git` 補助、apply process 保存を担当します。

## Read this when

- `cmoc` の共通処理を横断的に確認・修正したいとき。
- `repo.py` の repo root 探索、branch / state 判定、`git` 補助、runtime 保存の挙動を追いたいとき。
- `codex.py` の `codex exec` 実行、Structured Output 検証、再試行、quota 待機、INDEX メンテナンス連携を理解したいとき。
- `indexing.py` の `INDEX.md` 生成・更新・再利用判定・自動コミットの流れを確認したいとき。
- `subcommand_log.py`、`timing.py`、`timestamps.py`、`errors.py`、`report_files.py` の横断処理を追いたいとき。

## Do not read this when

- 個別サブコマンド `apply` / `session` / `review` / `init` の業務ロジックだけを確認したいときは、`src/sub_commands` 側を読むべきです。
- `cmoc` の利用手順や `oracles` 側の仕様断片だけを見たいときは、このディレクトリではなく `oracles/docs/app_specs/` 側を参照すべきです。
- `INDEX.md` の生成ルールだけを確認したいときは、このディレクトリではなく `indexing.py` を直接読むべきです。
- `__init__.py` のような package marker や、`__pycache__` などの生成物だけを確認したいときは、この目次を読む必要はありません。

## hash

- d5e41c1a835580022e6e13766e2f0ed30a039f4da3f1c7922953298af19ef7b9

# `main.py`

## Summary

- cmoc CLI のエントリーポイントで、Typer のルート `app` と `session` / `apply` / `review` の各サブアプリを組み立てるファイルです。
- `init`、`session`、`apply`、`review` の各コマンド登録に加えて、`eval-oracle` / `eval-oracles` の隠し別名や、`apply fork` の繰り返し回数・`scope`、`apply join` の `--force-resolve` などの既定値をまとめています。
- サブコマンド未指定時の `CmocError` 生成、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc CLI の起動点と、`session` / `apply` / `review` のサブアプリ構成を確認したいとき。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録名、隠し別名、既定オプションを確認したいとき。
- サブコマンド未指定時の利用者向けエラー、補完プローブ時の分岐、Click/Typer 例外の共通整形を追いたいとき。
- `python src/main.py` で直接起動する経路と、そのときの例外処理を確認したいとき。

## Do not read this when

- `src/sub_commands/` 配下の各サブコマンド本体の実装だけを追いたいとき。
- `commons.errors` のエラー型や `format_error_report()` の整形ロジックだけを確認したいとき。
- `INDEX.md` の生成ルールや `oracles` 側のルーティング方針だけを確認したいとき。

## hash

- 34ab9fdae7d4622e261437958669dd52ce211f233a2300c1c7c831efc256c365

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc の各サブコマンド実装を束ねる入口ディレクトリで、`__init__.py`、`init.py`、`apply/`、`review/`、`session/` を案内します。
- `__init__.py` はパッケージ宣言のみを担い、`init.py` は `cmoc init` の本体処理を担います。
- `apply/`、`review/`、`session/` はそれぞれ apply / review / session 系サブコマンドの入口目次です。

## Read this when

- `src/sub_commands` 配下のどの入口ファイルやサブディレクトリを読むべきか切り分けたいとき。
- `cmoc init` の本体や、`apply` / `review` / `session` 系の責務分担を俯瞰したいとき。
- `src/sub_commands` がパッケージ入口としてどう構成されているか確認したいとき。

## Do not read this when

- `src/sub_commands/init.py` の個別処理や `apply/join` などの詳細実装を追いたいとき。
- `review oracles` や `session` / `apply` の仕様断片を直接確認したいときは、各配下の仕様書を読むべきです。
- `src/sub_commands` ではなく、CLI 登録や共通基盤だけを確認したいとき。

## hash

- 8c91c2396f302826bbe9d1ce2fd39109ecfae119ba96a3301ce8d2052376944a
