# `commons`

## Summary

- `src/commons` は cmoc 全体で共有する基盤モジュール群です。
- `codex.py` は Codex CLI 起動、Structured Output 検証、quota/capacity 待機、INDEX メンテナンス、実行ログ保存を扱います。
- `repo.py` は repo root 探索、branch/worktree/session/apply 状態、`.cmoc` の保存先と変更検出を扱います。
- `errors.py`、`timing.py`、`subcommand_log.py`、`timestamps.py`、`report_files.py` は共通例外、計測、JSONL ログ、タイムスタンプ、レポート保存を担当します。

## Read this when

- `src/commons` 配下の共通処理を一覧したいとき。
- `codex.py`、`repo.py`、`errors.py` などの役割分担を確認したいとき。
- `session` / `apply` / ログ / レポート / 時刻まわりの共通仕様を追いたいとき。

## Do not read this when

- 個別サブコマンドの引数や業務ロジックだけを確認したいとき。
- `src/sub_commands` や `tests` の手順・期待値を確認したいとき。
- `INDEX.md` の生成ルールや `oracles` 全体の方針だけを確認したいとき。

## hash

- 5e6473dfa8087ee42cf0e006cfbc44d67d46eecd35514567d459a2c7aee6a6e5

# `main.py`

## Summary

- cmoc CLI のエントリーポイントで、Typer のルート `app` と `session` / `apply` / `review` の各サブアプリを組み立てるファイルです。
- `init`、`session`、`apply`、`review` の各コマンド登録に加えて、`eval-oracle` / `eval-oracles` の隠し別名や各コマンドの既定オプションをまとめています。
- サブコマンド未指定時の `CmocError` 生成、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc CLI の起点と、`session` / `apply` / `review` のサブアプリ構成を確認したいとき。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録名や隠し別名を確認したいとき。
- `apply fork` の繰り返し回数や `scope`、`apply join` の `--force-resolve` など既定オプションを確認したいとき。
- サブコマンド未指定時の利用者向けエラー、補完プローブ時の分岐、Click/Typer 例外の共通整形を追いたいとき。
- `python src/main.py` で直接起動する経路と、そのときの例外処理を確認したいとき。

## Do not read this when

- `src/sub_commands/` 配下の個別サブコマンド本体だけを確認したいとき。
- `commons.errors` の例外型や `format_error_report()` の整形ロジックだけを確認したいとき。
- CLI 登録や補完、例外変換ではなく、各機能の業務ロジックそのものを追いたいとき。
- `INDEX.md` の生成ルールや `oracles` 側の正本仕様だけを確認したいとき。

## hash

- 1a1bb5753238e77dc6df1252d876b3fc6c7cc1706bd8b8499554963755c0a4d7

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc のサブコマンド実装の入口で、`__init__.py`、`init.py`、`review/`、`apply/`、`session/` へ振り分ける目次です。
- `__init__.py` はパッケージ宣言のみ、`init.py` は `cmoc init`、`review/` は `cmoc review` 系、`apply/` と `session/` はそれぞれ個別の `INDEX.md` を持つ入口です。
- このディレクトリの目次は、個別サブコマンドの詳細へ入る前に、どの実装ファイルを開くべきかを素早く判断するための案内です。

## Read this when

- `src/sub_commands` 配下で、どのファイルやディレクトリがどのサブコマンドを担当するか確認したいとき。
- サブコマンド実装・修正・レビュー・テストの前に、該当モジュールや配下ディレクトリへ進む入口を整理したいとき。
- `__init__.py`、`init.py`、`review/`、`apply/`、`session/` の役割分担を素早く把握したいとき。

## Do not read this when

- 個別サブコマンドの引数、状態遷移、例外条件だけを確認したいとき。
- `apply/` や `session/` のさらに細かい仕様だけを確認したいとき。
- `src/commons` や `oracles` 全体の共通仕様だけを確認したいとき。

## hash

- 25fa5849ed06c2b67386ba01abd228a511913ff7d385869e8c3b30e0a85734a4
