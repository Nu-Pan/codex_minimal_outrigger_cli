# `commons`

## Summary

- cmoc の共通処理をまとめた Python パッケージです。
- Codex CLI 呼び出し、サブコマンド共通ラッパー、共通エラー整形、リポジトリ検出、サブコマンドログ、経過時間計測、タイムスタンプ生成、INDEX.md の生成・維持を扱います。
- 各サブモジュールの役割を把握したいときの入口です。

## Read this when

- 共通処理の責務分担や、どのモジュールに何が入っているかを俯瞰したいとき。
- Codex CLI 実行、エラー処理、リポジトリ判定、ログ、計時、タイムスタンプ生成、INDEX.md 生成の共通基盤を確認したいとき。
- `src/commons` 配下の具体的なモジュールを選ぶ前に、まず全体像を押さえたいとき。

## Do not read this when

- 個別モジュールの実装詳細だけを確認したいときは、このディレクトリではなく `codex.py`、`repo.py`、`errors.py` など該当モジュールを直接読むべきです。
- 個別サブコマンドの業務ロジックや CLI 引数だけを確認したいときは、このパッケージではなく `src/sub_commands` 側を読むべきです。
- `src/commons` 以外の仕様や `oracles` 全体の方針だけを確認したいときは、このディレクトリを読む必要はありません。

## hash

- b6d4bc262ec4e7241df2fb2a856e72018cf3d361cc056f9755d65ee37716671d

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
