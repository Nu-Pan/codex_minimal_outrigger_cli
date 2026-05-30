# `commons`

## Summary

- `src/commons` は、cmoc の各サブコマンドから共通利用される基盤処理をまとめたディレクトリです。
- 実行ラッパー、Codex 呼び出し、Git リポジトリ操作、共通エラー、サブコマンドログ、時間計測、タイムスタンプ生成、レポート保存、`INDEX.md` メンテナンスが入っています。
- サブコマンド実装の土台と、目次文書の自動維持を支える共通モジュール群の入口です。

## Read this when

- cmoc 全体で共有する実行制御、Codex 呼び出し、Git 操作、エラー整形、ログ記録、時間計測、レポート保存を確認したいとき。
- サブコマンド本体から呼び出す共通処理の役割分担や依存関係を整理したいとき。
- `INDEX.md` のメンテナンス本体や、目次情報の生成・更新ロジックを追いたいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや引数定義だけを確認したいとき。
- `oracles` 配下の正本仕様や運用手順だけを確認したいとき。
- `README.md` など、共通基盤ではない説明文書だけを追いたいとき。

## hash

- 8a44caf23fa8f57d2194a8092867be9d6db87d2631306324987a5f1b36913dcd

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

- `src/sub_commands` は `cmoc` のサブコマンド実装群をまとめるパッケージです。
- `__init__.py` はパッケージ宣言だけを担い、`init.py` は `cmoc init`、`eval_oracles.py` は `cmoc review oracles`、`apply/` と `session/` は各系サブコマンドの入口です。
- ここは実装入口の全体地図であり、個別の詳細仕様は各モジュールや下位の `INDEX.md` に分かれています。

## Read this when

- `src/sub_commands` 配下で、どのモジュールがどのサブコマンドを担当するか把握したいとき。
- `cmoc init`、`cmoc review oracles`、`cmoc apply`、`cmoc session` の実装入口を見分けたいとき。
- このパッケージ配下の実装・修正・レビュー・テストを始める前に、関連ファイルの役割を整理したいとき。

## Do not read this when

- `cmoc init`、`cmoc review oracles`、`cmoc apply`、`cmoc session` の個別仕様だけを確認したいとき。
- `src/sub_commands` 配下の実装コードやテストコードを直接修正するだけで足りるとき。
- `INDEX.md` の生成ルールや `oracles` 全体のルーティング方針だけを確認したいとき。

## hash

- beea7528881a9cb9942e2ee24f3feb6bf2638b7a5776bcb1aae900f6a1ee58f9
