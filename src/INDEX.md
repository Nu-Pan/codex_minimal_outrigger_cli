# `commons`

## Summary

- cmoc 全体で共有する実行基盤をまとめたディレクトリです。
- Codex CLI 呼び出し、共通エラー整形、repo root / branch / session state 操作、サブコマンドログ、経過時間計測、タイムスタンプ生成、INDEX.md メンテナンスを扱います。
- 個別サブコマンドではなく、複数機能から再利用される共通部品の入口です。

## Read this when

- Codex CLI 呼び出し、Structured Output 検証、quota 待機や再試行の共通処理を確認したいとき。
- repo root 探索、branch 判定、session/apply state、git 操作補助を確認したいとき。
- 共通エラー表示、サブコマンドログ、経過時間計測、タイムスタンプ、INDEX.md 自動生成の仕組みを追いたいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数だけを確認したいとき。
- `src/commons` の特定モジュールだけを直接見たいときは、この目次ではなく該当ファイルを読むべきです。
- `src` 配下の別機能や `tests` の実装だけを追いたいとき。

## hash

- e3dc47e0b9023b8290ec846676040ffde9c76196984d9bfc9120e260536bc102

# `main.py`

## Summary

- `cmoc` CLI のエントリーポイントで、Typer アプリ本体と `session` / `apply` / `review` のサブアプリを組み立てています。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の各コマンドを定義し、実処理は `src/sub_commands/` 側へ委譲しています。
- Typer / Click の例外を共通エラーレポートへ変換し、`NoArgsIsHelpError` を含む起動時エラーを終了コード付きで処理します。

## Read this when

- `cmoc` のエントリーポイント、Typer アプリの構成、サブコマンド登録を修正・レビューしたいとき
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` とその引数定義を確認したいとき
- サブコマンドなし起動時の `NoArgsIsHelpError` の扱い、`--help` 相当の挙動、終了コードの伝播を確認したいとき
- Typer / Click の例外を `CmocError` と共通エラーレポートへ変換する起動経路を確認したいとき
- `python src/main.py` で直接起動する経路の振る舞いを確認したいとき

## Do not read this when

- 各サブコマンド本体の処理内容だけを確認したいとき
- 共通エラー型やエラーレポートの整形だけを確認したいとき
- CLI の設計ルールや配置方針だけを確認したいとき
- サブコマンドごとの仕様断片だけを確認したいとき

## hash

- 0c76935e2e4d5e562d321e1b65e17c49e36e89415a7d311c6f037b13785a396f

# `sub_commands`

## Summary

- `src/sub_commands` は `cmoc` の各サブコマンド実装を束ねる入口で、パッケージ宣言の `__init__.py`、初期化の `init.py`、`review oracles` の `eval_oracles.py`、および `apply` と `session` の各サブパッケージを含みます。
- 個別の実装詳細は `apply/` と `session/` の下位 `INDEX.md`、単体モジュールの挙動は各 `.py` を参照します。
- この目次は `src/sub_commands` 配下の役割分担と、どこへ進むべきかを素早く判断するための入口です。

## Read this when

- `cmoc` のサブコマンド実装全体を俯瞰したいとき。
- `apply` や `session` の下位モジュール、`init.py`、`eval_oracles.py` のどこを読むべきか整理したいとき。
- `src/sub_commands` 配下の修正・レビュー・テストを始める前に、入口を確認したいとき。

## Do not read this when

- `cmoc apply` や `cmoc session` の個別処理だけを確認したいとき。
- `cmoc init` や `cmoc review oracles` の仕様断片だけを確認したいとき。
- `src/sub_commands` のパッケージ宣言だけで足りるときは、`__init__.py` を直接見れば十分なとき。

## hash

- b4ffe3521a35e962ab980065f23a8db158de7b63b81ca58c4e5411977247763f
