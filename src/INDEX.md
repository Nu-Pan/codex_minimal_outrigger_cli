# `commons`

## Summary

- `src/commons` は cmoc 全体で再利用する共通処理の集まりで、リポジトリ探索、例外整形、ログ tee、タイミング計測、タイムスタンプ生成、Codex CLI 呼び出し、INDEX.md 生成をまとめます。
- `repo.py` は `<repo-root>` の探索、git ブランチ、session state、差分判定を扱います。
- `command_runner.py`、`subcommand_log.py`、`timing.py`、`timestamps.py` はサブコマンド実行時の共通制御と記録を担います。
- `codex.py` と `indexing.py` は Codex exec のラッパーと `INDEX.md` 維持処理を担います。
- `errors.py` は `CmocError` と利用者向けエラーレポート整形を提供します。

## Read this when

- `src/commons` にある共通処理の置き場所や役割分担を把握したいとき。
- `<repo-root>` の探索、branch 判定、session state、差分判定を扱いたいとき。
- サブコマンドのログ、タイミング、エラー、Codex CLI 呼び出しを横断的に確認したいとき。
- `INDEX.md` の生成・再利用・更新ルールを確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや引数定義だけを確認したいとき。
- `src/sub_commands` の手順や `oracles` の正本仕様だけを追いたいとき。
- 特定の共通機能だけを深掘りしたいときは、該当する `src/commons/*.py` を直接読むべきです。
- 実装コードやテストコードだけで足りる場合は、このディレクトリの目次を読む必要はありません。

## hash

- 2462c8fc6b5ae5ce509c31f8287d1c2a69d34e0642d0e17c086ef6aa0d68734f

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

- cmoc の個別サブコマンド仕様への入口です。
- `apply`、`session`、`eval-oracles`、`init` の各サブコマンドの正本仕様へ案内します。
- このディレクトリを起点に、サブコマンドごとの前提条件、実行手順、状態遷移、終了条件を素早く辿れるようにします。

## Read this when

- cmoc の個別サブコマンドの入口をまとめて確認したいとき。
- `apply`、`session`、`eval-oracles`、`init` のどの仕様断片へ進むべきか整理したいとき。
- サブコマンドごとの目的、入力条件、実行手順、終了条件を俯瞰したいとき。

## Do not read this when

- 個別のサブコマンド仕様だけを確認したいときは、この目次ではなく該当する `apply_*`、`session_*`、`eval_oracles.md`、`init.md` を直接読むべきです。
- 実装コードやテストコードだけで足りる作業では、このディレクトリの案内を読む必要はありません。
- `branch_model`、`codex_call`、ログ、エラーハンドリング、`oracles` 全体の扱いなど、他の共通仕様を確認したいときは別の入口文書を読むべきです。

## hash

- c371104944fa464cdd093f23b2f1454afd60f91f5ffe47df8147e0a96a37e18d
