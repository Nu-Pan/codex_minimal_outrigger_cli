# `commons`

## Summary

- `src/commons` 配下にある、cmoc 全体で共通利用する基盤モジュール群のルーティング目次です。
- `codex exec` 呼び出し、`INDEX.md` 自動保守、git リポジトリ探索、共通エラー整形、タイムスタンプ生成、経過時間計測の入口をまとめています。
- サブコマンド実行の共通制御や、`oracles` / 実装ファイルの列挙・差分判定・初期化時の commit 処理など、横断的な処理の所在を案内します。
- `src/commons` の各モジュール詳細へ進む前に、このディレクトリ全体の役割を把握したいときの入口です。

## Read this when

- `src/commons` 配下のどのモジュールに共通処理があるか判断したいとき。
- `codex exec` のラッパー、Structured Output、ログ保存、リトライや quota 復帰処理を確認したいとき。
- git リポジトリルート探索、`.cmoc` の ignore 保証、未コミット差分判定、`oracles` / 実装ファイル列挙を確認したいとき。
- 共通エラーの表示形式や、サブコマンドの実行制御、終了コード変換を確認したいとき。
- タイムスタンプ文字列の生成や、サブコマンドのステップ別経過時間表示を確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数定義だけを確認したいとき。
- `cmoc` のユーザー向け実行時仕様や `oracles` 配下の仕様断片だけを確認したいとき。
- `src/commons` 以外の実装やテストの配置、構成、書き方だけを調べたいとき。
- `README.md`、`AGENTS.md`、`memo` などの運用ルールだけを確認したいとき。
- このディレクトリ全体ではなく、単一モジュールの実装詳細を直接読みたいとき。

## hash

- 90174a8563274a66fe2f98e5d84a0e4a0e94e6bd7e1e80f060a3623d447ee77c

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
