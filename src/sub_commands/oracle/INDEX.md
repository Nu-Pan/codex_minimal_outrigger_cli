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
- oracle review サブコマンドの実行責務を担う実装。active session branch 上で隔離 review run を作成し、対象 oracle のレビュー、INDEX 更新の統合、worktree・branch の cleanup、レビュー結果レポートの出力までを統括する。
- レビューの中断・例外・cleanup 失敗を含む終了経路、未コミット差分の拒否、サブコマンド進捗ログ、レビュー関連の公開関数を扱う。レビュー対象列挙・ループ・レポート描画の詳細実装は、インポート先の専用モジュールが入口となる。

## Read this when
- `cmoc oracle review` のCLI実行フロー、隔離worktree/run branchのライフサイクル、レビュー結果の統合またはレポート出力を変更・調査するとき。
- oracle review の中断時・例外時・cleanup失敗時の挙動、または実行前のworktree状態検査を確認するとき。
- oracle review 関連の公開関数がどのモジュールから提供されるかを確認するとき。

## Do not read this when
- レビュー対象ファイルの列挙条件だけを変更・調査する場合は、対象列挙を担当する専用モジュールを直接読む。
- レビュー反復処理や所見マージの詳細だけを変更・調査する場合は、review loop担当モジュールを直接読む。
- 所見の描画・レポートファイル生成だけを変更・調査する場合は、review report担当モジュールを直接読む。
- INDEX更新のcommit・merge・conflict解決だけを変更・調査する場合は、review index担当モジュールを直接読む。

## hash
- 12bf93f8e1a60f45f400a67b6b8b62633e458dea3a2978e3afbccefd6aac3a85

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
- oracle review の finding 列挙、関連 finding の抽出、merge、反証・擁護による検証、採否判定を一連のループとして実行する。
- review 中断時には、完了済み agent call の結果と評価済みファイルを部分結果として保持する。
- merge operation の形式・対象 ID・重複を検証し、意味的な Structured Output 検証失敗だけを規定回数まで再試行する。
- oracle review サブコマンドの review 状態管理と finding 操作の実装入口である。

## Read this when
- oracle review の finding 列挙・merge・検証・judge の挙動を変更または調査するとき
- review の中断時部分保存、semantic retry、finding merge operation の検証を確認するとき
- review progress や評価済み oracle file の追跡処理を変更するとき

## Do not read this when
- oracle review の prompt parameter 生成だけを変更するときは、各 prompt builder の対象ファイルを直接読む
- review 対象 path の定義だけを確認するときは、review_paths の対象ファイルを直接読む
- oracle review 全体の CLI 入出力や仕様だけを確認するときは、対応する oracle review の仕様文書を先に読む

## hash
- 52a56d1e0463dcd5aff5069d1e8e6d151553ef229caee15299f3b6a8336032cf

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
