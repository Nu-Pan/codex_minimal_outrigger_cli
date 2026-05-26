# `commons`

## Summary

- `cmoc` の共通処理をまとめたディレクトリの入口です。Codex CLI 呼び出し、サブコマンド実行制御、リポジトリ操作、共通エラー、ログ、タイムスタンプ、経過時間計測、`INDEX.md` メンテナンスを扱うモジュールへ案内します。
- `src/commons/INDEX.md` から、`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`subcommand_log.py`、`timestamps.py`、`timing.py`、`__init__.py` へたどれます。
- サブコマンド本体ではなく、複数箇所から再利用される基盤機能を集約する場所として使います。

## Read this when

- `cmoc` で共通利用するユーティリティ群の入口をまとめて確認したいとき。
- Codex CLI 呼び出し、サブコマンド実行制御、repo ルート探索、エラー整形、ログ保存、時間計測、タイムスタンプ生成、`INDEX.md` メンテナンスのどれへ進むべきか整理したいとき。
- 共通処理を追加・修正するときに、どのモジュールへ置くべきか判断したいとき。
- 共有機能の実装やレビューで、`src/commons` 配下の役割分担を素早く把握したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数定義だけを確認したいときは、このディレクトリではなく `src/sub_commands` 側を読むべきです。
- ユーザー向けのコマンド仕様やワークフロー仕様だけを確認したいときは、`oracles` 配下の該当仕様断片を直接読むべきです。
- この配下のうち特定モジュールだけを見たいときは、`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` を直接参照すべきです。
- `INDEX.md` の生成・更新ルールそのものだけを確認したいときは、このディレクトリの個別モジュールではなく `src/commons/indexing.py` を読むべきです。

## hash

- db52f008bf7130473d13c22d7fb03e10ee22591500ae81a99096f88c855400b8

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

- `src/sub_commands` は `cmoc` の各サブコマンド実装をまとめたディレクトリの入口です。
- `__init__.py` はパッケージ宣言のみを担い、`init.py`、`apply.py`、`apply_abandon.py`、`apply_join.py`、`session_fork.py`、`session_join.py`、`session_abandon.py`、`eval-oracles.py` が個別コマンド本体です。
- この目次は、実装コードを読む前に該当モジュールへ素早くたどり着くための案内です。

## Read this when

- `src/sub_commands` 配下にどのサブコマンド実装があるか、入口を一覧で把握したいとき。
- `cmoc init`、`cmoc apply`、`cmoc apply abandon`、`cmoc apply join`、`cmoc session fork`、`cmoc session join`、`cmoc session abandon`、`cmoc eval-oracles` の実装へ進む前に、該当モジュールを特定したいとき。
- `src/sub_commands` ディレクトリ全体のルーティング文書を作成・更新したいとき。
- サブコマンド実装と、パッケージ宣言だけの補助モジュールを切り分けて確認したいとき。

## Do not read this when

- `cmoc` のユーザー向け仕様や手順だけを確認したいときは、`oracles/app_specs/sub_commands/` 配下の正本仕様を読むべきです。
- 特定の実装モジュールだけを確認したいときは、この目次ではなく `init.py`、`apply.py`、`apply_abandon.py`、`apply_join.py`、`session_fork.py`、`session_join.py`、`session_abandon.py`、`eval-oracles.py` を直接読むべきです。
- `INDEX.md` の生成・更新ルールだけを確認したいときは、`oracles/app_specs/indexing.md` を読むべきです。
- `src/sub_commands` のパッケージ宣言だけを確認したいときは、`__init__.py` を直接読むべきです。

## hash

- 0ab29bd92000e72aedc361b6470001e67b797119444f6411695ea877cd6cf843
