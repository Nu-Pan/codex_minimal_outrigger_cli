# `commons`

## Summary

- `src/commons` は、cmoc 全体で共通利用する横断処理を集約した基盤モジュール群です。
- `codex.py` は `codex exec` の共通ラッパーで、サンドボックス指定、Model / Reasoning Effort、Structured Output、JSON/text 検証、リトライ、quota 復旧をまとめて扱います。
- `repo.py` は git リポジトリ探索、ブランチ・HEAD 情報、`.cmoc` の追跡回避、差分収集、oracle / 実装ファイル列挙、commit 補助処理を担当します。
- `indexing.py` は `INDEX.md` の自動生成・更新・再利用・自動コミットを担当します。
- `errors.py`、`subcommand_log.py`、`timestamps.py`、`timing.py`、`command_runner.py` は、共通エラー表示、サブコマンドログ、タイムスタンプ生成、経過時間計測、実行制御の入口を提供します。

## Read this when

- cmoc の共通ユーティリティの役割分担や、このディレクトリに何があるかを確認したいとき。
- `codex exec` の起動方法、Structured Output、検証、リトライ、quota 復旧の流れを確認したいとき。
- git リポジトリ探索、ブランチ・HEAD 取得、`.cmoc` の ignore 保証、差分収集、ファイル列挙、commit 補助の実装方針を知りたいとき。
- `INDEX.md` の自動生成・更新・再利用・自動コミットの仕組みを確認したいとき。
- 共通エラーハンドリング、サブコマンドログ、タイムスタンプ、経過時間表示、サブコマンド実行の共通ラッパーを確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数定義だけを調べたいとき。
- `oracles` 配下の正本仕様や、`src` / `tests` の別ディレクトリの細かな内容だけを確認したいとき。
- `README.md`、`AGENTS.md`、`memo` の運用ルールだけを確認したいとき。
- 共通処理の再利用関係ではなく、特定の CLI 引数や画面表示だけを追いたいとき。
- 個々の補助モジュールの詳細実装だけを確認したいとき。

## hash

- 923512335d977526ffdc78319c356951f3189e40e643f6edfc186443f86a1bdf

# `main.py`

## Summary

- `cmoc` CLI の Typer エントリーポイントを定義するファイルです。
- `init`、`branch`、`eval-oracles`、`apply`、`merge` を `app` に登録し、それぞれ対応する `sub_commands` 実装へ処理を委譲します。
- `main()` は Typer / Click の起動をラップし、parse error や想定外例外を共通エラーレポート形式に整えて終了コードを決定します。
- `python src/main.py` で直接実行された場合も `main()` を起動する入口です。

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

- 46a839a204d98681f3b4b8ae950eedaa799d921d99d7ab1989d89478396fd25d

# `sub_commands`

## Summary

- `cmoc` の各サブコマンド本体実装をまとめる `src/sub_commands` ディレクトリの目次です。
- `__init__.py` はパッケージ初期化、`init.py`、`branch.py`、`apply.py`、`eval_oracles.py`、`merge.py` は各サブコマンドの実装入口です。
- このディレクトリは、サブコマンドごとの処理の流れ、入出力、実行条件、進捗表示や終了判定を確認するための案内役です。

## Read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` のどの実装ファイルを読むべきか判断したいとき。
- 各サブコマンドの処理の流れ、引数、前提条件、終了条件、保存先などの実装詳細を確認したいとき。
- サブコマンド実装のパッケージ境界や、個別モジュールの役割を把握したいとき。

## Do not read this when

- `cmoc` の開発ルール、コーディング規約、テスト方針、開発環境だけを調べたいとき。
- CLI のユーザー向け利用方法や、サブコマンド一覧だけを確認したいとき。
- `README.md`、`AGENTS.md`、`oracles` の運用ルールや編集可否だけを確認したいとき。

## hash

- cb429b2d3c2360fd3d21bf461f7ca360685222b91aa33b70a81043eec5acd933
