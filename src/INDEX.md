# `commons`

## Summary

- cmoc の共通処理を集約する Python パッケージです。
- `codex.py`、`indexing.py`、`repo.py`、`errors.py`、`subcommand_log.py`、`timing.py`、`timestamps.py` をまとめ、Codex CLI 実行補助、git と状態管理、エラー整形、`INDEX.md` 維持、ログ、計時、タイムスタンプ生成を担います。
- `__init__.py` はパッケージ宣言のみで、ここでは公開 API や実行ロジックを持ちません。

## Read this when

- サブコマンド間で共通化したい処理や再利用先を探しているとき
- Codex CLI 呼び出し、Structured Output、`INDEX.md` メンテナンスの実装を確認したいとき
- repo root 探索、session/apply state、作業ツリー、共通エラー、ログ、計時、タイムスタンプを横断的に追いたいとき
- `src` 配下の実装で共通基盤の責務分担を把握したいとき

## Do not read this when

- `src/sub_commands` の個別コマンド処理だけを追いたいとき
- 特定のヘルパー 1 つの詳細だけを確認したいときは、そのモジュールを直接読むべきです
- `oracles` 側の上位フローや利用手順だけを確認したいとき
- テストの期待値やユーザー向け案内だけを確認したいとき

## hash

- 7f9eb8af132448178bd3cff3ec0172aa7bee3dcf8ad6216fef15a136a7746499

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
