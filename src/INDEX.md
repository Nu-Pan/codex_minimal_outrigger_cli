# `commons`

## Summary

- `cmoc` の各サブコマンドから共通利用される基盤処理をまとめたディレクトリです。
- 実行ラッパー、Codex 呼び出し、Git リポジトリ操作、共通エラー、サブコマンドログ、時間計測、タイムスタンプ生成、レポート保存、`INDEX.md` 目次維持が入っています。
- サブコマンド実装の土台と、目次文書の自動維持を支える共通モジュール群の入口です。

## Read this when

- `cmoc` 全体で共有する実行制御、エラー整形、Git 操作、ログ記録の役割分担を把握したいとき。
- `codex exec` 呼び出し、`INDEX.md` 生成・維持、レポート保存、タイムスタンプ生成の共通処理を確認したいとき。
- サブコマンド本体の土台になるユーティリティ群の入口をまとめて見たいとき。

## Do not read this when

- 個別サブコマンドの引数解析や業務ロジックだけを確認したいとき。
- `src/sub_commands` 側の実装や各コマンドの実行フローだけを追いたいとき。
- `oracles` 配下の正本仕様や運用手順だけを確認したいとき。

## hash

- 70ff3c924c8ffd5f7a868ca72c53bac80361aa4256253209aa91510602584892

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

- `cmoc` の個別サブコマンド実装への入口です。
- `apply/` と `session/` の各パッケージ、`init.py`、`eval_oracles.py`、`__init__.py` をまとめて案内します。
- 各コマンド本体の配置先を素早く選べるようにする目次です。

## Read this when

- `src/sub_commands` 配下で、どのモジュールがどのサブコマンドを担当しているか整理したいとき。
- `apply`、`session`、`init`、`review oracles` の実装入口を一覧したいとき。
- `src/sub_commands` のパッケージ構造と、各入口ファイルへの導線を確認したいとき。

## Do not read this when

- 個別の `cmoc apply fork/join/abandon` や `cmoc session fork/join/abandon` の詳細仕様だけを確認したいとき。
- `cmoc review oracles` の評価条件や出力仕様だけを追いたいとき。
- 共通仕様や `oracles` 配下の正本断片だけを確認したいとき。

## hash

- 47c5b8acb94db4eda4a37758a044fcca71e0ed0a5202ebfee9fd1554a327da5a
