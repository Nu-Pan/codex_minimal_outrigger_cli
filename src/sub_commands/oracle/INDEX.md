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
- CLI の `oracle review` サブコマンドを実行するためのランタイム実装。active session branch の検証、隔離 review worktree の作成・レビュー実行・中断処理・差分マージ・レポート出力までを統括する。レビュー対象列挙、所見処理、INDEX 更新、レポート生成など下位モジュールへの入口でもある。

## Read this when
- `oracle review` の実行フロー、active session や clean worktree の前提、隔離 worktree と review branch のライフサイクルを変更・調査するとき。
- oracle review の中断時処理、エラー時レポート、INDEX 差分のマージ、サブコマンド進捗記録を確認するとき。
- レビュー対象列挙・レビュー loop・レポート生成・review branch 操作の連携箇所を確認するとき。

## Do not read this when
- レビュー対象の列挙規則だけを変更・調査する場合は、対象列挙を担う下位モジュールを直接読む。
- レビュー loop の判定・所見マージだけを変更・調査する場合は、review loop の実装を直接読む。
- レビュー結果レポートの表示・保存形式だけを変更・調査する場合は、review report の実装を直接読む。
- INDEX 更新や review branch の commit・merge・conflict 解決だけを変更・調査する場合は、review index の実装を直接読む。

## hash
- 94a5626e4e4687d276799bce9e48f34fa1324106a9db94865f9715fc39d67828

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
- oracle review の所見列挙・マージ・妥当性検証・採否判定を反復実行する制御ロジック。中断時の確定済み進捗保持、Structured Output のマージ操作検証、再試行、step 通知も扱う。oracle review の実行フローや finding 操作の挙動を変更・調査するときの実装入口。

## Read this when
- oracle review のループ制御、中断時の部分結果、進捗通知を変更・調査するとき。
- finding の列挙・マージ・検証・judge の呼び出し順や反復条件を確認するとき。
- merge operation の target_ids、kind、finding の検証や semantic retry を確認するとき。

## Do not read this when
- 個別 agent call の prompt 内容や Structured Output schema 自体を変更・調査するときは、対応する oracle review builder を直接読む。
- oracle review のパス解決や finding の oracle path 判定だけを確認するときは、review_paths の実装を直接読む。
- 一般的な Codex 実行規則や中断仕様を確認するときは、参照されている oracle 文書を直接読む。

## hash
- a6977438ed5d3435e24e83ae2c6222c1f19fb5b02aeb878cc9e77ae910f49b7b

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
