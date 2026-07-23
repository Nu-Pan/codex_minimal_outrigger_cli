# `__init__.py`

## Summary
- oracle 系サブコマンドをまとめる package の境界を示す。oracle サブコマンド群への入口として扱う。

## Read this when
- oracle 系サブコマンドの package 構成や入口を確認するとき。

## Do not read this when
- 個別の oracle サブコマンド実装の詳細を確認するとき。

## hash
- 2c8110c7811042f7162e1264e7027bb2d801f4687eb66f48f1668402c8eeb0df

# `edit`

## Summary
- `cmoc oracle edit` サブコマンドで、main worktree 向け TUI の起動をオーケストレーションする実装。プロンプト入力の収集、oracle 編集用パラメータ構築、indexing preflight、Codex TUI 起動を扱う。
- main worktree、active な session branch・session、clean worktree などの起動前提条件を検証するための入口。

## Read this when
- `cmoc oracle edit` の CLI runtime、TUI 起動、プロンプト入力、起動前提条件を変更・調査するとき
- main worktree や session branch の検証、oracle 編集 instruction の受け渡しを確認するとき

## Do not read this when
- oracle 編集対象の選択・編集ロジック自体を調査するとき
- 共通 CLI runtime、git 状態検証、runtime state の詳細だけを調査するとき

## hash
- 99fe6a83f2e498107c96577726f81954d9450edc5ac116049c82d97f4c8d9d56

# `investigation.py`

## Summary
- `cmoc oracle investigation` サブコマンドの read-only TUI workload を実装するエントリポイント。インデックス事前処理、調査指示の入力、Codex TUI 起動パラメータの構築、設定済みランタイムでの TUI 起動を担当する。

## Read this when
- `cmoc oracle investigation` の CLI 実行フロー、調査指示入力、Codex TUI 起動処理を変更・調査するとき。
- oracle investigation サブコマンドのステップ構成や実行時コンテキストを確認するとき。

## Do not read this when
- Oracle investigation の調査指示テンプレートや正本仕様を確認したいときは、対応する oracle doc を直接読む。
- TUI 起動パラメータの詳細実装を確認したいときは、`acp.builder.oracle.investigation.launch_tui` を直接読む。
- 共通 CLI ランタイム、プロンプトエディタ入力、インデックス事前処理の仕様だけを確認したいときは、各共通モジュールを直接読む。

## hash
- 7ea8e16b7d631e28f1e208d4683ec600dd20c333046f5eae32e94aca5e25d58b

# `review.py`

## Summary
- oracle review サブコマンドの CLI 実行入口と本体を担うモジュール。active session branch の検証、隔離 review worktree の作成・実行・後処理、所見のマージ、レビュー報告生成、中断・失敗時の処理を統括する。関連する review_targets、review_loop、review_index、review_report の公開要素も再エクスポートする。

## Read this when
- oracle review サブコマンドの実行フロー、worktree 分離、ブランチ検証、レビュー結果の統合や報告処理を変更・調査するとき。
- oracle review の中断時・例外時の挙動や未コミット差分の扱いを確認するとき。

## Do not read this when
- レビュー対象ファイルの列挙条件だけを変更・調査する場合は review_targets を直接読む。
- レビュー反復処理や所見適用の詳細だけを変更・調査する場合は review_loop を直接読む。
- INDEX 更新のコミット・マージ・競合解決だけを変更・調査する場合は review_index を直接読む。
- レビュー報告の表示内容や書き込みだけを変更・調査する場合は review_report を直接読む。

## hash
- ba2912fe91746f77201bc2337c28c7b3904f34cd76d29d8d3ba3749dffe4df86

# `review_index.py`

## Summary
- oracle review 用 worktree の差分を検査し、INDEX.md だけを commit・merge する処理を担う。変更対象の制限、review branch の差分確認、INDEX.md の merge conflict 解決が主な入口。

## Read this when
- oracle review による INDEX.md 変更の commit 条件を確認するとき
- review branch の merge や INDEX.md 限定の conflict 解決を変更・調査するとき

## Do not read this when
- 通常の INDEX.md 生成内容やルーティング方針を確認したいとき
- oracle review 自体の仕様を確認したいときは、対応する oracle 文書を先に読む

## hash
- 9586f7d7c1998e7bfed6efad77b4a94b9e1a634df874e307e6f8c4737b0ed5c9

# `review_loop.py`

## Summary
- oracle review の finding 列挙・マージ・妥当性検証・採否判定ループを実装する中核モジュール。中断時の確定済み進捗保持、対象 oracle file の関連付け、Structured Output のマージ操作検証と再試行も扱う。

## Read this when
- oracle review の処理フロー、finding の列挙・統合・検証・判定を変更または調査するとき
- KeyboardInterrupt 発生時の部分結果の扱いを確認するとき
- merge operation の target_ids、kind、finding の妥当性検証や semantic retry を確認するとき

## Do not read this when
- oracle review の各 agent call 用パラメータ生成文面だけを変更または調査するときは、対応する builder モジュールを直接読む
- oracle review の path 解決規則だけを確認するときは、review_paths モジュールを直接読む
- ステップ通知の表示やサブコマンド全体の割り込み制御だけを確認するときは、呼び出し元や割り込み仕様を直接読む

## hash
- 9f698fcd963ee8773aae1a36385c4f0b0f19d111af1c92f6144341d26b9d480d

# `review_paths.py`

## Summary
- Oracle の検出結果に含まれるパスを、シンボリックリンクを追跡せず絶対パスへ解決する処理と、Oracle ファイルをリポジトリ相対キーへ変換する処理を提供する。メイン worktree と cmoc 管理下の isolated worktree の境界を検証し、対象外のパスは無視する。

## Read this when
- Oracle review の finding から oracle_path を解決・正規化するとき
- worktree 間で Oracle ファイルの相対キーを生成するとき
- パスの所属範囲やシンボリックリンク非追跡の挙動を変更・確認するとき

## Do not read this when
- Oracle review のレポート生成や finding の内容自体を変更する作業
- 一般的なパス操作や runtime path の仕様を確認する作業

## hash
- eddbb1a5f24d266c525ab726d9961e9b5cc95ae97c62f3b4e1ce076712725fb7

# `review_report.py`

## Summary
- oracle review の結果を Markdown と YAML frontmatter のレポートとして生成・保存する実装。レビュー対象、実行状態、所見、判定結果を記録し、所見の分類・順序・表示形式と repository-relative な oracle file 表示を担う。

## Read this when
- oracle review レポートの生成内容、frontmatter、verdict 判定、finding の分類・表示順を変更または確認するとき
- レビュー結果の保存先、ファイル名、対象 oracle file の表示方法を調査するとき

## Do not read this when
- oracle review の対象 oracle file の選定やパス解決だけを調査するとき
- レビュー処理本体や session 制御を変更するときは、まずそれぞれの責務を持つ実装を直接読む場合

## hash
- 5d4fa434393103e8b269c934319904745378dbfc5706f46038f85be1abe647fc

# `review_targets.py`

## Summary
- oracle review の scope に応じてレビュー対象の oracle file を列挙する。full では全件、session 相当ではセッション fork から review fork までに oracle 配下で変更されたファイルに絞り込む。
- oracle 配下の候補を repository path として列挙し、通常ファイルと symlink を含めて oracle file 判定を適用する。

## Read this when
- oracle review の対象範囲や scope 別のファイル列挙条件を確認するとき
- oracle file の全件列挙、変更差分による絞り込み、symlink の扱いを変更・調査するとき

## Do not read this when
- oracle review の実行処理やレビュー内容の判定を変更するとき
- 対象ファイルの列挙を介さない一般的な CLI や runtime 処理を確認するとき

## hash
- e8cdb38c1e3701308cc7d8c4a4e022ea46066b283f91931b79f8b0f3f7a34eb4
