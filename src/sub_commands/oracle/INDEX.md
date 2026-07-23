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
- `cmoc oracle edit` サブコマンドの実行入口。入力された oracle 編集指示を受け取り、起動条件を検証したうえで Codex TUI を main worktree から起動する。

## Read this when
- `cmoc oracle edit` の CLI 起動経路、入力収集、TUI 起動パラメータ、起動前検証を変更・調査するとき。

## Do not read this when
- oracle 編集指示の具体的な仕様や TUI パラメータ生成処理だけを確認したいときは、参照されている oracle 仕様または `launch_tui` 実装を直接読む。

## hash
- 0346bbb279262e9497ffbfd8648d775278688a391de6cf2da8096bc8515b4fe0

# `investigation.py`

## Summary
- `cmoc oracle investigation` サブコマンドの read-only TUI workload を実装する。入力された oracle 調査指示を編集・収集し、TUI 起動パラメータを構築して Codex TUI を起動する。

## Read this when
- `cmoc oracle investigation` の CLI 実行フロー、入力テンプレート、TUI 起動処理を確認・変更するとき。
- oracle 調査指示の入力前処理や indexing preflight、実行ステップの構成を確認するとき。

## Do not read this when
- 他の oracle サブコマンドや、TUI 起動パラメータの具体的な構築ロジックだけを確認したいときは、それぞれの実装先を直接読む。
- Codex TUI 自体の実装や共通 CLI runtime の詳細だけを調べるとき。

## hash
- 82d05024db9f62a0c049f64b3f6163d532cdfe1b8d691142961abcf9e49b3c10

# `review.py`

## Summary
- oracle review サブコマンドの CLI 実行入口。active session branch の検証、隔離 worktree での oracle review loop 実行、所見・INDEX 変更の統合、レポート生成、中断・失敗時の処理を統括する。
- レビュー対象の列挙、レビュー処理、INDEX 変更の commit/merge/conflict 解決、レポート描画の公開入口もまとめて提供する。

## Read this when
- `cmoc oracle review` の実行フロー、前提条件、worktree/branch 生命周期を確認するとき
- oracle review の中断・例外時にレポートやログがどう扱われるか確認するとき
- oracle review に伴う INDEX 変更の統合処理の入口を確認するとき

## Do not read this when
- レビュー対象の列挙規則だけを確認したい場合は review_targets の実装を直接読む
- レビュー loop の所見判定や反復処理だけを確認したい場合は review_loop の実装を直接読む
- レポートの整形・出力形式だけを確認したい場合は review_report の実装を直接読む
- oracle review 以外のサブコマンドの実行フローを確認するとき

## hash
- 44f989f8b969aa8c77755c6ffa2529d050f0a5e29ce51ce266af416795faeff8

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
