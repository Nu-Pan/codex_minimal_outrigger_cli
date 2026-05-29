# `commons`

## Summary

- `src/commons` は cmoc 全体で使う共通処理の集まりです。
- 実行ラッパー、エラー処理、リポジトリ操作、サブコマンドログ、時間計測、タイムスタンプ、`INDEX.md` 生成をまとめています。
- 個別サブコマンドの実装よりも先に読む、横断的な基盤モジュール群の入口です。

## Read this when

- `cmoc` の共通実行制御、リポジトリルート解決、エラー整形、ログ記録、時間計測をまとめて把握したいとき。
- session / apply のブランチや state、`<repo-root>/.cmoc` 配下の共通管理処理を確認したいとき。
- `codex exec` 呼び出し、Structured Output 検証、`INDEX.md` 生成・維持などの横断的な共通処理を追いたいとき。
- タイムスタンプ生成やサブコマンド終了レポートなど、CLI 共通の補助機能を確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジック、引数定義、状態遷移だけを確認したいとき。
- `src/commons` のうち特定の 1 モジュールだけを深掘りしたいときは、この目次ではなく該当ファイルを直接読むべきです。
- テスト実装や CLI 全体の画面設計だけを確認したいとき。

## hash

- c701b4e26d0506a28395865d74053aaf24127950a695dc317d5bbb0094c93a5f

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

- `src/sub_commands` は `cmoc` のサブコマンド実装を束ねる入口ディレクトリです。
- `__init__.py` の最小パッケージ宣言に加えて、`init.py`、`eval_oracles.py`、`apply`、`session` を含みます。
- 個別コマンドの本体実装や下位パッケージへ進む前の目次として使います。

## Read this when

- `src/sub_commands` にどのサブコマンド実装が置かれているかを確認したいとき。
- `init`、`review oracles`、`apply`、`session` の実装入口を素早くたどりたいとき。
- この配下の実装・修正・レビュー・テストを始める前に、入口ファイルの役割分担を整理したいとき。

## Do not read this when

- 個別の `cmoc` サブコマンドの実装や引数だけを確認したいとき。
- `apply` や `session` の配下にある詳細仕様ではなく、サブコマンド全体の入口だけを把握したいとき。
- `src/sub_commands` のパッケージ宣言だけを確認したいときは、`__init__.py` を直接見れば足りるとき。

## hash

- bc3e316358fd1c7603c9e6c1a95370c492c4b2dcd779a2297c2ad74e98d2f433
