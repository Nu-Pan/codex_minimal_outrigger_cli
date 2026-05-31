# `commons`

## Summary

- `src/commons` は cmoc の共通基盤処理を集約したディレクトリの入口です。
- `__init__.py` は `src.commons` をパッケージ化するだけの最小モジュールです。
- `repo.py` は repo root 探索、branch/HEAD 判定、session/apply state、`.cmoc` 配下の保存・検査を担います。
- `errors.py` は共通例外 `CmocError` と stdout 向けエラーレポート整形を提供します。
- `command_runner.py` は Typer サブコマンドの共通実行制御、終了コード処理、完了レポートをまとめます。
- `subcommand_log.py` はサブコマンド呼び出し単位の JSON Lines ログと quota 待ち時間の記録を管理します。
- `timing.py` はステップ開始通知、経過時間計測、表示用 duration 整形を扱います。
- `timestamps.py` は cmoc 仕様の `<time-stamp>` とコンソール用日時文字列を生成・検証します。
- `report_files.py` はタイムスタンプ付き Markdown レポートの排他的生成と保存を担当します。
- `codex.py` は `codex exec` の起動、再試行、Structured Output 検証、oracle 保護を担います。
- `indexing.py` は `INDEX.md` の自動生成・更新・再利用判定と必要時の自動コミットを担当します。

## Read this when

- `src/commons` のどの共通モジュールを参照すべきか素早く切り分けたいとき。
- サブコマンド実装の前に、共有処理・エラー処理・ログ処理の責務分担を確認したいとき。
- クロスカットな基盤処理を修正する前に、関連モジュールの役割を俯瞰したいとき。
- このディレクトリ内で `indexing.py` から `INDEX.md` 生成の仕組みをたどりたいとき。

## Do not read this when

- 個別サブコマンドの入力仕様や業務ロジックだけを確認したいとき。
- `src/commons` のうち 1 ファイルだけの実装詳細を知りたいときは、この目次ではなく該当モジュールを直接読むべきです。
- `oracles` 配下の仕様断片や利用手順だけを確認したいとき。
- README や運用ルールなど、リポジトリ全体の別文書を探したいとき。

## hash

- d0dd5991895c59c23373f8e8190c668e1aa4bfcbb078145708dfff343c9051d7

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

- `cmoc` の個別サブコマンド実装の入口で、`apply`、`session`、`review`、`init` の各モジュールとその下位ディレクトリへ案内するディレクトリです。
- `__init__.py` はパッケージ宣言、`init.py` は `cmoc init` 本体、`apply` と `session` はそれぞれのサブコマンド群、`review` は `cmoc review oracles` の実装入口です。
- 個別実装へ進む前に、どのファイルを読むべきかを素早く切り分けるための目次です。

## Read this when

- `cmoc` の個別サブコマンドの入口をまとめて確認したいとき。
- `apply`、`session`、`review oracles`、`init` のどの実装へ進むべきか整理したいとき。
- サブコマンドごとの目的、入力条件、実行手順、状態遷移、終了条件を俯瞰したいとき。

## Do not read this when

- 個別の `apply`、`session`、`review oracles`、`init` の実装や詳細仕様だけを確認したいときは、この目次ではなく対応するモジュールを直接読むべきです。
- `src/sub_commands` 配下の実装コードやテストコードをそのまま修正したいだけのときは、この目次を読む必要はありません。
- `branch_model`、`codex_call`、ログ、エラーハンドリング、`oracles` 全体の扱いなど、他の共通仕様を確認したいときは別の入口文書を読むべきです。

## hash

- 4fa26ac1ec21851b8cd9d1e92cf2ce63eb59b419bb875f08e6b572f4f33d0fac
