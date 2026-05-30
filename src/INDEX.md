# `commons`

## Summary

- `cmoc` の各サブコマンドから共通利用される基盤処理をまとめたディレクトリです。
- 実行ラッパー、Codex 呼び出し、Git リポジトリ操作、共通エラー、サブコマンドログ、時間計測、タイムスタンプ生成、レポート保存、`INDEX.md` 目次維持が入っています。
- サブコマンド実装の土台と、目次文書の自動維持を支える共通モジュール群の入口です。

## Read this when

- cmoc 全体で共有する実行制御、エラー整形、Git 操作、ログ記録の役割分担を把握したいとき。
- `codex exec` 呼び出し、`INDEX.md` 生成・維持、レポート保存、タイムスタンプ生成の共通処理を確認したいとき。
- サブコマンド本体の土台になるユーティリティ群の入口をまとめて見たいとき。

## Do not read this when

- 個別サブコマンドの引数解析や業務ロジックだけを確認したいとき。
- `src/sub_commands` 側の実装や各コマンドの実行フローだけを追いたいとき。
- `oracles` 配下の正本仕様や運用手順だけを確認したいとき。

## hash

- 22f976ff2aecaba547007c41e07a03a0305957d597401236374a05dd05319740
<!-- cmoc-index-kind: directory -->

# `main.py`

## Summary

- cmoc CLI のエントリーポイントで、Typer のルート app と `session` / `apply` / `review` のサブアプリを組み立てます。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録と、それぞれのオプション既定値やエイリアスをまとめます。
- サブコマンド未指定時の利用者向けエラー、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc の起動点やサブコマンド登録の全体像を確認したいとき。
- `init`、`session`、`apply`、`review` のコマンド名、エイリアス、既定値を確認したいとき。
- サブコマンド未指定時の利用者向けエラーや終了コードの扱いを確認したいとき。
- `python src/main.py` で直接起動する経路と、その例外ハンドリングを確認したいとき。

## Do not read this when

- `src/sub_commands/` 配下の各サブコマンド本体の処理だけを確認したいとき。
- 共通エラー型やエラーレポート整形の詳細だけを確認したいとき。
- `INDEX.md` の生成ルールや共通ユーティリティの設計だけを追いたいとき。

## hash

- 17a01bf5b24f9947a86117e0ba85c891287ad99e26a1f7e625772b3eaa746447
<!-- cmoc-index-kind: file -->

# `sub_commands`

## Summary

- `cmoc` のサブコマンド実装をまとめるパッケージで、`__init__.py`、`init.py`、`eval_oracles.py` と `apply/`、`session/` の入口を持ちます。
- `cmoc init`、`cmoc review oracles`、`cmoc apply`、`cmoc session` の各実装を辿るときのルーティング起点です。
- 個別サブコマンドの実処理は各モジュール配下に分かれており、このディレクトリ自体は全体の入口として機能します。

## Read this when

- `cmoc` のサブコマンド実装全体の配置と役割分担を把握したいとき。
- `init`、`review oracles`、`apply`、`session` のどの実装ファイルへ進むべきか整理したいとき。
- 新しいサブコマンドを追加したり、既存サブコマンドの入口を確認したいとき。

## Do not read this when

- `commons` 配下の共通処理や Git・報告・計測の詳細だけを確認したいとき。
- `oracles` 配下の仕様断片そのものや、`INDEX.md` の生成ルールだけを確認したいとき。
- 対象モジュールが既に分かっていて、`init.py`、`eval_oracles.py`、`apply/`、`session/` の個別実装を直接読みたいとき。

## hash

- a04b55252d05e3b5d2dc808f226a956b1433be6da50c41a313ffd85c618382fb
<!-- cmoc-index-kind: directory -->
