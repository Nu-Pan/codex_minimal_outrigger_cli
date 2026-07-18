# `__init__.py`

## Summary
- oracle 系サブコマンドをまとめる package の境界を示す。oracle サブコマンド群への入口として扱う。

## Read this when
- oracle 系サブコマンドの package 構成や入口を確認するとき。

## Do not read this when
- 個別の oracle サブコマンド実装の詳細を確認するとき。

## hash
- 2c8110c7811042f7162e1264e7027bb2d801f4687eb66f48f1668402c8eeb0df

# `edit.py`

## Summary
- `cmoc oracle edit` サブコマンドの CLI 本体。ユーザー指示の収集、oracle 編集用 TUI 起動パラメータの構築、Codex TUI の実行を担当する。

## Read this when
- `cmoc oracle edit` の起動フロー、入力収集、TUI 起動、実行前チェックを変更・調査するとき。

## Do not read this when
- oracle 編集用 TUI パラメータの詳細を変更するときは、builder 実装を直接読む。
- プロンプト入力の収集・ignore 前提を変更するときは、prompt editor input の実装・仕様を直接読む。

## hash
- 8c0100a0068548e58eef41adfe54abca02fe36dbe5a67f324bf2abb3d9e2fd1d

# `review.py`

## Summary
- oracle review サブコマンドの CLI 実行入口。active session branch 上で、oracle ファイルを隔離 worktree でレビューし、所見の収集・中断処理・レビュー用 INDEX.md の反映・レポート出力までを統括する。

## Read this when
- oracle review サブコマンドの実行条件、隔離 worktree のライフサイクル、レビュー処理の全体フローを確認するとき。
- レビュー中断時の扱い、未コミット差分の検査、レビュー結果レポートの生成契約を確認するとき。

## Do not read this when
- レビュー対象ファイルの列挙条件だけを確認したいときは review_targets の実装を読む。
- レビュー所見のループ処理だけを確認したいときは review_loop の実装を読む。
- 所見レポートの表示形式だけを確認したいときは review_report の実装を読む。
- レビュー用 INDEX.md のコミット・マージ・競合解決だけを確認したいときは review_index の実装を読む。

## hash
- 59320e2db73efe87a69c7c10a28f1831d7d3775c12606659fec0cb5dae5b755c

# `review_index.py`

## Summary
- oracle review 用 worktree の変更を検査し、INDEX.md だけを commit・branch merge する処理を担う。非 INDEX.md 差分の検出、INDEX.md のみの conflict 解決、merge 後 HEAD の取得までを扱う。

## Read this when
- oracle review の INDEX.md 変更を commit または review branch から merge する処理を調査・変更するとき
- review worktree や review branch に INDEX.md 以外の差分が混入する条件を確認するとき
- INDEX.md 限定の merge conflict 解決ロジックを確認するとき

## Do not read this when
- 通常の oracle review 実行フローや INDEX.md の内容生成を調査するとき
- 一般的な git status・commit 処理や、INDEX.md 以外の成果物を扱う処理を調査するとき
- 対象モジュールから呼び出される共通 git ユーティリティの仕様を直接確認したいときは、共通ユーティリティ側を読む

## hash
- 1d21154227395ecc91d3883c67e4d49f381eadc5deb30011f9b0009d92ff1cb5

# `review_loop.py`

## Summary
- oracle review の所見列挙・マージ・妥当性検証・採否判定を反復実行するループ実装。中断時には確定済み所見と評価済みファイルを専用例外で返し、merge operation の形式・対象 ID・finding 内容を検証して所見リストへ適用する。
- oracle review のサブコマンド処理で、レビュー進捗通知、Codex 実行、所見の再試行、評価済みファイル管理、Structured Output の検証が必要な場合に読む。

## Read this when
- oracle review の列挙・マージ・validate・judge ループを変更または調査するとき
- レビュー処理の KeyboardInterrupt 時の部分結果保持や step callback 通知を確認するとき
- finding merge operation の適用規則、ID 重複・未知 ID・kind 別入力検証を確認するとき

## Do not read this when
- oracle review の各 agent prompt の内容だけを変更するときは、対応する builder 実装を直接読む
- oracle review のファイルパス解決だけを変更するときは、review_paths 実装を直接読む
- 共通の Codex 実行規則だけを確認するときは、codex_exec_rule の oracle file を読む

## hash
- 84fb42512cbc6c877bb71fc55fa3e7e94369be94cff4c6a72117a8c947961802

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
- Oracle review の結果を Markdown レポートとして生成・保存する実装。frontmatter、判定結果、評価対象一覧、severity・採否ごとの finding 表示、パス表示を扱う。oracle review のレポート出力仕様を確認・変更する際の入口。

## Read this when
- oracle review のレポート生成、保存、判定文面、frontmatter、finding の表示順や形式を確認・変更するとき
- レビュー結果の出力先や repository-relative な oracle file 表示を確認するとき

## Do not read this when
- oracle review の対象ファイル探索やパスキー生成そのものを変更するとき
- oracle review 以外のサブコマンドの処理や、レビュー実行フロー本体だけを確認するとき

## hash
- a360aa7eaced06afdccfe8e138577adee8d525366e90b2c735fe05403b2b40b3

# `review_targets.py`

## Summary
- oracle review の scope に応じてレビュー対象の oracle file を列挙する実装。full scope では oracle ツリー全体、session scope ではセッション開始コミットから review fork commit までに変更された oracle file に限定する。

## Read this when
- oracle review の対象範囲や、full/session scope における oracle file の列挙条件を変更・確認するとき。

## Do not read this when
- 特定の oracle file の内容やレビュー処理本体を確認したいときは、この対象ではなく該当する oracle 文書またはレビュー実行処理を直接読む。

## hash
- 5260a52f5d2563973baf416c7a9a87cdd90bf6222b28fdfaf3c0edcb73614bfa
