# `commons`

## Summary

- cmoc 全体で共有する基盤処理をまとめた Python パッケージです。
- リポジトリルート探索と branch / worktree / session 状態の扱い、共通例外とエラーレポート整形を含みます。
- Codex CLI 呼び出し、`INDEX.md` メンテナンス、サブコマンドログ、経過時間計測、タイムスタンプ生成、レポートファイル保存などの補助処理を集約しています。

## Read this when

- 複数のサブコマンドで共通に使う処理を実装・修正したいとき。
- リポジトリルート探索、`cmoc/session/*`・`cmoc/apply/*` の branch 判定、worktree 復元、`session` / `apply` 状態保存を確認したいとき。
- エラー整形、ログ出力、時間計測、Codex 実行、`INDEX.md` 生成や更新の共通挙動を追いたいとき。

## Do not read this when

- 個別サブコマンドの引数、状態遷移、業務ロジックだけを確認したいとき。
- `src/commons` 以外のドメイン固有コードや `tests` の実装だけを追いたいとき。
- `INDEX.md` の配置ルール全体や `oracles` の正本仕様だけを確認したいとき。

## hash

- feecba336afe9564f258d664f619e870da97af06fc611ad92b018ac1a3e04013

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

- `src/sub_commands` は `cmoc` の CLI サブコマンド実装をまとめる入口ディレクトリです。
- `__init__.py` によるパッケージ宣言のほか、`init.py`、`apply/`、`session/`、`review/` を束ねます。
- この配下から各サブコマンド本体へ進み、個別の処理順や状態遷移を確認できます。

## Read this when

- `src/sub_commands` 配下でどの実装ファイルを読むべきか整理したいとき。
- `cmoc init`、`cmoc apply`、`cmoc session`、`cmoc review oracles` の入口構造を俯瞰したいとき。
- サブコマンド実装の責務分担や、パッケージとしての構成を確認したいとき。

## Do not read this when

- 個別サブコマンドの引数や状態遷移だけを確認したいときは、各 `apply_*`、`session_*`、`review/oracles.py`、`init.py` を直接読むべきです。
- Python の一般的なパッケージ作法だけを確認したいときは、この目次ではなく実装コードを読むべきです。
- `oracles` 配下の正本仕様や `INDEX.md` 生成ルールだけを確認したいときは、別の仕様文書を読むべきです。

## hash

- 01c034b011e9d6e1cd1dc8f623cdfc00c2be3d8fcc0e4650cde93e27df5478f0
