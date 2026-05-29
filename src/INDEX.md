# `commons`

## Summary

- cmoc 全体で共有する実行基盤をまとめたディレクトリです。
- Codex CLI 呼び出し、git と repo root の共通処理、共通エラー整形、サブコマンドログ、経過時間計測、タイムスタンプ生成、INDEX.md メンテナンスを扱います。
- 個別サブコマンドではなく、複数機能から再利用される共通部品の入口です。

## Read this when

- Codex CLI の呼び出し方、Structured Output の検証、quota 待機や再試行の共通処理を確認したいとき。
- repo root 探索、session/apply の共通 state、branch 判定、git 操作の補助を確認したいとき。
- 共通エラー表示、サブコマンドログ、経過時間計測、タイムスタンプ、INDEX.md 自動生成の仕組みを追いたいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数だけを確認したいとき。
- src/commons の特定モジュールだけを直接見たいときは、この目次ではなく該当ファイルを読むべきです。
- src 配下の別機能や tests の実装だけを追いたいとき。

## hash

- 9e7c7bd2ed228c84e68832cd468604a3510aa13f98d09d56aac5cf6f340a58c9

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

- `src/sub_commands` 配下のサブコマンド実装全体を案内する入口です。
- `__init__.py`、`init.py`、`eval_oracles.py`、`apply/`、`session/` への導線をまとめる目次として使います。
- 個別コマンドの詳細は、各モジュールまたは下位ディレクトリの `INDEX.md` を参照します。

## Read this when

- `src/sub_commands` 配下にどのサブコマンド実装があるかを一覧で把握したいとき。
- `cmoc` の各サブコマンド入口が、どのモジュールやディレクトリに分かれているかを整理したいとき。
- 実装やテストを始める前に、`src/sub_commands` のルーティング先を確認したいとき。

## Do not read this when

- `cmoc init`、`cmoc review oracles`、`cmoc apply`、`cmoc session` の個別仕様や引数だけを確認したいとき。
- `src/sub_commands/apply` や `src/sub_commands/session` など、下位ディレクトリの詳細仕様だけを追いたいとき。
- `src/sub_commands/__init__.py` や `init.py` のような単一モジュールの実装詳細を直接見たいとき。

## hash

- fb7ca8757521c6107c82cd19d328d3fc1f374169a66fde4921f308128035a13d
