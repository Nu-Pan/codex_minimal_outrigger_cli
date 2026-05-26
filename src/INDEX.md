# `commons`

## Summary

- `cmoc` の共通処理をまとめるディレクトリで、コマンド実行制御、エラー整形、git リポジトリ操作、ログ、時刻、計測、`INDEX.md` 管理を集約します。
- `codex.py` は Codex CLI 呼び出しと Structured Output 検証、quota 待機再開、出力ログ保存を扱います。
- `command_runner.py`、`errors.py`、`repo.py`、`subcommand_log.py`、`timestamps.py`、`timing.py`、`indexing.py` が横断機能を分担します。
- `__init__.py` は `src.commons` パッケージを宣言するだけの最小モジュールです。

## Read this when

- 共通の実行制御やエラーレポートの流れを確認したいとき。
- `codex exec` の呼び出し、Structured Output、quota 待機再開、ログ保存の挙動を追いたいとき。
- git ルート探索、session/apply ブランチ判定、`.cmoc` の追跡除外、session state の読み書きを確認したいとき。
- `INDEX.md` の生成・更新、サブコマンドの tee ログ、タイムスタンプ、ステップ計測を扱いたいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや引数定義だけを確認したいときは、`src/sub_commands` 側を読むべきです。
- ユーザー向けのルーティング仕様やサブコマンド別の正本断片を確認したいときは、`oracles` 側を読むべきです。
- 実装やテストの配置方針だけを確認したいときは、`src` 全体や `tests` の方針を見れば足ります。
- `INDEX.md` の生成・更新ルールだけを確認したいときは、このディレクトリではなく `src/commons/indexing.py` を読むべきです。

## hash

- 51c5823f2776168a1285d5c1105157ba1b38c8e686e5f7119c7ef1c5b63d56a1

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

- このディレクトリには `cmoc` の各サブコマンド実装がまとまっており、`init`、`apply`、`eval-oracles`、`session fork/join/abandon` などの本体処理と、`__init__.py` のパッケージ宣言が含まれます。
- 各モジュールは共通ランナー呼び出し、`session.state` や branch/worktree の更新、`codex exec` 連携、`INDEX.md` メンテナンスなどの実行フローを担当します。
- このディレクトリの `INDEX.md` は、個別サブコマンド実装へ最短で進むための入口です。

## Read this when

- 特定の `cmoc` サブコマンドの実装・修正・レビューを行いたいとき。
- `apply` 系と `session` 系の処理フロー、状態更新、ブランチ操作の違いを横断して確認したいとき。
- `eval-oracles` や `init` を含む CLI の振る舞いを、仕様ではなく実装から追いたいとき。
- `src/sub_commands` 配下のどのモジュールに処理があるかを素早く特定したいとき。

## Do not read this when

- サブコマンドの仕様本文だけを確認したいときは、`oracles/app_specs/sub_commands` 側を読むべきです。
- `commons` 配下の共通処理、Git 操作ヘルパー、状態ファイルの共通基盤だけを確認したいときは、このディレクトリではなく共通モジュールを読むべきです。
- 個別コマンドのうち 1 つだけを確認したいときは、このディレクトリの入口ではなく該当モジュールを直接読むべきです。
- `src/sub_commands/__init__.py` のようなパッケージ宣言だけが目的なら、他の実装モジュールを読む必要はありません。

## hash

- b3ec1c7e532fc16130029a12cff29cc45c41a93aac8d617e89cb909743c5877a
