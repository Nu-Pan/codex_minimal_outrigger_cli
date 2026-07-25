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
- oracle review の所見列挙・マージ・妥当性検証・採否判定を一連のループとして実行する実装。レビュー進捗、finding の関連付け、semantic retry、KeyboardInterrupt 時の部分結果保存、merge operation の契約検証を扱う。

## Read this when
- oracle review の enumerate／merge／validate／judge のループ動作を変更・調査するとき
- レビュー中断時の確定済み所見や評価済みファイルの扱いを確認するとき
- finding の merge operation、ID、重複、対象妥当性、semantic retry の挙動を確認するとき

## Do not read this when
- oracle review の prompt parameter 構築だけを変更・調査するときは、各 review parameter builder を直接読む
- oracle review のファイルパス解決だけを変更・調査するときは、review_paths の実装を直接読む
- oracle review 以外のサブコマンドのループや所見処理を扱うとき

## hash
- fb099dd2b6671a992b5f01c1942f062d345e5b1c6972408f4408da05df098ab1

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
- oracle review の結果を Markdown レポートとして保存・描画する実装。YAML frontmatter、レビュー判定、評価対象 oracle file の一覧、severity・採否別の所見表示、YAML scalar とパスの整形を担当する。

## Read this when
- oracle review レポートの生成形式、判定ロジック、所見の分類・表示順、frontmatter の値の整形を変更または確認するとき。

## Do not read this when
- oracle review の実行フロー、対象 oracle file の探索、レビュー判定そのものの仕様を確認したいときは、呼び出し元や oracle review の仕様文書を先に読む。

## hash
- 3182414e5eb5fadeecfbd3ddafb31173120335632375792e1afb70b4c25ffc2d

# `review_targets.py`

## Summary
- oracle review の scope に応じてレビュー対象の oracle file を列挙する処理。full scope では全件、session scope ではセッション開始時点から review fork までに変更された oracle 配下のファイルだけを対象にする。対象判定には repository path 上の oracle file 判定を用い、symlink も扱う。

## Read this when
- oracle review の対象ファイル列挙、scope 別の対象範囲、session fork 間の差分判定を変更・確認するとき。

## Do not read this when
- oracle review の実行処理や、oracle file の内容そのものを確認したいとき。対象列挙後の処理や各 oracle file を直接読む方が適切。

## hash
- 95936d0c2a0e48b4b1d262160a9446dea0d9cb6d80f6fa8fe673a825e6e5ade3
