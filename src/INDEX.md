# `commons`

## Summary

- cmoc の共通処理を集めた `src/commons` パッケージの入口です。
- `codex` 実行、サブコマンド実行制御、git/セッション状態、ログ、レポート保存、エラー整形、タイムスタンプ生成、`INDEX.md` 更新の共通機能をまとめています。
- `__init__.py` はパッケージ宣言のみで、公開 API は各モジュール側にあります。

## Read this when

- サブコマンドや共通処理の実装で、どの共有モジュールに責務があるか素早く確認したいとき。
- `codex.py`、`command_runner.py`、`repo.py`、`subcommand_log.py`、`report_files.py`、`errors.py`、`timestamps.py`、`indexing.py` のどれを読むべきか判断したいとき。
- 共通ユーティリティを新規追加・修正するときに、既存の分担を俯瞰したいとき。

## Do not read this when

- 個別サブコマンドの入力・状態遷移・終了条件だけを確認したいとき。
- アプリ全体のワークフローや `oracles` の正本仕様だけを確認したいとき。
- 実装コードやテストコードの詳細だけを追いたいとき。

## hash

- 33505a5ed390c6edb0bcbceaf8ca9ae12b519cc2ce4e39b2acdc90c1703a32ed

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

- `src/sub_commands` は `cmoc` のサブコマンド実装群をまとめるパッケージで、`__init__.py`、`init.py`、`eval_oracles.py`、`apply/`、`session/` に役割が分かれています。
- `__init__.py` はパッケージ宣言だけを担い、`init.py` は `cmoc init`、`eval_oracles.py` は `cmoc review oracles`、`apply/` と `session/` は各系サブコマンドの入口です。
- ここは実装入口の全体地図であり、個別の詳細仕様は各モジュールや下位の `INDEX.md` に分かれています。

## Read this when

- `src/sub_commands` 配下で、どのモジュールがどのサブコマンドを担当するか把握したいとき。
- `cmoc init`、`cmoc review oracles`、`cmoc apply`、`cmoc session` の実装入口を見分けたいとき。
- このパッケージ配下の実装・修正・レビュー・テストを始める前に、関連ファイルの役割を整理したいとき。
- `src/sub_commands` が Python パッケージとして宣言されていることと、下位パッケージが分割されていることを確認したいとき。

## Do not read this when

- `cmoc init`、`cmoc review oracles`、`cmoc apply`、`cmoc session` の詳細仕様や状態遷移だけを確認したいとき。
- `src/sub_commands` のパッケージ宣言だけを確認したいときは、`__init__.py` を直接見れば足ります。
- `INDEX.md` の生成ルールや `oracles` 全体のルーティング方針だけを確認したいとき。

## hash

- d7fab01fd79e8a0f84379de45b1b90cdd239a4355f3705788300f88cf27d95da
