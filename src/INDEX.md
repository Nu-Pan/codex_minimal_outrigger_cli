# `commons`

## Summary

- `cmoc` の複数サブコマンドから共通利用する基盤処理をまとめたディレクトリです。
- Codex CLI 呼び出し、サブコマンド共通実行制御、共通エラー、リポジトリ操作、INDEX 生成、サブコマンドログ、タイムスタンプ、経過時間計測などの共通機能を収録します。
- 個別サブコマンド本体ではなく、横断的に使う共通機能の入口として参照します。

## Read this when

- 複数サブコマンドで共有する処理の実装・修正・レビューを確認したいとき。
- Codex CLI 呼び出し、共通実行制御、エラー整形、リポジトリ操作、INDEX 生成、ログ、タイムスタンプ、経過時間計測を確認したいとき。
- 共有処理をどこに置くべきか、`src/commons` の責務を整理したいとき。
- `src/commons` 配下の各モジュールの役割分担を横断的に把握したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックだけを確認したいとき。
- `src/main.py` や `src/sub_commands` の引数解析・コマンド分岐だけを確認したいとき。
- 特定の共通ユーティリティ 1 つだけを追いたいときは、該当モジュールを直接読むべきです。
- `INDEX.md` の生成・更新ルールだけを確認したいときは、`indexing.md` を読むべきです。

## hash

- ac1f414ca8f85b35c8f5b933d843b25191ef31e5513403c788a7e1e3f33ddb2c

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

- `cmoc` のサブコマンド実装をまとめた入口で、`apply` 系、`session` 系、`init`、`eval-oracles` の本体モジュールと、その周辺の専用処理を案内します。
- 各コマンドの実装は `apply.py`、`apply_abandon.py`、`apply_join.py`、`session_fork.py`、`session_join.py`、`session_abandon.py`、`init.py`、`eval-oracles.py` に分かれています。
- `__init__.py` はパッケージ宣言用の最小モジュールです。

## Read this when

- `cmoc apply`、`cmoc apply abandon`、`cmoc apply join` の実装・修正・テスト・レビューを行うとき。
- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` の実装・修正・テスト・レビューを行うとき。
- `cmoc init` や `cmoc eval-oracles` の本体処理、またはサブコマンド間の責務分担を確認したいとき。
- `src/sub_commands` 配下のどのモジュールを読むべきか、このディレクトリの目次から判断したいとき。

## Do not read this when

- 共有の Git・リポジトリ操作や補助ユーティリティだけを見たいときは、`src/commons` 側を読むべきです。
- `cmoc` 全体の起動・引数解釈・トップレベルルーティングだけを追いたいときは、`src/main.py` を読むべきです。
- `oracles` 側の正本仕様や `INDEX.md` の生成・更新ルールだけを確認したいときは、このディレクトリではなく `oracles` 配下を読むべきです。

## hash

- 3a0255fd4676be0a92adccbe848880b8cf8e32971db0c625bf5faff1242a6530
