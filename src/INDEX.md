# `commons`

## Summary

- `src/commons` は、cmoc 全体で使う共通基盤モジュール群をまとめたディレクトリです。
- `codex.py` が Codex CLI 呼び出しと Structured Output、再試行、ログ保存、`INDEX.md` 事前メンテナンスを担当します。
- `command_runner.py` がサブコマンドの共通実行ラッパー、`errors.py` が共通例外とエラーレポート整形を担当します。
- `indexing.py` が `INDEX.md` の自動生成・再生成・更新・自動コミットを担い、`repo.py` が git リポジトリと cmoc の状態管理を扱います。
- `subcommand_log.py` が JSON Lines ログ、`timestamps.py` が `<time-stamp>` 生成、`timing.py` がステップ経過時間計測を担当します。
- `__init__.py` は `src.commons` をパッケージとして定義するだけの最小モジュールです。

## Read this when

- `src/commons` にある共通処理の役割分担をまとめて把握したいとき。
- repo ルート探索、ブランチ判定、session/apply 状態管理などの git 共通処理を確認したいとき。
- `codex exec` 呼び出し、エラー整形、サブコマンドログ、タイムスタンプ、経過時間計測、`INDEX.md` メンテナンスの実装を追いたいとき。

## Do not read this when

- cmoc の個別サブコマンドの引数、状態遷移、実行手順だけを確認したいとき。
- `INDEX.md` の生成・維持ルールそのものを確認したいとき。
- `src/commons` の外にある CLI 本体やテストコードだけを確認したいとき。

## hash

- 97404f4833288d7bea57f3c5538425b7e5797a3fe4a59d46d426772b62396695

# `main.py`

## Summary

- `cmoc` CLI のエントリーポイントで、Typer のルートアプリと `session` / `apply` / `review` のサブアプリを組み立てる。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` のコマンド登録と引数定義をまとめる。
- サブコマンド未指定時のエラー化、Typer / Click 例外の共通エラーレポート化、`python src/main.py` 直実行の起動経路を扱う。

## Read this when

- `cmoc` の起動点やサブコマンド登録を修正・レビューしたいとき。
- `init` / `session` / `apply` / `review` のコマンド名、エイリアス、オプション既定値を確認したいとき。
- サブコマンドなし起動時の利用者向けエラー、終了コード、`--help` への誘導を確認したいとき。
- `python src/main.py` で直接起動する経路と、その例外ハンドリングを確認したいとき。

## Do not read this when

- 各サブコマンドの本体ロジックや `src/sub_commands/` 配下の業務処理だけを見たいとき。
- 共通エラー型や `format_error_report` の整形仕様だけを確認したいとき。
- `INDEX.md` の生成ルールや共有ユーティリティの設計だけを追いたいとき。

## hash

- f1f3971b766959a15809687fc7f59cd60f74eaa1bdee3c4da218fb15412853e0

# `sub_commands`

## Summary

- `src/sub_commands` は、`cmoc` の各サブコマンド実装をまとめたパッケージの入口です。
- `__init__.py` はパッケージ宣言、`init.py` は `cmoc init`、`eval_oracles.py` は `cmoc review oracles` の本体を持ちます。
- `apply/` と `session/` はそれぞれ `cmoc apply` 系と `cmoc session` 系の実装ディレクトリで、個別コマンドの詳細は各配下の `INDEX.md` に分かれています。

## Read this when

- `src/sub_commands` 配下の `cmoc` サブコマンド実装の入口と、どのモジュール・ディレクトリに進むべきかを整理したいとき。
- `init.py`、`eval_oracles.py`、`apply/`、`session/` の役割分担を俯瞰して、実装・修正・レビュー・テストの入口を確認したいとき。
- `src/sub_commands` パッケージ全体の構成を把握し、個別サブコマンドの詳細へ進む前の案内が欲しいとき。

## Do not read this when

- `cmoc init` だけの詳細な初期化手順や、`.cmoc` の ignore 保証だけを確認したいとき。
- `cmoc review oracles` の評価フロー、Structured Output スキーマ、レポート出力だけを確認したいとき。
- `cmoc apply` 系や `cmoc session` 系の個別サブコマンド仕様だけを確認したいときは、この目次ではなく各配下の `INDEX.md` を読むべきです。

## hash

- 8fbbe32e27831a91ef8f6f0a1cd1551924aedb2adf0c44fd172fd52669e7523f
