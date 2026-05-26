# `commons`

## Summary

- `src/commons` は、cmoc の各サブコマンドから共通利用する処理をまとめたモジュール群です。
- `codex.py` は `codex exec` 呼び出し、Structured Output 検証、quota 待機再開、ログ保存を担います。
- `command_runner.py` は repo root 解決、`typer.Exit` と例外の共通処理、終了時レポート出力をまとめます。
- `errors.py` は共通例外 `CmocError` と stdout 向けエラーレポート整形を提供します。
- `repo.py` は git ルート探索、ブランチ判定、session state、差分や commit 系の共通処理を扱います。
- `indexing.py` は `INDEX.md` の配置、再生成、ハッシュ管理、自動コミットの制御を担います。
- `subcommand_log.py`、`timing.py`、`timestamps.py` はログ tee、経過時間計測、タイムスタンプ生成を提供します。
- `__init__.py` は `src.commons` パッケージを宣言するだけの入口です。

## Read this when

- サブコマンド間で共有するユーティリティや共通制御の置き場所を確認したいとき。
- `codex exec` の共通ラッパー、Structured Output、ログ保存、quota 再開の流れを追いたいとき。
- git ルート探索、session state、cmoc 管理ブランチ、差分コミットなど repo 系の共通処理を修正したいとき。
- 共通エラー、サブコマンド実行制御、タイミング計測、タイムスタンプ、tee ログの仕様を確認したいとき。
- `INDEX.md` の生成ルールや維持処理を実装・調整したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数定義だけを確認したいときは、`src/sub_commands` を読むべきです。
- `oracles` 配下の正本仕様そのものや、サブコマンドごとのユーザー向け手順だけを調べたいときは、このディレクトリではありません。
- 開発ルール、テスト規約、環境構築など、共通モジュール以外の仕様を確認したいときは、`oracles/dev_rules` を読むべきです。
- リポジトリ全体の運用ルールやファイルアクセス規則だけを確認したいときは、`README.md` や `AGENTS.md` を参照すべきです。

## hash

- eff44b7f15ef90ead4a7cf7cb160fa20457f05f5b49d954867dbb6e49aee4d15

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

- `cmoc` のサブコマンド実装の入口をまとめたディレクトリです。
- `apply` 系、`session` 系、`init`、`eval-oracles` の各コマンド本体と、その周辺の専用処理が入っています。
- 各コマンドの細かな仕様本文は `oracles/app_specs/sub_commands` 側にあり、このディレクトリはそれを実装する側の入口として使います。

## Read this when

- `cmoc apply`、`cmoc apply abandon`、`cmoc apply join` の実装・修正・テスト・レビューを行うとき。
- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` の実装・修正・テスト・レビューを行うとき。
- `cmoc init` や `cmoc eval-oracles` のサブコマンド本体の振る舞いを確認したいとき。
- サブコマンド間の責務分担や、各コマンドがどの処理を担当するかを整理したいとき。

## Do not read this when

- 共通の Git/Repository ヘルパーや `commons` 側の実装だけを確認したいときは、このディレクトリではなく対応する共通モジュールを読むべきです。
- `oracles` の仕様本文や `INDEX.md` の生成ルールだけを確認したいときは、このディレクトリではなく `oracles` 配下の正本仕様を読むべきです。
- サブコマンドの外側にある CLI 起動・引数解釈・設定値だけを追いたいときは、このディレクトリを読む必要はありません。

## hash

- 419c2f8b95e25475525f2ab52a148360e56aef8b9e2f56fbbeb0577f548c4653
