# `commons`

## Summary

- `src/commons` は cmoc 全体で再利用する共通基盤をまとめたパッケージで、Codex 呼び出し、実行ラッパー、共通エラー、repo 探索、ログ、レポート保存、タイムスタンプ、経過時間計測を扱います。
- この配下の各モジュールは個別サブコマンドではなく、複数コマンドから共通利用される実装です。
- 主要ファイルは `codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` と `__init__.py` です。

## Read this when

- 共通の実行制御、エラー整形、ログ、計測、レポート保存の仕組みを確認したいとき。
- repo ルート探索、session/apply の state、branch 判定、`oracles` や `INDEX.md` の保守ルールを追いたいとき。
- Codex CLI 呼び出しや Structured Output 検証、`INDEX.md` 生成・更新の共通処理を見直したいとき。
- `src/commons` 配下のどのモジュールを読むべきかを先に整理したいとき。

## Do not read this when

- 個別サブコマンドの引数、状態遷移、業務ロジックだけを確認したいとき。
- `src/sub_commands` 側の実装やテストだけを追いたいとき。
- 共通モジュールではなく、コマンド別の仕様断片だけを読みたいとき。
- すでに特定の共通モジュール名が分かっていて、そのモジュールを直接読む段階にあるとき。

## hash

- 3add487965a58566630cfe65437814a6ed43c97b7c4c4c459b9b929cf31f7287

# `main.py`

## Summary

- cmoc CLI のエントリーポイントで、Typer のルート app と `session` / `apply` / `review` のサブアプリを組み立てます。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録と、それぞれのオプション既定値やエイリアスをまとめます。
- サブコマンド未指定時の利用者向けエラー、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc の起動点やサブコマンド登録を修正・レビューしたいとき。
- `init` / `session` / `apply` / `review` のコマンド名、エイリアス、オプション既定値を確認したいとき。
- サブコマンドなし起動時の利用者向けエラー、終了コード、`--help` への誘導を確認したいとき。
- `python src/main.py` で直接起動する経路と、その例外ハンドリングを確認したいとき。

## Do not read this when

- 各サブコマンドの本体ロジックや `src/sub_commands/` 配下の処理だけを確認したいとき。
- 共通エラー型や `format_error_report` の整形仕様だけを確認したいとき。
- `INDEX.md` の生成ルールや共通ユーティリティの設計だけを追いたいとき。

## hash

- 725244cd04649c14efdc472340862818b2eabfb76416af919258408edf3121cc

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc のサブコマンド実装の入口で、`__init__.py`、`init.py`、`eval_oracles.py`、`apply/`、`session/` を含みます。
- `init.py` は `cmoc init`、`eval_oracles.py` は `cmoc review oracles` を担当します。
- `apply/` と `session/` は、それぞれ apply 系・session 系サブコマンドをまとめたサブパッケージです。

## Read this when

- `src/sub_commands` 配下にどのサブコマンド実装が置かれているかを俯瞰したいとき。
- `cmoc init`、`cmoc review oracles`、`cmoc apply`、`cmoc session` の入口を素早く見分けたいとき。
- このディレクトリが Python パッケージとして宣言され、個別コマンド実装とサブパッケージに分かれていることを確認したいとき。

## Do not read this when

- `cmoc init` や `cmoc review oracles` の個別実装だけを確認したいときは、各モジュールを直接読むべきです。
- `cmoc apply` や `cmoc session` の配下の詳細仕様や処理順を確認したいときは、それぞれの子ディレクトリの `INDEX.md` を読むべきです。
- `src/sub_commands` のパッケージ宣言だけを確認したいときは、`__init__.py` を直接見れば足ります。

## hash

- 4a44f7ece48a1e788e7e6d51cd5391778d3ee926f1c8268b1f78143c6527a766
