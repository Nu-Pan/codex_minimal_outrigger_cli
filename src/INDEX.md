# `commons`

## Summary

- `src/commons` は、cmoc の各サブコマンドから共通利用される基盤処理をまとめたディレクトリです。
- 実行ラッパー、Codex 呼び出し、Git リポジトリ操作、共通エラー、サブコマンドログ、時間計測、タイムスタンプ生成、レポート保存、`INDEX.md` メンテナンスが入っています。
- サブコマンド実装の土台と、目次文書の自動維持を支える共通モジュール群の入口です。

## Read this when

- cmoc 全体で共有する実行制御、エラー処理、リポジトリ操作、ログ、時間計測、レポート保存、`INDEX.md` 生成の共通処理を確認したいとき。
- サブコマンド本体から呼び出す基盤処理を修正・レビューしたいとき。
- `INDEX.md` のメンテナンス本体や、目次情報の生成・更新ロジックを追いたいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや引数定義だけを確認したいとき。
- `oracles` 配下の正本仕様や運用手順を確認したいとき。
- `README.md` や `AGENTS.md` など、共通基盤ではない説明文書だけを追いたいとき。

## hash

- 520c969165df034a20bac92fa42c87161b34b9e8f738134bf29cb762b0ffecea

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

- 728e3bbfbd277c77e6314ca1a62d4f6cc4fa0cd4d59e6bb6793f6254755a4108
