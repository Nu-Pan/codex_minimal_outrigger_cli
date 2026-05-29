# `commons`

## Summary

- `src/commons` 配下にある共有モジュール群の入口で、Codex 呼び出し、共通実行制御、エラー、リポジトリ判定、`INDEX.md` 生成、ログ、タイムスタンプ、経過時間計測をまとめています。
- CLI 本体や個別サブコマンドから再利用される基盤処理の置き場で、役割ごとにモジュールが分かれています。
- `__init__.py` はパッケージ宣言のみで、実装の本体は各モジュールに分かれています。

## Read this when

- `cmoc` の共通処理をどのモジュールに置くべきか判断したいとき。
- `<repo-root>` の探索、ブランチ判定、session/apply の管理、エラー整形、ログ、時間計測、タイムスタンプ生成、`INDEX.md` メンテナンスを確認したいとき。
- CLI やサブコマンドの実装で、共通部品を再利用したり修正範囲を切り分けたりしたいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや引数仕様だけを確認したいとき。
- 対象の共通モジュールがすでに分かっていて、`codex.py` や `repo.py` などを直接読みたいとき。
- テストコードや `oracles` 全体の方針だけを見たいとき。

## hash

- be6fc6449dc13c04c7aa32d97629d34fe888e721ae143133a480f6b2aefcef13

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
- 個別コマンドの詳細は各モジュールまたは下位ディレクトリの `INDEX.md` を参照します。

## Read this when

- `src/sub_commands` 配下にどのサブコマンド実装があるかを一覧で把握したいとき。
- `cmoc` の各サブコマンド入口がどのモジュールやディレクトリに分かれているかを整理したいとき。
- 実装やテストを始める前に、`src/sub_commands` のルーティング先を確認したいとき。

## Do not read this when

- `cmoc init`、`cmoc review oracles`、`cmoc apply`、`cmoc session` の個別仕様や引数だけを確認したいとき。
- `src/sub_commands/apply` や `src/sub_commands/session` の下位実装だけを深く追いたいとき。
- `src/sub_commands/__init__.py` や `init.py` など、単一モジュールの実装詳細を直接見たいとき。

## hash

- 2951c538a564c07d8a5652a32655d2d30b7752961cae421a9bb0424eaeaa3f09
