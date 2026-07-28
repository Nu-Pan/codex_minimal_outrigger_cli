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
- 編集関連の実装ファイルを含まない空のディレクトリです。現時点で下位要素へのルーティング先はありません。

## Read this when
- このディレクトリに編集関連ファイルが追加されたか確認するとき。

## Do not read this when
- Oracle サブコマンドの実装を調査するとき。親ディレクトリの実装ファイルを直接確認してください。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `edit.py`

## Summary
- `cmoc oracle edit` サブコマンドの実装。oracle 編集指示を収集し、main worktree の active session branch と clean 状態を検証したうえで Codex TUI を起動する。

## Read this when
- `cmoc oracle edit` の起動処理、入力テンプレート、TUI 起動パラメータ、または起動前提条件を変更・調査するとき。

## Do not read this when
- oracle 編集処理そのものの仕様や TUI パラメータ構築の詳細を確認したいときは、対応する oracle 文書や `acp/builder/oracle/edit/launch_tui` の実装を直接読む。

## hash
- 476a738e23265d2f782dbf5646861067f56b647d0f4ad96cdba6ff6e2e541c57

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
- oracle review サブコマンドの CLI 実行入口。active session の検証、隔離 worktree/run branch の作成と cleanup、oracle 対象の列挙・レビュー実行、INDEX 変更の統合、レポート生成、中断・失敗時処理を統括する。

## Read this when
- oracle review サブコマンドの実行フロー、session branch の前提、隔離 run のライフサイクル、レビュー完了・中断・失敗時の挙動を確認するとき。
- oracle review に関する cleanup、worktree/branch 操作、レビュー結果の統合やレポート出力の呼び出し関係を調査するとき。

## Do not read this when
- レビュー対象の列挙規則だけを確認したい場合は review_targets の実装を直接読む。
- レビュー loop の所見収集・中断処理だけを確認したい場合は review_loop の実装を直接読む。
- INDEX 変更の commit・merge・conflict 解決だけを確認したい場合は review_index の実装を直接読む。
- レポートの表示形式や保存処理だけを確認したい場合は review_report の実装を直接読む。

## hash
- 375060db5e099a207cd2ca68ac49dba04ee1ece7cb26daefa3573d10d10b3748

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
- oracle review の結果を Markdown レポートとして保存・描画する実装。YAML frontmatter、判定結果、評価対象 oracle file、finding の分類・順序・安全な Markdown 表示を扱う。

## Read this when
- oracle review レポートの保存先、frontmatter、verdict 判定、finding 表示、対象 path 表示の挙動を変更・確認するとき。
- oracle review の出力形式や、エラー・中断・対象なし・fatal・minor・ok の結果処理を調査するとき。

## Do not read this when
- oracle review の対象 oracle file の収集・評価ロジック自体を変更・確認するとき。
- 他のサブコマンドのレポート形式や、共通の timestamp path 予約処理だけを調査するとき。

## hash
- 975b64084bf01f45bfc91495bde6359f29dca3875d6df4cf23cf9ecb478b2eca

# `review_targets.py`

## Summary
- oracle review の scope に応じてレビュー対象の oracle file を列挙する処理。full scope では全件、session scope ではセッション開始時点から review fork までに変更された oracle 配下のファイルだけを対象にする。対象判定には repository path 上の oracle file 判定を用い、symlink も扱う。

## Read this when
- oracle review の対象ファイル列挙、scope 別の対象範囲、session fork 間の差分判定を変更・確認するとき。

## Do not read this when
- oracle review の実行処理や、oracle file の内容そのものを確認したいとき。対象列挙後の処理や各 oracle file を直接読む方が適切。

## hash
- 95936d0c2a0e48b4b1d262160a9446dea0d9cb6d80f6fa8fe673a825e6e5ade3
