# `commons`

## Summary

- `src/commons` は cmoc のサブコマンド横断で使う共通 Python モジュール群を収めるディレクトリです。
- Codex CLI 実行、Structured Output 検証、ログ保存、quota 待機・resume、JSON 応答パースなどの Codex 連携処理は `codex.py` に集約されています。
- Typer サブコマンド共通の repo root 解決、例外捕捉、終了コード変換は `command_runner.py` が担当します。
- 利用者向け復旧アクション付き例外 `CmocError` と共通エラーレポート整形は `errors.py` に定義されています。
- `INDEX.md` の自動配置・更新、目次対象列挙、除外規則、内容 hash による再利用判定、目次生成用 Codex 呼び出しは `indexing.py` が扱います。
- git リポジトリ探索、ブランチ・HEAD 取得、`.cmoc` ignore 保証、pathspec commit、oracle・実装ファイル列挙、変更・削除検出、git コマンド実行は `repo.py` にまとまっています。
- cmoc 仕様のタイムスタンプ生成は `timestamps.py`、サブコマンドのステップ別経過時間計測と表示は `timing.py` が提供します。
- `__init__.py` は `src.commons` を Python パッケージとして宣言するだけで、実行時ロジックや公開 API の集約は行っていません。

## Read this when

- cmoc の個別サブコマンド実装から使う共通処理がどのモジュールにあるか判断したいとき。
- Codex CLI 呼び出し、model・reasoning effort、sandbox、Structured Output、ログ保存、リトライ、quota resume の実装入口を探しているとき。
- サブコマンドの Typer 関数から本体 handler を呼び出す共通ラッパー、repo root への移動、例外から `typer.Exit` への変換を確認したいとき。
- `CmocError` の作り方、共通エラーレポートの見出し構成、次アクションや詳細・コールスタックの表示形式を調べたいとき。
- `INDEX.md` の生成対象、除外対象、既存ブロック再利用、hash 判定、Structured Output schema、Codex への目次生成依頼を実装・修正したいとき。
- git repository root 探索、現在ブランチ、HEAD、cmoc ブランチ判定、`.cmoc` の git 追跡対象外保証、未コミット差分検査を使う・直すとき。
- oracle ファイルや実装ファイルの列挙、変更済みファイルの抽出、削除検出、root `.gitignore` の適用範囲を確認したいとき。
- 初期化差分や INDEX メンテナンス差分など、指定 path だけを既存 staged 差分と混ぜずに commit する共通処理を理解したいとき。
- cmoc の `<time-stamp>` 形式や、サブコマンド完了時のステップ別タイミング表示を確認したいとき。

## Do not read this when

- 個別サブコマンドのユーザー向け仕様、引数、標準出力、ワークフローの詳細だけを調べたいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の本体処理そのものを追いたいとき。
- 設定ファイル `comconfig.json` や `CMOConfig` の読み書き・補完・公開プロパティだけを確認したいとき。
- cmoc の正本仕様断片を読むためのルーティングが目的で、実装コードの共通モジュール配置を調べる必要がないとき。
- テスト fixture、Fake Codex CLI、pytest 設定など、テストコード側の具体的な構成だけを探しているとき。
- Codex CLI や git の一般的な外部仕様だけを知りたいとき。
- `src.commons` が Python パッケージかどうかだけを確認したい場合を除き、空に近い `__init__.py` の実装詳細を読む必要があるとき。

## hash

- 0144237a77df11e66fd423d3c695956f948f7084e985b8cb66bcb7824314588b

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

- `src/sub_commands` は cmoc の各 CLI サブコマンド本体実装を集約するパッケージです。
- `init.py` は `cmoc init` の処理を実装し、`.cmoc` の git ignore 保証、初期化差分のコミット、進捗表示、時間計測を扱います。
- `branch.py` は `cmoc branch` の処理を実装し、`cmoc_<timestamp>` 形式の作業ブランチ作成、base commit 記録、`.cmoc` ignore 保証、ブランチ名衝突時のリトライを扱います。
- `eval_oracles.py` は `cmoc eval-oracles` の処理を実装し、INDEX.md メンテナンス、評価対象 oracle の選定、Codex CLI による oracle 評価、Markdown レポート保存を扱います。
- `apply.py` は `cmoc apply` の処理を実装し、cmoc ブランチ検証、oracle 差分コミット、INDEX.md メンテナンス、oracle と実装の不整合調査、Codex CLI による実装追従、変更コミット、apply レポート生成を扱います。
- `merge.py` は `cmoc merge` の処理を実装し、未コミット差分検査、マージ元 cmoc ブランチ解決、git merge、conflict marker 解消の Codex CLI 委譲、merge commit、作業ブランチ削除を扱います。
- `__init__.py` はサブコマンド実装パッケージであることを示すだけの初期化ファイルで、実行ロジックは含みません。
- `INDEX.md` はこのディレクトリ内の各実装ファイルへのルーティング情報を保持します。
- `__pycache__` は Python の生成物であり、実装理解や仕様確認のために読む対象ではありません。

## Read this when

- cmoc のサブコマンド本体実装がどのファイルにあるか判断したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の実行フロー、進捗表示、終了時処理をコード上で確認したいとき。
- 各サブコマンドが共通 runner、repo ユーティリティ、Codex CLI 呼び出し、INDEX.md メンテナンス、StepTimer をどのように呼び出しているか調べたいとき。
- `.cmoc` の git ignore 保証、cmoc 作業ブランチ作成、base commit 記録、oracle 評価、oracle と実装の不整合追従、マージ conflict 解消など、サブコマンド単位の制御フローを追いたいとき。
- Codex CLI に渡すサブコマンド固有のプロンプト、Structured Output schema、出力検証、レポート生成条件を確認したいとき。
- サブコマンド実装に関する自動テストを追加・修正する前に、テスト対象の関数名、分岐条件、副作用、保存先パスを把握したいとき。
- CLI エントリーポイントから呼ばれる実処理の委譲先を確認したいとき。

## Do not read this when

- CLI 引数パーサやサブコマンド登録の実装だけを調べたいとき。
- repo root 探索、git コマンド実行、変更ファイル列挙、`.cmoc` パス生成、timestamp 生成、StepTimer、Codex CLI 実行ラッパーなどの共通ユーティリティそのものを詳しく調べたいとき。
- cmoc の正本仕様断片を確認したいだけで、実装コードの制御フローを読む必要がないとき。
- Python コーディング規約、テスト規約、開発環境など、cmoc 開発ルールだけを調べたいとき。
- `<repo-root>` 側の oracle、実装ファイル、生成されたレポート、`.cmoc` 配下の成果物を調べたいとき。
- `README.md`、`AGENTS.md`、`oracles`、`memo` などの編集可否やリポジトリ運用ルールだけを確認したいとき。
- Python の `__pycache__` や `.pyc` 生成物を確認しようとしているとき。

## hash

- 57a7167b19f9c39848ecb0acc4b0c09d857607a9de3d1e3346eb60e03aad66a5
