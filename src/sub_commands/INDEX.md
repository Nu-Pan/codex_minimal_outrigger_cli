# `__init__.py`

## Summary

- cmoc のサブコマンド実装パッケージであることを示すパッケージ初期化ファイル。
- 実行ロジックや公開 API の定義は含まず、パッケージ用途を docstring で説明するだけのファイル。

## Read this when

- src/sub_commands 配下が何のためのパッケージかを最小限確認したいとき。
- サブコマンド実装モジュール群のパッケージ境界や概要を確認したいとき。

## Do not read this when

- 個別サブコマンドの処理内容、引数、実行フローを調べたいとき。
- cmoc のコマンドルーティング、CLI エントリポイント、サブコマンド登録方法を調べたいとき。
- 実装上の詳細な仕様やテスト対象の振る舞いを確認したいとき。

## hash

- ea4df02b820eba1ca77dfb1b2227c81dbff61cd7c4c2bf4d26d891369b57fa77

# `apply.py`

## Summary

- `cmoc apply` サブコマンドの本体処理を実装するファイルです。
- cmoc 作業ブランチ上でのみ実行できることを検査し、oracle 以外の未コミット差分を拒否し、`.gitignore`・`.cmoc`・`oracles` の保証差分を必要に応じて commit します。
- `INDEX.md` のメンテナンス後、oracle ファイルごとに Codex CLI の read-only 実行で実装との明確な不整合を Structured Output として収集します。
- 検出した不整合を Codex CLI の workspace-write 実行へ渡して実装・テスト修正を依頼し、禁止領域の変更検査、INDEX 更新、Codex 生成 commit message による commit を反復します。
- 反復回数上限、未収束時の終了コード、apply レポート生成、進捗表示、StepTimer による経過時間表示を扱います。
- 不整合調査用 JSON schema、schema 検証、実装修正用 prompt、commit message 生成用 prompt、作業レポート生成用 prompt をこのファイル内で定義しています。

## Read this when

- `cmoc apply` の実行フロー、ステップ表示、終了コード、反復処理の条件を確認したいとき。
- apply 実行前にどの git 状態を許可・拒否し、どの保証差分を自動 commit するか調べたいとき。
- oracle と実装の不整合調査を Codex CLI にどう依頼し、Structured Output をどう検証・集約するか確認したいとき。
- 不整合追従のための Codex CLI workspace-write 呼び出し、禁止パス検査、実装差分 commit の流れを変更したいとき。
- `oracles/`、`.agents/`、`memo` など apply 中の禁止領域や読み書き制約を確認したいとき。
- apply レポートの保存先、ファイル名、レポート生成 prompt、収束・未収束の扱いを調べたいとき。
- `--repeat` 相当の反復回数、負数拒否、未収束時の `APPLY_INCOMPLETE_EXIT_CODE` の意味を確認したいとき。

## Do not read this when

- `cmoc apply` 以外のサブコマンド、たとえば `init`、`branch`、`merge`、`eval-oracles` の個別実装だけを調べたいとき。
- Codex CLI 呼び出しの低レベル実装、JSON パース共通処理、git コマンド実行共通処理そのものを調べたいとき。
- `INDEX.md` 自動メンテナンスの詳細アルゴリズムや対象ファイル判定だけを調べたいとき。
- oracle ファイル列挙、cmoc ブランチ判定、未コミット差分検査など repo 共通ユーティリティの内部実装だけを確認したいとき。
- cmoc の開発規約、テスト規約、ディレクトリ構成ルールなど、アプリケーション実行時挙動ではなく開発者向けルールを調べたいとき。
- apply が生成したレポート本文や過去実行ログの内容を読みたいだけのとき。

## hash

- a98c33e48651bb1a4461d3952ac5768c7e848a5223db2bdaa9e5f09c4d7d81c2

# `branch.py`

## Summary

- `cmoc branch` サブコマンドの本体処理を実装するファイル。
- `cmoc_branch_impl` は実行ラッパー経由の起動と、`repo_root` 指定時の実処理を分岐し、作業用ブランチ作成、`.cmoc` の git 追跡対象外保証、作成元 commit の記録を順に行う。
- 処理中は `StepTimer` と stdout により `branch (1/3)` から `branch (3/3)` までの進捗を表示し、最後に作成したブランチ名と経過時間を出力する。
- 作業用ブランチ名は `cmoc_<timestamp>` 形式で生成され、衝突時は最大 10 回まで短い待機を挟んで再生成と `git checkout -b` をリトライする。
- 作成元 commit はブランチ作成前の HEAD として取得され、ブランチ名に対応する `.cmoc/branch` 側の保存先へ UTF-8 テキストで記録される。

## Read this when

- `cmoc branch` の実装本体、処理順序、stdout 進捗表示を確認したいとき。
- 作業用ブランチ名の生成規則、timestamp 衝突時のリトライ回数、`git checkout -b` の呼び出し方を調べたいとき。
- ブランチ作成前の HEAD を base commit としてどこで取得し、どのタイミングで保存するか確認したいとき。
- `.cmoc` を git 追跡対象外にする処理が `cmoc branch` のどこで呼ばれるか確認したいとき。
- `cmoc_branch_impl` が `repo_root` 未指定時に `run_command` 経由で再実行される構造を確認したいとき。

## Do not read this when

- `cmoc branch` のユーザー向け仕様全体や正本仕様を確認したいだけで、実装コードの詳細が不要なとき。
- `cmoc init`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` など他サブコマンドの実装を調べたいとき。
- git 実行ラッパー、HEAD 取得、`.cmoc` 保存パス、ignore 保証などの共通関数そのものの実装を確認したいとき。
- CLI 引数定義やサブコマンドの登録箇所を探しているとき。
- 自動テストの期待値や Fake Codex CLI など、テスト側の構成を確認したいとき。

## hash

- d63df091c9ef6d597b28b7db7b3e90d677994ae4b36961ca44e96b9996b7123b

# `eval_oracles.py`

## Summary

- `cmoc eval-oracles` サブコマンドの本体処理を実装する Python モジュール。
- `.cmoc` の git ignore 保証、`INDEX.md` メンテナンス、評価対象 oracle の選択、Codex CLI による oracle 評価、Markdown レポート保存までの一連の処理を扱う。
- cmoc 作業ブランチかつ `--full` 未指定で oracle 削除がない場合は、ブランチ基点から変更された oracle だけを部分評価し、それ以外は全 oracle を全体評価する。
- oracle 評価用プロンプトでは、実装・テスト・設定ファイルを参照せず、oracles ツリーと `INDEX.md` のルーティング情報に基づいて致命的な仕様問題を報告するよう Codex CLI に指示する。
- 評価結果は `.cmoc/reports/eval-oracles/<timestamp>.md` に、評価モード、ブランチ名、HEAD コミット、oracle 件数を frontmatter として含む Markdown レポートとして保存する。

## Read this when

- `cmoc eval-oracles` の実行ステップ、stdout 進捗表示、処理順序を確認したいとき。
- oracle 評価が部分評価になる条件と、全体評価へフォールバックする条件を調べたいとき。
- 評価対象 oracle ファイルの列挙、変更 oracle の抽出、削除 oracle 検出、ブランチ基点コミットの利用箇所を確認したいとき。
- `cmoc eval-oracles` が Codex CLI に渡す評価プロンプトの内容や、読み取り専用実行の扱いを確認したいとき。
- 評価レポートの保存先、ファイル名、frontmatter、oracle ごとの出力構造を調べたいとき。
- `commons.codex`、`commons.indexing`、`commons.repo`、`commons.timing`、`commons.timestamps` と `eval-oracles` 本体処理のつながりを把握したいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc merge` など、`eval-oracles` 以外のサブコマンド本体だけを調べたいとき。
- Codex CLI 呼び出しの低レベル実装、コマンド実行共通処理、repo 探索や git 操作の詳細実装だけを確認したいとき。
- `INDEX.md` 自動メンテナンス処理そのものの詳細や Structured Output 目次生成ロジックだけを調べたいとき。
- oracle 正本仕様の内容や、個別 oracle ファイルの仕様レビュー観点そのものを調べたいとき。
- 評価レポートのタイムスタンプ生成ルールや `.cmoc` ignore 保証の内部実装だけを確認したいとき。
- 自動テストの構成、Fake Codex CLI、テストデータの作り方だけを調べたいとき。

## hash

- 9c24cfba3b471b2ec3d42ad3a9e2f08e07d4749d3b6637ec5f9aa1e3403e7a3b

# `init.py`

## Summary

- `cmoc init` サブコマンドの本体処理を定義するファイル。
- `repo_root` が未指定の場合は `run_command(cmoc_init_impl)` に処理を委譲し、共通のコマンド実行経路で再実行する。
- `repo_root` が指定された場合は `.cmoc` を git 追跡対象外にするため、既存の `.gitignore` ルール確認、ignore ルール保証、tracked file 解除を実行する。
- 初期化によって発生した `.gitignore` や git index の変更だけを `commit_cmoc_initialization_changes` でコミットし、変更有無に応じた進捗メッセージを表示する。
- `StepTimer` を使って `init` の各ステップ開始と完了時の経過時間レポートを扱う。

## Read this when

- `cmoc init` の実装入口や、`cmoc_init_impl` がどの共通処理に委譲するかを確認したいとき。
- `.cmoc` を `.gitignore` に追加し、git 追跡対象外にする初期化処理の流れを調べたいとき。
- `cmoc init` が初期化時の変更をどの条件でコミットするか確認したいとき。
- `cmoc init` の stdout 進捗表示や `StepTimer` による計測箇所を確認したいとき。
- `commons.repo` の `gitignore_has_cmoc_rule`、`ensure_cmoc_ignored`、`commit_cmoc_initialization_changes` がどこから呼ばれるか追跡したいとき。

## Do not read this when

- CLI 全体の引数定義、サブコマンド登録、エントリーポイントを調べたいとき。
- `.cmoc` ignore ルールの具体的なファイル操作や git コマンド実行の詳細実装だけを調べたいとき。
- `cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` など、`init` 以外のサブコマンド仕様や実装を調べたいとき。
- Codex CLI 呼び出し、Structured Output、oracle 評価、INDEX.md 生成など、`cmoc init` の初期化処理と直接関係しない実行時仕様を調べたいとき。
- cmoc 自体の開発規約、テスト規約、依存管理、リポジトリ運用ルールだけを確認したいとき。

## hash

- 2c48b415912ebdaa8880a49e09e96ea6f73388f4c54484d6da5bc22e5ce0987d

# `merge.py`

## Summary

- `cmoc merge` サブコマンドの本体処理を実装するファイル。
- 対象リポジトリの検出後、作業ツリーの未コミット変更確認、`.cmoc` の ignore 確認、マージ元 cmoc ブランチの解決、`git merge --no-ff` 実行、必要時の conflict 解消、マージ後のブランチ削除までを担う。
- 明示された cmoc ブランチがない場合は、未マージブランチ一覧から cmoc 命名規則に一致する候補を 1 件だけ自動選択する。
- 通常の git merge が失敗した場合、unmerged path を固定して Codex CLI に conflict marker 解消を依頼し、marker 残存確認、`git add`、`git commit --no-edit` を行う。
- Codex に conflict 解消を依頼するプロンプトでは、`oracles`、`.agents`、`memo` の編集・アクセス禁止範囲や、`git add` / `git commit` 禁止を明示する。
- merge 開始後に例外が発生した場合は、cmoc が merge state をロールバックしないことと手動解決が必要なことを stderr に表示する。

## Read this when

- `cmoc merge` の実行フロー、進捗表示、StepTimer による計測対象を確認したいとき。
- マージ元 cmoc ブランチの自動解決条件や、候補が 0 件または複数件だった場合のエラー内容を調べたいとき。
- `git merge --no-ff` 失敗時に、Codex CLI に conflict marker 解消を依頼する条件や、その後の検証・commit 手順を確認したいとき。
- conflict marker 残存検査、unmerged path 検出、merge commit 作成、マージ元ブランチ削除の実装を変更・テストしたいとき。
- merge conflict 解消用 Codex プロンプトに含める禁止事項、対象ファイル一覧、INDEX メンテナンス例外指定を確認したいとき。
- merge 開始後の例外時に表示される手動解決案内メッセージや、cmoc がロールバックしない方針を確認したいとき。

## Do not read this when

- `cmoc merge` の CLI 引数定義や argparse への登録だけを確認したいとき。
- Codex CLI 呼び出しの共通実装、サンドボックス指定、Structured Output 処理など `run_codex_exec` 側の詳細を調べたいとき。
- `run_git`、`assert_no_uncommitted_changes`、`ensure_cmoc_ignored`、`is_cmoc_branch` など git・リポジトリ共通処理の内部実装だけを確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles` など merge 以外のサブコマンド挙動を調べたいとき。
- `oracles` 配下の正本仕様そのものや、merge 仕様の設計意図を確認したいだけで、Python 実装の制御フローが不要なとき。
- 対象リポジトリ側の個別 conflict 内容や、実際のマージ結果を調査したいとき。

## hash

- e679357fc26f4c6d06e0536d8082ddd0e167b8b486183d97502699e599be74bc
