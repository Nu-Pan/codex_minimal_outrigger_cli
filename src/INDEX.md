# `commons`

## Summary

- `src/commons` は、cmoc 全体で共有する共通処理をまとめた基盤モジュール群です。
- git リポジトリ探索、作業ルート移動、ブランチや HEAD の取得、差分収集、`.cmoc` の追跡回避など、repo 操作の入口を提供します。
- Codex CLI 呼び出しラッパー、`INDEX.md` 自動メンテナンス、共通エラー整形、タイムスタンプ生成、経過時間計測を集約しています。
- 個別サブコマンドの業務ロジックではなく、複数のサブコマンドから再利用される横断的な処理を扱います。

## Read this when

- `cmoc` の共通機能の実装や呼び出し順を確認したいとき。
- `codex exec` の起動方法、Structured Output、ログ保存、リトライ、quota 復旧の流れを調べたいとき。
- git の repo root 探索、`.cmoc` の ignore 保証、変更ファイル列挙、部分評価・部分適用用の差分収集を確認したいとき。
- `INDEX.md` の自動生成・更新、エラーレポート形式、タイムスタンプ生成、ステップ時間計測を確認したいとき。

## Do not read this when

- `cmoc init` や `cmoc apply` など、個別サブコマンドの業務ロジックだけを調べたいとき。
- `oracles` 配下の正本仕様そのものや、開発ルール・テストルールだけを確認したいとき。
- CLI 引数定義やユーザー向けフローよりも、共通ユーティリティの再利用関係に関心がないとき。
- `README.md`、`AGENTS.md`、`memo` などの運用ルールだけを確認したいとき。

## hash

- 1cc50a89492e65e2e24935fff683b97a1426e469f8384e43b3528ec71f4eea7d

# `main.py`

## Summary

- cmoc CLI の Typer エントリーポイントを定義するファイル。
- `cmoc` アプリケーション本体を作成し、`init`、`branch`、`eval-oracles`、`apply`、`merge` の各サブコマンド名を CLI に登録する。
- 各 CLI コールバックは引数やオプションを受け取り、実処理を `sub_commands` 配下の対応する `cmoc_*_impl` 関数へ委譲する。
- `eval-oracles` は `--full` / `-f`、`apply` は `--repeat` / `-r` と `--full` / `-f`、`merge` は任意の `cmoc_branch` 引数を定義する。
- `main()` は Typer/Click の起動経路をラップし、parse error や想定外例外を `commons.errors.format_error_report` による共通エラーレポート形式で表示して終了コードを決定する。
- `python src/main.py` による直接実行時も `main()` を呼び出して cmoc CLI を起動する。

## Read this when

- cmoc のトップレベル CLI コマンド一覧やサブコマンド登録箇所を確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` がどの実装関数へ委譲されるか調べたいとき。
- サブコマンドの Typer 引数・オプション定義、デフォルト値、短縮オプションを確認したいとき。
- Typer や Click の例外、CLI parse error、想定外例外が cmoc の共通エラーレポートと終了コードへどう変換されるか確認したいとき。
- cmoc の起動入口、`app` オブジェクト、`main()`、直接実行時の挙動を修正または調査したいとき。

## Do not read this when

- 各サブコマンドの具体的な処理内容、git 操作、ファイル生成、Codex CLI 呼び出しなどの本体実装を調べたいとき。
- 共通エラーレポートのフォーマット処理そのものを詳しく確認したいとき。
- cmoc の設定ファイル、oracle 評価、INDEX.md 生成、ログ保存などの詳細仕様や処理フローを調べたいとき。
- Typer ではなく個別モジュール内のビジネスロジックやテスト対象の詳細を確認したいとき。
- cmoc を使う対象リポジトリ側の `<repo-root>` 構造やファイル内容を調査したいとき。

## hash

- d752eef82e7384747c693c0afe234254d441d6ba098d33d86bec3b0c9e31da62

# `sub_commands`

## Summary

- `src/sub_commands` は、cmoc の各サブコマンド本体処理を実装するパッケージです。
- `init.py` は `cmoc init` の実装で、`.cmoc` の追跡除外保証、初期化差分のコミット、進捗表示、`StepTimer` による時間計測を扱います。
- `branch.py` は `cmoc branch` の実装で、`cmoc_<timestamp>` 形式の作業用ブランチ作成、作成元 commit の保存、`.cmoc` ignore 保証、衝突時リトライを扱います。
- `apply.py` は `cmoc apply` の実装で、cmoc ブランチ検証、oracle 差分のコミット、`INDEX.md` メンテナンス、不整合調査、実装追従、変更コミット、apply レポート生成を扱います。
- `eval_oracles.py` は `cmoc eval-oracles` の実装で、評価対象 oracle の選定、`INDEX.md` メンテナンス、Codex CLI による oracle 評価、Markdown レポート保存を扱います。
- `merge.py` は `cmoc merge` の実装で、未コミット差分検証、マージ元ブランチ解決、`git merge`、conflict 解消支援、作業ブランチ削除を扱います。
- `__init__.py` はサブコマンド実装パッケージであることを示す最小限の初期化ファイルです。

## Read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` のうち、どの本体実装ファイルを読むべきか判断したいとき。
- サブコマンド全体の一覧と、それぞれの処理責務を確認したいとき。
- 各サブコマンドが共通処理、`StepTimer`、`INDEX.md` メンテナンス、Codex CLI 呼び出しをどの順序で使うか確認したいとき。
- `.cmoc` 追跡除外、作業ブランチ、oracle 差分、実装差分、merge conflict などが各サブコマンド内でどう扱われるかを知りたいとき。
- サブコマンド単位のテストを書くために、直接呼び出し可能な実装関数の責務を把握したいとき。

## Do not read this when

- 特定のサブコマンドの詳細仕様だけをすでに把握していて、このディレクトリ全体の案内が不要なとき。
- cmoc の開発ルール、コーディング規約、テスト方針などの開発者向け情報だけを調べたいとき。
- 共通ユーティリティの実装や、`src/commons` 側の処理を調べたいとき。
- 実装コードやテストコードの具体的な配置、修正方法だけを確認したいとき。
- cmoc の正本仕様断片そのものを読みたいとき。仕様への入口は `oracles` 配下の `INDEX.md` です。

## hash

- f29c03d2f46bdca4c712089824a5424c7c6904d0445cd5bf193db8758e6e6e2e
