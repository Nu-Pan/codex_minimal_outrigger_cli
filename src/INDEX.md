# `commons`

## Summary

- `src/commons` にある共通ユーティリティ群の入口です。`codex` 呼び出し、サブコマンド実行制御、エラー整形、git リポジトリ処理、`INDEX.md` メンテナンス、サブコマンドログ、タイムスタンプ生成、経過時間計測をまとめます。
- 個別の共有処理を追うときは、`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` へ進めます。

## Read this when

- `src/commons` にある共通処理の役割分担や、どのモジュールへ進むべきかを確認したいとき。
- `codex exec` の共通ラッパー、Structured Output、quota 待機再開、oracle 保護の流れを追いたいとき。
- サブコマンド実行の共通制御、エラー整形、repo ルート探索、ログ出力、タイミング計測を横断的に見直したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックだけを確認したいときは、`src/sub_commands` 側を直接読むべきです。
- `src/commons` のうち読むべきモジュールがすでに分かっているときは、この目次ではなく該当ファイルへ直接進むべきです。
- 実装コードやテストコードだけで足りる場合は、このディレクトリの案内を読む必要はありません。

## hash

- 19c08db1879a69f91f761dc4d324f1a8c998cf345243dbd5accafcf48fef231d

# `main.py`

## Summary

- `cmoc` CLI の Typer エントリーポイントで、`init`、`session`、`apply`、`eval-oracles` のトップレベルルーティングを定義します。
- `session fork/join/abandon` と `apply fork/join/abandon` の CLI 入口を登録し、各サブコマンド実装への委譲をまとめています。
- `eval-oracles` は `src/sub_commands/eval-oracles.py` を動的読み込みし、互換の `eval-oracle` hidden alias も含めています。
- `main()` は Typer / Click の例外を `cmoc` 形式のエラーレポートへ変換し、`python src/main.py` の直接起動経路も担います。

## Read this when

- `cmoc` のトップレベルコマンド登録と、`init`、`session`、`apply`、`eval-oracles` のルーティング構成を確認したいとき。
- `session fork/join/abandon` や `apply fork/join/abandon` の CLI 入口がどこで登録されているかを確認したいとき。
- `eval-oracles` の動的読み込みや、互換用の hidden alias `eval-oracle` の扱いを確認したいとき。
- `NoArgsIsHelpError` を含む Typer / Click の例外を、`cmoc` 形式のエラーレポートへ変換する流れや、`python src/main.py` での直接起動経路を確認したいとき。

## Do not read this when

- 各サブコマンド本体の業務ロジックや状態遷移だけを確認したいときは、`src/sub_commands` 配下の該当モジュールを読むべきです。
- 共通エラー整形の内部実装や、`commons.errors` の詳細だけを追いたいときは、このファイルではなく共通モジュールを読むべきです。
- `cmoc` の利用手順や `oracles` 側の正本仕様だけを確認したいときは、この CLI  प्रवेश点ではなく該当文書を読むべきです。
- `apply` や `session` の個別処理そのものを見たいだけで、トップレベルのルーティングや起動処理が不要なときは読む必要がありません。

## hash

- 1d39a93edfb5c7866f8de10ccc4cb645f39cf6684d9ede63ee90507bed1e7431

# `sub_commands`

## Summary

- `src/sub_commands` は `cmoc` のサブコマンド本体をまとめる入口です。
- `apply.py`、`apply_abandon.py`、`apply_join.py` が apply 系、`session_fork.py`、`session_join.py`、`session_abandon.py` が session 系を担当します。
- `init.py` は初期化、`eval-oracles.py` は oracle 評価、`__init__.py` はパッケージ宣言のみを担当します。
- このディレクトリは、各コマンド本体へ進むための目次として使います。

## Read this when

- `cmoc apply` とその補助コマンドの実装・修正・レビューを確認したいとき。
- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` の実装・修正・レビューを確認したいとき。
- `cmoc init` や `cmoc eval-oracles` の本体処理を追いたいとき。
- `src/sub_commands` 配下のどのモジュールを読むべきかを、入口から判断したいとき。
- パッケージ宣言だけの `__init__.py` を含め、各サブコマンド本体の配置を確認したいとき。

## Do not read this when

- 共有ユーティリティや git 操作、`INDEX.md` 生成の共通処理だけを確認したいときは、`src/commons` を読むべきです。
- CLI のトップレベル引数解釈やコマンド登録だけを確認したいときは、`src/main.py` を読むべきです。
- `oracles` 側の正本仕様や、そのルーティング文書だけを確認したいときは、このディレクトリではなく `oracles` 配下を読むべきです。
- `src/sub_commands` の個別実装ではなく、仕様断片だけを読みたいときは、対応する oracle 文書へ進むべきです。

## hash

- a9b5d3d47f0ded2a9fa1914f0933efa75034d5386c6adc42cee523075c581efa
