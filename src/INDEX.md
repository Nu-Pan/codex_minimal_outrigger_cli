# `commons`

## Summary

- `cmoc` の共通処理をまとめた Python パッケージの入口です。
- `codex` 呼び出しラッパー、サブコマンド共通実行制御、エラー処理、リポジトリ探索、ログ、タイムスタンプ、計時、`INDEX.md` 生成の補助処理が入っています。
- サブコマンド本体ではなく、複数機能で再利用する基盤ロジックを読むための目次です。

## Read this when

- `codex exec` 呼び出し、Structured Output、`INDEX.md` メンテナンスの共通処理を確認したいとき。
- リポジトリルート探索、`session` / `apply` 系の branch 判定、未コミット差分の扱いを確認したいとき。
- 共通エラー整形、サブコマンドログ、タイムスタンプ、経過時間表示の実装を見直したいとき。

## Do not read this when

- 個別サブコマンドの引数解析や業務ロジックだけを確認したいときは、この配下ではなく `src/sub_commands` 側を読むべきです。
- `INDEX.md` の自動生成ルールや `oracles` 側の正本仕様だけを確認したいときは、この配下を読む必要はありません。
- テスト実装だけを追いたいときは、この配下ではなく `tests` 側を確認すべきです。

## hash

- 4c5b2dfb2cc0c99fdb4c9c700e149aa7a4e7fdb1fc1371005c4938e31a0c15a4

# `main.py`

## Summary

- `cmoc` CLI のエントリーポイントで、Typer アプリ本体と `session` / `apply` のサブアプリを組み立てています。
- `init`、`session`、`apply`、`review oracles` の各コマンドを定義し、実処理は `src/sub_commands/` 側の実装へ委譲しています。
- Typer / Click の例外処理をまとめて受け、`NoArgsIsHelpError` を含むエラーを `format_error_report()` で整形して終了コード付きで終了します。

## Read this when

- `cmoc` のエントリーポイント、Typer アプリの構成、サブコマンド登録を修正・レビューしたいとき。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` とその引数定義を確認したいとき。
- サブコマンドなし起動時の `NoArgsIsHelpError` の扱い、`--help` 相当の挙動、終了コードの伝播を確認したいとき。
- Typer / Click の例外を `CmocError` と共通エラーレポートへ変換する起動経路を確認したいとき。
- `python src/main.py` で直接起動する経路の振る舞いを確認したいとき。

## Do not read this when

- 各サブコマンド本体の処理内容だけを確認したいときは、このファイルではなく `src/sub_commands/` 配下の実装を見るべきです。
- 共通エラー型やエラーレポートの整形だけを確認したいときは、このファイルではなく `src/commons/errors.py` を見るべきです。
- CLI の設計ルールや配置方針だけを確認したいときは、このファイルではなく `oracles/dev_rules/design_rules.md` を見るべきです。
- サブコマンドごとの仕様断片だけを確認したいときは、このファイルではなく `oracles/app_specs/sub_commands/` 配下の文書を見るべきです。

## hash

- fd4b3fe58ddc1bb32e637e83cc5ddca509458ade3b15a69c1c5d5bc677ba138b

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc のサブコマンド実装の入口で、`apply` と `session` の各パッケージ、`init.py`、`eval_oracles.py`、`__init__.py` への案内をまとめます。
- `apply` と `session` はそれぞれ独立したサブコマンド群として、配下の `INDEX.md` から個別実装へたどれます。
- `init.py` と `eval_oracles.py` は単体モジュールとして、初期化処理と oracle 評価処理の入口を担います。
- `__init__.py` は `src.sub_commands` パッケージを宣言するだけの最小モジュールです。

## Read this when

- cmoc のサブコマンド実装全体の入口を確認したいときに読むべきです。
- `apply` や `session` のような複数ファイルの実装群と、`init.py` / `eval_oracles.py` の単体モジュールを見分けたいときに読むべきです。
- どのサブコマンド実装へ進むべきか、このディレクトリの目次から判断したいときに読むべきです。
- `src/sub_commands` 配下の個別 `INDEX.md` や実装ファイルの入口を探したいときに読むべきです。

## Do not read this when

- CLI の起動口やコマンド登録全体を確認したいときは、このディレクトリではなく `src/main.py` を読むべきです。
- 個別サブコマンドの利用手順や正本仕様だけを確認したいときは、`oracles/app_specs/sub_commands/` 側の文書を直接読むべきです。
- 共通処理やリポジトリ操作、エラー整形などの横断的な仕組みを確認したいときは、`src/commons/` 側を読むべきです。
- `apply`、`session`、`init.py`、`eval_oracles.py` のうち特定の 1 つだけを深く追いたいときは、この目次ではなく該当する配下の `INDEX.md` やモジュールを直接読むべきです。

## hash

- 27ae0f3b8a363a5d0016844369bcfc6b98fa48c65f73d47956ca23feb0234de5
