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

- `src/sub_commands` は cmoc のサブコマンド実装を集約する入口で、`__init__.py`、`init.py`、`eval_oracles.py`、`apply/`、`session/` をまとめます。
- `__init__.py` はパッケージ宣言のみ、`init.py` は `cmoc init`、`eval_oracles.py` は `cmoc review oracles` の本体です。
- `apply/` と `session/` はそれぞれ `cmoc apply` 系と `cmoc session` 系の実装ディレクトリで、個別コマンド詳細は配下の INDEX へ分岐します。

## Read this when

- `src/sub_commands` 配下のどのモジュールがどの CLI を担当するかを先に整理したいとき。
- `cmoc init` や `cmoc review oracles` から `apply/` や `session/` 系へどこを辿ればよいか確認したいとき。
- このディレクトリをサブコマンド実装の入口として、全体の役割分担だけ把握したいとき。

## Do not read this when

- 個別サブコマンドの処理順、状態遷移、エラー処理を確認したいときは、この目次ではなく各モジュールや配下の INDEX を読むべきです。
- `cmoc apply` や `cmoc session` の詳細仕様だけを見たいときは、このディレクトリではなくそれぞれの配下の INDEX を読むべきです。
- `src/sub_commands/__init__.py` のパッケージ宣言だけを確認すれば足りるときは、ここを読む必要はありません。

## hash

- de88c5fe81e4d6a86b997e1b7cc5d937ee11ea92049bd566f4a5e04e4cecbb63
