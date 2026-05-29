# `commons`

## Summary

- `src/commons` は `cmoc` 全体で共有する基盤モジュール群のディレクトリです。
- 実行制御、エラー処理、git リポジトリ操作、サブコマンドログ、時間計測、タイムスタンプ、`INDEX.md` メンテナンスをまとめています。
- 個別サブコマンドより先に読む、横断的な共通処理の入口です。

## Read this when

- `cmoc` 全体で使う共通処理の入口をまとめて把握したいとき。
- 実行ラッパー、エラー整形、repo root 解決、共通ログ、経過時間計測、タイムスタンプ生成の役割分担を確認したいとき。
- `codex exec` の共通化や Structured Output 検証、`INDEX.md` メンテナンスの共通基盤を追いたいとき。
- `cmoc` の CLI 実装やサブコマンド実装を書く前に、横断的な基盤モジュールの位置づけを整理したいとき。

## Do not read this when

- 個別モジュールの実装詳細だけを確認したいときは、この目次ではなく `src/commons` 配下の該当ファイルを直接読むべきです。
- `cmoc` のサブコマンド本体の業務ロジックや引数定義だけを確認したいときは、このディレクトリではなく `src/sub_commands` 側を読むべきです。
- `INDEX.md` の生成ルールそのものや、他ディレクトリのルーティング方針だけを確認したいときは、このディレクトリを読む必要はありません。
- テスト実装や CLI の画面設計だけを確認したいときは、この共通モジュール群を読む必要はありません。

## hash

- 7998dc3d75fac6201ef702706d017ac7c729fd5f782e5606b0f03d1f012c33ae

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
