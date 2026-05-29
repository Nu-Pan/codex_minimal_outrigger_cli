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

- このディレクトリは `cmoc` の各サブコマンド実装を集めた入口です。
- `__init__.py`、`init.py`、`eval_oracles.py`、`apply/`、`session/` の役割分担をまとめています。
- 個別コマンドの実装本文へ進む前のルーティング目次です。

## Read this when

- `src/sub_commands` 配下にどのコマンド実装があるか俯瞰したいとき。
- `init`、`review oracles`、`apply`、`session` の入口を切り分けたいとき。
- どのファイルを先に読むべきか整理したいとき。

## Do not read this when

- `cmoc apply` や `cmoc session` の単一コマンドの詳細仕様だけを確認したいとき。
- `src/main.py` のコマンド登録や共通処理だけを追いたいとき。
- `src/commons` の共通基盤や `oracles` 配下の仕様断片だけを確認したいとき。

## hash

- 4be7079c1f7ac3c627cb68bdf0b618b63f954d3c0035506d7eb8b79eda4d863d
