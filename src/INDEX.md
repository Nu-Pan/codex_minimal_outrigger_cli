# `commons`

## Summary

- `src/commons` は、cmoc 全体で共有する横断的な共通処理を集約した基盤モジュール群です。
- `codex.py` は `codex exec` の共通ラッパーで、Structured Output、実行ログ、JSON/text 検証、リトライ、quota 復旧を扱います。
- `repo.py` は git リポジトリ探索、`.cmoc` の追跡回避、差分収集、oracle / implementation ファイル列挙を扱います。
- `indexing.py` は `INDEX.md` の自動生成・更新・再利用・自動コミットをまとめます。
- `errors.py`、`subcommand_log.py`、`timestamps.py`、`timing.py`、`command_runner.py` は、共通エラーレポート、サブコマンドログ、タイムスタンプ、経過時間計測、実行制御を担います。

## Read this when

- `cmoc` の共通ユーティリティの役割分担や、このディレクトリに何があるかを確認したいとき。
- git リポジトリ探索、ブランチや HEAD の取得、`.cmoc` の ignore 保証、差分収集、ファイル列挙の実装方針を知りたいとき。
- `codex exec` の起動方法、Structured Output、ログ保存、検証リトライ、quota 復旧の流れを確認したいとき。
- `INDEX.md` の自動生成・更新・再利用・自動コミットの仕組みを確認したいとき。
- 共通エラーレポート、サブコマンドログ、タイムスタンプ生成、経過時間表示、サブコマンド実行の共通ラッパーを確認したいとき。

## Do not read this when

- `cmoc` の個別サブコマンドの業務ロジックだけを調べたいとき。
- `oracles` 配下の正本仕様や、`src` / `tests` の別ディレクトリの細かな内容だけを確認したいとき。
- `README.md`、`AGENTS.md`、`memo` の運用ルールだけを確認したいとき。
- 共通処理の再利用関係ではなく、特定の CLI 引数や画面表示だけを追いたいとき。

## hash

- 616501ed94add89800835497d89e3d07552e4f841b5fbfcdd7fd2e1f63539b2f

# `main.py`

## Summary

- `cmoc` CLI の Typer エントリーポイントを定義するファイルです。
- `init`、`branch`、`eval-oracles`、`apply`、`merge` の各サブコマンドを `app` に登録し、引数やオプションを受けて対応する `sub_commands` 実装へ処理を委譲します。
- `main()` は Typer/Click の起動をラップし、parse error や想定外例外を共通エラーレポート形式に整えて終了コードを決定します。
- `python src/main.py` で直接実行された場合も `main()` を起動する入口になっています。

## Read this when

- `cmoc` のトップレベル CLI コマンド一覧やサブコマンド登録箇所を確認したいとき。
- `init`、`branch`、`eval-oracles`、`apply`、`merge` がどの実装関数へ委譲されるか調べたいとき。
- サブコマンドの Typer 引数・オプション定義、デフォルト値、短縮オプションを確認したいとき。
- Typer や Click の例外、CLI の parse error、想定外例外がどのように共通エラーレポートと終了コードへ変換されるか確認したいとき。
- `app` オブジェクト、`main()`、直接実行時の挙動を修正または調査したいとき。

## Do not read this when

- 各サブコマンドの具体的な処理内容、git 操作、ファイル生成、Codex CLI 呼び出しなどの本体実装を調べたいとき。
- 共通エラーレポートのフォーマット処理そのものを詳しく確認したいとき。
- cmoc の設定ファイル、oracle 評価、INDEX.md 生成、ログ保存などの詳細仕様や処理フローを調べたいとき。
- Typer ではなく個別モジュール内のビジネスロジックやテスト対象の詳細を確認したいとき。
- cmoc を使う対象リポジトリ側の `<repo-root>` 構造やファイル内容を調査したいとき。

## hash

- 36e5e2fb8b0363de44466a80240381ed5c51c543fb23b58d66d935e199d46b02

# `sub_commands`

## Summary

- `cmoc` のサブコマンド本体実装をまとめるディレクトリです。
- `init.py`、`branch.py`、`apply.py`、`eval_oracles.py`、`merge.py` など、各サブコマンドの実処理への入口を案内します。
- サブコマンドごとの引数処理、前提条件、実行フロー、終了処理を確認するときのルーティング用目です。
- `cmoc` のコマンド単位の挙動を実装・修正・テストする際に、読むべき本体ファイルを素早く特定するための目次です。

## Read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の実装や修正をするとき。
- 特定のサブコマンドの本体処理がどの Python ファイルにあるか確認したいとき。
- サブコマンドごとの前提条件、実行手順、分岐、例外処理、完了判定を追いたいとき。
- `src/sub_commands` 配下の構成を把握して、個別実装へ移動したいとき。

## Do not read this when

- cmoc 全体の設計方針や開発ルールだけを確認したいとき。
- `oracles` 配下の正本仕様断片だけを調べたいとき。
- テストコードや共通ユーティリティの場所を探しているとき。
- サブコマンド横断の共通仕様だけを見たいが、個別実装の入口は不要なとき。

## hash

- 75c517936677a6be2379b6cabc1e9edcfb4cc328d04ac0dd866b3b4ee6c3cf3d
