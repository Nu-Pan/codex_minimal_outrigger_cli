# `commons`

## Summary

- cmoc で共通利用する基盤ユーティリティ群をまとめたディレクトリです。`codex exec` 呼び出し、サブコマンド共通制御、`<repo-root>` 解決、共通例外、ログ、時間計測、タイムスタンプ、レポート保存、`INDEX.md` メンテナンスを扱います。
- 個別サブコマンド本体ではなく、実行基盤や横断処理を共通化するモジュール群が中心です。

## Read this when

- CLI 共通制御やエラー整形、終了コードの扱いを追いたいとき。
- `codex exec` の起動、Structured Output の検証、`INDEX.md` の自動保守を確認したいとき。
- `<repo-root>` 探索、git 共通処理、サブコマンドログ、時間計測、タイムスタンプ生成、レポート保存の挙動を確認したいとき。
- `src/commons` 配下の各モジュールがどの役割を担うか整理したいとき。

## Do not read this when

- 個別サブコマンドの引数、状態遷移、業務ロジックだけを確認したいとき。
- `src/commons` 以外の実装やテストを確認したいとき。
- `INDEX.md` の生成ルールそのものや `oracles` 側の正本仕様だけを確認したいとき。

## hash

- 3193880661db19a317b434a38c88e60c79f06fbe2671e0644b1c066d35647ea6

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

- `src/sub_commands` は cmoc のサブコマンド実装を束ねる入口ディレクトリです。
- `__init__.py` はパッケージ宣言のみを担い、`init.py` は `cmoc init` の本体処理を実装します。
- `apply`、`review`、`session` はそれぞれ `cmoc apply`、`cmoc review`、`cmoc session` 系の実装入口です。
- 個別サブコマンドの詳細は、各配下の `INDEX.md` へ進んで確認します。

## Read this when

- `src/sub_commands` 配下で、どのファイルがどの `cmoc` コマンドを担当しているか整理したいとき。
- `cmoc init`、`cmoc apply`、`cmoc review`、`cmoc session` の実装入口を先に把握したいとき。
- 各機能の詳細実装へ進む前に、関連モジュールの位置関係を確認したいとき。

## Do not read this when

- `cmoc apply`、`cmoc session`、`cmoc review oracles`、`cmoc init` の個別処理や例外条件を深掘りしたいときは、この目次ではなく各実装モジュールを直接読むべきです。
- `src/sub_commands` のパッケージ宣言だけを確認したいときは、`__init__.py` を直接読むべきです。
- `oracles` 側の正本仕様や `INDEX.md` の生成ルールだけを確認したいときは、この目次を読む必要はありません。

## hash

- 6312caa3f61e2578e8466a46c1f44a23d9285583a01127e8570afbea11284e2e
