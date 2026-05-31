# `commons`

## Summary

- `src/commons` は cmoc で共有する基盤モジュール群をまとめたディレクトリです。
- `errors.py` は共通例外とエラーレポート整形、`repo.py` は Git リポジトリや cmoc 作業領域の判定と state 管理を担当します。
- `codex.py` は Codex CLI 実行基盤、`indexing.py` は `INDEX.md` の自動メンテナンス、`subcommand_log.py` はサブコマンド単位のログ管理を担当します。
- `command_runner.py` と `timing.py` はサブコマンドの実行制御と時間計測を、`timestamps.py` と `report_files.py` はタイムスタンプ生成とレポート保存を担当します。
- `__init__.py` は `src.commons` を Python パッケージとして宣言します。

## Read this when

- cmoc 全体で共有する基盤処理を把握したいときに読む。
- repo root 探索、branch / commit 判定、session / apply state、worktree パス復元など Git 周りの共通処理を確認したいときに読む。
- `codex exec` の呼び出し、Structured Output の検証、quota / capacity の再試行、`INDEX.md` メンテナンスや oracle 保護を確認したいときに読む。
- サブコマンドの共通実行制御、エラー整形、JSON Lines ログ、ステップ計測、timestamp 生成、タイムスタンプ付きレポート保存の実装を確認したいときに読む。
- 共通モジュール同士の依存関係や、どの責務をどのファイルが持つかを最短で見たいときに読む。

## Do not read this when

- 個別のサブコマンド実装や引数解析だけを追いたいときは、このディレクトリではなく `src/sub_commands` 側を読む。
- `codex exec` の詳細な起動・再試行・Structured Output 仕様だけを確認したいときは、`codex.py` だけを読む。
- Git リポジトリ状態や cmoc の作業ブランチ・state の仕様だけを確認したいときは、`repo.py` を読む。
- `INDEX.md` の配置ルールやメンテナンス方針の正本仕様だけを確認したいときは、`oracles/docs/app_specs/indexing.md` を読む。
- テストコードや他のパッケージの実装を探したいときは、このディレクトリではなく対象の `tests` や別モジュールを読む。

## hash

- e1dc6b06c7369e21bc2481d8a73423e009f5c88c2eb120ef21c0e8bf261e2d01

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

- `src/sub_commands` は `cmoc` のサブコマンド実装の入口で、`__init__.py` によるパッケージ宣言、`init.py` による `cmoc init`、および `apply/`・`session/`・`review/` の各系統への入口をまとめるルーティング用ディレクトリです。
- この目次は、個別サブコマンドの実装へ進む前に、どのファイルや下位ディレクトリを読むべきかを振り分けるための案内です。

## Read this when

- `cmoc` のどのサブコマンド実装がこの配下にあるかを俯瞰したいとき。
- `init`、`apply`、`session`、`review` のうち、どの入口ファイルや配下ディレクトリを読むべきか整理したいとき。
- `src/sub_commands` が Python パッケージとして成立していることや、各サブコマンドの入口構造を確認したいとき。

## Do not read this when

- 個別サブコマンドの引数、状態遷移、終了条件などの詳細仕様だけを確認したいときは、各実装ファイルか `oracles/docs/app_specs/sub_commands/` 側を読むべきです。
- `cmoc` 全体の使い方や開発ルールだけを確認したいときは、このディレクトリではなく上位の案内文書を参照すべきです。
- `src/sub_commands` のパッケージ宣言だけを確認したいときは、この目次ではなく `__init__.py` を直接読むべきです。

## hash

- 64ed138cfb1cfa275503e239f8f5378e7557a32803a636d0a557f07cb83cf22c
